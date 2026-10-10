/* Plata Marine · acciones de la ficha (ES/CA/EN/FR), solo en barcos disponibles:
   1) "Quiero verlo en persona" lleva a la agenda de visitas (/visita/?barco=…), dentro de la web.
   2) Recuadro "Presupuesto de traslado": por carretera y, si el barco lo permite, navegando.
      La solicitud entra en la hoja de leads (source "traslado"); Juan pide el presupuesto y contesta. */
(function () {
  'use strict';
  var INV = window.PM_INV;
  if (!INV || !INV.boats) return;
  var slug = (location.pathname.match(/\/barcos\/([^\/]+)\.html$/) || [])[1];
  var b = null;
  for (var i = 0; i < INV.boats.length; i++) if (INV.boats[i].slug === slug) b = INV.boats[i];
  if (!b || b.status !== 'available') return;
  var lang = (document.documentElement.lang || 'es').slice(0, 2);
  var PRE = lang === 'es' ? '' : '/' + lang;
  var LEADS_URL = 'https://script.google.com/macros/s/AKfycbwJtBkktakE0qgmu_b8oHOOopCDnG6BDpBjg2zBUsZKi8l3_OBEuez_OHWmE9j8qCBF/exec';
  // Por mar solo veleros y barcos de 7 m o más (los pequeños y las semirrígidas, por carretera)
  var mar = b.kind === 'vela' || (b.kind === 'motor' && b.length >= 7);
  var T = {
    es: {visit: 'Solicitar visita', ey: 'Traslado', h: '¿Lo quieres en otro puerto?', p: mar ? 'Te pido presupuesto para llevarlo por carretera o navegando hasta donde lo quieras tener.' : 'Te pido presupuesto para llevarlo por carretera hasta donde lo quieras tener.',
      open: 'Pedir presupuesto de traslado', dest: 'Destino (puerto o población) *', country: 'País', countries: ['España', 'Francia', 'Italia', 'Portugal', 'Otro'], how: 'Cómo', road: 'Por carretera', sea: 'Navegando', any: 'Lo que me recomiendes',
      name: 'Nombre *', tel: 'Teléfono *', mail: 'Correo *', consent: 'Acepto que Plata Marine use estos datos para enviarme el presupuesto, según la <a href="' + PRE + '/privacidad.html" target="_blank" rel="noopener">política de privacidad</a>. *',
      note: 'El traslado lo hace una empresa de transporte o un patrón profesional; te paso su presupuesto tal cual, sin compromiso. Para pedirlo solo doy el barco y el destino, no tus datos. Plazos y precio dependen del trayecto y la meteorología.',
      send: 'Pedir presupuesto', sending: 'Enviando…', ok: 'Recibido. Te escribo con el presupuesto en cuanto lo tenga.', okBtn: 'Enviado ✓',
      eDest: 'Dime a dónde lo quieres llevar.', eName: 'Necesito tu nombre.', eTel: 'Revisa el teléfono: puedes escribirlo con prefijo, por ejemplo +34 600 000 000.', eMail: 'Revisa el correo, no parece correcto.', eConsent: 'Necesito que aceptes la política de privacidad.',
      fail: 'No he podido confirmar que ha llegado. Tus datos siguen aquí: vuelve a intentarlo en unos minutos o escríbeme por <a href="https://wa.me/34633742973" target="_blank" rel="noopener">WhatsApp</a>.'},
    ca: {visit: 'Sol·licitar visita', ey: 'Trasllat', h: 'El vols en un altre port?', p: mar ? 'Et demano pressupost per portar-lo per carretera o navegant fins on el vulguis tenir.' : 'Et demano pressupost per portar-lo per carretera fins on el vulguis tenir.',
      open: 'Demanar pressupost de trasllat', dest: 'Destinació (port o població) *', country: 'País', countries: ['Espanya', 'França', 'Itàlia', 'Portugal', 'Altre'], how: 'Com', road: 'Per carretera', sea: 'Navegant', any: 'El que em recomanis',
      name: 'Nom *', tel: 'Telèfon *', mail: 'Correu *', consent: 'Accepto que Plata Marine faci servir aquestes dades per enviar-me el pressupost, segons la <a href="' + PRE + '/privacidad.html" target="_blank" rel="noopener">política de privacitat</a>. *',
      note: 'El trasllat el fa una empresa de transport o un patró professional; et passo el seu pressupost tal qual, sense compromís. Per demanar-lo només dono el vaixell i la destinació, no les teves dades. Terminis i preu depenen del trajecte i de la meteorologia.',
      send: 'Demanar pressupost', sending: 'Enviant…', ok: 'Rebut. T’escric amb el pressupost tan aviat com el tingui.', okBtn: 'Enviat ✓',
      eDest: 'Digues-me on el vols portar.', eName: 'Necessito el teu nom.', eTel: 'Revisa el telèfon: el pots escriure amb prefix, per exemple +34 600 000 000.', eMail: 'Revisa el correu, no sembla correcte.', eConsent: 'Necessito que acceptis la política de privacitat.',
      fail: 'No he pogut confirmar que ha arribat. Les teves dades segueixen aquí: torna-ho a provar d’aquí a uns minuts o escriu-me per <a href="https://wa.me/34633742973" target="_blank" rel="noopener">WhatsApp</a>.'},
    en: {visit: 'Book a viewing', ey: 'Delivery', h: 'Want it in another marina?', p: mar ? 'I can get you a quote to move it by road or by sea to wherever you want to keep it.' : 'I can get you a quote to move it by road to wherever you want to keep it.',
      open: 'Get a delivery quote', dest: 'Destination (marina or town) *', country: 'Country', countries: ['Spain', 'France', 'Italy', 'Portugal', 'Other'], how: 'How', road: 'By road', sea: 'By sea', any: 'Whatever you recommend',
      name: 'Name *', tel: 'Phone *', mail: 'Email *', consent: 'I agree that Plata Marine may use these details to send me the quote, as set out in the <a href="' + PRE + '/privacidad.html" target="_blank" rel="noopener">privacy policy</a>. *',
      note: 'The delivery is carried out by a transport company or a professional skipper; I pass on their quote as it is, with no obligation. To request it I only share the boat and the destination, not your details. Timing and price depend on the route and the weather.',
      send: 'Request quote', sending: 'Sending…', ok: "Received. I'll get back to you with the quote as soon as I have it.", okBtn: 'Sent ✓',
      eDest: 'Tell me where you want it delivered.', eName: 'I need your name.', eTel: 'Please check the phone number, e.g. +34 600 000 000.', eMail: "Please check the email, it doesn't look right.", eConsent: 'Please accept the privacy policy.',
      fail: "I couldn't confirm that it arrived. Your details are still here: try again in a few minutes or message me on <a href=\"https://wa.me/34633742973\" target=\"_blank\" rel=\"noopener\">WhatsApp</a>."},
    fr: {visit: 'Demander une visite', ey: 'Convoyage', h: 'Vous le voulez dans un autre port ?', p: mar ? 'Je vous obtiens un devis pour l’acheminer par la route ou par la mer jusqu’à l’endroit de votre choix.' : 'Je vous obtiens un devis pour l’acheminer par la route jusqu’à l’endroit de votre choix.',
      open: 'Demander un devis de transport', dest: 'Destination (port ou ville) *', country: 'Pays', countries: ['France', 'Espagne', 'Italie', 'Portugal', 'Autre'], how: 'Comment', road: 'Par la route', sea: 'Par la mer', any: 'Ce que vous me conseillez',
      name: 'Nom *', tel: 'Téléphone *', mail: 'E-mail *', consent: 'J’accepte que Plata Marine utilise ces données pour m’envoyer le devis, conformément à la <a href="' + PRE + '/privacidad.html" target="_blank" rel="noopener">politique de confidentialité</a>. *',
      note: 'Le transport est assuré par une entreprise de transport ou un skipper professionnel ; je vous transmets leur devis tel quel, sans engagement. Pour le demander, je ne communique que le bateau et la destination, pas vos données. Délais et prix dépendent du trajet et de la météo.',
      send: 'Demander le devis', sending: 'Envoi…', ok: 'Bien reçu. Je vous écris avec le devis dès que je l’ai.', okBtn: 'Envoyé ✓',
      eDest: 'Indiquez-moi où vous voulez le bateau.', eName: 'J’ai besoin de votre nom.', eTel: 'Vérifiez le téléphone, par exemple +33 6 00 00 00 00.', eMail: 'Vérifiez l’e-mail, il ne semble pas correct.', eConsent: 'Merci d’accepter la politique de confidentialité.',
      fail: 'Je n’ai pas pu confirmer la réception. Vos données sont toujours là : réessayez dans quelques minutes ou écrivez-moi sur <a href="https://wa.me/34633742973" target="_blank" rel="noopener">WhatsApp</a>.'}
  }[lang] || null;
  if (!T) return;

  /* 1) Botón de visita → agenda de la web */
  var vis = document.querySelectorAll('a[data-wa-context="ficha_visita"]');
  for (var v = 0; v < vis.length; v++) {
    vis[v].setAttribute('href', PRE + '/visita/?barco=' + encodeURIComponent(b.slug));
    vis[v].removeAttribute('target'); vis[v].removeAttribute('rel');
    vis[v].setAttribute('data-wa-context', 'ficha_agenda');
    vis[v].textContent = T.visit;
  }

  /* 2) Presupuesto de traslado */
  var card = document.querySelector('aside.aside .card');
  if (!card) return;
  var css = document.createElement('style');
  css.textContent = '.pm-tr{margin:16px 0 0}.pm-tr h3{margin:.2em 0 .4em}.pm-tr form{margin:12px 0 0}.pm-tr label{display:block;font-family:var(--display);font-size:12.5px;font-weight:600;color:var(--ink-2);margin:0 0 4px}' +
    '.pm-tr input[type=text],.pm-tr input[type=tel],.pm-tr input[type=email],.pm-tr select{width:100%;box-sizing:border-box;font:15px var(--serif);padding:9px 10px;border:1px solid var(--plata-2);border-radius:6px;background:#fff;color:var(--ink);margin:0 0 10px}' +
    '.pm-tr .chk{display:flex;gap:8px;align-items:flex-start;font-weight:400;line-height:1.4}.pm-tr .small{font-family:var(--display);font-size:11.5px;line-height:1.45;color:var(--ink-3,#7F929E);margin:10px 0 0}' +
    '.pm-tr .msg{font-family:var(--display);font-size:13px;color:#c0392b;margin:8px 0 0}.pm-tr .msg.ok{color:#2e8b57}.pm-tr .btn{width:100%;cursor:pointer;margin-top:4px}';
  document.head.appendChild(css);
  var opts = '<option>' + T.road + '</option>' + (mar ? '<option>' + T.sea + '</option><option>' + T.any + '</option>' : '');
  var box = document.createElement('div');
  box.className = 'card pm-tr';
  box.innerHTML = '<p class="eyebrow">' + T.ey + '</p><h3>' + T.h + '</h3><p>' + T.p + '</p>' +
    '<button type="button" class="btn btn-ghost" aria-expanded="false" aria-controls="pmTrForm">' + T.open + '</button>' +
    '<form id="pmTrForm" hidden novalidate>' +
    '<label for="tr-dest">' + T.dest + '</label><input type="text" id="tr-dest" name="destino" maxlength="80" required>' +
    '<label for="tr-pais">' + T.country + '</label><select id="tr-pais" name="pais">' + T.countries.map(function (c) { return '<option>' + c + '</option>'; }).join('') + '</select>' +
    '<label for="tr-modo">' + T.how + '</label><select id="tr-modo" name="modo">' + opts + '</select>' +
    '<label for="tr-nombre">' + T.name + '</label><input type="text" id="tr-nombre" name="nombre" autocomplete="name" maxlength="80" required>' +
    '<label for="tr-tel">' + T.tel + '</label><input type="tel" id="tr-tel" name="telefono" autocomplete="tel" inputmode="tel" maxlength="20" required>' +
    '<label for="tr-mail">' + T.mail + '</label><input type="email" id="tr-mail" name="email" autocomplete="email" maxlength="120" required>' +
    '<label class="chk"><input type="checkbox" name="consent"> <span>' + T.consent + '</span></label>' +
    '<button type="submit" class="btn btn-wa">' + T.send + '</button><p class="msg" role="status" aria-live="polite"></p>' +
    '<p class="small">' + T.note + '</p></form>';
  card.parentNode.insertBefore(box, card.nextSibling);
  var tog = box.querySelector('button[aria-controls]'), f = box.querySelector('form'), msg = f.querySelector('.msg');
  tog.addEventListener('click', function () {
    f.hidden = !f.hidden; tog.setAttribute('aria-expanded', String(!f.hidden));
    if (!f.hidden) { f.querySelector('#tr-dest').focus(); try { if (window.pmTrack) window.pmTrack('view_form', {form_id: 'trasladoForm', boat: b.slug}); } catch (e) {} }
  });
  function val(n) { var x = f.querySelector('[name=' + n + ']'); return x.type === 'checkbox' ? x.checked : (x.value || '').trim(); }
  var ES_PAIS = ['España', 'Francia', 'Italia', 'Portugal', 'Otro'], ES_MODO = ['Por carretera', 'Navegando', 'Lo que recomiende Juan'];
  var sent = false, busy = false;
  f.addEventListener('submit', function (ev) {
    ev.preventDefault();
    if (sent || busy) return;
    msg.className = 'msg'; msg.textContent = '';
    function bad(t, n) { msg.textContent = t; var x = n && f.querySelector('[name=' + n + ']'); if (x) x.focus(); }
    var dest = val('destino'); if (!dest) return bad(T.eDest, 'destino');
    var nom = val('nombre'); if (!nom) return bad(T.eName, 'nombre');
    var tel = val('telefono'); if (!/^\+?[0-9 ().-]{6,20}$/.test(tel) || tel.replace(/\D/g, '').length < 6) return bad(T.eTel, 'telefono');
    var em = val('email'); if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)) return bad(T.eMail, 'email');
    if (!val('consent')) return bad(T.eConsent, 'consent');
    if (!window.submitConfirmed) { msg.innerHTML = T.fail; return; }
    var p = {source: 'traslado', nombre: nom, telefono: tel, email: em, lang: lang, page: location.pathname,
      detail: 'Traslado: ' + b.name + ' (' + b.length + ' m) → ' + dest + ', ' + ES_PAIS[lang === 'fr' ? [1, 0, 2, 3, 4][f.querySelector('[name=pais]').selectedIndex] : f.querySelector('[name=pais]').selectedIndex] + ' | ' + ES_MODO[f.querySelector('[name=modo]').selectedIndex],
      consent: true, consent_v: '2026-10', consent_at: new Date().toISOString(), ua: navigator.userAgent.slice(0, 120)};
    var btn = f.querySelector('button[type=submit]'), lbl = btn.textContent;
    btn.disabled = true; btn.textContent = T.sending; busy = true;
    window.submitConfirmed(LEADS_URL, p, 'json', f).then(function () {
      sent = true; busy = false; msg.className = 'msg ok'; msg.textContent = T.ok; btn.textContent = T.okBtn;
      try { if (window.pmTrack) window.pmTrack('generate_lead', {form_id: 'trasladoForm', contact_purpose: 'delivery_quote', boat: b.slug}); } catch (e) {}
    }).catch(function () {
      busy = false; btn.disabled = false; btn.textContent = lbl; msg.innerHTML = T.fail;
      try { if (window.pmTrack) window.pmTrack('contact_form_error', {form_id: 'trasladoForm'}); } catch (e) {}
    });
  });
})();
