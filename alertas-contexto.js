/* Plata Marine · alerta con contexto.
   Si se llega a /alertas/ desde una ficha (?ref=slug), rellena el formulario con
   un punto de partida parecido a ese barco (tipo, eslora, presupuesto y zona) y lo
   dice arriba del formulario. El usuario puede cambiarlo todo. Sin datos personales. */
(function () {
  'use strict';
  function run() {
    var inv = window.PM_INV, form = document.getElementById('alertaForm');
    if (!inv || !form) return;
    var ref = new URLSearchParams(location.search).get('ref');
    var b = ref && inv.get(ref);
    if (!b) return;
    var lang = inv.lang();
    function pick(id, idx) {
      var s = document.getElementById(id);
      if (s && idx > 0 && idx < s.options.length && !s.value) s.selectedIndex = idx;
    }
    /* Orden de opciones (igual en ES/CA/EN):
       tipo: 1 cualquiera, 2 velero, 3 open, 4 sundeck, 5 walkaround, 6 cabinado, 7 pilothouse, 8 fly, 9 semirrígida */
    var T = {velero: 2, open: 3, sundeck: 4, walkaround: 5, cabinado: 6, pilothouse: 7, fly: 8, rib: 9};
    pick('a-tipo', T[(b.types || [])[0]] || 1);
    var L = b.length || 0;
    pick('a-eslora', L < 6 ? 1 : L < 8 ? 2 : L < 10 ? 3 : L < 12 ? 4 : L < 15 ? 5 : 6);
    var P = b.price || 0;
    pick('a-presu', P < 30000 ? 1 : P < 60000 ? 2 : P < 120000 ? 3 : P < 250000 ? 4 : 5);
    if (b.zone === 'baleares') pick('a-zona', 6);
    var txt = {
      es: 'He dejado rellenada la alerta con algo parecido al <b>' + b.name + '</b>. Cámbiala como quieras: te aviso si entra un barco que encaje.',
      ca: 'He deixat l’alerta emplenada amb una cosa semblant al <b>' + b.name + '</b>. Canvia-la com vulguis: t’aviso si entra un vaixell que encaixi.',
      en: 'I’ve pre-filled the alert with something similar to the <b>' + b.name + '</b>. Change anything you like: I’ll let you know if a matching boat comes in.'
    }[lang];
    var note = document.createElement('p');
    note.className = 'alerta-contexto';
    note.setAttribute('style', 'background:#eef4f7;border-left:3px solid #0e3042;padding:10px 12px;border-radius:8px;margin:0 0 14px;font-size:.95em');
    note.innerHTML = txt;
    form.parentNode.insertBefore(note, form);
    var n = document.getElementById('a-notas');
    var pre = {es: 'Visto en la web: ', ca: 'Vist al web: ', en: 'Seen on the website: '}[lang];
    if (n && !n.value) n.value = pre + b.name + '. ';
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
