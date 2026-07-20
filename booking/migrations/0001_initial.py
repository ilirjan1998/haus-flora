from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BlockedPeriod",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start_date", models.DateField(verbose_name="Anreise (erster belegter Tag)")),
                ("end_date", models.DateField(verbose_name="Abreise (an diesem Tag wieder frei)")),
                ("note", models.CharField(blank=True, help_text="Nur für euch sichtbar, z. B. Name des Gastes.", max_length=200, verbose_name="Notiz")),
            ],
            options={
                "verbose_name": "Belegter Zeitraum",
                "verbose_name_plural": "Belegte Zeiträume",
                "ordering": ["start_date"],
            },
        ),
        migrations.CreateModel(
            name="Inquiry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("arrival", models.DateField(verbose_name="Anreise")),
                ("departure", models.DateField(verbose_name="Abreise")),
                ("adults", models.PositiveSmallIntegerField(verbose_name="Erwachsene")),
                ("children", models.PositiveSmallIntegerField(default=0, verbose_name="Kinder")),
                ("name", models.CharField(max_length=120, verbose_name="Name")),
                ("email", models.EmailField(max_length=254, verbose_name="E-Mail")),
                ("message", models.TextField(blank=True, verbose_name="Nachricht")),
                ("quoted_total", models.DecimalField(blank=True, decimal_places=2, help_text="Gesamtschätzung inklusive Endreinigung und Ortstaxe.", max_digits=8, null=True, verbose_name="Angezeigter Gesamtpreis (€)")),
                ("language", models.CharField(default="de", max_length=5, verbose_name="Sprache des Gastes")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Eingegangen am")),
            ],
            options={
                "verbose_name": "Anfrage",
                "verbose_name_plural": "Anfragen",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Photo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="galerie/", verbose_name="Bild")),
                ("title_de", models.CharField(blank=True, max_length=120, verbose_name="Titel (Deutsch)")),
                ("title_en", models.CharField(blank=True, max_length=120, verbose_name="Titel (Englisch)")),
                ("order", models.PositiveIntegerField(default=0, help_text="Kleinere Zahl = weiter vorne in der Galerie.", verbose_name="Reihenfolge")),
                ("is_active", models.BooleanField(default=True, verbose_name="Sichtbar")),
            ],
            options={
                "verbose_name": "Foto",
                "verbose_name_plural": "Fotos",
                "ordering": ["order", "id"],
            },
        ),
        migrations.CreateModel(
            name="SiteSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("booking_enabled", models.BooleanField(default=True, help_text="Ausschalten, um das Anfrageformular vorübergehend zu deaktivieren.", verbose_name="Anfragen aktiviert")),
                ("calendar_visible", models.BooleanField(default=True, help_text="Ausschalten, um den Belegungskalender komplett auszublenden.", verbose_name="Kalender sichtbar")),
                ("price_2_adults", models.DecimalField(decimal_places=2, default=150, max_digits=6, verbose_name="2 Erwachsene (€/Nacht)")),
                ("price_3_adults", models.DecimalField(decimal_places=2, default=175, max_digits=6, verbose_name="3 Erwachsene (€/Nacht)")),
                ("price_2a_1c", models.DecimalField(decimal_places=2, default=165, max_digits=6, verbose_name="2 Erwachsene + 1 Kind (€/Nacht)")),
                ("price_2a_2c", models.DecimalField(decimal_places=2, default=180, max_digits=6, verbose_name="2 Erwachsene + 2 Kinder (€/Nacht)")),
                ("single_adult_discount", models.DecimalField(decimal_places=1, default=5, help_text="Abschlag auf den Preis für 2 Erwachsene.", max_digits=4, verbose_name="Rabatt für 1 Erwachsenen (%)")),
                ("cleaning_fee", models.DecimalField(decimal_places=2, default=60, max_digits=6, verbose_name="Endreinigung (€)")),
                ("city_tax", models.DecimalField(decimal_places=2, default=2.7, max_digits=5, verbose_name="Ortstaxe pro Person ab 18 (€/Nacht)")),
                ("min_nights", models.PositiveSmallIntegerField(default=5, verbose_name="Mindestaufenthalt (Nächte)")),
                ("house_rules_de", models.TextField(default="Check-in ab 14:00 Uhr, Check-out bis 10:00 Uhr.\nKeine Haustiere.\nRauchen ist in der Wohnung nicht gestattet.\nNachtruhe von 22:00 bis 07:00 Uhr.", verbose_name="Hausregeln (Deutsch)")),
                ("house_rules_en", models.TextField(default="Check-in from 2:00 pm, check-out until 10:00 am.\nNo pets.\nSmoking is not allowed inside the apartment.\nQuiet hours from 10:00 pm to 7:00 am.", verbose_name="Hausregeln (Englisch)")),
                ("pool_rules_de", models.TextField(default="Poolbenutzung auf eigene Gefahr.\nKinder nur in Begleitung eines Erwachsenen.\nBitte vor dem Baden duschen.\nKeine Glasflaschen im Poolbereich.", verbose_name="Poolregeln (Deutsch)")),
                ("pool_rules_en", models.TextField(default="Use of the pool is at your own risk.\nChildren only when accompanied by an adult.\nPlease shower before swimming.\nNo glass bottles in the pool area.", verbose_name="Poolregeln (Englisch)")),
                ("cancellation_de", models.TextField(default="Bis 42 Tage vor Anreise: kostenlose Stornierung.\nAb 42 Tage vor Anreise: 25 % des Gesamtpreises.", verbose_name="Stornobedingungen (Deutsch)")),
                ("cancellation_en", models.TextField(default="Up to 42 days before arrival: free cancellation.\nLess than 42 days before arrival: 25% of the total price.", verbose_name="Stornobedingungen (Englisch)")),
            ],
            options={
                "verbose_name": "Einstellungen",
                "verbose_name_plural": "Einstellungen",
            },
        ),
    ]
