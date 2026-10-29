/* Plata Marine · financiación orientativa en las páginas de barcos nuevos (ES/CA/EN/FR).
   Lee el total del configurador de cada marca (sin impuestos), le suma el IVA (21 %) y calcula una cuota orientativa.
   TIN orientativo 6,95 %, plazo máximo 15 años, entrada 0-90 %. No incluye impuesto de matriculación ni transporte.
   No es una oferta de financiación: Plata Marine no concede préstamos. */
(function () {
  'use strict';
  if (window.__pmFinNew) return; window.__pmFinNew = 1;
  var TIN = 6.95, MAXY = 15, VAT = 1.21, i = TIN / 100 / 12, TAE = (Math.pow(1 + i, 12) - 1) * 100;
  var SEL = '.sk-total,.mm-tot,.ss-cfg-sum,.pc-tot,#cc-tot,[data-pm-total]';
  var lg = (document.documentElement.lang || 'es').slice(0, 2); if (['es', 'ca', 'en', 'fr'].indexOf(lg) < 0) lg = 'es';
  var T = {
    es: { from: 'o desde', m: '/mes', cond: function (n) { return n + ' meses sin entrada · IVA incl. · TIN 6,95 % · TAE ' + pct(TAE); }, see: 'calcula tu cuota', h: 'Calcula tu cuota y fináncialo', s: 'Pon el precio del barco tal como lo configures (con IVA), elige entrada y plazo y pide el estudio sin compromiso.', p: 'Precio con IVA', d: 'Entrada', y: 'Plazo', yu: 'años', q: 'Cuota mensual aprox.', f: 'Importe a financiar', t: 'Total a pagar aprox.', btn: 'Solicitar financiación', ex: function (a, n, q, tot) { return 'Ejemplo representativo: para financiar ' + a + ' a ' + n + ' meses, cuota de ' + q + ', TIN 6,95 %, TAE ' + pct(TAE) + ' (sin comisiones), importe total adeudado ' + tot + '.'; }, n: 'Cálculo orientativo, sin comisiones ni seguros. No incluye el impuesto de matriculación (barcos de más de 8 m) ni el transporte. No es una oferta de financiación: la aprobación, el tipo, el plazo y las condiciones dependen de la entidad financiera y de tu perfil. Plata Marine no concede préstamos; te pongo en contacto con una financiera.', wa: 'Hola Juan, me interesa financiar un barco nuevo', wd: 'Entrada', wy: 'Plazo', wq: 'Cuota orientativa', wp: 'Precio con IVA' },
    ca: { from: 'o des de', m: '/mes', cond: function (n) { return n + ' mesos sense entrada · IVA incl. · TIN 6,95 % · TAE ' + pct(TAE); }, see: 'calcula la teva quota', h: 'Calcula la teva quota i finança’l', s: 'Posa el preu del vaixell tal com el configuris (amb IVA), tria entrada i termini i demana l’estudi sense compromís.', p: 'Preu amb IVA', d: 'Entrada', y: 'Termini', yu: 'anys', q: 'Quota mensual aprox.', f: 'Import a finançar', t: 'Total a pagar aprox.', btn: 'Sol·licitar finançament', ex: function (a, n, q, tot) { return 'Exemple representatiu: per finançar ' + a + ' a ' + n + ' mesos, quota de ' + q + ', TIN 6,95 %, TAE ' + pct(TAE) + ' (sense comissions), import total degut ' + tot + '.'; }, n: 'Càlcul orientatiu, sense comissions ni assegurances. No inclou l’impost de matriculació (vaixells de més de 8 m) ni el transport. No és una oferta de finançament: l’aprovació, el tipus, el termini i les condicions depenen de l’entitat financera i del teu perfil. Plata Marine no concedeix préstecs; et poso en contacte amb una financera.', wa: 'Hola Juan, m’interessa finançar un vaixell nou', wd: 'Entrada', wy: 'Termini', wq: 'Quota orientativa', wp: 'Preu amb IVA' },
    en: { from: 'or from', m: '/month', cond: function (n) { return n + ' months, no deposit · VAT incl. · TIN 6.95% · APR ' + pct(TAE); }, see: 'work out your payment', h: 'Work out your payment and finance it', s: 'Enter the price of the boat as you configure it (VAT included), choose deposit and term, and ask for a no-obligation study.', p: 'Price incl. VAT', d: 'Deposit', y: 'Term', yu: 'years', q: 'Approx. monthly payment', f: 'Amount financed', t: 'Approx. total payable', btn: 'Ask about finance', ex: function (a, n, q, tot) { return 'Representative example: financing ' + a + ' over ' + n + ' months, monthly payment ' + q + ', TIN 6.95%, APR ' + pct(TAE) + ' (no fees), total amount payable ' + tot + '.'; }, n: 'Indicative calculation, excluding fees and insurance. It does not include Spanish registration tax (boats over 8 m) or transport. This is not a finance offer: approval, rate, term and conditions depend on the lender and your profile. Plata Marine does not grant loans; I put you in touch with a finance company.', wa: 'Hi Juan, I would like to finance a new boat', wd: 'Deposit', wy: 'Term', wq: 'Indicative payment', wp: 'Price incl. VAT' },
    fr: { from: 'ou dès', m: '/mois', cond: function (n) { return n + ' mois sans apport · TVA incl. · TIN 6,95 % · TAEG ' + pct(TAE); }, see: 'calculez votre mensualité', h: 'Calculez votre mensualité et financez-le', s: 'Indiquez le prix du bateau tel que vous le configurez (TVA incluse), choisissez l’apport et la durée et demandez l’étude sans engagement.', p: 'Prix TVA incluse', d: 'Apport', y: 'Durée', yu: 'ans', q: 'Mensualité approx.', f: 'Montant financé', t: 'Total à payer approx.', btn: 'Demander un financement', ex: function (a, n, q, tot) { return 'Exemple représentatif : pour financer ' + a + ' sur ' + n + ' mois, mensualité de ' + q + ', TIN 6,95 %, TAEG ' + pct(TAE) + ' (sans frais), montant total dû ' + tot + '.'; }, n: 'Calcul indicatif, hors frais et assurances. N’inclut pas la taxe d’immatriculation espagnole (bateaux de plus de 8 m) ni le transport. Ce n’est pas une offre de financement : l’accord, le taux, la durée et les conditions dépendent de l’organisme et de votre profil. Plata Marine n’accorde pas de prêts ; je vous mets en relation avec un organisme de financement.', wa: 'Bonjour Juan, je souhaite financer un bateau neuf', wd: 'Apport', wy: 'Durée', wq: 'Mensualité indicative', wp: 'Prix TVA incluse' }
  }[lg];
  function pct(x) { var s = x.toFixed(2); return (lg === 'en' ? s : s.replace('.', ',')) + (lg === 'en' ? '%' : ' %'); }
  function eur(n) { var s = Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, lg === 'en' ? ',' : (lg === 'fr' ? ' ' : '.')); return lg === 'en' ? '€' + s : s + ' €'; }
  function pay(loan, n) { return loan > 0 ? loan * i / (1 - Math.pow(1 + i, -n)) : 0; }
  function parse(el) {
    var t = (el.innerText || el.textContent || '').replace(/[  ]/g, ' ');
    var m = lg === 'en' ? t.match(/€ ?(\d{1,3}(?:,\d{3})+|\d{4,})/) : t.match(/(\d{1,3}(?:[. ]\d{3})+|\d{4,}) ?€/);
    if (!m) return 0;
    var v = +m[1].replace(/[.,\s]/g, '');
    return v > 1000 ? v : 0;
  }
  var css = '.pmf-line{margin:8px 0 0;font-size:14px;line-height:1.4}.pmf-line b{font-size:1.15em;color:#E8590C}.pmf-dark b{color:#ffb74d}.pmf-line small{display:block;opacity:.75;font-size:12px}.pmf-line a{color:inherit;text-decoration:underline}' +
    '.pm-fin{margin:32px auto;max-width:760px;padding:22px;border:1.5px solid #dfe5e8;border-radius:16px;background:#fff;color:#0E3042}.pm-fin h3{margin:0 0 6px;font-size:1.25rem}.pm-fin>p{margin:0 0 16px;color:#44545F;font-size:.95rem}.pm-fin .g{display:grid;grid-template-columns:1fr 1fr;gap:14px}.pm-fin label{display:block;font-weight:600;font-size:14px;margin:0 0 6px}.pm-fin .row{display:flex;gap:8px;align-items:center}.pm-fin input[type=range]{flex:1;accent-color:#0B766B}.pm-fin input[type=number],.pm-fin select{width:100%;box-sizing:border-box;padding:10px 12px;border:1.5px solid #dfe5e8;border-radius:10px;font:inherit}.pm-fin .row input[type=number]{width:130px}.pm-fin .res{margin-top:16px;padding:16px;border-radius:12px;background:#0E3042;color:#fff;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:center}.pm-fin .res b{font-size:1.7rem}.pm-fin .res small{display:block;opacity:.8;font-size:13px}.pm-fin .res a{display:inline-block;padding:12px 18px;border-radius:12px;background:#0B766B;color:#fff;font-weight:700;text-decoration:none}.pm-fin .n{font-size:12px;color:#6b7a84;margin:12px 0 0;line-height:1.45}@media(max-width:640px){.pm-fin .g{grid-template-columns:1fr}.pm-fin{margin:24px 16px}}';
  function go() {
    var els = [].slice.call(document.querySelectorAll(SEL)).filter(function (e) { return parse(e) > 0; });
    if (!els.length) return;
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    function NM(p) { return (p < 15000 ? 8 : (p < 40000 ? 10 : MAXY)) * 12; }
    function line(el) {
      var p = parse(el); if (!p) return;
      var ln = el.nextElementSibling && el.nextElementSibling.classList.contains('pmf-line') ? el.nextElementSibling : null;
      if (!ln) {
        ln = document.createElement('div'); ln.className = 'pmf-line';
        var bg = getComputedStyle(el).color; var c = bg.match(/\d+/g);
        if (c && (+c[0] + +c[1] + +c[2]) > 600) ln.className += ' pmf-dark';
        el.parentNode.insertBefore(ln, el.nextSibling);
      }
      var N = NM(p * VAT), html = T.from + ' <b>' + eur(pay(p * VAT, N)) + T.m + '</b><small>' + T.cond(N) + ' · <a href="#pm-fin">' + T.see + '</a></small>';
      if (ln.__h !== html) { ln.innerHTML = html; ln.__h = html; }
    }
    els.forEach(function (el) {
      line(el);
      new MutationObserver(function () { line(el); }).observe(el, { childList: true, subtree: true, characterData: true });
    });
    // calculadora
    var box = document.createElement('section'); box.className = 'pm-fin'; box.id = 'pm-fin';
    var opts = ''; for (var y = 2; y <= MAXY; y++) opts += '<option value="' + y + '"' + (y === 10 ? ' selected' : '') + '>' + y + ' ' + T.yu + '</option>';
    box.innerHTML = '<h3>' + T.h + '</h3><p>' + T.s + '</p><div class="g">' +
      '<div><label for="pf-p">' + T.p + '</label><input type="number" id="pf-p" min="1000" step="500" inputmode="numeric"></div>' +
      '<div><label for="pf-y">' + T.y + '</label><select id="pf-y">' + opts + '</select></div>' +
      '<div style="grid-column:1/-1"><label for="pf-d">' + T.d + '</label><div class="row"><input type="range" id="pf-r" min="0" max="90" step="5" value="20" aria-label="' + T.d + ' %"><input type="number" id="pf-d" min="0" step="500" inputmode="numeric"></div></div>' +
      '</div><div class="res"><div><small>' + T.q + '</small><b id="pf-q"></b><small id="pf-x"></small></div><a id="pf-wa" target="_blank" rel="noopener" data-wa-context="financiacion">' + T.btn + '</a></div><p class="n" id="pf-ex"></p><p class="n">' + T.n + '</p>';
    var anchor = document.querySelector('footer');
    var host = els[0].closest('section') || els[0].parentNode;
    if (host && host.parentNode) host.parentNode.insertBefore(box, host.nextSibling); else if (anchor) anchor.parentNode.insertBefore(box, anchor); else return;
    var P = box.querySelector('#pf-p'), r = box.querySelector('#pf-r'), d = box.querySelector('#pf-d'), ys = box.querySelector('#pf-y'), touched = false;
    function visibleTotal() { var v = els.filter(function (e) { return e.offsetParent !== null; })[0] || els[0]; return parse(v); }
    function sync() { if (!touched) { P.value = Math.round(visibleTotal() * VAT); d.value = Math.round(P.value * r.value / 100 / 100) * 100; calc(); } }
    function calc() {
      var price = +P.value || 0, dep = Math.min(Math.max(+d.value || 0, 0), price * 0.9), loan = Math.max(0, price - dep), n = +ys.value * 12, q = pay(loan, n);
      box.querySelector('#pf-q').textContent = eur(q) + ' ' + T.m;
      box.querySelector('#pf-x').textContent = T.f + ': ' + eur(loan) + ' · ' + T.t + ': ' + eur(q * n + dep);
      box.querySelector('#pf-ex').textContent = T.ex(eur(loan), n, eur(q), eur(q * n));
      var h1 = document.querySelector('h1'), msg = T.wa + (h1 ? ' (' + h1.textContent.trim() + ')' : '') + '.\n- ' + T.wp + ': ' + eur(price) + '\n- ' + T.wd + ': ' + eur(dep) + '\n- ' + T.wy + ': ' + ys.value + ' ' + T.yu + '\n- ' + T.wq + ': ' + eur(q) + ' ' + T.m + '\n' + location.origin + location.pathname;
      box.querySelector('#pf-wa').href = 'https://wa.me/34633742973?text=' + encodeURIComponent(msg);
    }
    P.addEventListener('input', function () { touched = true; d.value = Math.round((+P.value || 0) * r.value / 100 / 100) * 100; calc(); });
    r.addEventListener('input', function () { d.value = Math.round((+P.value || 0) * r.value / 100 / 100) * 100; calc(); });
    d.addEventListener('input', function () { var p = +P.value || 1, v = Math.min(Math.max(+d.value || 0, 0), p * 0.9); r.value = Math.round(v / p * 20) * 5; calc(); });
    ys.addEventListener('change', calc);
    box.querySelector('#pf-wa').addEventListener('click', function () { if (window.pmTrack) window.pmTrack('contact_intent', { method: 'whatsapp', placement: 'financiacion_nuevo' }); });
    els.forEach(function (el) { new MutationObserver(sync).observe(el, { childList: true, subtree: true, characterData: true }); });
    document.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('[role=tab],.sk-tabs button')) setTimeout(sync, 50); });
    sync();
  }
  if (document.readyState === 'complete') setTimeout(go, 300); else window.addEventListener('load', function () { setTimeout(go, 300); });
})();
