/* Prepare an email locally; sending remains an explicit action in the email app. */
(function () {
  'use strict';
  var button = document.getElementById('preview-inquiry-button');
  var form = document.getElementById('inquiry-form');
  if (!button || !form) return;
  var english = form.dataset.lang === 'en';
  var feedback = document.getElementById('inquiry-feedback');
  function field(name) { return form.querySelector('[name="' + name + '"]'); }
  function value(name) { return field(name).value.trim(); }
  function invalid(message) {
    feedback.textContent = message;
    feedback.hidden = false;
    feedback.scrollIntoView({block: 'nearest'});
  }
  button.addEventListener('click', function () {
    feedback.hidden = true;
    var today = new Date();
    var todayIso = today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
    field('arrival').min = todayIso;
    field('departure').min = todayIso;
    var inputs = form.querySelectorAll('input, select, textarea');
    for (var i = 0; i < inputs.length; i++) {
      if (!inputs[i].disabled && !inputs[i].reportValidity()) return;
    }
    var nights = (Date.parse(value('departure')) - Date.parse(value('arrival'))) / 86400000;
    var minimum = Number(form.dataset.minNights || 5);
    if (!Number.isFinite(nights) || nights < minimum) {
      invalid(english ? 'Please choose a stay of at least ' + minimum + ' nights.' : 'Bitte wählt einen Aufenthalt von mindestens ' + minimum + ' Nächten.');
      return;
    }
    var prices = JSON.parse(form.dataset.prices || '{}');
    if (prices[value('adults') + '_' + value('children')] === undefined) {
      invalid(english ? 'Please choose 3 adults without children or one of the listed family combinations.' : 'Bitte wählt 3 Erwachsene ohne Kinder oder eine der aufgeführten Familienkombinationen.');
      return;
    }
    var children = Number(value('children'));
    if (children > 0 && (value('taxable_children') === '' || Number(value('taxable_children')) > children)) {
      invalid(english ? 'Please select how many children are aged 16 or 17.' : 'Bitte wählt aus, wie viele Kinder 16 oder 17 Jahre alt sind.');
      return;
    }
    var labels = english ? ['Arrival', 'Departure', 'Adults', 'Children', 'Children aged 16–17', 'Name', 'Email', 'Message'] : ['Anreise', 'Abreise', 'Erwachsene', 'Kinder', 'Davon 16–17 Jahre', 'Name', 'E-Mail', 'Nachricht'];
    var values = [value('arrival'), value('departure'), value('adults'), value('children'), children ? value('taxable_children') : '0', value('name'), value('email'), value('message')];
    var body = (english ? 'Hello Haus Flora,\nI would like to ask about the following stay:\n\n' : 'Hallo Haus Flora,\nich möchte folgenden Aufenthalt anfragen:\n\n') + labels.map(function (label, index) { return label + ': ' + values[index]; }).join('\n');
    var subject = (english ? 'Holiday inquiry: ' : 'Urlaubsanfrage: ') + value('arrival') + ' – ' + value('departure');
    window.location.href = 'mailto:' + encodeURIComponent(button.dataset.email) + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  });
})();
