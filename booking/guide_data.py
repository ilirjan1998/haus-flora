"""Original guest-guide copy; official links checked on 2026-10-18."""

# Verified English destinations; translated slugs must not be guessed.
EN_URLS = {'https://www.visitvillach.at/de/kostenfreie-seezugaenge.html': 'https://www.visitvillach.at/en/free-of-charge-lake-access-points.html',
 'https://www.gerlitzen.com/de': 'https://www.gerlitzen.com/en',
 'https://www.visitvillach.at/de/das-bleistaetter-moor.html': 'https://www.visitvillach.at/en/bleistaetter-moor.html',
 'https://www.kaernten.at/motorrad/sehenswertes/kaernten-vom-wasser-aus/ossiacher-see-schifffahrt/': 'https://www.visitvillach.at/en/ossiacher-see-boat-trip.html',
 'https://adlerarena.com/': 'https://adlerarena.com/en/',
 'https://www.affenberg.com/': 'https://www.affenberg.com/en/',
 'https://www.familywald.at/': 'https://www.familywald.at/english/',
 'https://www.visitvillach.at/': 'https://www.visitvillach.at/en/',
 'https://www.kaerntentherme.com/': 'https://www.kaerntentherme.com/en/',
 'https://www.visitvillach.at/de/tours/ossiacher-see-radweg-r2-und-r2a.html?reloaded=true': 'https://www.visitvillach.at/en/tours/lake-ossiacher-see-cycle-path-r2-r2a.html',
 'https://www.visitvillach.at/de/drauradweg.html': 'https://www.visitvillach.at/en/drau-cycle-path.html',
 'https://www.visitvillach.at/de/alpe-adria-radweg.html': 'https://www.visitvillach.at/en/alpe-adria-cycle-path.html',
 'https://www.visitvillach.at/de/alles-rund-ums-rad.html': 'https://www.visitvillach.at/en/all-about-cycling.html',
 'https://www.visitvillach.at/de/erlebnis-card.html': 'https://www.visitvillach.at/en/erlebnis-card.html',
 'https://www.kaerntencard.at/': 'https://www.kaerntencard.at/sommer/en/',
 'https://fahrplan.oebb.at/': 'https://fahrplan.oebb.at/bin/query.exe/en'}

def item(title, en_title, text, en_text, url, tag, en_tag,
         *, image="", image_alt="", en_image_alt=""):
    return {"de": {"title": title, "text": text, "url": url, "tag": tag,
                   "image": image, "image_alt": image_alt},
            "en": {"title": en_title, "text": en_text, "url": EN_URLS.get(url, url), "tag": en_tag,
                   "image": image, "image_alt": en_image_alt}}


