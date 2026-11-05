import time
from datetime import timedelta
from decimal import Decimal

from django.core import mail
from django.test import Client, TestCase, override_settings
from django.utils import timezone

from .models import BlockedPeriod, Inquiry


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
                   DEFAULT_FROM_EMAIL="haus@example.com", OWNER_EMAIL="owner@example.com",
                   BOOKING_ICAL_URL="", SITE_PREVIEW=False)
class OnePageTests(TestCase):
    def data(self):
        arrival = timezone.localdate() + timedelta(days=30)
        return {"arrival": arrival, "departure": arrival + timedelta(days=5),
                "adults": 2, "children": 0, "name": "Test Guest", "email": "guest@example.com",
                "message": "", "website": "", "form_ts": str(time.time() - 10)}

    def test_old_links_land_on_the_relevant_section(self):
        routes = {"wohnung/": "wohnung", "preise/": "preise", "anfrage/": "anfrage",
                  "gastgeber/": "gastgeber", "anreise/": "anreise", "regeln/": "regeln",
                  "gut-zu-wissen/": "fragen", "galerie/": "fotos",
                  "galerie/?category=apartment": "wohnungsfotos", "galerie/?category=outdoor": "garten"}
        for lang in ("de", "en"):
            for path, anchor in routes.items():
                self.assertRedirects(self.client.get(f"/{lang}/{path}"), f"/{lang}/#{anchor}",
                                     status_code=301, fetch_redirect_response=False)
            self.assertRedirects(self.client.get(f"/{lang}/galerie/?category=area"),
                                 f"/{lang}/galerie/area/", status_code=301)

    def test_main_page_inquiry_uses_csrf_and_sends_once(self):
        client = Client(enforce_csrf_checks=True)
        client.get("/de/")
        data = self.data()
        self.assertEqual(client.post("/de/", data).status_code, 403)
        self.assertFalse(Inquiry.objects.exists())
        data["csrfmiddlewaretoken"] = client.cookies["csrftoken"].value
        self.assertRedirects(client.post("/de/", data), "/de/anfrage/danke/")
        self.assertEqual(Inquiry.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 2)

    def test_blocked_dates_still_show_errors_on_the_main_page(self):
        data = self.data()
        BlockedPeriod.objects.create(start_date=data["arrival"], end_date=data["departure"])
        response = self.client.post("/de/", data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("arrival", response.context["form"].errors)
        self.assertContains(response, 'id="anfrage"')
        self.assertFalse(Inquiry.objects.exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_older_teenager_tax_reaches_saved_inquiry_and_both_emails(self):
        data = self.data()
        data.update(children=2, taxable_children=1)
        self.assertRedirects(self.client.post("/de/", data), "/de/anfrage/danke/")
        inquiry = Inquiry.objects.get()
        self.assertEqual(inquiry.taxable_children, 1)
        self.assertEqual(inquiry.quoted_total, Decimal("1047.50"))
        self.assertEqual(len(mail.outbox), 2)
        for message in mail.outbox:
            self.assertIn("Davon 16–17 Jahre: 1", message.body)
            self.assertIn("Nächtigungstaxe (ab 16 Jahren): 67.50 €", message.body)

    @override_settings(SITE_PREVIEW=True)
    def test_preview_cannot_submit_or_store_an_inquiry(self):
        response = self.client.post("/de/", self.data())
        self.assertContains(response, 'id="preview-inquiry-button"')
        self.assertNotContains(response, "<form")
        self.assertNotContains(response, 'type="submit"')
        self.assertFalse(Inquiry.objects.exists())
        self.assertEqual(len(mail.outbox), 0)
