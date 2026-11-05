import json
from pathlib import Path

from django import template
from booking.image_assets import photo_attributes

register = template.Library()
PHOTO_CREDITS = json.loads((Path(__file__).resolve().parents[1] / "data" / "area_photo_credits.json").read_text())


@register.simple_tag
def responsive_photo(photo):
    return photo_attributes(photo)


@register.simple_tag
def photo_credit(photo):
    return PHOTO_CREDITS.get(photo.image.name, {})


@register.simple_tag
def gallery_credits(photos):
    return [PHOTO_CREDITS[photo.image.name] for photo in photos
            if photo.image.name in PHOTO_CREDITS]
