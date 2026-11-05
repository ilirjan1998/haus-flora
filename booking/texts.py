"""
Alle festen Website-Texte in Deutsch und Englisch.

Im Template erreichbar über {{ t.schluessel }} – die richtige Sprache
wird automatisch anhand der URL (/de/... oder /en/...) gewählt.
Texte, die ihr selbst ändern wollt (Regeln, Storno), liegen dagegen
in der Datenbank und sind im Admin bearbeitbar.
"""

TEXTS = {
    "de": {
        # Navigation & Allgemeines
        "site_name": "Haus Flora",
        "tagline": "Ferienwohnung am Ossiacher See",
        "nav_home": "Start",
        "nav_apartment": "Die Wohnung",
        "nav_gallery": "Galerie",
        "nav_prices": "Preise",
        "nav_area": "Lage & Umgebung",
        "nav_rules": "Haus & Pool",
        "nav_inquiry": "Kalender & Anfrage",
        "footer_imprint": "Impressum",
        "footer_privacy": "Datenschutz",
        "lang_switch": "English",

        # Startseite
        "home_meta": (
            "Haus Flora in Bodensdorf: 74 m² Ferienwohnung für bis zu vier "
            "Personen mit Pool, Klimaanlage und Nähe zum Ossiacher See."
        ),
        "home_eyebrow": "Bodensdorf · Ossiacher See · Kärnten",
        "home_title": "Willkommen im Haus Flora",
        "home_intro": (
            "Unsere Ferienwohnung liegt in Bodensdorf, nur wenige Gehminuten "
            "vom Ossiacher See entfernt. Auf 74 m² finden bis zu 4 Personen "
            "Platz – mit Pool, Klimaanlage und allem, was ein entspannter "
            "Urlaub in Kärnten braucht."
        ),
        "home_cta": "Verfügbarkeit prüfen",
        "home_secondary_cta": "Wohnung entdecken",
        "home_from": "ab",
        "home_facts_size": "74 m² Wohnfläche",
        "home_facts_guests": "Bis zu 4 Personen",
        "home_facts_pool": "Pool im Garten",
        "home_facts_lake": "Nahe am Ossiacher See",
        "home_fact_size_label": "Wohnfläche",
        "home_fact_guests_label": "Gäste maximal",
        "home_fact_nights_label": "Nächte mindestens",
        "home_fact_checkin_label": "Check-in ab",
        "home_apartment_eyebrow": "Ankommen und wohlfühlen",
        "home_apartment_title": "Alles für entspannte Tage am See",
        "home_apartment_text": (
            "Ein großzügiges Zuhause auf Zeit: Die 74 m² große Wohnung verbindet "
            "ruhiges Wohnen mit kurzen Wegen zum Ossiacher See und zur Gerlitzen Alpe."
        ),
        "home_apartment_link": "Die Wohnung ansehen",
        "home_features": [
            {"title": "Pool im Garten", "text": "Erfrischung direkt am Haus – ideal für warme Urlaubstage."},
            {"title": "Komfort für vier", "text": "Kingsize-Bett, Einzelbett und großes Schlafsofa bieten flexibel Platz."},
            {"title": "Komplett ausgestattet", "text": "Küche, Klimaanlage, WLAN, Waschmaschine und Parkplatz inklusive."},
            {"title": "Erlebnis CARD", "text": "Viele regionale Leistungen und Ausflugsziele kostenlos oder ermäßigt."},
        ],
        "home_gallery_eyebrow": "Einblicke",
        "home_gallery_title": "So wohnt ihr im Haus Flora",
        "home_gallery_link": "Alle Fotos ansehen",
        "home_price_eyebrow": "Transparent geplant",
        "home_price_title": "Einfache Preise ohne Überraschungen",
        "home_price_text": (
            "Wählt die Personenzahl und Reisedaten – der Kalender berechnet sofort "
            "einen übersichtlichen Gesamtpreis."
        ),
        "home_price_link": "Alle Preise und Bedingungen",
        "home_location_eyebrow": "Zwischen See und Berg",
        "home_location_title": "Bodensdorf als perfekter Ausgangspunkt",
        "home_location_text": (
            "Baden, Wandern, Skifahren oder ein Ausflug nach Villach: Rund um das "
            "Haus Flora beginnt der Urlaub direkt vor der Tür."
        ),
        "home_location_facts": [
            "Ossiacher See in wenigen Minuten erreichbar",
            "Gerlitzen Alpe für Sommer und Winter",
            "Villach etwa 15 Autominuten entfernt",
        ],
        "home_location_link": "Lage und Umgebung entdecken",
        "home_cta_eyebrow": "Urlaub am Ossiacher See",
        "home_cta_title": "Sind eure Wunschtage noch frei?",
        "home_cta_text": "Prüft den Kalender und sendet uns unverbindlich eure Anfrage.",

        # Wohnung
        "apt_title": "Die Wohnung",
        "apt_intro": (
            "Die Wohnung bietet 74 m² Platz für maximal 4 Personen – hell, "
            "klimatisiert und komplett ausgestattet."
        ),
        "apt_sleeping_title": "Schlafplätze",
        "apt_sleeping": ["1 Kingsize-Bett", "1 Einzelbett", "1 großes Schlafsofa"],
        "apt_amenities_title": "Ausstattung",
        "apt_amenities": [
            "WLAN (kostenlos)",
            "Klimaanlage",
            "Voll ausgestattete Küche",
            "Badezimmer mit Dusche",
            "Fernseher mit IPTV und Netflix",
            "Pool",
            "Parkplatz am Haus",
            "Terrasse mit Sitzgelegenheit",
            "Waschmaschine",
            "Bettwäsche und Handtücher inklusive",
        ],
        "apt_card_title": "Erlebnis CARD inklusive",
        "apt_card_text": (
            "Als unsere Gäste erhaltet ihr die Erlebnis CARD mit vielen "
            "regionalen Angeboten laut aktuellem Programm. "
            "Bitte prüft Leistungen und Anmeldung für euren Reisezeitraum."
        ),

        # Galerie
        "gallery_title": "Galerie",
        "gallery_empty": "Die Fotos werden gerade vorbereitet – schaut bald wieder vorbei!",
        "gallery_lightbox_label": "Große Fotoansicht",
        "gallery_close": "Fotoansicht schließen",
        "gallery_previous": "Vorheriges Foto",
        "gallery_next": "Nächstes Foto",

        # Preise
        "prices_title": "Preise",
        "prices_per_night": "pro Nacht",
        "prices_2a": "2 Erwachsene",
        "prices_3a": "3 Erwachsene",
        "prices_2a1c": "2 Erwachsene + 1 Kind",
        "prices_2a2c": "2 Erwachsene + 2 Kinder",
        "prices_1a": "1 Erwachsener",
        "prices_1a_note": "Rabatt auf den Preis für 2 Erwachsene",
        "prices_cleaning": "Endreinigung (einmalig)",
        "prices_tax_title": "Nächtigungstaxe",
        "prices_tax_text": "pro Person ab 16 Jahren und Nacht – wird vor Ort verrechnet. Kinder unter 16 Jahren zahlen keine Nächtigungstaxe.",
        "prices_min_stay": "Mindestaufenthalt",
        "prices_checkin": "Check-in ab 14:00 Uhr · Check-out bis 10:00 Uhr",
        "prices_cancel_title": "Stornobedingungen",

        # Regeln
        "rules_title": "Haus- & Poolregeln",
        "rules_house": "Hausregeln",
        "rules_pool": "Poolregeln",

        # Umgebung
        "area_title": "Lage & Umgebung",
        "area_intro": (
            "Das Haus Flora liegt in Bodensdorf am Nordufer des Ossiacher Sees, "
            "einem der wärmsten Badeseen Kärntens. Strandbad, Geschäfte und "
            "Restaurants sind in wenigen Minuten erreichbar."
        ),
        "area_tips_title": "Ausflugsziele in der Nähe",
        "area_tips": [
            "Ossiacher See – Baden, Radfahren, Schifffahrt",
            "Gerlitzen Alpe – Wandern im Sommer, Skifahren im Winter (Kanzelbahn ab Annenheim)",
            "Stift Ossiach – Kloster und Konzerte am Südufer",
            "Villach – Altstadt, Thermen und Einkaufsmöglichkeiten (ca. 15 Minuten)",
            "Burg Landskron – Adlerflugschau und Affenberg",
            "Wörthersee und Klagenfurt – ca. 30 Minuten mit dem Auto",
        ],
        "area_map_text": "Bodensdorf und die Umgebung auf OpenStreetMap ansehen.",
        "area_map_link": "Karte in neuem Fenster öffnen",

        # Anfrage & Kalender
        "inquiry_title": "Kalender & Anfrage",
        "inquiry_intro": (
            "Wählt eure Reisedaten im Kalender – belegte Tage sind markiert. "
            "Nach dem Absenden melden wir uns so schnell wie möglich per E-Mail."
        ),
        "calendar_hint": "Der Abreisetag eines Gastes kann der Anreisetag des nächsten sein.",
        "calendar_legend_free": "frei",
        "calendar_legend_booked": "belegt",
        "calendar_hidden": "Der Belegungskalender ist derzeit nicht verfügbar. Schickt uns gerne eine Anfrage – wir melden uns rasch.",
        "booking_disabled": (
            "Anfragen sind im Moment leider nicht möglich. "
            "Bitte versucht es später noch einmal."
        ),
        "form_arrival": "Anreise",
        "form_departure": "Abreise",
        "form_adults": "Erwachsene (ab 18 Jahren)",
        "form_children": "Kinder & Jugendliche (0–17 Jahre)",
        "form_taxable_children": "Wie viele davon sind 16 oder 17 Jahre alt?",
        "form_tax_age_hint": "Für die Nächtigungstaxe zählen alle Personen ab 16 Jahren. Bitte gebt das Alter bei der Anreise an.",
        "form_name": "Name",
        "form_email": "E-Mail",
        "form_message": "Nachricht (optional)",
        "form_submit": "Anfrage senden",
        "form_price_label": "Preisübersicht",
        "form_accommodation": "Nächtigung",
        "form_cleaning": "Endreinigung",
        "form_city_tax": "Nächtigungstaxe (ab 16 Jahren, vor Ort)",
        "form_estimated_total": "Voraussichtlicher Gesamtpreis",
        "form_price_hint": "Die Nächtigungstaxe gilt ab 16 Jahren, ist in der Gesamtschätzung enthalten und wird vor Ort bezahlt.",
        "form_nights": "Nächte",
        "thanks_title": "Danke für eure Anfrage!",
        "thanks_text": (
            "Wir haben eure Anfrage gespeichert und melden uns so schnell wie "
            "möglich persönlich per E-Mail."
        ),
        "thanks_back": "Zurück zur Startseite",
    },
    "en": {
        "site_name": "Haus Flora",
        "tagline": "Holiday apartment at Lake Ossiach",
        "nav_home": "Home",
        "nav_apartment": "The apartment",
        "nav_gallery": "Gallery",
        "nav_prices": "Prices",
        "nav_area": "Location & area",
        "nav_rules": "House & pool",
        "nav_inquiry": "Calendar & inquiry",
        "footer_imprint": "Legal notice",
        "footer_privacy": "Privacy policy",
        "lang_switch": "Deutsch",

        "home_meta": (
            "Haus Flora in Bodensdorf: a 74 m² holiday apartment for up to four "
            "guests with a pool, air conditioning and Lake Ossiach nearby."
        ),
        "home_eyebrow": "Bodensdorf · Lake Ossiach · Carinthia",
        "home_title": "Welcome to Haus Flora",
        "home_intro": (
            "Our holiday apartment is located in Bodensdorf, just a few "
            "minutes' walk from Lake Ossiach. With 74 m² for up to 4 guests, "
            "a pool and air conditioning, it has everything you need for a "
            "relaxing holiday in Carinthia, Austria."
        ),
        "home_cta": "Check availability",
        "home_secondary_cta": "Discover the apartment",
        "home_from": "from",
        "home_facts_size": "74 m² living space",
        "home_facts_guests": "Up to 4 guests",
        "home_facts_pool": "Pool in the garden",
        "home_facts_lake": "Close to Lake Ossiach",
        "home_fact_size_label": "living space",
        "home_fact_guests_label": "guests maximum",
        "home_fact_nights_label": "nights minimum",
        "home_fact_checkin_label": "check-in from",
        "home_apartment_eyebrow": "Arrive and unwind",
        "home_apartment_title": "Everything you need for relaxing days by the lake",
        "home_apartment_text": (
            "A spacious home away from home: the 74 m² apartment combines a quiet "
            "setting with easy access to Lake Ossiach and Gerlitzen Alpe."
        ),
        "home_apartment_link": "Explore the apartment",
        "home_features": [
            {"title": "Pool in the garden", "text": "Refreshment right by the house – perfect for warm summer days."},
            {"title": "Comfort for four", "text": "A king-size bed, single bed and large sofa bed offer flexible space."},
            {"title": "Fully equipped", "text": "Kitchen, air conditioning, Wi-Fi, washing machine and parking included."},
            {"title": "Erlebnis CARD", "text": "Many regional activities and attractions free of charge or discounted."},
        ],
        "home_gallery_eyebrow": "A first look",
        "home_gallery_title": "Your stay at Haus Flora",
        "home_gallery_link": "View all photos",
        "home_price_eyebrow": "Easy to plan",
        "home_price_title": "Clear prices without surprises",
        "home_price_text": (
            "Choose your group and travel dates – the calendar instantly shows "
            "a clear estimated total."
        ),
        "home_price_link": "All prices and conditions",
        "home_location_eyebrow": "Between lake and mountain",
        "home_location_title": "Bodensdorf is the perfect base",
        "home_location_text": (
            "Swimming, hiking, skiing or a trip to Villach: your holiday starts "
            "right outside Haus Flora."
        ),
        "home_location_facts": [
            "Lake Ossiach just a few minutes away",
            "Gerlitzen Alpe for summer and winter",
            "Villach around 15 minutes by car",
        ],
        "home_location_link": "Discover the location and area",
        "home_cta_eyebrow": "A holiday at Lake Ossiach",
        "home_cta_title": "Are your preferred dates still available?",
        "home_cta_text": "Check the calendar and send us your no-obligation inquiry.",

        "apt_title": "The apartment",
        "apt_intro": (
            "The apartment offers 74 m² for up to 4 guests – bright, "
            "air-conditioned and fully equipped."
        ),
        "apt_sleeping_title": "Sleeping arrangements",
        "apt_sleeping": ["1 king-size bed", "1 single bed", "1 large sofa bed"],
        "apt_amenities_title": "Amenities",
        "apt_amenities": [
            "Free Wi-Fi",
            "Air conditioning",
            "Fully equipped kitchen",
            "Bathroom with shower",
            "TV with IPTV and Netflix",
            "Pool",
            "Free parking on site",
            "Terrace with seating",
            "Washing machine",
            "Bed linen and towels included",
        ],
        "apt_card_title": "Erlebnis CARD included",
        "apt_card_text": (
            "As our guests you receive the Erlebnis CARD with regional activities "
            "according to the current programme. Check the benefits and "
            "registration requirements for your travel dates."
        ),

        "gallery_title": "Gallery",
        "gallery_empty": "Photos are being prepared – please check back soon!",
        "gallery_lightbox_label": "Large photo view",
        "gallery_close": "Close photo view",
        "gallery_previous": "Previous photo",
        "gallery_next": "Next photo",

        "prices_title": "Prices",
        "prices_per_night": "per night",
        "prices_2a": "2 adults",
        "prices_3a": "3 adults",
        "prices_2a1c": "2 adults + 1 child",
        "prices_2a2c": "2 adults + 2 children",
        "prices_1a": "1 adult",
        "prices_1a_note": "discount on the price for 2 adults",
        "prices_cleaning": "Final cleaning (one-time)",
        "prices_tax_title": "Local tourist tax",
        "prices_tax_text": "per person aged 16 or over per night – payable on site. Children under 16 do not pay local tourist tax.",
        "prices_min_stay": "Minimum stay",
        "prices_checkin": "Check-in from 2:00 pm · Check-out until 10:00 am",
        "prices_cancel_title": "Cancellation policy",

        "rules_title": "House & pool rules",
        "rules_house": "House rules",
        "rules_pool": "Pool rules",

        "area_title": "Location & area",
        "area_intro": (
            "Haus Flora is located in Bodensdorf on the northern shore of "
            "Lake Ossiach, one of the warmest lakes in Carinthia. The lido, "
            "shops and restaurants are just a few minutes away."
        ),
        "area_tips_title": "Things to do nearby",
        "area_tips": [
            "Lake Ossiach – swimming, cycling, boat trips",
            "Gerlitzen Alpe – hiking in summer, skiing in winter (cable car from Annenheim)",
            "Ossiach Abbey – monastery and concerts on the southern shore",
            "Villach – old town, thermal spas and shopping (approx. 15 minutes)",
            "Landskron Castle – falconry shows and Monkey Mountain",
            "Lake Wörthersee and Klagenfurt – approx. 30 minutes by car",
        ],
        "area_map_text": "View Bodensdorf and the surrounding area on OpenStreetMap.",
        "area_map_link": "Open map in a new window",

        "inquiry_title": "Calendar & inquiry",
        "inquiry_intro": (
            "Pick your travel dates in the calendar – occupied days are "
            "marked. After sending your inquiry we will get back to you by "
            "e-mail as soon as possible."
        ),
        "calendar_hint": "One guest's departure day can be the next guest's arrival day.",
        "calendar_legend_free": "available",
        "calendar_legend_booked": "occupied",
        "calendar_hidden": "The availability calendar is currently unavailable. Feel free to send us an inquiry – we will get back to you quickly.",
        "booking_disabled": (
            "Inquiries are currently not possible. Please try again later."
        ),
        "form_arrival": "Arrival",
        "form_departure": "Departure",
        "form_adults": "Adults (18 and over)",
        "form_children": "Children & teenagers (ages 0–17)",
        "form_taxable_children": "How many of them are aged 16 or 17?",
        "form_tax_age_hint": "Local tourist tax applies to all guests aged 16 or over. Please use their age on arrival.",
        "form_name": "Name",
        "form_email": "E-mail",
        "form_message": "Message (optional)",
        "form_submit": "Send booking request",
        "form_price_label": "Price summary",
        "form_accommodation": "Accommodation",
        "form_cleaning": "Final cleaning",
        "form_city_tax": "Local tax (ages 16+, payable on site)",
        "form_estimated_total": "Estimated total",
        "form_price_hint": "Local tax applies from age 16, is included in the estimate and is payable on site.",
        "form_nights": "nights",
        "thanks_title": "Thank you for your inquiry!",
        "thanks_text": (
            "We have saved your inquiry and will get back to you personally "
            "by e-mail as soon as possible."
        ),
        "thanks_back": "Back to the homepage",
    },
}


def get_texts(lang):
    from .guide_texts import GUIDE_TEXTS
    from .ux_texts import UX_TEXTS
    from .holiday_texts import HOLIDAY_TEXTS
    language = "en" if lang == "en" else "de"
    return {**TEXTS[language], **GUIDE_TEXTS[language], **UX_TEXTS[language], **HOLIDAY_TEXTS[language]}
