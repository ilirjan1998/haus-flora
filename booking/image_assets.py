"""Smaller local WebP variants; originals remain available in the gallery."""
from pathlib import Path
from django.conf import settings
from PIL import Image, ImageOps

WIDTHS = (320, 640, 960)


def variant_name(image_name, width):
    name = Path(image_name)
    return str(Path("responsive") / name.parent / f"{name.stem}-{width}.webp")


def prepare_variants(photos):
    count = 0
    for photo in photos:
        if not photo.image:
            continue
        source = Path(photo.image.path)
        if not source.is_file():
            continue
        with Image.open(source) as original:
            original = ImageOps.exif_transpose(original).convert("RGB")
            for width in WIDTHS:
                if width >= original.width:
                    continue
                destination = Path(settings.MEDIA_ROOT) / variant_name(photo.image.name, width)
                if destination.exists() and destination.stat().st_mtime >= source.stat().st_mtime:
                    continue
                destination.parent.mkdir(parents=True, exist_ok=True)
                variant = original.resize((width, round(original.height * width / original.width)), Image.Resampling.LANCZOS)
                variant.save(destination, "WEBP", quality=78, method=6)
                count += 1
    return count


def photo_attributes(photo):
    if not photo or not photo.image:
        return {}
    attributes = {"src": photo.image.url}
    source = Path(photo.image.path)
    try:
        with Image.open(source) as original:
            width, height = original.size
        attributes.update(width=width, height=height)
        sources = []
        for variant_width in WIDTHS:
            if variant_width >= width:
                continue
            name = variant_name(photo.image.name, variant_width)
            path = Path(settings.MEDIA_ROOT) / name
            if path.is_file() and path.stat().st_mtime >= source.stat().st_mtime:
                url = settings.MEDIA_URL + name
                sources.append(f"{url} {variant_width}w")
                if variant_width == 640:
                    attributes["src"] = url
        sources.append(f"{photo.image.url} {width}w")
        attributes["srcset"] = ", ".join(sources)
    except (OSError, ValueError):
        pass  # A missing uploaded file must not take the whole page down.
    return attributes
