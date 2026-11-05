"""Page metadata and search discovery from one shared, bilingual source.

Indexing is opt-in. The static preview always forces it off; a live Django
installation needs both SEO_INDEXABLE=True and a configured HTTPS SITE_URL.
"""
import json
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.urls import reverse
from django.utils import translation

from .models import Photo
from .navigation import SECTION_ANCHORS


# name: (German title, German description, English title, English description)
PAGE_META = {
    "home": (
        "Ferienwohnung Bodensdorf am Ossiacher See | Haus Flora",
        "Ferienwohnung Haus Flora in Bodensdorf am Ossiacher See: 74 m² für bis zu 4 Personen, Balkon und Gartenpool. Fotos und Preise ansehen, Urlaub anfragen.",
        "Haus Flora | Holiday apartment in Bodensdorf, Lake Ossiach",
        "Discover Haus Flora in Bodensdorf by Lake Ossiach: a 74 m² holiday apartment for up to 4 guests, with a balcony, kitchen and garden pool.",
    ),
    "apartment": (
        "Ferienwohnung mit Balkon & Pool in Bodensdorf | Haus Flora",
        "Entdeckt die 74 m² große Ferienwohnung im Haus Flora: Platz für bis zu 4 Personen, Küche, Wohnbereich, Balkon und Gartenpool in Bodensdorf.",
        "Apartment with balcony & garden pool in Bodensdorf | Haus Flora",
        "Explore the 74 m² Haus Flora holiday apartment in Bodensdorf: space for up to 4 guests, a kitchen, living area, balcony and garden pool.",
    ),
    "gallery": (
        "Fotos der Ferienwohnung, Garten & Pool | Haus Flora",
        "Schaut euch Haus Flora in Bodensdorf an: echte Fotos der Ferienwohnung, vom Balkon, Garten und Pool sowie vom Ossiacher See in der Umgebung.",
        "Apartment, garden & pool photos | Haus Flora Bodensdorf",
        "Take a look around Haus Flora in Bodensdorf: real photos of the apartment, balcony, garden and pool, plus Lake Ossiach in the surrounding area.",
    ),
    "prices": (
        "Preise & Zahlungsinformationen | Haus Flora Bodensdorf",
        "Preise der Ferienwohnung Haus Flora in Bodensdorf: Übernachtung, Endreinigung, Nächtigungstaxe, Mindestaufenthalt und Informationen zur Zahlung.",
        "Apartment prices & payment information | Haus Flora",
        "Plan your stay at Haus Flora in Bodensdorf: nightly prices, final cleaning, local tourist tax, minimum stay and information about payment.",
    ),
    "area": (
        "Ausflüge am Ossiacher See & rund um Villach | Haus Flora",
        "Ausflüge ab Bodensdorf: Ossiacher See, Gerlitzen, Bleistätter Moor, Affenberg und mehr. Mit Fotos und offiziellen Links für eure Urlaubsplanung.",
        "Days out around Lake Ossiach & Villach | Haus Flora",
        "Discover days out from Bodensdorf: Lake Ossiach, Gerlitzen, Bleistätter Moor, Monkey Mountain and more, with photos and official planning links.",
    ),
    "cycling": (
        "Radfahren am Ossiacher See ab Bodensdorf | Haus Flora",
        "Plant eure Radtour ab Bodensdorf: Ossiacher-See-Radweg, Drauradweg und Alpe-Adria-Radweg. Dazu offizielle Informationen zu Touren und Radverleih.",
        "Cycling around Lake Ossiach from Bodensdorf | Haus Flora",
        "Plan a cycling day from Bodensdorf: Lake Ossiach, the Drau Cycle Path and the Alpe-Adria route, with official route and bicycle rental links.",
    ),
    "arrival": (
        "Anreise nach Bodensdorf am Ossiacher See | Haus Flora",
        "So plant ihr eure Anreise zu Haus Flora in Bodensdorf am Ossiacher See: Informationen zu Auto, Bahn, Flug und zur Ankunft in der Ferienwohnung.",
        "Getting to Bodensdorf by Lake Ossiach | Haus Flora",
        "Plan your journey to Haus Flora in Bodensdorf by Lake Ossiach. Find information about travelling by car, train or plane and your arrival.",
    ),
    "holiday_links": (
        "Nützliche Urlaubslinks für Kärnten & Villach | Haus Flora",
        "Praktische Links für euren Urlaub im Haus Flora: Region Villach, Gästekarten, Fahrpläne, Radportal und Wetter auf der Gerlitzen im Überblick.",
        "Useful holiday links for Carinthia & Villach | Haus Flora",
        "Useful links for your Haus Flora holiday: Villach tourism, guest cards, train and bus timetables, cycling information and Gerlitzen weather.",
    ),
    "guest_info": (
        "Fragen zum Aufenthalt in der Ferienwohnung | Haus Flora",
        "Antworten für euren Aufenthalt im Haus Flora in Bodensdorf: Anreise, Abreise, Gästezahl, Mindestaufenthalt, Bezahlung und weitere praktische Infos.",
        "Questions about your holiday apartment stay | Haus Flora",
        "Find answers about staying at Haus Flora in Bodensdorf: arrival, departure, guest numbers, minimum stay, payment and other useful information.",
    ),
    "hosts": (
        "Familie Markaj – eure Gastgeber in Bodensdorf | Haus Flora",
        "Lernt eure Gastgeber im Haus Flora kennen. Familie Markaj begrüßt euch in Bodensdorf und hilft bei Fragen zur Ferienwohnung und eurem Aufenthalt.",
        "Meet the Markaj family, your hosts in Bodensdorf | Haus Flora",
        "Meet your hosts at Haus Flora. The Markaj family welcomes you to Bodensdorf and can help with questions about the holiday apartment and your stay.",
    ),
    "rules": (
        "Hausregeln, Pool & Stornobedingungen | Haus Flora",
        "Gut vorbereitet ins Haus Flora: Lest die Haus- und Poolregeln sowie die Stornobedingungen für euren Aufenthalt in der Ferienwohnung in Bodensdorf.",
        "House rules, pool rules & cancellation | Haus Flora",
        "Get ready for your stay at Haus Flora in Bodensdorf. Read the house rules, pool rules and cancellation conditions before planning your holiday.",
    ),
    "inquiry": (
        "Ferienwohnung in Bodensdorf anfragen | Haus Flora",
        "Plant euren Aufenthalt im Haus Flora am Ossiacher See. Wählt eure Reisedaten und Gästezahl und richtet eure Anfrage direkt an Familie Markaj.",
        "Ask about a holiday apartment in Bodensdorf | Haus Flora",
        "Plan your Haus Flora stay by Lake Ossiach. Choose your travel dates and number of guests, then send your inquiry directly to the Markaj family.",
    ),
    "thanks": (
        "Eure Anfrage | Haus Flora Bodensdorf",
        "Informationen zum nächsten Schritt nach eurer Anfrage an Haus Flora in Bodensdorf am Ossiacher See.",
        "Your inquiry | Haus Flora Bodensdorf",
        "Information about the next step after your inquiry to Haus Flora in Bodensdorf by Lake Ossiach.",
    ),
    "imprint": (
        "Impressum & Kontakt | Haus Flora Bodensdorf",
        "Angaben zum Betreiber und Kontaktinformationen zur Website der Ferienwohnung Haus Flora in Bodensdorf am Ossiacher See.",
        "Legal notice & contact | Haus Flora Bodensdorf",
        "Operator details and contact information for the Haus Flora holiday apartment website in Bodensdorf by Lake Ossiach.",
    ),
    "privacy": (
        "Datenschutz | Haus Flora Bodensdorf",
        "Informationen zur Verarbeitung personenbezogener Daten auf der Website und bei Anfragen an Haus Flora in Bodensdorf.",
        "Privacy information | Haus Flora Bodensdorf",
        "Information about the processing of personal data on the website and when making an inquiry to Haus Flora in Bodensdorf.",
    ),
}

