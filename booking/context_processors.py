"""Stellt in allen Templates "t" (Texte in der aktuellen Sprache)
und "site_settings" bereit."""
from django.utils import translation

from .models import SiteSettings
from .texts import get_texts


def site_texts(request):
    lang = translation.get_language() or "de"
    return {
        "t": get_texts(lang),
        "lang": "en" if lang.startswith("en") else "de",
        "site_settings": SiteSettings.load(),
    }
