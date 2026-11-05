"""
Preisberechnung für Haus Flora.

Erlaubte Kombinationen (Erwachsene, Kinder):
    (1, 0)  -> Preis für 2 Erwachsene minus Rabatt (Standard: 5 %)
    (2, 0)  -> price_2_adults
    (3, 0)  -> price_3_adults
    (2, 1)  -> price_2a_1c
    (2, 2)  -> price_2a_2c

Alle anderen Kombinationen (z. B. 4 Erwachsene) sind nicht buchbar.
Die Preisaufschlüsselung enthält Nächtigung, einmalige Endreinigung und
Nächtigungstaxe für Erwachsene und Jugendliche ab 16 Jahren. Sie wird vor Ort bezahlt,
ist in der angezeigten Gesamtschätzung aber bereits berücksichtigt.
"""
from decimal import Decimal, ROUND_HALF_UP

ALLOWED_COMBOS = {(1, 0), (2, 0), (3, 0), (2, 1), (2, 2)}


def _decimal(value):
    """Normalisiert auch noch nicht neu aus der Datenbank geladene Defaults."""
    return value if isinstance(value, Decimal) else Decimal(str(value))


def combo_allowed(adults: int, children: int) -> bool:
    return (adults, children) in ALLOWED_COMBOS


def nightly_price(settings, adults: int, children: int):
    """Preis pro Nacht als Decimal – oder None, wenn nicht buchbar."""
    combo = (adults, children)
    if combo == (1, 0):
        factor = (Decimal("100") - _decimal(settings.single_adult_discount)) / Decimal("100")
        price = _decimal(settings.price_2_adults) * factor
    elif combo == (2, 0):
        price = _decimal(settings.price_2_adults)
    elif combo == (3, 0):
        price = _decimal(settings.price_3_adults)
    elif combo == (2, 1):
        price = _decimal(settings.price_2a_1c)
    elif combo == (2, 2):
        price = _decimal(settings.price_2a_2c)
    else:
        return None
    return price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def total_price(settings, adults: int, children: int, nights: int, taxable_children: int = 0):
    """Geschätzter Gesamtpreis inklusive Reinigung und Ortstaxe – oder None."""
    breakdown = price_breakdown(settings, adults, children, nights, taxable_children)
    return breakdown["total"] if breakdown else None


def price_breakdown(settings, adults: int, children: int, nights: int, taxable_children: int = 0):
    """Liefert die vollständige, centgenaue Preisaufschlüsselung."""
    per_night = nightly_price(settings, adults, children)
    if per_night is None or nights <= 0 or not 0 <= taxable_children <= children:
        return None
    accommodation = (per_night * nights).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    cleaning = _decimal(settings.cleaning_fee).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    city_tax = (_decimal(settings.city_tax) * (adults + taxable_children) * nights).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    return {
        "per_night": per_night,
        "accommodation": accommodation,
        "cleaning": cleaning,
        "city_tax": city_tax,
        "total": (accommodation + cleaning + city_tax).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        ),
    }


def price_table_for_js(settings):
    """Preistabelle als dict für das JavaScript im Anfrageformular.
    Schlüssel: "erwachsene_kinder", z. B. "2_1"."""
    table = {}
    for adults, children in ALLOWED_COMBOS:
        table[f"{adults}_{children}"] = str(nightly_price(settings, adults, children))
    return table
