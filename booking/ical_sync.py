"""Sicherer Import belegter Zeiträume aus dem Booking.com-iCal-Kalender."""

import hashlib
import logging
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from django.conf import settings as dj_settings
from django.db import transaction
from django.utils import timezone

from .models import BlockedPeriod, SiteSettings

logger = logging.getLogger(__name__)
MAX_ICAL_BYTES = 2_000_000


@dataclass(frozen=True)
class CalendarEvent:
    uid: str
    start_date: date
    end_date: date


def _unfold_lines(text):
    lines = []
    for raw_line in text.splitlines():
        if raw_line.startswith((" ", "\t")) and lines:
            lines[-1] += raw_line[1:]
        else:
            lines.append(raw_line.rstrip("\r"))
    return lines


def _ical_value(line):
    if ":" not in line:
        return "", ""
    key, value = line.split(":", 1)
    return key.split(";", 1)[0].upper(), value.strip()


def _parse_ical_date(value):
    """Booking nutzt Ganztagesdaten; Zeitwerte werden defensiv unterstützt."""
    compact = value.replace("-", "")
    if len(compact) < 8 or not compact[:8].isdigit():
        raise ValueError(f"Ungültiges iCal-Datum: {value!r}")
    return datetime.strptime(compact[:8], "%Y%m%d").date()


def parse_ical(text):
    """Liest DTSTART, DTEND und UID aus allen VEVENT-Blöcken."""
    if "BEGIN:VCALENDAR" not in text or "END:VCALENDAR" not in text:
        raise ValueError("Die Antwort ist kein gültiger iCal-Kalender.")

    events = []
    current = None
    for line in _unfold_lines(text):
        if line == "BEGIN:VEVENT":
            current = {}
            continue
        if line == "END:VEVENT":
            if current is not None and current.get("DTSTART"):
                start = _parse_ical_date(current["DTSTART"])
                end = _parse_ical_date(current.get("DTEND", "")) if current.get("DTEND") else start + timedelta(days=1)
                if end <= start:
                    raise ValueError("Ein Booking.com-Termin hat ein ungültiges Abreisedatum.")
                uid = current.get("UID") or hashlib.sha256(
                    f"{start.isoformat()}|{end.isoformat()}".encode()
                ).hexdigest()
                events.append(CalendarEvent(uid[:255], start, end))
            current = None
            continue
        if current is not None:
            key, value = _ical_value(line)
            if key in {"UID", "DTSTART", "DTEND"}:
                current[key] = value
    return events


def _validate_booking_url(url):
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or not (host == "booking.com" or host.endswith(".booking.com")):
        raise ValueError("BOOKING_ICAL_URL muss ein sicherer https-Link von Booking.com sein.")


def fetch_booking_events(url):
    _validate_booking_url(url)
    request = Request(url, headers={"User-Agent": "Haus-Flora-Calendar-Sync/1.0"})
    with urlopen(request, timeout=10) as response:  # noqa: S310 – Host ist validiert
        data = response.read(MAX_ICAL_BYTES + 1)
    if len(data) > MAX_ICAL_BYTES:
        raise ValueError("Der Booking.com-Kalender ist unerwartet groß.")
    return parse_ical(data.decode("utf-8-sig"))


def sync_booking_calendar(force=False):
    """Ersetzt nur Booking.com-Importe; manuelle Sperren bleiben erhalten."""
    site_settings = SiteSettings.load()
    url = dj_settings.BOOKING_ICAL_URL
    if not site_settings.booking_calendar_enabled:
        return {"status": "disabled", "imported": 0}
    if not url:
        raise ValueError("BOOKING_ICAL_URL fehlt in der .env-Datei.")

    now = timezone.now()
    interval = timedelta(minutes=max(dj_settings.BOOKING_ICAL_SYNC_MINUTES, 1))
    if not force and site_settings.booking_last_sync_at:
        if now - site_settings.booking_last_sync_at < interval:
            return {"status": "fresh", "imported": None}

    try:
        events = fetch_booking_events(url)
        with transaction.atomic():
            BlockedPeriod.objects.filter(source=BlockedPeriod.SOURCE_BOOKING).delete()
            BlockedPeriod.objects.bulk_create([
                BlockedPeriod(
                    start_date=event.start_date,
                    end_date=event.end_date,
                    note="Booking.com",
                    source=BlockedPeriod.SOURCE_BOOKING,
                    external_uid=event.uid,
                )
                for event in events
            ])
            site_settings.booking_last_sync_at = now
            site_settings.booking_last_sync_error = ""
            site_settings.save(update_fields=(
                "booking_last_sync_at", "booking_last_sync_error",
            ))
    except Exception as exc:
        site_settings.booking_last_sync_error = str(exc)[:2000]
        site_settings.save(update_fields=("booking_last_sync_error",))
        raise

    return {"status": "synced", "imported": len(events)}


def sync_booking_calendar_safely():
    """Öffentliche Seiten bleiben bei einem Netzwerkfehler verfügbar."""
    try:
        return sync_booking_calendar()
    except Exception:
        logger.exception("Booking.com-Kalender konnte nicht synchronisiert werden")
        return {"status": "error", "imported": 0}
