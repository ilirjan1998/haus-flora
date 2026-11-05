from decimal import Decimal

from django.db import migrations, models


def update_cleaning_fee(apps, schema_editor):
    settings = apps.get_model("booking", "SiteSettings")
    settings.objects.using(schema_editor.connection.alias).all().update(cleaning_fee=Decimal("80.00"))


class Migration(migrations.Migration):
    dependencies = [("booking", "0004_nightly_tax_from_sixteen")]

    operations = [
        migrations.AlterField(
            model_name="sitesettings", name="cleaning_fee",
            field=models.DecimalField(decimal_places=2, default=80, max_digits=6,
                                      verbose_name="Endreinigung (€)"),
        ),
        migrations.RunPython(update_cleaning_fee, migrations.RunPython.noop),
    ]
