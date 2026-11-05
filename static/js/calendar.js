/*
 * Belegungskalender + Live-Preisberechnung für Haus Flora.
 *
 * - zeigt immer 2 Monate nebeneinander
 * - blätterbar bis 18 Monate in die Zukunft
 * - belegte NÄCHTE sind markiert und nicht als Anreise wählbar;
 *   der Abreisetag eines Gastes ist als Anreisetag wieder frei
 * - Klick 1 = Anreise, Klick 2 = Abreise (Formularfelder werden befüllt)
 * - Preis wird sofort aus der eingebetteten Preistabelle berechnet
 */
(function () {
  "use strict";

  var form = document.getElementById("inquiry-form");
  var calRoot = document.getElementById("calendar");

  /* ---------- Hilfsfunktionen ---------- */

  function iso(d) {
    return d.getFullYear() + "-" +
      String(d.getMonth() + 1).padStart(2, "0") + "-" +
      String(d.getDate()).padStart(2, "0");
  }
  function fromIso(s) {
    var p = s.split("-");
    return new Date(+p[0], +p[1] - 1, +p[2]);
  }
  function addDays(d, n) {
    var c = new Date(d);
    c.setDate(c.getDate() + n);
    return c;
  }
  function startOfMonth(d) { return new Date(d.getFullYear(), d.getMonth(), 1); }
  function addMonths(d, n) { return new Date(d.getFullYear(), d.getMonth() + n, 1); }

  /* ---------- Preisberechnung im Formular ---------- */

  var STRINGS = {
    de: {
      months: ["Jänner", "Februar", "März", "April", "Mai", "Juni", "Juli",
               "August", "September", "Oktober", "November", "Dezember"],
      weekdays: ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"],
      combo: "Diese Personenkombination ist leider nicht buchbar (3 Erwachsene ohne Kinder oder bis zu 2 Erwachsene mit Kindern).",
      taxAge: "Bitte wählt aus, wie viele der Kinder 16 oder 17 Jahre alt sind.",
      minNights: "Mindestaufenthalt: {n} Nächte.",
      chooseArrival: "Wählt euren Anreisetag aus.",
      chooseDeparture: "Anreise: {date}. Wählt jetzt euren Abreisetag aus.",
      selectedDates: "Ausgewählt: {arrival} bis {departure}. Füllt jetzt eure Angaben unten aus.",
      arrivalAction: "Als Anreise auswählen", departureAction: "Als Abreise auswählen"
    },
    en: {
      months: ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"],
      weekdays: ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
      combo: "This combination of guests is not bookable (3 adults without children or up to 2 adults with children).",
      taxAge: "Please select how many of the children are aged 16 or 17.",
      minNights: "Minimum stay: {n} nights.",
      chooseArrival: "Choose your arrival date.",
      chooseDeparture: "Arrival: {date}. Now choose your departure date.",
      selectedDates: "Selected: {arrival} to {departure}. Now fill in your details below.",
      arrivalAction: "Choose as arrival", departureAction: "Choose as departure"
    }
  };

  var configRoot = form || calRoot;
  var lang = (configRoot && configRoot.dataset.lang) === "en" ? "en" : "de";
  var TXT = STRINGS[lang];
  var minNights = configRoot ? parseInt(configRoot.dataset.minNights || "5", 10) : 5;

  function euro(value) {
    return value.toLocaleString(lang === "en" ? "en-IE" : "de-AT", {
      style: "currency", currency: "EUR"
    });
  }

  function updatePrice() {
    if (!form) return;
    var prices = JSON.parse(form.dataset.prices || "{}");
    var arrival = form.querySelector('[name="arrival"]').value;
    var departure = form.querySelector('[name="departure"]').value;
    var adults = form.querySelector('[name="adults"]').value;
    var children = form.querySelector('[name="children"]').value;
    var taxAgeField = form.querySelector('[name="taxable_children"]');
    var taxAgeRow = document.getElementById("taxable-children-row");
    var childCount = parseInt(children, 10);
    if (taxAgeField && taxAgeRow) {
      taxAgeRow.hidden = childCount === 0;
      taxAgeField.disabled = childCount === 0;
      taxAgeField.required = childCount > 0;
      Array.from(taxAgeField.options).forEach(function (option) {
        option.disabled = option.value !== "" && parseInt(option.value, 10) > childCount;
      });
      if (childCount === 0 || parseInt(taxAgeField.value, 10) > childCount) taxAgeField.value = "";
    }
    var cleaningFee = parseFloat(form.dataset.cleaningFee || "0");
    var cityTaxRate = parseFloat(form.dataset.cityTax || "0");
    var box = document.getElementById("price-box");
    var warn = document.getElementById("combo-warning");
    box.hidden = true;
    warn.hidden = true;

    var perNight = prices[adults + "_" + children];
    if (perNight === undefined) {
      warn.textContent = TXT.combo;
      warn.hidden = false;
      return;
    }
    if (childCount > 0 && (!taxAgeField || taxAgeField.value === "")) {
      warn.textContent = TXT.taxAge;
      warn.hidden = false;
      return;
    }
    if (!arrival || !departure) return;

    var nights = Math.round((fromIso(departure) - fromIso(arrival)) / 86400000);
    if (nights < minNights) {
      if (nights > 0) {
        warn.textContent = TXT.minNights.replace("{n}", minNights);
        warn.hidden = false;
      }
      return;
    }
    var accommodation = nights * parseFloat(perNight);
    var taxableChildren = taxAgeField && taxAgeField.value !== "" ? parseInt(taxAgeField.value, 10) : 0;
    var cityTax = nights * (parseInt(adults, 10) + taxableChildren) * cityTaxRate;
    var total = accommodation + cleaningFee + cityTax;
    document.getElementById("price-night").textContent = euro(parseFloat(perNight));
    document.getElementById("price-nights").textContent = nights;
    document.getElementById("price-accommodation").textContent = euro(accommodation);
    document.getElementById("price-cleaning").textContent = euro(cleaningFee);
    document.getElementById("price-tax").textContent = euro(cityTax);
    document.getElementById("price-total").textContent = euro(total);
    box.hidden = false;
  }

  if (form) {
    ["arrival", "departure", "adults", "children", "taxable_children"].forEach(function (name) {
      var field = form.querySelector('[name="' + name + '"]');
      if (field) field.addEventListener("change", updatePrice);
    });
    updatePrice();
  }

  /* ---------- Kalender ---------- */

  if (!calRoot) return;

  var blocked = {};           // ISO-Datum -> true (belegte Nacht)
  var today = new Date();
  today.setHours(0, 0, 0, 0);
  var viewMonth = startOfMonth(today);   // linker der beiden Monate
  var maxMonth = addMonths(startOfMonth(today), 17); // bis zu 18 Monate
  var selArrival = null;
  var selDeparture = null;

  fetch(calRoot.dataset.availabilityUrl)
    .then(function (r) { return r.json(); })
    .then(function (data) {
      (data.blocked || []).forEach(function (d) { blocked[d] = true; });
      render();
    })
    .catch(render); // auch ohne Daten den Kalender zeigen

  document.getElementById("cal-prev").addEventListener("click", function () {
    if (viewMonth > startOfMonth(today)) { viewMonth = addMonths(viewMonth, -1); render(); }
  });
  document.getElementById("cal-next").addEventListener("click", function () {
    if (addMonths(viewMonth, 1) < maxMonth) { viewMonth = addMonths(viewMonth, 1); render(); }
  });

  function nightsFree(a, b) {
    // sind alle Nächte von a (inkl.) bis b (exkl.) frei?
    for (var d = new Date(a); d < b; d = addDays(d, 1)) {
      if (blocked[iso(d)]) return false;
    }
    return true;
  }

  function onDayClick(d) {
    if (!selArrival || (selArrival && selDeparture)) {
      // neue Auswahl beginnen: Anreisetag darf keine belegte Nacht sein
      if (blocked[iso(d)] || d < today) return;
      selArrival = d;
      selDeparture = null;
    } else {
      if (d <= selArrival) {          // rückwärts geklickt -> neue Anreise
        if (!blocked[iso(d)] && d >= today) { selArrival = d; }
      } else if (nightsFree(selArrival, d)) {
        selDeparture = d;             // Abreisetag darf selbst belegt "beginnen"
      } else {
        return;                       // Auswahl überspannt belegte Nächte
      }
    }
    if (form) {
      form.querySelector('[name="arrival"]').value = selArrival ? iso(selArrival) : "";
      form.querySelector('[name="departure"]').value = selDeparture ? iso(selDeparture) : "";
      updatePrice();
    }
    render();
  }

  function monthTable(monthStart) {
    var table = document.createElement("table");
    table.className = "cal-month";
    var caption = table.createCaption();
    caption.textContent = TXT.months[monthStart.getMonth()] + " " + monthStart.getFullYear();

    var head = table.createTHead().insertRow();
    TXT.weekdays.forEach(function (wd) {
      var th = document.createElement("th");
      th.textContent = wd;
      head.appendChild(th);
    });

    var body = table.createTBody();
    var firstWeekday = (monthStart.getDay() + 6) % 7; // Montag = 0
    var daysInMonth = new Date(monthStart.getFullYear(), monthStart.getMonth() + 1, 0).getDate();
    var row = body.insertRow();
    for (var i = 0; i < firstWeekday; i++) row.insertCell();

    for (var day = 1; day <= daysInMonth; day++) {
      if (row.cells.length === 7) row = body.insertRow();
      var cell = row.insertCell();
      var d = new Date(monthStart.getFullYear(), monthStart.getMonth(), day);
      var key = iso(d);
      cell.textContent = day;

      var departureAllowed = blocked[key] && selArrival && !selDeparture &&
          d > selArrival && nightsFree(selArrival, d);
      if (d < today) {
        cell.className = "past";
      } else if (blocked[key] && !departureAllowed) {
        cell.className = "booked";
      } else {
        cell.className = departureAllowed ? "booked departure-ok" : "free";
        cell.textContent = "";
        var dayButton = document.createElement("button");
        dayButton.type = "button";
        dayButton.className = "calendar-day";
        dayButton.dataset.date = key;
        dayButton.textContent = day;
        dayButton.setAttribute("aria-label", d.toLocaleDateString(lang === "en" ? "en-GB" : "de-AT", {
          weekday: "long", day: "numeric", month: "long", year: "numeric"
        }) + ": " + (selArrival && !selDeparture ? TXT.departureAction : TXT.arrivalAction));
        dayButton.setAttribute("aria-pressed", String(Boolean(
          (selArrival && key === iso(selArrival)) || (selDeparture && key === iso(selDeparture)))));
        (function (dd) {
          dayButton.addEventListener("click", function () {
            onDayClick(dd);
            var newButton = calRoot.querySelector('[data-date="' + iso(dd) + '"]');
            if (newButton) newButton.focus({preventScroll: true});
          });
        })(d);
        cell.appendChild(dayButton);
      }
      if (selArrival && key === iso(selArrival)) cell.classList.add("selected");
      if (selDeparture && key === iso(selDeparture)) cell.classList.add("selected");
      if (selArrival && selDeparture && d > selArrival && d < selDeparture) {
        cell.classList.add("in-range");
      }
    }
    while (row.cells.length < 7) row.insertCell();
    return table;
  }

  function render() {
    var wrapEl = document.getElementById("cal-months");
    wrapEl.innerHTML = "";
    wrapEl.appendChild(monthTable(viewMonth));
    wrapEl.appendChild(monthTable(addMonths(viewMonth, 1)));
    var hint = document.getElementById("cal-selection-hint");
    function dateLabel(date) {
      return date.toLocaleDateString(lang === "en" ? "en-GB" : "de-AT", {day: "numeric", month: "long", year: "numeric"});
    }
    if (hint) hint.textContent = !selArrival ? TXT.chooseArrival :
      !selDeparture ? TXT.chooseDeparture.replace("{date}", dateLabel(selArrival)) :
      TXT.selectedDates.replace("{arrival}", dateLabel(selArrival)).replace("{departure}", dateLabel(selDeparture));
    document.getElementById("cal-prev").disabled = viewMonth <= startOfMonth(today);
    document.getElementById("cal-next").disabled = addMonths(viewMonth, 1) >= maxMonth;
  }
})();
