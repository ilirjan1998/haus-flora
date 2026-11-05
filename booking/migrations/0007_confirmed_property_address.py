from django.db import migrations, models


ADDRESS = "Jägerweg 20, 9551 Bodensdorf"


def fill_property_address(apps, schema_editor):
    settings = apps.get_model("booking", "SiteSettings")
    settings.objects.using(schema_editor.connection.alias).filter(property_address="").update(property_address=ADDRESS)


class Migration(migrations.Migration):
    dependencies = [("booking", "0006_cancellation_fifty_percent")]

    operations = [
        migrations.AlterField(
            model_name="sitesettings", name="property_address",
            field=models.CharField(
                blank=True, default=ADDRESS, max_length=250,
                verbose_name="Adresse der Unterkunft",
                help_text="Straße, Hausnummer, PLZ und Ort. Wird für die Anreise angezeigt.",
            ),
        ),
        migrations.RunPython(fill_property_address, migrations.RunPython.noop),
    ]
