from decimal import Decimal

from django.db import migrations, models


def update_tax_rate(apps, schema_editor):
    settings = apps.get_model("booking", "SiteSettings")
    settings.objects.using(schema_editor.connection.alias).all().update(city_tax=Decimal("4.50"))


class Migration(migrations.Migration):
    dependencies = [("booking", "0003_guestreview_photo_category_and_more")]

    operations = [
        migrations.AddField(
            model_name="inquiry", name="taxable_children",
            field=models.PositiveSmallIntegerField(default=0, verbose_name="Davon 16–17 Jahre"),
        ),
        migrations.AlterField(
            model_name="sitesettings", name="city_tax",
            field=models.DecimalField(decimal_places=2, default=Decimal("4.50"), max_digits=5,
                                      verbose_name="Nächtigungstaxe pro Person ab 16 (€/Nacht)"),
        ),
        migrations.RunPython(update_tax_rate, migrations.RunPython.noop),
    ]
