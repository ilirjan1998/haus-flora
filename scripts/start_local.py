"""Prepare a local installation without replacing existing settings or photos."""
import os
from pathlib import Path
import secrets
import sys

ROOT = Path(__file__).resolve().parent.parent


def main():
    os.chdir(ROOT)
    sys.path.insert(0, str(ROOT))
    env_path = ROOT / ".env"
    if not env_path.exists():
        example = (ROOT / ".env.example").read_text(encoding="utf-8")
        example = example.replace(
            "SECRET_KEY=hier-einen-langen-zufaelligen-schluessel-eintragen",
            "SECRET_KEY=" + secrets.token_urlsafe(50),
        )
        with env_path.open("x", encoding="utf-8") as env_file:
            env_file.write(example)
        print(".env mit eigenem Secret Key angelegt.")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hausflora.settings")
    import django
    django.setup()
    from django.core.management import call_command
    from booking.models import Photo

    call_command("migrate", interactive=False)
    # Fixture has fixed IDs: never overwrite a gallery with existing records.
    if not Photo.objects.exists():
        call_command("loaddata", "property_photos")
    call_command("prepare_photo_variants")
    call_command("check")


if __name__ == "__main__":
    main()
