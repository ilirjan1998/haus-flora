import time
from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from django.core import mail
from django.test import TestCase, override_settings
from django.utils import timezone

from .emails import send_inquiry_mails
from .forms import InquiryForm
from .ical_sync import parse_ical, sync_booking_calendar
from .models import BlockedPeriod, Inquiry, SiteSettings
from .pricing import price_breakdown, total_price


class PricingTests(TestCase):
    def setUp(self):
        self.settings = SiteSettings.load()

    def test_total_includes_cleaning_and_city_tax(self):
        price = price_breakdown(self.settings, adults=2, children=0, nights=5)
        self.assertEqual(price["accommodation"], Decimal("750.00"))
        self.assertEqual(price["cleaning"], Decimal("60.00"))
        self.assertEqual(price["city_tax"], Decimal("27.00"))
        self.assertEqual(price["total"], Decimal("837.00"))
        self.assertEqual(total_price(self.settings, 2, 0, 5), Decimal("837.00"))

    def test_unsupported_guest_combination_has_no_price(self):
        self.assertIsNone(total_price(self.settings, 1, 1, 5))


class BookingCalendarSyncTests(TestCase):
    ICAL = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID:booking-test-1
DTSTART;VALUE=DATE:20260810
DTEND;VALUE=DATE:20260815
END:VEVENT
END:VCALENDAR
"""

    class FakeResponse:
        def __init__(self, content):
            self.content = content

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self, size=-1):
            return self.content

    def test_parser_reads_booking_event(self):
        events = parse_ical(self.ICAL)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].uid, "booking-test-1")
        self.assertEqual(events[0].start_date.isoformat(), "2026-08-10")
        self.assertEqual(events[0].end_date.isoformat(), "2026-08-15")

    @override_settings(
        BOOKING_ICAL_URL="https://admin.booking.com/hotel/hoteladmin/ical.html?t=test",
        BOOKING_ICAL_SYNC_MINUTES=30,
    )
    def test_sync_replaces_booking_periods_and_preserves_manual_periods(self):
        settings = SiteSettings.load()
        settings.booking_calendar_enabled = True
        settings.save()
        BlockedPeriod.objects.create(
            start_date=timezone.localdate() + timedelta(days=1),
            end_date=timezone.localdate() + timedelta(days=2),
            note="Privat",
        )
        BlockedPeriod.objects.create(
            start_date=timezone.localdate() + timedelta(days=3),
            end_date=timezone.localdate() + timedelta(days=4),
            source=BlockedPeriod.SOURCE_BOOKING,
            external_uid="stale",
        )

        response = self.FakeResponse(self.ICAL.encode())
        with patch("booking.ical_sync.urlopen", return_value=response):
            result = sync_booking_calendar(force=True)

        self.assertEqual(result, {"status": "synced", "imported": 1})
        self.assertTrue(BlockedPeriod.objects.filter(note="Privat").exists())
        self.assertFalse(BlockedPeriod.objects.filter(external_uid="stale").exists())
        imported = BlockedPeriod.objects.get(external_uid="booking-test-1")
        self.assertEqual(imported.source, BlockedPeriod.SOURCE_BOOKING)
        self.assertEqual(imported.start_date.isoformat(), "2026-08-10")


class InquiryFormTests(TestCase):
    def setUp(self):
        self.settings = SiteSettings.load()
        self.arrival = timezone.localdate() + timedelta(days=10)

    def form_data(self, **changes):
        data = {
            "arrival": self.arrival,
            "departure": self.arrival + timedelta(days=5),
            "adults": 2,
            "children": 0,
            "name": "Test Gast",
            "email": "gast@example.com",
            "message": "",
            "website": "",
            "form_ts": str(time.time() - 10),
        }
        data.update(changes)
        return data

    def test_valid_inquiry(self):
        form = InquiryForm(self.form_data(), site_settings=self.settings, lang="de")
        self.assertTrue(form.is_valid(), form.errors)

    def test_blocked_dates_are_rejected(self):
        BlockedPeriod.objects.create(
            start_date=self.arrival + timedelta(days=2),
            end_date=self.arrival + timedelta(days=4),
        )
        form = InquiryForm(self.form_data(), site_settings=self.settings, lang="de")
        self.assertFalse(form.is_valid())
        self.assertIn("arrival", form.errors)


class PageTests(TestCase):
    def test_all_public_pages_work_in_both_languages(self):
        paths = (
            "",
            "wohnung/",
            "galerie/",
            "preise/",
            "umgebung/",
            "regeln/",
            "anfrage/",
            "anfrage/danke/",
            "impressum/",
            "datenschutz/",
        )
        for language in ("de", "en"):
            for suffix in paths:
                path = f"/{language}/{suffix}"
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200, path)
                self.assertContains(response, "Haus Flora")

    def test_availability_api_returns_json(self):
        for path in ("/de/api/verfuegbarkeit/", "/en/api/verfuegbarkeit/"):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"blocked": []})


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="haus@example.com",
    OWNER_EMAIL="owner@example.com",
)
class EmailTests(TestCase):
    def test_owner_reply_goes_to_guest_and_prices_are_dynamic(self):
        settings = SiteSettings.load()
        settings.cleaning_fee = Decimal("75.00")
        settings.save()
        arrival = timezone.localdate() + timedelta(days=20)
        inquiry = Inquiry.objects.create(
            arrival=arrival,
            departure=arrival + timedelta(days=5),
            adults=2,
            children=0,
            name="Test Gast",
            email="gast@example.com",
            quoted_total=Decimal("852.00"),
            language="de",
        )

        send_inquiry_mails(inquiry, settings)

        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].reply_to, ["gast@example.com"])
        self.assertEqual(
            mail.outbox[0].subject,
            f"[Haus Flora] Neue Anfrage: Test Gast | "
            f"{arrival.strftime('%d.%m.%Y')}–"
            f"{(arrival + timedelta(days=5)).strftime('%d.%m.%Y')}",
        )
        self.assertIn("Endreinigung: 75.00 €", mail.outbox[0].body)