EXCLUDED_PAGES = {"thanks", "imprint", "privacy"}
PAGE_META["gallery_area"] = (
    "Ossiacher See & Umgebung in Bildern | Haus Flora",
    "Echte Fotos rund um den Ossiacher See: Bodensdorf, Bleistätter Moor, Burg Landskron, Segelboote und Abendstimmung am See.",
    "Lake Ossiach & surroundings in photos | Haus Flora",
    "Explore Lake Ossiach in photos: Bodensdorf, Bleistätter Moor, Landskron Castle, sailing boats and evening light by the lake.",
)
SITEMAP_PAGES = ("home", "area", "gallery_area", "cycling", "holiday_links")


def site_origin():
    value = getattr(settings, "SITE_URL", "").strip().rstrip("/")
    if not value:
        if getattr(settings, "SEO_INDEXABLE", False):
            raise ImproperlyConfigured("Indexing requires an explicit HTTPS SITE_URL.")
        return ""
    url = urlsplit(value)
    if (url.scheme != "https" or not url.hostname or url.path or url.query
            or url.fragment or url.username or url.password):
        raise ImproperlyConfigured("SITE_URL must be an HTTPS origin, without a path, credentials, query or fragment.")
    return value


def indexing_enabled():
    return bool(getattr(settings, "SEO_INDEXABLE", False) and site_origin())


