"""Dated public rating snapshot, selected summaries and short original excerpts.

These are curated entries, not GuestReview submissions or live ratings.
Source evidence and update instructions are in review-sources.md at repo root.
Keep the full Booking.com score separate from the selected 10/10 entries.
"""
from datetime import date


BOOKING_RATING = {
    "score_de": "9,3",
    "score_en": "9.3",
    "count": 16,
    "checked_on": date(2026, 10, 20),
}
REVIEW_EVIDENCE_URL = "https://de.planetofhotels.com/osterreich/bodensdorf/haus-flora-ferienwohnung-bodensdorf"

SELECTED_REVIEWS = (
    {
        "name": "Annette", "country_de": "Deutschland", "country_en": "Germany",
        "date": date(2026, 8, 2), "score": 10,
        "title_de": "Balkon und Gastfreundschaft", "title_en": "Balcony and hospitality",
        "summary_de": "Annette lobt die großzügige Wohnung, den Balkon mit Gartenblick und die aufmerksamen Gastgeber.",
        "summary_en": "Annette highlights the spacious apartment, garden views from the balcony and attentive hosts.",
    },
    {
        "name": "Gerold", "country_de": "Österreich", "country_en": "Austria",
        "date": date(2025, 2, 26), "score": 10,
        "title_de": "Herzlich willkommen", "title_en": "A warm welcome",
        "summary_de": "Gerold hebt den herzlichen Empfang, die Sauberkeit und den großen Balkon hervor.",
        "summary_en": "Gerold highlights the warm welcome, cleanliness and large balcony.",
    },
    {
        "name": "Ernst", "country_de": "Schweiz", "country_en": "Switzerland",
        "date": date(2024, 10, 24), "score": 10,
        "title_de": "Komfort und Aussicht", "title_en": "Comfort and views",
        "summary_de": "Ernst gefallen die Küchenausstattung, die bequemen Betten und die Aussicht beim Essen auf dem Balkon.",
        "summary_en": "Ernst praises the kitchen, comfortable beds and balcony views during meals.",
    },
    {
        "name": "Reinhard", "country_de": "Deutschland", "country_en": "Germany",
        "date": date(2024, 8, 9), "score": 10,
        "title_de": "Ruhe und Platz", "title_en": "Peace and space",
        "summary_de": "Reinhard schätzt die ruhige Lage, den Platz in der Wohnung und die hilfsbereiten Gastgeber.",
        "summary_en": "Reinhard appreciates the peaceful location, spacious rooms and helpful hosts.",
    },
)

# The visible source excerpts confirm the comments, but not scores or dates.
# Keep these voices separate so they never increase the 10/10 badge count.
ADDITIONAL_GUEST_VOICES = (
    {
        "name": "Nelly", "country_de": "Niederlande", "country_en": "Netherlands",
        "title_de": "Aussicht vom Balkon", "title_en": "Balcony views",
        "excerpt": "Het mooie, grote appartement met een fantastisch uitzicht vanaf het balkon.",
        "excerpt_de": "Die schöne, große Wohnung mit einer fantastischen Aussicht vom Balkon.",
        "excerpt_language": "nl",
        "language_de": "Niederländisch", "language_en": "Dutch",
    },
    {
        "name": "Ciurla", "country_de": "Italien", "country_en": "Italy",
        "title_de": "Aufmerksame Gastgeber", "title_en": "Attentive hosts",
        "excerpt": "La casa in ottima posizione, i proprietari molto attenti e ospitali..",
        "excerpt_de": "Das Haus in ausgezeichneter Lage, die Eigentümer sehr aufmerksam und gastfreundlich..",
        "excerpt_language": "it",
        "language_de": "Italienisch", "language_en": "Italian",
    },
)


def review_context(lang):
    language = "en" if lang == "en" else "de"
    suffix = "en-gb" if language == "en" else "de"
    return {
        "booking_rating": {
            **BOOKING_RATING,
            "score": BOOKING_RATING[f"score_{language}"],
            "label": "Superb" if language == "en" else "Hervorragend",
            "url": f"https://www.booking.com/hotel/at/haus-flora-ferienwohnung-bodensdorf.{suffix}.html#tab-reviews",
        },
        "selected_booking_reviews": [
            {
                **review,
                "country": review[f"country_{language}"],
                "title": review[f"title_{language}"],
                "summary": review[f"summary_{language}"],
            }
            for review in SELECTED_REVIEWS if review["score"] == 10
        ],
        "additional_guest_voices": [
            {
                **voice,
                "country": voice[f"country_{language}"],
                "title": voice[f"title_{language}"],
                "language_label": voice[f"language_{language}"],
                "excerpt": voice["excerpt_de"] if language == "de" else voice["excerpt"],
                "excerpt_language": "de" if language == "de" else voice["excerpt_language"],
            }
            for voice in ADDITIONAL_GUEST_VOICES
        ],
        "review_evidence_url": REVIEW_EVIDENCE_URL,
    }