EXCURSIONS = [
    item("Ossiacher See", "Lake Ossiach", "Ein Badetag, ein Spaziergang am Ufer oder eine Pause mit Seeblick: Rund um den See findet ihr Strandbäder und öffentliche Seezugänge.", "Swim, walk along the shore or take a break with a lake view. Explore the lidos and public access points around the lake.", "https://www.visitvillach.at/de/kostenfreie-seezugaenge.html", "See & Sommer", "Lake & summer", image='images/excursions/ossiacher-see.webp', image_alt='Blick über den Ossiacher See auf Ossiach und die grünen Hügel.', en_image_alt='View across Lake Ossiach towards Ossiach and the green hills.'),
    item("Gerlitzen Alpe", "Gerlitzen Alpe", "Wanderwege und Hütten mit Aussicht. Die Kanzelbahn startet in Annenheim. Im Winter findet ihr hier das Skigebiet; prüft den aktuellen Liftbetrieb vor eurem Ausflug.", "Walking trails, mountain huts and wide views. The Kanzelbahn starts in Annenheim. In winter, explore the ski area; check lift operations before setting off.", "https://www.gerlitzen.com/de", "Berge & Winter", "Mountains & winter", image='images/excursions/gerlitzen.webp', image_alt='Zwei Wanderer genießen die Aussicht von der Gerlitzen Alpe.', en_image_alt='Two walkers enjoying the view from Gerlitzen Alpe.'),
    item("Bleistätter Moor", "Bleistätter Moor", "Am Ostufer des Sees laden Wege und Beobachtungsplätze zu einer ruhigen Naturpause ein. Ideal, wenn ihr die Umgebung zu Fuß entdecken möchtet.", "At the eastern end of the lake, walking paths and observation points invite you to slow down and discover the natural surroundings on foot.", "https://www.visitvillach.at/de/das-bleistaetter-moor.html", "Natur & Spaziergänge", "Nature & walks", image='images/excursions/bleistaetter-moor.webp', image_alt='Schilf, Wasser und Berge am Bleistätter Moor.', en_image_alt='Reeds, water and mountains at Bleistätter Moor.'),
    item("Schifffahrt am Ossiacher See", "Lake Ossiach boat trips", "Die Landschaft vom Wasser aus sehen und einen Ausflug am See planen. Fahrplan, Anlegestellen und Saisonzeiten vorab beim Anbieter prüfen.", "See the landscape from the water and plan a day around the lake. Check the operator’s current timetable, landing stages and seasonal service.", "https://www.kaernten.at/motorrad/sehenswertes/kaernten-vom-wasser-aus/ossiacher-see-schifffahrt/", "See & Ausflüge", "Lake & days out", image='images/excursions/schifffahrt.webp', image_alt='Das Ausflugsschiff Ossiach auf dem Ossiacher See.', en_image_alt='The passenger boat Ossiach on Lake Ossiach.'),
    item("Adlerarena Burg Landskron", "Landskron Eagle Arena", "Greifvögel bei einer Flugschau erleben und den Besuch mit einem Ausflug zur Burg verbinden. Vorführungszeiten und Tickets findet ihr direkt beim Anbieter.", "Watch birds of prey in flight and combine your visit with a trip to Landskron Castle. See the operator’s website for show times and tickets.", "https://adlerarena.com/", "Familie & Tiere", "Family & wildlife", image='images/excursions/adlerarena.webp', image_alt='Ein Weißkopfseeadler mit ausgebreiteten Flügeln in der Adlerarena.', en_image_alt='A bald eagle spreading its wings at the Eagle Arena.'),
    item("Abenteuer Affenberg", "Monkey Mountain", "Ein gemeinsamer Familienausflug zu den Japanmakaken bei Landskron. Informiert euch vorab über Führungen, Besuchszeiten und die Regeln vor Ort.", "A family outing to see Japanese macaques near Landskron. Check tours, visiting hours and visitor rules before your trip.", "https://www.affenberg.com/", "Familie & Tiere", "Family & wildlife", image='images/excursions/affenberg.webp', image_alt='Ein Japanmakake klettert auf einem Ast am Affenberg.', en_image_alt='A Japanese macaque climbing on a branch at Monkey Mountain.'),
    item("Familywald Ossiacher See", "Familywald Lake Ossiach", "Ein Naturfreizeitpark für einen aktiven Tag mit der Familie. Welche Attraktionen zum Alter eurer Kinder passen, erfahrt ihr auf der offiziellen Website.", "A nature adventure park for an active family day. The official website explains the attractions and which are suitable for your children’s ages.", "https://www.familywald.at/", "Familie & Abenteuer", "Family & adventure", image='images/excursions/familywald.webp', image_alt='Eine Besucherin gleitet zwischen den Bäumen im Familywald.', en_image_alt='A visitor gliding between the trees at Familywald.'),
    item("Villach & Kultur", "Villach & culture", "Durch die Altstadt bummeln, einen Cafébesuch einplanen oder das regionale Kulturangebot entdecken. Der Tourismusverband hilft mit aktuellen Tipps weiter.", "Stroll through the old town, stop at a café or discover local culture. The regional tourism website provides current ideas for your visit.", "https://www.visitvillach.at/", "Stadt & Kultur", "Town & culture", image='images/excursions/villach.webp', image_alt='Die beleuchtete Altstadt von Villach an der Drau am Abend.', en_image_alt='Villach’s illuminated old town beside the River Drau in the evening.'),
    item("KärntenTherme", "KärntenTherme", "Eine Idee für kühlere Tage: Baden und Entspannen in Warmbad-Villach. Öffnungszeiten, verfügbare Bereiche und Eintrittspreise direkt nachsehen.", "An option for cooler days: swimming and relaxation in Warmbad-Villach. Check opening hours, available facilities and admission prices directly.", "https://www.kaerntentherme.com/", "Auch bei Regen", "Rainy-day idea", image='images/excursions/kaerntentherme.webp', image_alt='Türkisblaues Außenbecken vor der modernen KärntenTherme.', en_image_alt='Turquoise outdoor pool beside the modern KärntenTherme.'),
]

CYCLING = [
    item("Ossiacher See – R2 / R2A", "Lake Ossiach – R2 / R2A", "Rund um den See durch die Uferorte. Die offizielle Rundtour ist etwa 28 km lang und als mittel eingestuft. Plant Bade- und Fotopausen nach Lust und Kondition ein.", "A circuit through the lakeside villages. The official round trip is about 28 km and rated moderate. Allow time for swimming and photo stops to suit your fitness.", "https://www.visitvillach.at/de/tours/ossiacher-see-radweg-r2-und-r2a.html?reloaded=true", "Rundtour · ca. 28 km", "Circuit · about 28 km"),
    item("Drauradweg ab Villach", "Drau Cycle Path from Villach", "Wählt eine passende Etappe entlang der Drau. Länge und Rückfahrt könnt ihr an eure Tagesplanung anpassen; bei Zugrückfahrt Fahrradmitnahme vorher prüfen.", "Choose a section along the River Drau to suit your day. Plan the distance and return journey in advance, including bicycle transport if returning by train.", "https://www.visitvillach.at/de/drauradweg.html", "Etappe frei wählen", "Choose your stage"),
    item("Alpe-Adria-Radweg", "Alpe-Adria Cycle Route", "Für einen längeren Radausflug bietet sich eine Etappe ab Villach an. Streckenverlauf, Höhenprofil und Rückfahrt findet ihr beim Tourismusverband.", "For a longer cycling day, choose a stage starting in Villach. Find route details, elevation profiles and return options on the tourism website.", "https://www.visitvillach.at/de/alpe-adria-radweg.html", "Für einen Tagesausflug", "A full-day option"),
    item("Touren, Verleih & E-Bikes", "Routes, rentals & e-bikes", "Das regionale Radportal bündelt Tourenvorschläge und Informationen zum Radverleih. Reserviert passende Räder frühzeitig direkt beim jeweiligen Verleih.", "The regional cycling portal brings together route ideas and bicycle rental information. Reserve suitable bikes with the rental provider in advance.", "https://www.visitvillach.at/de/alles-rund-ums-rad.html", "Planung & Service", "Planning & service"),
]

