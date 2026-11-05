"""Stellt in allen Templates "t" (Texte in der aktuellen Sprache)
und "site_settings" bereit."""
from django.utils import translation
from django.conf import settings
from django.urls import reverse

from .amenity_details import AMENITY_GROUPS
from .models import SiteSettings
from .texts import get_texts
from .ux_texts import NAVIGATION, GUIDE_PAGES
from .seo import page_metadata
from .navigation import SECTION_ANCHORS


AMENITY_ICONS = (
    "wifi", "cooling", "kitchen", "shower", "tv", "pool",
    "parking", "terrace", "laundry", "linen",
)


def site_texts(request):
    lang = translation.get_language() or "de"
    lang = "en" if lang.startswith("en") else "de"
    config = SiteSettings.load()
    texts = get_texts(lang)
    home_url = reverse("booking:home")
    navigation = [{"name": name, "route": f"booking:{name}", "label": texts[key],
                   "url": home_url + "#" + SECTION_ANCHORS[name] if name in SECTION_ANCHORS else reverse(f"booking:{name}"),
                   "is_section": name in SECTION_ANCHORS}
                  for name, key in NAVIGATION]
    return {
        "t": texts,
        "amenity_groups": AMENITY_GROUPS[lang],
        "amenities": [{"label": label, "icon": icon}
                      for label, icon in zip(texts["apt_amenities"], AMENITY_ICONS, strict=True)],
        "sleeping_places": [{"label": label, "icon": icon}
                            for label, icon in zip(texts["apt_sleeping"],
                                                   ("double-bed", "single-bed", "sofa-bed"), strict=True)],
        "navigation": navigation,
        "page_navigation": [{**item, "label": texts["sidebar_pages"][item["name"]]}
                            for item in navigation if not item["is_section"]],
        "sidebar_sections": [{**item, "label": texts["sidebar_sections"][item["name"]]}
                             for item in navigation if item["is_section"]],
        "section_navigation": [item for item in navigation if item["is_section"]],
        "guide_navigation": [{**item, "label": texts["sidebar_pages"][item["name"]]}
                             for item in navigation if item["name"] in GUIDE_PAGES],
        "lang": "en" if lang.startswith("en") else "de",
        "site_settings": config,
        "preview_mode": getattr(settings, "SITE_PREVIEW", False),
        "seo": page_metadata(request, lang, config),
        "owner_content": {field: config.localized(field, lang) for field in (
            "host_intro", "amenities_detail", "bike_service", "arrival_notes",
            "payment_methods", "deposit", "balance", "security_deposit",
        )},
    }