def page_url(name, lang):
    with translation.override(lang):
        return site_origin() + reverse(f"booking:{name}")


def _json_for_html(value):
    # JSON inside an executable-type script element must not close that element.
    return (json.dumps(value, ensure_ascii=False, separators=(",", ":"))
            .replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e"))


def page_metadata(request, lang, config):
    match = request.resolver_match
    name = match.url_name if match else "home"
    if name in SECTION_ANCHORS:
        name = "home"
    if name not in PAGE_META:
        return {"robots": "noindex, follow"}
    values = PAGE_META[name]
    title, description = values[2:4] if lang == "en" else values[0:2]
    enabled = indexing_enabled()
    seo = {
        "title": title, "description": description,
        "robots": "index, follow, max-image-preview:large" if enabled and name not in EXCLUDED_PAGES else "noindex, follow",
        "locale": "en_GB" if lang == "en" else "de_AT",
        "alternate_locale": "de_AT" if lang == "en" else "en_GB",
        "verification": getattr(settings, "GOOGLE_SITE_VERIFICATION", ""),
    }
    origin = site_origin()
    if not origin:
        return seo
    canonical = page_url(name, lang)
    home = page_url("home", lang)
    # Query strings (gallery filters, tracking parameters) share the main page.
    seo.update({
        "canonical": canonical,
        "alternates": [{"lang": code, "url": page_url(name, code)} for code in ("de", "en")],
        "default_url": page_url(name, "de"),
    })
    # Regional scenery belongs in the gallery, not in the accommodation's image list.
    photos = list(Photo.objects.filter(is_active=True).exclude(category="area"))
    house_photo = next((p for p in photos if p.image.name.endswith("/haus-flora.webp")), None)
    primary = house_photo or (photos[0] if photos else None)
    if name == "gallery_area":
        primary = Photo.objects.filter(is_active=True, category="area").first() or primary
    if primary:
        seo["image"] = {
            "url": origin + primary.image.url,
            "alt": primary.title_en if lang == "en" and primary.title_en else primary.title_de,
            "width": primary.image.width, "height": primary.image.height,
        }
    website_id, property_id = origin + "/#website", origin + "/#haus-flora"
    graph = [{
        "@type": "WebSite", "@id": website_id,
        "url": origin + "/", "name": "Haus Flora",
        "inLanguage": ["de", "en"],
    }, {
        "@type": "WebPage", "@id": canonical + "#webpage",
        "url": canonical, "name": title, "description": description,
        "inLanguage": lang, "isPartOf": {"@id": website_id},
    }]
    if primary:
        graph[-1]["primaryImageOfPage"] = {"@type": "ImageObject", **seo["image"]}
        graph[-1]["primaryImageOfPage"].pop("alt")
        graph[-1]["primaryImageOfPage"]["caption"] = seo["image"]["alt"]
    if name not in {"home", "thanks"}:
        breadcrumb_id = canonical + "#breadcrumb"
        graph[-1]["breadcrumb"] = {"@id": breadcrumb_id}
        graph.append({
            "@type": "BreadcrumbList", "@id": breadcrumb_id,
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home" if lang == "en" else "Startseite", "item": home},
                {"@type": "ListItem", "position": 2, "name": title.split(" | ")[0], "item": canonical},
            ],
        })
    if name in {"home", "apartment", "hosts", "arrival"}:
        property_data = {
            "@type": "LodgingBusiness", "@id": property_id,
            "name": "Haus Flora", "url": home,
            "description": PAGE_META["home"][3 if lang == "en" else 1],
            "address": config.property_address or {
                "@type": "PostalAddress", "addressLocality": "Bodensdorf",
                "addressRegion": "Kärnten", "addressCountry": "AT",
            },
        }
        if config.public_email:
            property_data["email"] = config.public_email
        if config.public_phone:
            property_data["telephone"] = config.public_phone
        if photos:
            property_data["image"] = [origin + p.image.url for p in photos]
        if name in {"home", "apartment"}:
            property_data["containsPlace"] = {
                "@type": "Apartment", "name": "Haus Flora Ferienwohnung",
                "floorSize": {"@type": "QuantitativeValue", "value": 74, "unitCode": "MTK"},
                "occupancy": {"@type": "QuantitativeValue", "maxValue": 4},
            }
        graph[1]["about"] = {"@id": property_id}
        graph.append(property_data)
    seo["json_ld"] = _json_for_html({"@context": "https://schema.org", "@graph": graph})
    return seo


