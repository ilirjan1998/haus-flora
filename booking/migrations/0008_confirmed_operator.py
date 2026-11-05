from django.db import migrations, models

NAME = "Flore Markaj"
ADDRESS = "Jägerweg 20\n9551 Bodensdorf\nÖsterreich"


def fill_confirmed_operator(apps, schema_editor):
    settings = apps.get_model("booking", "SiteSettings")
    records = settings.objects.using(schema_editor.connection.alias)
    records.filter(operator_name="").update(operator_name=NAME)
    records.filter(operator_address="").update(operator_address=ADDRESS)


class Migration(migrations.Migration):
    dependencies = [("booking", "0007_confirmed_property_address")]
    operations = [
        migrations.AlterField(
            model_name="sitesettings", name="operator_name",
            field=models.CharField("Vollständiger Betreibername", max_length=200, blank=True, default=NAME),
        ),
        migrations.AlterField(
            model_name="sitesettings", name="operator_address",
            field=models.TextField("Betreiberanschrift", blank=True, default=ADDRESS),
        ),
        migrations.RunPython(fill_confirmed_operator, migrations.RunPython.noop),
    ]
