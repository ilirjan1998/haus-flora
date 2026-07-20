"""
Django-Settings für die Ferienwohnungs-Website "Haus Flora".

Sensible Werte (Secret Key, E-Mail-Passwort) kommen aus der Datei ".env"
im Projektordner – siehe ".env.example" und README.md.
"""
from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("SECRET_KEY", "nur-fuer-entwicklung-unsicher")
DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "booking",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # wichtig für Deutsch/Englisch
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hausflora.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                # Eigener Context-Processor: stellt "t" (Texte) und
                # "site_settings" in allen Templates bereit.
                "booking.context_processors.site_texts",
            ],
        },
    },
]

WSGI_APPLICATION = "hausflora.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# Sprache & Zeitzone
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "de"
LANGUAGES = [
    ("de", "Deutsch"),
    ("en", "English"),
]
TIME_ZONE = "Europe/Vienna"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Statische Dateien & hochgeladene Fotos
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # für "collectstatic" beim Deployment

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# E-Mail-Versand über Gmail
# In der Entwicklung (DEBUG=True, kein Passwort gesetzt) werden Mails nur
# in der Konsole ausgegeben – so kann man ohne echtes Konto testen.
# ---------------------------------------------------------------------------
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
OWNER_EMAIL = os.environ.get("OWNER_EMAIL", "markajflore@gmail.com")

if EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER or "haus-flora@localhost"

# ---------------------------------------------------------------------------
# Booking.com-iCal-Synchronisation
# Der private Link bleibt ausschließlich in .env und wird nie im HTML gezeigt.
# ---------------------------------------------------------------------------
BOOKING_ICAL_URL = os.environ.get("BOOKING_ICAL_URL", "").strip()
BOOKING_ICAL_SYNC_MINUTES = int(os.environ.get("BOOKING_ICAL_SYNC_MINUTES", "30"))