def robots_content():
    # Let crawlers read noindex. Authentication keeps the private Site private.
    lines = ["User-agent: *", "Allow: /", "Disallow: /admin/", "Disallow: /de/api/", "Disallow: /en/api/"]
    if indexing_enabled():
        lines.extend(["", "Sitemap: " + site_origin() + "/sitemap.xml"])
    return "\n".join(lines) + "\n"


def sitemap_content():
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    image_ns = "http://www.google.com/schemas/sitemap-image/1.1"
    ET.register_namespace("", namespace)
    ET.register_namespace("image", image_ns)
    root = ET.Element("{" + namespace + "}urlset")
    if indexing_enabled():
        photos = list(Photo.objects.filter(is_active=True))
        image_urls = {
            "home": [site_origin() + p.image.url for p in photos if p.category != "area"],
            "gallery_area": [site_origin() + p.image.url for p in photos if p.category == "area"],
        }
        for lang in ("de", "en"):
            for name in SITEMAP_PAGES:
                entry = ET.SubElement(root, "{" + namespace + "}url")
                ET.SubElement(entry, "{" + namespace + "}loc").text = page_url(name, lang)
                for image_url in image_urls.get(name, []):
                    image_entry = ET.SubElement(entry, "{" + image_ns + "}image")
                    ET.SubElement(image_entry, "{" + image_ns + "}loc").text = image_url
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def robots(request):
    return HttpResponse(robots_content(), content_type="text/plain; charset=utf-8")


def sitemap(request):
    response = HttpResponse(sitemap_content(), content_type="application/xml; charset=utf-8")
    if not indexing_enabled():
        response["X-Robots-Tag"] = "noindex"
    return response
