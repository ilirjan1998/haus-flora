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
from .models import BlockedPeriod, Inquiry, SiteSettings, GuestReview, Photo
from .pricing import price_breakdown, total_price


class PricingTests(TestCase):
    def setUp(self):
        self.settings = SiteSettings.load()

    def test_total_includes_cleaning_and_city_tax(self):
        price = price_breakdown(self.settings, adults=2, children=0, nights=5)
        self.assertEqual(price["accommodation"], Decimal("750.00"))
        self.assertEqual(price["cleaning"], Decimal("80.00"))
        self.assertEqual(price["city_tax"], Decimal("45.00"))
        self.assertEqual(price["total"], Decimal("875.00"))
        self.assertEqual(total_price(self.settings, 2, 0, 5), Decimal("875.00"))

    def test_children_under_sixteen_are_exempt_and_older_teenagers_count(self):
        for teenagers, expected_tax, expected_total in ((0, "45.00", "1025.00"),
                                                       (1, "67.50", "1047.50"),
                                                       (2, "90.00", "1070.00")):
            with self.subTest(teenagers=teenagers):
                price = price_breakdown(self.settings, 2, 2, 5, teenagers)
                self.assertEqual(price["accommodation"], Decimal("900.00"))
                self.assertEqual(price["city_tax"], Decimal(expected_tax))
                self.assertEqual(price["total"], Decimal(expected_total))

    def test_taxable_children_must_be_part_of_the_party(self):
        self.assertIsNone(total_price(self.settings, 2, 1, 5, 2))
        self.assertIsNone(total_price(self.settings, 2, 1, 5, -1))

    def test_three_adults_price_and_tax(self):
        price = price_breakdown(self.settings, 3, 0, 5)
        self.assertEqual(price["per_night"], Decimal("175.00"))
        self.assertEqual(price["accommodation"], Decimal("875.00"))
        self.assertEqual(price["city_tax"], Decimal("67.50"))
        self.assertEqual(price["total"], Decimal("1022.50"))
        self.assertIsNone(total_price(self.settings, 3, 1, 5))
        self.assertIn((3, "3"), InquiryForm().fields["adults"].choices)

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

    def test_tax_age_selection_is_required_for_children_and_validated(self):
        for children, teenagers in ((1, ""), (1, 2), (0, 1), (2, -1)):
            with self.subTest(children=children, teenagers=teenagers):
                form = InquiryForm(self.form_data(children=children, taxable_children=teenagers),
                                   site_settings=self.settings, lang="de")
                self.assertFalse(form.is_valid())
                self.assertIn("taxable_children", form.errors)
        for teenagers in (0, 1, 2):
            form = InquiryForm(self.form_data(children=2, taxable_children=teenagers),
                               site_settings=self.settings, lang="en")
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
        paths = ("", "galerie/area/", "umgebung/", "radfahren/", "urlaubslinks/",
                 "anfrage/danke/", "impressum/", "datenschutz/")
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
            quoted_total=Decimal("870.00"),
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


class GuestGuideTests(TestCase):
    def test_payments_do_not_invent_terms_and_use_selected_language(self):
        settings = SiteSettings.load()
        response = self.client.get("/de/")
        self.assertContains(response, "Eure Anfrage löst keine Onlinezahlung aus")
        settings.payment_methods_de = "Überweisung nach Vereinbarung"
        settings.deposit_de = "Individuell vereinbarte Anzahlung"
        settings.save()
        self.assertContains(self.client.get("/de/"), settings.payment_methods_de)
        self.assertNotContains(self.client.get("/en/"), settings.payment_methods_de)
        settings.payment_methods_en = "Bank transfer as agreed"
        settings.save()
        self.assertContains(self.client.get("/en/"), settings.payment_methods_en)

    def test_only_approved_real_reviews_are_public(self):
        review = GuestReview.objects.create(display_name="Test guest", text_de="Review fixture", is_published=True)
        self.assertNotContains(self.client.get("/de/"), "Review fixture")
        review.permission_confirmed = True
        review.save()
        self.assertContains(self.client.get("/de/"), "Review fixture")
        self.assertContains(self.client.get("/en/"), "Original review in German")

    def test_main_gallery_and_region_keep_hidden_photos_private(self):
        Photo.objects.create(image="test-room.jpg", title_de="Room fixture", category="apartment")
        Photo.objects.create(image="test-garden.jpg", title_de="Garden fixture", category="outdoor")
        Photo.objects.create(image="test-area.jpg", title_de="Area fixture", category="area")
        Photo.objects.create(image="test-hidden.jpg", title_de="Hidden fixture", category="area", is_active=False)
        home = self.client.get("/de/")
        self.assertContains(home, "Garden fixture")
        self.assertContains(home, "Room fixture")
        self.assertNotContains(home, "Hidden fixture")
        region = self.client.get("/de/galerie/area/")
        self.assertContains(region, "Area fixture")
        self.assertNotContains(region, "Room fixture")
        self.assertNotContains(region, "Garden fixture")
        self.assertNotContains(region, "Hidden fixture")

    def test_address_and_owner_text_are_escaped(self):
        settings = SiteSettings.load()
        settings.property_address = "Testweg 1 & 2, Bodensdorf"
        settings.host_intro_de = "<script>alert('test')</script>"
        settings.save()
        self.assertContains(self.client.get("/de/"), "Testweg 1 &amp; 2")
        response = self.client.get("/de/")
        self.assertContains(response, "&lt;script&gt;")
        self.assertNotContains(response, "<script>alert")
