import json
import time
from datetime import timedelta

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone, translation

from .emails import send_inquiry_mails
from .forms import InquiryForm
from .ical_sync import sync_booking_calendar_safely
from .models import BlockedPeriod, Photo, SiteSettings, GuestReview
from .guide_data import EXCURSIONS, CYCLING, LINKS, localized
from .pricing import price_table_for_js, total_price
from .navigation import SECTION_ANCHORS
from .review_data import review_context


def _lang():
    lang = translation.get_language() or "de"
    return "en" if lang.startswith("en") else "de"


def _gallery_preview_ids(photos, preferred=(), limit=5):
    """Choose a small overview while keeping the full album in its existing order."""
    selected = [photo.pk for photo in photos if photo.image.name.rsplit("/", 1)[-1] in preferred][:limit]
    for photo in photos:
        if len(selected) >= limit:
            break
        if photo.pk not in selected:
            selected.append(photo.pk)
    return [photo.pk for photo in photos if photo.pk in selected]


def home(request):
    inquiry_context = _inquiry_state(request)
    if not isinstance(inquiry_context, dict):
        return inquiry_context
    photos = list(Photo.objects.filter(is_active=True))
    apartment_photos = [photo for photo in photos if photo.category == "apartment"]
    outdoor_photos = [photo for photo in photos if photo.category == "outdoor"]
    property_photos = apartment_photos + outdoor_photos
    property_preview_ids = _gallery_preview_ids(property_photos,
        ("schlafzimmer.webp", "wohnzimmer.webp", "balkon.webp", "haus-flora.webp", "garten-pool-ausblick.webp"))

    def choose_photo(filename, category):
        return (next((photo for photo in photos if photo.image.name.endswith('/' + filename)), None)
                or next((photo for photo in photos if photo.category == category), None)
                or (photos[0] if photos else None))

    return render(request, "booking/home.html", {
        **inquiry_context,
        **review_context(_lang()),
        "hero_photo": choose_photo('haus-flora.webp', 'outdoor'),
        "lake_photo": choose_photo('seeufer.webp', 'area'),
        "apartment_photos": apartment_photos,
        "outdoor_photos": outdoor_photos,
        "property_photos": property_photos,
        "property_preview_ids": property_preview_ids,
        "property_remaining_count": len(property_photos) - len(property_preview_ids),
        "reviews": GuestReview.objects.filter(is_published=True, permission_confirmed=True),
    })


def apartment(request):
    return _section_redirect("apartment")


def gallery(request):
    category = request.GET.get("category", "")
    if category == "area":
        return redirect("booking:gallery_area", permanent=True)
    anchor = {"apartment": "wohnungsfotos", "outdoor": "garten"}.get(category, "fotos")
    return redirect(reverse("booking:home") + "#" + anchor, permanent=True)


def gallery_area(request):
    return render(request, "booking/gallery.html", {
        "photos": Photo.objects.filter(is_active=True, category="area"),
        "active_category": "area",
    })


def prices(request):
    return _section_redirect("prices")


def area(request):
    return render(request, "booking/area.html", {"cards": localized(EXCURSIONS, _lang())})


def cycling(request):
    return render(request, "booking/cycling.html", {"cards": localized(CYCLING, _lang())})


def arrival(request):
    return _section_redirect("arrival")


def holiday_links(request):
    return render(request, "booking/holiday_links.html", {"cards": localized(LINKS, _lang())})


def guest_info(request):
    return _section_redirect("guest_info")


def hosts(request):
    return _section_redirect("hosts")


def rules(request):
    return _section_redirect("rules")


def _section_redirect(name):
    return redirect(reverse("booking:home") + "#" + SECTION_ANCHORS[name], permanent=True)


def imprint(request):
    return render(request, "booking/imprint.html")


def privacy(request):
    return render(request, "booking/privacy.html")


def thanks(request):
    return render(request, "booking/thanks.html")


def inquiry(request):
    if request.method == "POST":
        return home(request)  # Existing form endpoints keep server-side validation.
    return _section_redirect("inquiry")


def _inquiry_state(request):
    """Kalender + Anfrageformular mit automatischer Preisberechnung."""
    site_settings = SiteSettings.load()
    lang = _lang()

    if request.method == "POST" and site_settings.booking_enabled and not getattr(settings, "SITE_PREVIEW", False):
        form = InquiryForm(request.POST, site_settings=site_settings, lang=lang)
        if form.is_valid():
            d = form.cleaned_data
            nights = (d["departure"] - d["arrival"]).days
            quoted = total_price(site_settings, d["adults"], d["children"], nights, d["taxable_children"])
            inq = form_to_inquiry(d, quoted, lang)
            send_inquiry_mails(inq, site_settings)
            return redirect("booking:thanks")
    else:
        form = InquiryForm(site_settings=site_settings, lang=lang)

    return {
        "form": form,
        "form_ts": f"{time.time():.0f}",
        "price_table_json": json.dumps(price_table_for_js(site_settings)),
        "min_nights": site_settings.min_nights,
    }


def form_to_inquiry(d, quoted, lang):
    from .models import Inquiry
    return Inquiry.objects.create(
        arrival=d["arrival"],
        departure=d["departure"],
        adults=d["adults"],
        children=d["children"],
        taxable_children=d["taxable_children"],
        name=d["name"],
        email=d["email"],
        message=d.get("message", ""),
        quoted_total=quoted,
        language=lang,
    )


def availability(request):
    """Liefert alle belegten NÄCHTE der nächsten 18 Monate als JSON.
    Ein Zeitraum start..end belegt die Nächte start bis end-1, der
    Abreisetag selbst ist also wieder als Anreisetag wählbar."""
    sync_booking_calendar_safely()
    today = timezone.localdate()
    horizon = today + timedelta(days=560)  # ~18 Monate
    blocked = set()
    for period in BlockedPeriod.objects.filter(end_date__gt=today, start_date__lte=horizon):
        current = period.start_date
        while current < period.end_date and current <= horizon:
            if current >= today:
                blocked.add(current.isoformat())
            current += timedelta(days=1)
    return JsonResponse({"blocked": sorted(blocked)})
