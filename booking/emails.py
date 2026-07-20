"""
E-Mail-Versand bei einer neuen Anfrage:
1. Benachrichtigung an euch (OWNER_EMAIL, siehe .env)
2. Bestätigung an den Gast – in dessen Sprache (Deutsch oder Englisch)

Fehler beim Versand lassen die Anfrage NICHT scheitern: sie ist in der
Datenbank gespeichert und im Admin sichtbar, auch wenn eine Mail hakt.
"""
import logging

from django.conf import settings as dj_settings
from django.core.mail import EmailMessage

from .pricing import price_breakdown

logger = logging.getLogger(__name__)


def send_inquiry_mails(inquiry, site_settings):
    _send_owner_mail(inquiry, site_settings)
    _send_guest_mail(inquiry, site_settings)


def _send_owner_mail(inquiry, site_settings):
    price = price_breakdown(
        site_settings, inquiry.adults, inquiry.children, inquiry.nights
    )
    arrival = inquiry.arrival.strftime("%d.%m.%Y")
    departure = inquiry.departure.strftime("%d.%m.%Y")
    subject = f"[Haus Flora] Neue Anfrage: {inquiry.name} | {arrival}–{departure}"
    body = (
        "Neue Anfrage über die Website Haus Flora:\n\n"
        f"Name:       {inquiry.name}\n"
        f"E-Mail:     {inquiry.email}\n"
        f"Anreise:    {inquiry.arrival.strftime('%d.%m.%Y')}\n"
        f"Abreise:    {inquiry.departure.strftime('%d.%m.%Y')} ({inquiry.nights} Nächte)\n"
        f"Erwachsene: {inquiry.adults}\n"
        f"Kinder:     {inquiry.children}\n"
        f"Nächtigung: {price['accommodation']} €\n"
        f"Endreinigung: {price['cleaning']} €\n"
        f"Ortstaxe: {price['city_tax']} € (vor Ort)\n"
        f"Angezeigter Gesamtpreis: {inquiry.quoted_total} €\n\n"
        f"Nachricht:\n{inquiry.message or '-'}\n\n"
        "Zum Antworten einfach direkt an die E-Mail-Adresse des Gastes schreiben."
    )
    _safe_send(subject, body, [dj_settings.OWNER_EMAIL], reply_to_guest=inquiry.email)


def _send_guest_mail(inquiry, site_settings):
    price = price_breakdown(
        site_settings, inquiry.adults, inquiry.children, inquiry.nights
    )
    if inquiry.language == "en":
        subject = "Haus Flora – we received your inquiry"
        body = (
            f"Dear {inquiry.name},\n\n"
            "thank you for your inquiry! Here is a summary:\n\n"
            f"Arrival:    {inquiry.arrival.strftime('%d.%m.%Y')}\n"
            f"Departure:  {inquiry.departure.strftime('%d.%m.%Y')} ({inquiry.nights} nights)\n"
            f"Adults:     {inquiry.adults}\n"
            f"Children:   {inquiry.children}\n"
            f"Accommodation: EUR {price['accommodation']}\n"
            f"Final cleaning: EUR {price['cleaning']}\n"
            f"Local tax: EUR {price['city_tax']} (payable on site)\n"
            f"Estimated total: EUR {inquiry.quoted_total}\n\n"
            "This is not a binding booking yet – we will get back to you "
            "personally by e-mail as soon as possible to confirm availability "
            "and all details.\n\n"
            "Best regards,\nFamily Markaj – Haus Flora, Bodensdorf at Lake Ossiach"
        )
    else:
        subject = "Haus Flora – wir haben eure Anfrage erhalten"
        body = (
            f"Hallo {inquiry.name},\n\n"
            "vielen Dank für die Anfrage! Hier die Zusammenfassung:\n\n"
            f"Anreise:    {inquiry.arrival.strftime('%d.%m.%Y')}\n"
            f"Abreise:    {inquiry.departure.strftime('%d.%m.%Y')} ({inquiry.nights} Nächte)\n"
            f"Erwachsene: {inquiry.adults}\n"
            f"Kinder:     {inquiry.children}\n"
            f"Nächtigung: {price['accommodation']} €\n"
            f"Endreinigung: {price['cleaning']} €\n"
            f"Ortstaxe: {price['city_tax']} € (vor Ort)\n"
            f"Voraussichtlicher Gesamtpreis: {inquiry.quoted_total} €\n\n"
            "Das ist noch keine verbindliche Buchung – wir melden uns so "
            "schnell wie möglich persönlich per E-Mail, um Verfügbarkeit und "
            "alle Details zu bestätigen.\n\n"
            "Liebe Grüße\nFamilie Markaj – Haus Flora, Bodensdorf am Ossiacher See"
        )
    _safe_send(subject, body, [inquiry.email])


def _safe_send(subject, body, recipients, reply_to_guest=None):
    try:
        message = EmailMessage(
            subject=subject,
            body=body,
            from_email=dj_settings.DEFAULT_FROM_EMAIL,
            to=recipients,
            reply_to=[reply_to_guest] if reply_to_guest else None,
        )
        message.send(fail_silently=False)
    except Exception:  # noqa: BLE001 – Versand darf die Anfrage nie blockieren
        logger.exception("E-Mail-Versand fehlgeschlagen an %s", recipients)
