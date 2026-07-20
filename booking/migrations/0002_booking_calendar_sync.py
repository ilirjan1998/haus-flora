from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("booking", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="blockedperiod",
            name="source",
            field=models.CharField(
                choices=[("manual", "Manuell"), ("booking", "Booking.com")],
                db_index=True,
                default="manual",
                max_length=20,
                verbose_name="Quelle",
            ),
        ),
        migrations.AddField(
            model_name="blockedperiod",
            name="external_uid",
            field=models.CharField(
                blank=True,
                db_index=True,
                help_text="Wird bei importierten Kalenderterminen automatisch gesetzt.",
                max_length=255,
                verbose_name="Externe ID",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="booking_calendar_enabled",
            field=models.BooleanField(
                default=False,
                help_text="Aktivieren, nachdem BOOKING_ICAL_URL in der .env eingetragen wurde.",
                verbose_name="Booking.com-Kalender synchronisieren",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="booking_last_sync_at",
            field=models.DateTimeField(
                blank=True,
                editable=False,
                null=True,
                verbose_name="Booking.com zuletzt synchronisiert",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="booking_last_sync_error",
            field=models.TextField(
                blank=True,
                editable=False,
                verbose_name="Letzter Booking.com-Fehler",
            ),
        ),
    ]
