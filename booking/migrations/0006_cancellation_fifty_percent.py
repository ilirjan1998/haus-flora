from django.db import migrations, models


OLD_DE = "Bis 42 Tage vor Anreise: kostenlose Stornierung.\nAb 42 Tage vor Anreise: 25 % des Gesamtpreises."
OLD_EN = "Up to 42 days before arrival: free cancellation.\nLess than 42 days before arrival: 25% of the total price."
NEW_DE = OLD_DE.replace("25 %", "50 %")
NEW_EN = OLD_EN.replace("25%", "50%")


def update_cancellation(apps, schema_editor):
    settings = apps.get_model("booking", "SiteSettings").objects.using(schema_editor.connection.alias)
    settings.filter(cancellation_de=OLD_DE).update(cancellation_de=NEW_DE)
    settings.filter(cancellation_en=OLD_EN).update(cancellation_en=NEW_EN)


class Migration(migrations.Migration):
    dependencies = [("booking", "0005_cleaning_fee_eighty")]

    operations = [
        migrations.AlterField(
            model_name="sitesettings", name="cancellation_de",
            field=models.TextField(default=NEW_DE, verbose_name="Stornobedingungen (Deutsch)"),
        ),
        migrations.AlterField(
            model_name="sitesettings", name="cancellation_en",
            field=models.TextField(default=NEW_EN, verbose_name="Stornobedingungen (Englisch)"),
        ),
        migrations.RunPython(update_cancellation, migrations.RunPython.noop),
    ]
