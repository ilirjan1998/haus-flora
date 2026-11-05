"""
Datenmodelle für Haus Flora.

- Photo:          Bilder für die Galerie (im Admin verwaltbar)
- BlockedPeriod:  belegte Zeiträume, die im Kalender rot erscheinen
- Inquiry:        eingegangene Anfragen von Gästen
- SiteSettings:   zentrale Einstellungen (Preise, Regeln, Schalter) –
                  existiert genau einmal ("Singleton")
"""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models


class Photo(models.Model):
    CATEGORY_CHOICES = [("apartment", "Wohnung"), ("outdoor", "Garten & Pool"), ("area", "Umgebung")]
    category = models.CharField("Bereich", max_length=20, choices=CATEGORY_CHOICES, default="apartment")
    image = models.ImageField("Bild", upload_to="galerie/")
    title_de = models.CharField("Titel (Deutsch)", max_length=120, blank=True)
    title_en = models.CharField("Titel (Englisch)", max_length=120, blank=True)
    order = models.PositiveIntegerField(
        "Reihenfolge", default=0,
        help_text="Kleinere Zahl = weiter vorne in der Galerie.",
    )
    is_active = models.BooleanField("Sichtbar", default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Foto"
        verbose_name_plural = "Fotos"

    def __str__(self):
        return self.title_de or f"Foto {self.pk}"

    def title(self, lang):
        return self.title_en if lang == "en" and self.title_en else self.title_de


class BlockedPeriod(models.Model):
    """Ein belegter Zeitraum. Die Nacht des Abreisetags ist wieder frei,
    d. h. der Abreisetag eines Gastes kann der Anreisetag des nächsten sein."""
    SOURCE_MANUAL = "manual"
    SOURCE_BOOKING = "booking"
    SOURCE_CHOICES = [
        (SOURCE_MANUAL, "Manuell"),
        (SOURCE_BOOKING, "Booking.com"),
    ]

    start_date = models.DateField("Anreise (erster belegter Tag)")
    end_date = models.DateField("Abreise (an diesem Tag wieder frei)")
    note = models.CharField(
        "Notiz", max_length=200, blank=True,
        help_text="Nur für euch sichtbar, z. B. Name des Gastes.",
    )
    source = models.CharField(
        "Quelle", max_length=20, choices=SOURCE_CHOICES,
        default=SOURCE_MANUAL, db_index=True,
    )
    external_uid = models.CharField(
        "Externe ID", max_length=255, blank=True, db_index=True,
        help_text="Wird bei importierten Kalenderterminen automatisch gesetzt.",
    )

    class Meta:
        ordering = ["start_date"]
        verbose_name = "Belegter Zeitraum"
        verbose_name_plural = "Belegte Zeiträume"

    def __str__(self):
        return f"{self.start_date} – {self.end_date} {self.note}".strip()

    def clean(self):
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            raise ValidationError({
                "end_date": "Die Abreise muss nach der Anreise liegen."
            })


class Inquiry(models.Model):
    arrival = models.DateField("Anreise")
    departure = models.DateField("Abreise")
    adults = models.PositiveSmallIntegerField("Erwachsene")
    children = models.PositiveSmallIntegerField("Kinder", default=0)
    taxable_children = models.PositiveSmallIntegerField("Davon 16–17 Jahre", default=0)
    name = models.CharField("Name", max_length=120)
    email = models.EmailField("E-Mail")
    message = models.TextField("Nachricht", blank=True)
    quoted_total = models.DecimalField(
        "Angezeigter Gesamtpreis (€)", max_digits=8, decimal_places=2,
        null=True, blank=True,
        help_text="Gesamtschätzung inklusive Endreinigung und Ortstaxe.",
    )
    language = models.CharField("Sprache des Gastes", max_length=5, default="de")
    created_at = models.DateTimeField("Eingegangen am", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Anfrage"
        verbose_name_plural = "Anfragen"

    def __str__(self):
        return f"{self.name}: {self.arrival} – {self.departure}"

    @property
    def nights(self):
        return (self.departure - self.arrival).days


DEFAULT_HOUSE_RULES_DE = """Check-in ab 14:00 Uhr, Check-out bis 10:00 Uhr.
Keine Haustiere.
Rauchen ist in der Wohnung nicht gestattet.
Nachtruhe von 22:00 bis 07:00 Uhr."""

DEFAULT_HOUSE_RULES_EN = """Check-in from 2:00 pm, check-out until 10:00 am.
No pets.
Smoking is not allowed inside the apartment.
Quiet hours from 10:00 pm to 7:00 am."""

DEFAULT_POOL_RULES_DE = """Poolbenutzung auf eigene Gefahr.
Kinder nur in Begleitung eines Erwachsenen.
Bitte vor dem Baden duschen.
Keine Glasflaschen im Poolbereich."""

DEFAULT_POOL_RULES_EN = """Use of the pool is at your own risk.
Children only when accompanied by an adult.
Please shower before swimming.
No glass bottles in the pool area."""

DEFAULT_CANCELLATION_DE = """Bis 42 Tage vor Anreise: kostenlose Stornierung.
Ab 42 Tage vor Anreise: 50 % des Gesamtpreises."""

DEFAULT_CANCELLATION_EN = """Up to 42 days before arrival: free cancellation.
Less than 42 days before arrival: 50% of the total price."""


class SiteSettings(models.Model):
    """Zentrale Einstellungen – es gibt genau einen Datensatz (pk=1)."""

    # Schalter
    booking_enabled = models.BooleanField(
        "Anfragen aktiviert", default=True,
        help_text="Ausschalten, um das Anfrageformular vorübergehend zu deaktivieren.",
    )
    calendar_visible = models.BooleanField(
        "Kalender sichtbar", default=True,
        help_text="Ausschalten, um den Belegungskalender komplett auszublenden.",
    )
    booking_calendar_enabled = models.BooleanField(
        "Booking.com-Kalender synchronisieren", default=False,
        help_text="Aktivieren, nachdem BOOKING_ICAL_URL in der .env eingetragen wurde.",
    )
    booking_last_sync_at = models.DateTimeField(
        "Booking.com zuletzt synchronisiert", null=True, blank=True, editable=False,
    )
    booking_last_sync_error = models.TextField(
        "Letzter Booking.com-Fehler", blank=True, editable=False,
    )

    # Preise pro Nacht
    price_2_adults = models.DecimalField("2 Erwachsene (€/Nacht)", max_digits=6, decimal_places=2, default=150)
    price_3_adults = models.DecimalField("3 Erwachsene (€/Nacht)", max_digits=6, decimal_places=2, default=175)
    price_2a_1c = models.DecimalField("2 Erwachsene + 1 Kind (€/Nacht)", max_digits=6, decimal_places=2, default=165)
    price_2a_2c = models.DecimalField("2 Erwachsene + 2 Kinder (€/Nacht)", max_digits=6, decimal_places=2, default=180)
    single_adult_discount = models.DecimalField(
        "Rabatt für 1 Erwachsenen (%)", max_digits=4, decimal_places=1, default=5,
        help_text="Abschlag auf den Preis für 2 Erwachsene.",
    )
    cleaning_fee = models.DecimalField("Endreinigung (€)", max_digits=6, decimal_places=2, default=80)
    city_tax = models.DecimalField("Nächtigungstaxe pro Person ab 16 (€/Nacht)", max_digits=5, decimal_places=2, default=Decimal("4.50"))
    min_nights = models.PositiveSmallIntegerField("Mindestaufenthalt (Nächte)", default=5)

    # Only confirmed owner details should be entered here. Blank extras stay hidden.
    public_email = models.EmailField("Öffentliche E-Mail", default="markajflore@gmail.com")
    public_phone = models.CharField("Öffentliche Telefonnummer", max_length=40, blank=True)
    property_address = models.CharField("Adresse der Unterkunft", max_length=250, blank=True,
        default="Jägerweg 20, 9551 Bodensdorf",
        help_text="Straße, Hausnummer, PLZ und Ort. Wird für die Anreise angezeigt.")
    operator_name = models.CharField("Vollständiger Betreibername", max_length=200, blank=True, default="Flore Markaj")
    operator_address = models.TextField("Betreiberanschrift", blank=True, default="Jägerweg 20\n9551 Bodensdorf\nÖsterreich")
    host_name = models.CharField("Anzeigename der Gastgeber", max_length=150, default="Familie Markaj")
    host_photo = models.ImageField("Gastgeberfoto", upload_to="gastgeber/", blank=True)
    host_intro_de = models.TextField("Vorstellung (Deutsch)", blank=True)
    host_intro_en = models.TextField("Vorstellung (Englisch)", blank=True)
    floor_plan = models.ImageField("Grundriss", upload_to="wohnung/", blank=True)
    amenities_detail_de = models.TextField("Weitere Ausstattung (Deutsch)", blank=True,
        help_text="Nur tatsächlich vorhandene Ausstattung; ein Punkt pro Zeile.")
    amenities_detail_en = models.TextField("Weitere Ausstattung (Englisch)", blank=True)
    bike_service_de = models.TextField("Radservice am Haus (Deutsch)", blank=True,
        help_text="Nur bestätigte Leistungen, z. B. sicherer Abstellplatz. Leer = keine Zusage.")
    bike_service_en = models.TextField("Radservice am Haus (Englisch)", blank=True)
    arrival_notes_de = models.TextField("Letzter Weg zur Unterkunft (Deutsch)", blank=True)
    arrival_notes_en = models.TextField("Letzter Weg zur Unterkunft (Englisch)", blank=True)
    payment_methods_de = models.CharField("Zahlungsarten (Deutsch)", max_length=250, blank=True)
    payment_methods_en = models.CharField("Zahlungsarten (Englisch)", max_length=250, blank=True)
    deposit_de = models.TextField("Anzahlung (Deutsch)", blank=True)
    deposit_en = models.TextField("Anzahlung (Englisch)", blank=True)
    balance_de = models.TextField("Restzahlung (Deutsch)", blank=True)
    balance_en = models.TextField("Restzahlung (Englisch)", blank=True)
    security_deposit_de = models.TextField("Kaution (Deutsch)", blank=True)
    security_deposit_en = models.TextField("Kaution (Englisch)", blank=True)

    # Regeln (zweisprachig, im Admin bearbeitbar; eine Zeile = ein Punkt)
    house_rules_de = models.TextField("Hausregeln (Deutsch)", default=DEFAULT_HOUSE_RULES_DE)
    house_rules_en = models.TextField("Hausregeln (Englisch)", default=DEFAULT_HOUSE_RULES_EN)
    pool_rules_de = models.TextField("Poolregeln (Deutsch)", default=DEFAULT_POOL_RULES_DE)
    pool_rules_en = models.TextField("Poolregeln (Englisch)", default=DEFAULT_POOL_RULES_EN)
    cancellation_de = models.TextField("Stornobedingungen (Deutsch)", default=DEFAULT_CANCELLATION_DE)
    cancellation_en = models.TextField("Stornobedingungen (Englisch)", default=DEFAULT_CANCELLATION_EN)

    class Meta:
        verbose_name = "Einstellungen"
        verbose_name_plural = "Einstellungen"

    def __str__(self):
        return "Einstellungen Haus Flora"

    def save(self, *args, **kwargs):
        self.pk = 1  # erzwingt: es gibt immer nur einen Datensatz
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def rules(self, field, lang):
        """Liefert z. B. rules("house_rules", "en") als Liste von Zeilen."""
        text = getattr(self, f"{field}_{'en' if lang == 'en' else 'de'}")
        return [line.strip() for line in text.splitlines() if line.strip()]

    def localized(self, field, lang):
        # Do not silently show German terms on an English booking page.
        return getattr(self, f"{field}_{'en' if lang == 'en' else 'de'}", "")


class GuestReview(models.Model):
    display_name = models.CharField("Anzeigename", max_length=100)
    text_de = models.TextField("Gästestimme (Deutsch)")
    text_en = models.TextField("Gästestimme (Englisch)", blank=True)
    source_label = models.CharField("Quelle", max_length=150, blank=True)
    source_url = models.URLField("Link zur Originalbewertung", blank=True)
    permission_confirmed = models.BooleanField("Veröffentlichung erlaubt", default=False,
        help_text="Nur echte Bewertungen mit geklärter Erlaubnis veröffentlichen.")
    is_published = models.BooleanField("Sichtbar", default=False)
    order = models.PositiveIntegerField("Reihenfolge", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Gästestimme"
        verbose_name_plural = "Gästestimmen"

    def __str__(self):
        return self.display_name

    def clean(self):
        super().clean()
        if self.is_published and not self.permission_confirmed:
            raise ValidationError("Vor Veröffentlichung bitte die Erlaubnis bestätigen.")
