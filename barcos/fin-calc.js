/* Plata Marine · calculadora de financiación orientativa en las fichas de barcos (ES/CA/EN/FR).
   Lee precio y año del inventario común (window.PM_INV). TIN orientativo 6,95 %, entrada 0-90 %,
   plazo máximo según antigüedad (antigüedad del barco + plazo <= 35 años, máx. 15 años); barcos anteriores a 1995, vendidos o retirados: no se muestra.
   No es una oferta de financiación: Plata Marine no concede préstamos. */
(function () {
  'use strict';
  var TIN = 6.95, MAXY = 15, MAXAGE = 35;
  function go() {
    var el = document.querySelector('[data-pm-boat]'), inv = window.PM_INV;
    if (!el || !inv || document.getElementById('pm-fin')) return;
    var slug = el.getAttribute('data-pm-boat'), b = (inv.boats || []).filter(function (x) { return x.slug === slug; })[0];
    if (!b || !b.price || !b.year || b.year < 1995 || b.status === 'sold' || b.status === 'paused') return;
    var now = new Date().getFullYear(), age = Math.max(0, now - b.year), maxY = Math.min(MAXY, MAXAGE - age);
    if (maxY < 2) return;
    var lg = (document.documentElement.lang || 'es').slice(0, 2); if (['es', 'ca', 'en', 'fr'].indexOf(lg) < 0) lg = 'es';
    var T = {
      es: { h: 'Financiación orientativa', s: 'Calcula una cuota aproximada para este barco. Pon la entrada que quieras (0 € = financiarlo entero).', p: 'Precio', pv: 'IVA incluido', d: 'Entrada', y: 'Plazo', yu: 'años', q: 'Cuota mensual aprox.', m: '/mes', f: 'Importe a financiar', i: 'Intereses totales aprox.', btn: 'Solicitar financiación', n: 'Cálculo orientativo con un tipo de interés nominal (TIN) del 6,95 %, sin comisiones ni seguros. No es una oferta de financiación: la aprobación, el tipo, el plazo y las condiciones dependen de la entidad financiera y de tu perfil. Plata Marine no concede préstamos; te pongo en contacto con una financiera.', wa: 'Hola Juan, me interesa financiar el ' + b.name + '.', wd: 'Entrada', wy: 'Plazo', wq: 'Cuota orientativa' },
      ca: { h: 'Finançament orientatiu', s: 'Calcula una quota aproximada per a aquest vaixell. Posa l’entrada que vulguis (0 € = finançar-lo sencer).', p: 'Preu', pv: 'IVA inclòs', d: 'Entrada', y: 'Termini', yu: 'anys', q: 'Quota mensual aprox.', m: '/mes', f: 'Import a finançar', i: 'Interessos totals aprox.', btn: 'Sol·licitar finançament', n: 'Càlcul orientatiu amb un tipus d’interès nominal (TIN) del 6,95 %, sense comissions ni assegurances. No és una oferta de finançament: l’aprovació, el tipus, el termini i les condicions depenen de l’entitat financera i del teu perfil. Plata Marine no concedeix préstecs; et poso en contacte amb una financera.', wa: 'Hola Juan, m’interessa finançar el ' + b.name + '.', wd: 'Entrada', wy: 'Termini', wq: 'Quota orientativa' },
      en: { h: 'Indicative finance', s: 'Work out an approximate monthly payment for this boat. Enter any deposit you like (€0 = finance it in full).', p: 'Price', pv: 'VAT included', d: 'Deposit', y: 'Term', yu: 'years', q: 'Approx. monthly payment', m: '/month', f: 'Amount financed', i: 'Approx. total interest', btn: 'Ask about finance', n: 'Indicative calculation with a nominal interest rate (TIN) of 6.95%, excluding fees and insurance. This is not a finance offer: approval, rate, term and conditions depend on the lender and your profile. Plata Marine does not grant loans; I put you in touch with a finance company.', wa: 'Hi Juan, I would like to finance the ' + b.name + '.', wd: 'Deposit', wy: 'Term', wq: 'Indicative payment' },
      fr: { h: 'Financement indicatif', s: 'Calculez une mensualité approximative pour ce bateau. Indiquez l’apport que vous souhaitez (0 € = tout financer).', p: 'Prix', pv: 'TVA incluse', d: 'Apport', y: 'Durée', yu: 'ans', q: 'Mensualité approx.', m: '/mois', f: 'Montant financé', i: 'Intérêts totaux approx.', btn: 'Demander un financement', n: 'Calcul indicatif avec un taux nominal (TIN) de 6,95 %, hors frais et assurances. Ce n’est pas une offre de financement : l’accord, le taux, la durée et les conditions dépendent de l’organisme et de votre profil. Plata Marine n’accorde pas de prêts ; je vous mets en relation avec un organisme de financement.', wa: 'Bonjour Juan, je souhaite financer le ' + b.name + '.', wd: 'Apport', wy: 'Durée', wq: 'Mensualité indicative' }
    }[lg];
    function eur(n) { var s = Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, lg === 'en' ? ',' : (lg === 'fr' ? ' ' : '.')); return lg === 'en' ? '€' + s : s + ' €'; }
    var price = b.vat ? Math.round(b.price * 1.21) : b.price;
    var st = document.createElement('style');
    st.textContent = '.pm-fin{margin:28px auto;max-width:760px;padding:22px;border:1.5px solid var(--line,#dfe5e8);border-radius:16px;background:#fff}.pm-fin h3{margin:0 0 6px;font-size:1.2rem}.pm-fin>p{margin:0 0 16px;color:#44545F;font-size:.95rem}.pm-fin .g{display:grid;grid-template-columns:1fr 1fr;gap:14px}.pm-fin label{display:block;font-weight:600;font-size:14px;margin:0 0 6px}.pm-fin .row{display:flex;gap:8px;align-items:center}.pm-fin input[type=range]{flex:1;accent-color:var(--wa,#0B766B)}.pm-fin input[type=number],.pm-fin select{width:100%;box-sizing:border-box;padding:10px 12px;border:1.5px solid var(--line,#dfe5e8);border-radius:10px;font:inherit}.pm-fin .row input[type=number]{width:120px}.pm-fin .res{margin-top:16px;padding:16px;border-radius:12px;background:#0E3042;color:#fff;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:center}.pm-fin .res b{font-size:1.7rem}.pm-fin .res small{display:block;opacity:.8;font-size:13px}.pm-fin .res a{display:inline-block;padding:12px 18px;border-radius:12px;background:var(--wa,#0B766B);color:#fff;font-weight:700;text-decoration:none}.pm-fin .n{font-size:12px;color:#6b7a84;margin:12px 0 0;line-height:1.45}@media(max-width:640px){.pm-fin .g{grid-template-columns:1fr}.pm-fin{margin:24px 16px}}';
    document.head.appendChild(st);
    var box = document.createElement('section'); box.className = 'pm-fin'; box.id = 'pm-fin';
    var opts = ''; for (var y = 2; y <= maxY; y++) opts += '<option value="' + y + '"' + (y === Math.min(10, maxY) ? ' selected' : '') + '>' + y + ' ' + T.yu + '</option>';
    box.innerHTML = '<h3>' + T.h + '</h3><p>' + T.s + '</p><div class="g">' +
      '<div><label>' + T.p + '</label><div style="font-size:1.25rem;font-weight:700;padding:8px 0">' + eur(price) + (b.vat ? ' <small style="font-weight:400;font-size:13px">(' + T.pv + ')</small>' : '') + '</div></div>' +
      '<div><label for="pf-y">' + T.y + '</label><select id="pf-y">' + opts + '</select></div>' +
      '<div style="grid-column:1/-1"><label for="pf-d">' + T.d + '</label><div class="row"><input type="range" id="pf-r" min="0" max="90" step="5" value="20" aria-label="' + T.d + ' %"><input type="number" id="pf-d" min="0" max="' + Math.round(price * 0.9) + '" step="500" inputmode="numeric"></div></div>' +
      '</div><div class="res"><div><small>' + T.q + '</small><b id="pf-q"></b><small id="pf-x"></small></div><a id="pf-wa" target="_blank" rel="noopener" data-wa-context="financiacion">' + T.btn + '</a></div><p class="n">' + T.n + '</p>';
    var anchor = document.getElementById('coste') || document.querySelector('.specs') || document.getElementById('presupuesto');
    if (anchor && anchor.parentNode) anchor.parentNode.insertBefore(box, anchor); else return;
    var r = box.querySelector('#pf-r'), d = box.querySelector('#pf-d'), ys = box.querySelector('#pf-y');
    d.value = Math.round(price * 0.2);
    function calc() {
      var dep = Math.min(Math.max(+d.value || 0, 0), price * 0.9), loan = price - dep, n = +ys.value * 12, i = TIN / 100 / 12;
      var q = loan > 0 ? loan * i / (1 - Math.pow(1 + i, -n)) : 0;
      box.querySelector('#pf-q').textContent = eur(q) + ' ' + T.m;
      box.querySelector('#pf-x').textContent = T.f + ': ' + eur(loan) + ' · ' + T.i + ': ' + eur(Math.max(0, q * n - loan));
      var msg = T.wa + '\n- ' + T.wd + ': ' + eur(dep) + '\n- ' + T.wy + ': ' + ys.value + ' ' + T.yu + '\n- ' + T.wq + ': ' + eur(q) + ' ' + T.m + '\n' + location.origin + location.pathname;
      box.querySelector('#pf-wa').href = 'https://wa.me/34633742973?text=' + encodeURIComponent(msg);
    }
    r.addEventListener('input', function () { d.value = Math.round(price * r.value / 100 / 100) * 100; calc(); });
    d.addEventListener('input', function () { var v = Math.min(Math.max(+d.value || 0, 0), price * 0.9); r.value = Math.round(v / price * 20) * 5; calc(); });
    ys.addEventListener('change', calc);
    box.querySelector('#pf-wa').addEventListener('click', function () { if (window.pmTrack) window.pmTrack('contact_intent', { method: 'whatsapp', placement: 'financiacion', boat: b.name }); });
    calc();
  }
  if (window.PM_INV) go();
  else { var t = 0, iv = setInterval(function () { if (window.PM_INV || ++t > 40) { clearInterval(iv); go(); } }, 150); }
})();
