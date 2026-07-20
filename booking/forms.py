"""
Anfrageformular inkl. Spam-Schutz und allen fachlichen Prüfungen.

Spam-Schutz (ohne Captcha, gästefreundlich):
1. Honeypot: verstecktes Feld "website" – Menschen sehen es nicht,
   Bots füllen es aus -> Anfrage wird abgelehnt.
2. Zeitprüfung: das Formular trägt einen Zeitstempel; wird es in
   unter 3 Sekunden abgeschickt, war es sehr sicher ein Bot.
"""
import time

from django import forms
from django.utils import timezone

from .models import BlockedPeriod
from .pricing import combo_allowed

ERRORS = {
    "de": {
        "honeypot": "Die Anfrage konnte nicht verarbeitet werden.",
        "too_fast": "Das ging zu schnell – bitte noch einmal absenden.",
        "past": "Die Anreise darf nicht in der Vergangenheit liegen.",
        "order": "Die Abreise muss nach der Anreise liegen.",
        "min_nights": "Der Mindestaufenthalt beträgt {n} Nächte.",
        "combo": "Diese Personenkombination ist leider nicht buchbar (max. 3 Erwachsene, max. 4 Personen).",
        "occupied": "In diesem Zeitraum ist die Wohnung leider schon belegt. Bitte wählt andere Daten.",
    },
    "en": {
        "honeypot": "Your inquiry could not be processed.",
        "too_fast": "That was too fast – please submit again.",
        "past": "The arrival date must not be in the past.",
        "order": "The departure date must be after the arrival date.",
        "min_nights": "The minimum stay is {n} nights.",
        "combo": "This combination of guests is not bookable (max. 3 adults, max. 4 guests).",
        "occupied": "The apartment is already occupied in this period. Please choose different dates.",
    },
}


class InquiryForm(forms.Form):
    arrival = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    departure = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    adults = forms.TypedChoiceField(coerce=int, choices=[(1, "1"), (2, "2"), (3, "3")], initial=2)
    children = forms.TypedChoiceField(coerce=int, choices=[(0, "0"), (1, "1"), (2, "2")], initial=0)
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 4}), required=False)

    # Spam-Schutz
    website = forms.CharField(required=False)          # Honeypot (per CSS versteckt)
    form_ts = forms.CharField(required=False)          # Zeitstempel beim Laden

    def __init__(self, *args, site_settings=None, lang="de", **kwargs):
        super().__init__(*args, **kwargs)
        self.site_settings = site_settings
        self.err = ERRORS["en"] if lang == "en" else ERRORS["de"]
        today = timezone.localdate().isoformat()
        self.fields["arrival"].widget.attrs["min"] = today
        self.fields["departure"].widget.attrs["min"] = today

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError(self.err["honeypot"])
        return ""

    def clean_form_ts(self):
        value = self.cleaned_data.get("form_ts", "")
        try:
            loaded_at = float(value)
        except (TypeError, ValueError):
            raise forms.ValidationError(self.err["honeypot"])
        if time.time() - loaded_at < 3:
            raise forms.ValidationError(self.err["too_fast"])
        return value

    def clean(self):
        data = super().clean()
        arrival = data.get("arrival")
        departure = data.get("departure")
        adults = data.get("adults")
        children = data.get("children")

        if adults is not None and children is not None:
            if not combo_allowed(adults, children):
                self.add_error("adults", self.err["combo"])

        if arrival and departure:
            today = timezone.localdate()
            if arrival < today:
                self.add_error("arrival", self.err["past"])
            if departure <= arrival:
                self.add_error("departure", self.err["order"])
            else:
                nights = (departure - arrival).days
                min_nights = self.site_settings.min_nights if self.site_settings else 5
                if nights < min_nights:
                    self.add_error("departure", self.err["min_nights"].format(n=min_nights))
                if self._overlaps(arrival, departure):
                    self.add_error("arrival", self.err["occupied"])
        return data

    @staticmethod
    def _overlaps(arrival, departure):
        """Belegt sind die Nächte start..(end-1). Zwei Zeiträume überlappen,
        wenn arrival < p.end_date und departure > p.start_date. Dadurch ist
        der Abreisetag eines Gastes automatisch als Anreisetag frei."""
        return BlockedPeriod.objects.filter(
            start_date__lt=departure, end_date__gt=arrival
        ).exists()
