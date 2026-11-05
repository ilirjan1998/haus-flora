"""
Adminbereich – erreichbar unter /admin/ nach dem Anlegen eines
Superusers (python manage.py createsuperuser).

Hier könnt ihr:
- Fotos hinzufügen, sortieren, ausblenden und löschen
- Preise, Regeln und Schalter (Anfragen an/aus, Kalender an/aus) ändern
- belegte Zeiträume eintragen
- eingegangene Anfragen ansehen
"""
from django.contrib import admin
from django.utils.html import format_html

from .models import BlockedPeriod, Inquiry, Photo, SiteSettings, GuestReview

admin.site.site_header = "Haus Flora – Verwaltung"
admin.site.site_title = "Haus Flora"
admin.site.index_title = "Website verwalten"


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("preview", "title_de", "category", "order", "is_active")
    list_filter = ("category", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("preview", "title_de")

    @admin.display(description="Vorschau")
    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:6px;">', obj.image.url
            )
        return "–"


@admin.register(BlockedPeriod)
class BlockedPeriodAdmin(admin.ModelAdmin):
    list_display = ("start_date", "end_date", "nights", "source", "note")
    list_filter = ("source",)
    readonly_fields = ("source", "external_uid")
    ordering = ("start_date",)

    @admin.display(description="Nächte")
    def nights(self, obj):
        return (obj.end_date - obj.start_date).days


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("created_at", "name", "email", "arrival", "departure",
                    "adults", "children", "taxable_children", "quoted_total")
    list_filter = ("arrival",)
    search_fields = ("name", "email")
    readonly_fields = [f.name for f in Inquiry._meta.fields]

    def has_add_permission(self, request):
        return False  # Anfragen entstehen nur über die Website


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Kontakt & Betreiber", {"fields": (
            "public_email", "public_phone", "property_address", "operator_name", "operator_address",
        ), "description": "Betreiberangaben vor Veröffentlichung vervollständigen. Unterkunft und Betreiberanschrift können abweichen."}),
        ("Gastgeber & Wohnung", {"fields": (
            "host_name", "host_photo", "host_intro_de", "host_intro_en", "floor_plan",
            "amenities_detail_de", "amenities_detail_en",
        )}),
        ("Anreise & Radservice", {"fields": (
            "arrival_notes_de", "arrival_notes_en", "bike_service_de", "bike_service_en",
        )}),
        ("Zahlungsinformationen", {"fields": (
            "payment_methods_de", "payment_methods_en", "deposit_de", "deposit_en",
            "balance_de", "balance_en", "security_deposit_de", "security_deposit_en",
        ), "description": "Eigene Bedingungen in beiden Sprachen eintragen. Leer = keine pauschale Zahlungszusage; der Gast wird auf die individuelle Klärung verwiesen."}),
        ("Schalter", {"fields": (
            "booking_enabled", "calendar_visible", "booking_calendar_enabled",
        )}),
        ("Booking.com-Synchronisation", {"fields": (
            "booking_last_sync_at", "booking_last_sync_error",
        )}),
        ("Preise", {"fields": (
            "price_2_adults", "price_3_adults", "price_2a_1c", "price_2a_2c",
            "single_adult_discount", "cleaning_fee", "city_tax", "min_nights",
        )}),
        ("Hausregeln", {"fields": ("house_rules_de", "house_rules_en")}),
        ("Poolregeln", {"fields": ("pool_rules_de", "pool_rules_en")}),
        ("Stornobedingungen", {"fields": ("cancellation_de", "cancellation_en")}),
    )

    def has_add_permission(self, request):
        # Es gibt genau einen Einstellungs-Datensatz
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    readonly_fields = ("booking_last_sync_at", "booking_last_sync_error")


@admin.register(GuestReview)
class GuestReviewAdmin(admin.ModelAdmin):
    list_display = ("display_name", "source_label", "permission_confirmed", "is_published", "order")
    list_filter = ("is_published", "permission_confirmed")
