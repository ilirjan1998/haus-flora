import json
import time
from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone, translation

from .emails import send_inquiry_mails
from .forms import InquiryForm
from .ical_sync import sync_booking_calendar_safely
from .models import BlockedPeriod, Photo, SiteSettings
from .pricing import price_table_for_js, total_price


def _lang():
    lang = translation.get_language() or "de"
    return "en" if lang.startswith("en") else "de"


def home(request):
    photos = Photo.objects.filter(is_active=True)
    return render(request, "booking/home.html", {
        "hero_photo": photos.first(),
        "teaser_photos": photos[1:7],
    })


def apartment(request):
    return render(request, "booking/apartment.html")


def gallery(request):
    return render(request, "booking/gallery.html", {
        "photos": Photo.objects.filter(is_active=True),
    })


def prices(request):
    return render(request, "booking/prices.html")


def area(request):
    return render(request, "booking/area.html")


def rules(request):
    return render(request, "booking/rules.html")


def imprint(request):
    return render(request, "booking/imprint.html")


def privacy(request):
    return render(request, "booking/privacy.html")


def thanks(request):
    return render(request, "booking/thanks.html")


def inquiry(request):
    """Kalender + Anfrageformular mit automatischer Preisberechnung."""
    site_settings = SiteSettings.load()
    lang = _lang()

    if request.method == "POST" and site_settings.booking_enabled:
        form = InquiryForm(request.POST, site_settings=site_settings, lang=lang)
        if form.is_valid():
            d = form.cleaned_data
            nights = (d["departure"] - d["arrival"]).days
            quoted = total_price(site_settings, d["adults"], d["children"], nights)
            inq = form_to_inquiry(d, quoted, lang)
            send_inquiry_mails(inq, site_settings)
            return redirect("booking:thanks")
    else:
        form = InquiryForm(site_settings=site_settings, lang=lang)

    return render(request, "booking/inquiry.html", {
        "form": form,
        "form_ts": f"{time.time():.0f}",
        "price_table_json": json.dumps(price_table_for_js(site_settings)),
        "min_nights": site_settings.min_nights,
    })


def form_to_inquiry(d, quoted, lang):
    from .models import Inquiry
    return Inquiry.objects.create(
        arrival=d["arrival"],
        departure=d["departure"],
        adults=d["adults"],
        children=d["children"],
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
