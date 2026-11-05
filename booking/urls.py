from django.urls import path

from . import views

app_name = "booking"

urlpatterns = [
    path("", views.home, name="home"),
    path("wohnung/", views.apartment, name="apartment"),
    path("galerie/", views.gallery, name="gallery"),
    path("galerie/area/", views.gallery_area, name="gallery_area"),
    path("preise/", views.prices, name="prices"),
    path("umgebung/", views.area, name="area"),
    path("radfahren/", views.cycling, name="cycling"),
    path("anreise/", views.arrival, name="arrival"),
    path("urlaubslinks/", views.holiday_links, name="holiday_links"),
    path("gut-zu-wissen/", views.guest_info, name="guest_info"),
    path("gastgeber/", views.hosts, name="hosts"),
    path("regeln/", views.rules, name="rules"),
    path("anfrage/", views.inquiry, name="inquiry"),
    path("anfrage/danke/", views.thanks, name="thanks"),
    path("impressum/", views.imprint, name="imprint"),
    path("datenschutz/", views.privacy, name="privacy"),
    path("api/verfuegbarkeit/", views.availability, name="availability"),
]
