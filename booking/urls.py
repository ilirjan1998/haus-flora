from django.urls import path

from . import views

app_name = "booking"

urlpatterns = [
    path("", views.home, name="home"),
    path("wohnung/", views.apartment, name="apartment"),
    path("galerie/", views.gallery, name="gallery"),
    path("preise/", views.prices, name="prices"),
    path("umgebung/", views.area, name="area"),
    path("regeln/", views.rules, name="rules"),
    path("anfrage/", views.inquiry, name="inquiry"),
    path("anfrage/danke/", views.thanks, name="thanks"),
    path("impressum/", views.imprint, name="imprint"),
    path("datenschutz/", views.privacy, name="privacy"),
    path("api/verfuegbarkeit/", views.availability, name="availability"),
]