LINKS = [
    item("Region Villach", "Villach region", "Ausflüge, Veranstaltungen und aktuelle Urlaubstipps.", "Days out, events and current holiday inspiration.", "https://www.visitvillach.at/", "Urlaubsplanung", "Holiday planning"),
    item("Erlebnis CARD", "Erlebnis CARD", "Bei eurem Aufenthalt im Haus Flora bekommt ihr die Erlebnis CARD kostenlos dazu. Entdeckt damit zahlreiche Freizeitangebote in der Region Villach – Faaker See – Ossiacher See und macht noch mehr aus eurem Urlaub.", "Your stay at Haus Flora includes the Erlebnis CARD free of charge. Discover a wide range of activities in the Villach – Faaker See – Ossiacher See region and make even more of your holiday.", "https://www.visitvillach.at/de/erlebnis-card.html", "Gästekarte", "Guest card"),
    item("Kärnten Card", "Kärnten Card", "Eine eigene Ausflugskarte mit separaten Konditionen. Sie ist nicht mit der Erlebnis CARD gleichzusetzen.", "A separate sightseeing card with its own conditions. It is different from the Erlebnis CARD.", "https://www.kaerntencard.at/", "Ausflugskarte", "Sightseeing card"),
    item("ÖBB Fahrplan", "ÖBB journey planner", "Zugverbindungen nach Bodensdorf suchen und die passende Weiterfahrt zur Unterkunft planen.", "Search rail connections to Bodensdorf and plan your onward journey to the accommodation.", "https://fahrplan.oebb.at/", "Bahn", "Rail"),
    item("Kärntner Linien", "Kärntner Linien", "Bus- und Bahnverbindungen für Ausflüge und die Anreise in Kärnten.", "Regional bus and rail information for arrival and days out in Carinthia. Website in German.", "https://www.kaerntner-linien.at/", "Bus & Bahn", "Bus & rail"),
    item("Gerlitzen: Wetter & Webcams", "Gerlitzen: weather & webcams", "Bergwetter, Webcams und Betriebsinformationen direkt auf der Bergbahn-Website prüfen.", "Check mountain weather, webcams and operating information on the cable-car website.", "https://www.gerlitzen.com/de", "Bergplanung", "Mountain planning"),
    item("Flughafen Klagenfurt", "Klagenfurt Airport", "Aktuelle Flugverbindungen und Hinweise zur An- und Weiterreise.", "Current flights and information for arrival and onward travel.", "https://www.klagenfurt-airport.at/en/home", "Flugzeug", "Air travel"),
    item("Radportal der Region", "Regional cycling portal", "Tourenideen, Radverleih und weitere Informationen für eure Radtage.", "Route ideas, bicycle rental and information for your cycling days.", "https://www.visitvillach.at/de/alles-rund-ums-rad.html", "Radfahren", "Cycling"),
]


# Compact illustrations for planning and cycling cards, shared across languages.
for entries, visuals in ((CYCLING, ("area", "arrival", "cycling", "cycling")),
                         (LINKS, ("area", "guest-card", "sightseeing-card", "train", "bus", "area", "plane", "cycling"))):
    for entry, visual in zip(entries, visuals, strict=True):
        for language in ("de", "en"):
            entry[language]["illustration"] = visual



# Official provider marks and the host-provided guest-card pictures.
for entry, filename in zip(LINKS, (
    "villach.svg", "erlebnis-card-landscape.png", "kaernten-card.svg", "oebb.svg",
    "linien.svg", "gerlitzen.svg", "airport.svg", "villach.svg"
), strict=True):
    for language in ("de", "en"):
        entry[language]["brand_image"] = "images/brands/" + filename
        entry[language]["brand_dark"] = filename == "linien.svg"


def localized(items, lang):
    return [entry["en" if lang == "en" else "de"] for entry in items]

# A specific action label for the included guest card.
LINKS[1]["de"]["button_label"] = "Erlebnis CARD entdecken"
LINKS[1]["en"]["button_label"] = "Discover the Erlebnis CARD"
