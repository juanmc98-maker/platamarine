/* Plata Marine · solicitar visita (ES/CA/EN/FR).
   Lee los huecos libres de la agenda (Apps Script + hoja "agenda de visitas") y envía la solicitud.
   La visita queda "Pendiente" hasta que Juan la cuadra con el propietario y la confirma por WhatsApp.
   Solo se da por enviada si el servidor responde ok:true (submit-confirmed.js). */
(function () {
  'use strict';
  var API = 'https://script.google.com/macros/s/AKfycbzHhz2H3yl_4d9XuHPr_n4BTzgj7_HJ6EDbNMR4C2j1j8xnkAU9wYqMW5tyMANmc3fb/exec';
  var f = document.getElementById('visitaForm');
  if (!f) return;
  var path = location.pathname;
  var LANG = path.indexOf('/ca/') === 0 ? 'ca' : path.indexOf('/en/') === 0 ? 'en' : path.indexOf('/fr/') === 0 ? 'fr' : 'es';
  var PRE = LANG === 'es' ? '' : '/' + LANG;
  var T = {
    es: {pop: {title: 'Solicitud recibida', meanwhile: 'Mientras te lo confirmo', guide: 'Qué revisar el día de la visita', guideSub: 'La lista que uso yo cuando enseño un barco', similar: 'Otros barcos que te pueden gustar', alert: 'Avísame si entra uno parecido', alertSub: 'Te escribo solo si encaja con lo que buscas', close: 'Cerrar', vat: '+IVA'}, wd: ['L', 'M', 'X', 'J', 'V', 'S', 'D'], loading: 'Cargando los días disponibles…', loadFail: 'Ahora mismo no puedo mostrar el calendario. Escríbeme por WhatsApp y lo cuadramos.',
      pickDay: 'Elige primero un día.', noHours: 'Ese día ya no quedan horas libres.', request: 'Este día es bajo solicitud: dime qué franja te va mejor y te propongo una hora.',
      franja: 'Franja que te va mejor', fr: ['Por la mañana', 'A mediodía', 'Por la tarde'], any: 'Todavía no lo sé / quiero ver varios', choose: 'Elige un barco',
      chosen: 'Has elegido', change: 'cambiar', prev: 'Mes anterior', next: 'Mes siguiente', legendReq: 'bajo solicitud',
      errBoat: 'Elige el barco que quieres ver.', errDay: 'Elige el día de la visita.', errHour: 'Elige una hora.', errName: 'Necesito tu nombre para poder organizar la visita.',
      errTel: 'Revisa el teléfono: puedes escribirlo con prefijo internacional, por ejemplo +34 600 000 000.', errMail: 'Revisa el correo, no parece correcto.', errConsent: 'Necesito que aceptes la política de privacidad para poder gestionar la visita.',
      sending: 'Enviando…', ok: 'Solicitud recibida. La visita queda pendiente hasta que la cuadre con el propietario; te escribo por WhatsApp para confirmarte día, hora y punto de encuentro.', okBtn: 'Solicitud enviada ✓',
      taken: 'Esa hora se acaba de ocupar. Elige otra, por favor.', fail: 'No he podido confirmar que tu solicitud ha llegado. Tus datos siguen aquí: vuelve a intentarlo en unos minutos o escríbeme por <a href="https://wa.me/34633742973" target="_blank" rel="noopener">WhatsApp</a>.',
      summary: function (d, h) { return 'Visita: ' + d + (h ? ' a las ' + h : '') + '.'; }},
    ca: {pop: {title: 'Sol·licitud rebuda', meanwhile: 'Mentre t’ho confirmo', guide: 'Què revisar el dia de la visita', guideSub: 'La llista que faig servir quan ensenyo un vaixell', similar: 'Altres vaixells que et poden agradar', alert: 'Avisa’m si n’entra un de semblant', alertSub: 'T’escric només si encaixa amb el que busques', close: 'Tancar', vat: '+IVA'}, wd: ['Dl', 'Dt', 'Dc', 'Dj', 'Dv', 'Ds', 'Dg'], loading: 'Carregant els dies disponibles…', loadFail: "Ara mateix no puc mostrar el calendari. Escriu-me per WhatsApp i ho quadrem.",
      pickDay: 'Tria primer un dia.', noHours: "Aquest dia ja no queden hores lliures.", request: "Aquest dia és sota petició: digues-me quina franja et va millor i et proposo una hora.",
      franja: 'Franja que et va millor', fr: ['Al matí', 'Al migdia', 'A la tarda'], any: 'Encara no ho sé / vull veure’n diversos', choose: 'Tria un vaixell',
      chosen: 'Has triat', change: 'canviar', prev: 'Mes anterior', next: 'Mes següent', legendReq: 'sota petició',
      errBoat: 'Tria el vaixell que vols veure.', errDay: 'Tria el dia de la visita.', errHour: 'Tria una hora.', errName: 'Necessito el teu nom per poder organitzar la visita.',
      errTel: 'Revisa el telèfon: el pots escriure amb prefix internacional, per exemple +34 600 000 000.', errMail: 'Revisa el correu, no sembla correcte.', errConsent: 'Necessito que acceptis la política de privacitat per poder gestionar la visita.',
      sending: 'Enviant…', ok: "Sol·licitud rebuda. La visita queda pendent fins que la quadri amb el propietari; t’escric per WhatsApp per confirmar-te dia, hora i punt de trobada.", okBtn: 'Sol·licitud enviada ✓',
      taken: "Aquesta hora s’acaba d’ocupar. Tria’n una altra, si us plau.", fail: 'No he pogut confirmar que la sol·licitud ha arribat. Les teves dades segueixen aquí: torna-ho a provar d’aquí a uns minuts o escriu-me per <a href="https://wa.me/34633742973" target="_blank" rel="noopener">WhatsApp</a>.',
      summary: function (d, h) { return 'Visita: ' + d + (h ? ' a les ' + h : '') + '.'; }},
    en: {pop: {title: 'Request received', meanwhile: 'While I confirm it', guide: 'What to check on viewing day', guideSub: 'The checklist I use when I show a boat', similar: 'Other boats you may like', alert: 'Let me know if a similar one comes in', alertSub: 'I only write if it matches what you are looking for', close: 'Close', vat: '+VAT'}, wd: ['M', 'T', 'W', 'T', 'F', 'S', 'S'], loading: 'Loading available days…', loadFail: "I can't show the calendar right now. Message me on WhatsApp and we'll arrange it.",
      pickDay: 'Choose a day first.', noHours: 'There are no free times left that day.', request: "This day is on request: tell me which part of the day suits you and I'll suggest a time.",
      franja: 'Time of day that suits you', fr: ['Morning', 'Around midday', 'Afternoon'], any: "I don't know yet / I'd like to see several", choose: 'Choose a boat',
      chosen: "You've chosen", change: 'change', prev: 'Previous month', next: 'Next month', legendReq: 'on request',
      errBoat: 'Choose the boat you want to see.', errDay: 'Choose the day of the viewing.', errHour: 'Choose a time.', errName: 'I need your name to arrange the viewing.',
      errTel: 'Please check the phone number: you can include the international prefix, e.g. +34 600 000 000.', errMail: "Please check the email, it doesn't look right.", errConsent: 'Please accept the privacy policy so I can arrange the viewing.',
      sending: 'Sending…', ok: "Request received. The viewing stays pending until I've arranged it with the owner; I'll message you on WhatsApp to confirm the day, time and meeting point.", okBtn: 'Request sent ✓',
      taken: 'That time has just been taken. Please choose another one.', fail: "I couldn't confirm that your request arrived. Your details are still here: try again in a few minutes or message me on <a href=\"https://wa.me/34633742973\" target=\"_blank\" rel=\"noopener\">WhatsApp</a>.",
      summary: function (d, h) { return 'Viewing: ' + d + (h ? ' at ' + h : '') + '.'; }},
    fr: {pop: {title: 'Demande reçue', meanwhile: 'En attendant ma confirmation', guide: 'Que vérifier le jour de la visite', guideSub: 'La liste que j’utilise quand je montre un bateau', similar: 'D’autres bateaux qui pourraient vous plaire', alert: 'Prévenez-moi si un bateau similaire arrive', alertSub: 'Je n’écris que si cela correspond à votre recherche', close: 'Fermer', vat: '+TVA'}, wd: ['L', 'M', 'M', 'J', 'V', 'S', 'D'], loading: 'Chargement des jours disponibles…', loadFail: "Je ne peux pas afficher le calendrier pour le moment. Écrivez-moi sur WhatsApp et nous l’organiserons.",
      pickDay: 'Choisissez d’abord un jour.', noHours: 'Il n’y a plus de créneau libre ce jour-là.', request: 'Ce jour est sur demande : dites-moi quel moment vous convient et je vous proposerai une heure.',
      franja: 'Moment qui vous convient', fr: ['Le matin', 'Vers midi', 'L’après-midi'], any: 'Je ne sais pas encore / je veux en voir plusieurs', choose: 'Choisissez un bateau',
      chosen: 'Vous avez choisi', change: 'modifier', prev: 'Mois précédent', next: 'Mois suivant', legendReq: 'sur demande',
      errBoat: 'Choisissez le bateau que vous voulez voir.', errDay: 'Choisissez le jour de la visite.', errHour: 'Choisissez une heure.', errName: 'J’ai besoin de votre nom pour organiser la visite.',
      errTel: 'Vérifiez le téléphone : vous pouvez l’écrire avec l’indicatif international, par exemple +33 6 00 00 00 00.', errMail: 'Vérifiez l’e-mail, il ne semble pas correct.', errConsent: 'Merci d’accepter la politique de confidentialité pour que je puisse organiser la visite.',
      sending: 'Envoi…', ok: 'Demande reçue. La visite reste en attente jusqu’à ce que je l’organise avec le propriétaire ; je vous écrirai sur WhatsApp pour confirmer le jour, l’heure et le point de rendez-vous.', okBtn: 'Demande envoyée ✓',
      taken: 'Ce créneau vient d’être pris. Choisissez-en un autre, s’il vous plaît.', fail: 'Je n’ai pas pu confirmer que votre demande est arrivée. Vos données sont toujours là : réessayez dans quelques minutes ou écrivez-moi sur <a href="https://wa.me/34633742973" target="_blank" rel="noopener">WhatsApp</a>.',
      summary: function (d, h) { return 'Visite : ' + d + (h ? ' à ' + h : '') + '.'; }}
  }[LANG];

  var $ = function (s) { return f.querySelector(s); };
  var boatBox = $('#v-barco-box'), cal = $('#v-cal'), hoursBox = $('#v-horas'), msg = $('.msg'), sum = $('#v-resumen');
  var state = {dias: {}, mes: null, fecha: '', hora: '', modo: '', barco: null, sent: false, busy: false};

  /* ---------- barco ---------- */
  var INV = window.PM_INV, boats = INV && INV.boats ? INV.boats.filter(function (b) { return b.status === 'available'; }) : [];
  boats.sort(function (a, b) { return (b.price || 0) - (a.price || 0); });
  function boatBySlug(s) { for (var i = 0; i < boats.length; i++) if (boats[i].slug === s) return boats[i]; return null; }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]; }); }
  function renderBoat(fixed) {
    if (fixed) {
      var d = fixed.d && fixed.d[LANG] ? ' · ' + fixed.d[LANG] : '';
      boatBox.innerHTML = '<p class="v-boat">' + T.chosen + ': <a href="' + PRE + '/barcos/' + fixed.slug + '.html"><strong>' + esc(fixed.name) + '</strong></a>' + esc(d) +
        ' <button type="button" class="v-link" id="v-cambiar">(' + T.change + ')</button></p>';
      $('#v-cambiar').addEventListener('click', function () { state.barco = null; renderBoat(null); });
      state.barco = fixed;
      return;
    }
    var o = '<label class="l" for="v-barco">' + boatBox.getAttribute('data-label') + ' *</label><select id="v-barco" name="barco"><option value="">' + T.choose + '</option>';
    boats.forEach(function (b) { o += '<option value="' + b.slug + '">' + esc(b.name) + (b.year ? ' (' + b.year + ')' : '') + '</option>'; });
    o += '<option value="*">' + T.any + '</option></select>';
    boatBox.innerHTML = o;
    $('#v-barco').addEventListener('change', function (e) { var v = e.target.value; state.barco = v === '*' ? {slug: '', name: T.any} : boatBySlug(v); });
  }
  var q = new URLSearchParams(location.search).get('barco');
  renderBoat(q ? boatBySlug(q) : null);

  /* ---------- calendario ---------- */
  function ymd(y, m, d) { return y + '-' + ('0' + (m + 1)).slice(-2) + '-' + ('0' + d).slice(-2); }
  function fmtLong(s) {
    var p = s.split('-'), dt = new Date(+p[0], p[1] - 1, +p[2], 12);
    try { return dt.toLocaleDateString(LANG, {weekday: 'long', day: 'numeric', month: 'long'}); } catch (e) { return s; }
  }
  function monthTitle(y, m) {
    try { var t = new Date(y, m, 1, 12).toLocaleDateString(LANG, {month: 'long', year: 'numeric'}); return t.charAt(0).toUpperCase() + t.slice(1); } catch (e) { return (m + 1) + '/' + y; }
  }
  function renderCal() {
    var y = state.mes[0], m = state.mes[1];
    var first = new Date(y, m, 1, 12), lead = (first.getDay() + 6) % 7, days = new Date(y, m + 1, 0).getDate();
    var keys = Object.keys(state.dias).sort(), minK = keys[0], maxK = keys[keys.length - 1];
    var h = '<div class="v-cal-head"><button type="button" class="v-nav" data-d="-1" aria-label="' + T.prev + '">‹</button><strong>' + monthTitle(y, m) +
      '</strong><button type="button" class="v-nav" data-d="1" aria-label="' + T.next + '">›</button></div><div class="v-grid" role="grid">';
    T.wd.forEach(function (w) { h += '<span class="v-wd">' + w + '</span>'; });
    for (var i = 0; i < lead; i++) h += '<span></span>';
    for (var d = 1; d <= days; d++) {
      var k = ymd(y, m, d), info = state.dias[k], on = info && info.modo !== 'cerrado';
      var cls = 'v-day' + (on ? '' : ' off') + (info && info.modo === 'solicitud' ? ' req' : '') + (state.fecha === k ? ' sel' : '');
      h += '<button type="button" class="' + cls + '" data-k="' + k + '"' + (on ? '' : ' disabled') + ' aria-pressed="' + (state.fecha === k) + '" aria-label="' + fmtLong(k) + '">' + d + '</button>';
    }
    h += '</div><p class="v-legend"><span class="v-dot"></span> ' + T.legendReq + '</p>';
    cal.innerHTML = h;
    var prevOk = ymd(y, m, 1) > minK, nextOk = ymd(y, m, days) < maxK;
    cal.querySelector('[data-d="-1"]').disabled = !prevOk;
    cal.querySelector('[data-d="1"]').disabled = !nextOk;
  }
  cal.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b || b.disabled) return;
    if (b.hasAttribute('data-d')) {
      var m = state.mes[1] + Number(b.getAttribute('data-d')), y = state.mes[0];
      if (m < 0) { m = 11; y--; } if (m > 11) { m = 0; y++; }
      state.mes = [y, m]; renderCal(); return;
    }
    state.fecha = b.getAttribute('data-k'); state.hora = ''; renderCal(); renderHours();
  });
  function renderHours() {
    var info = state.dias[state.fecha];
    state.modo = info ? info.modo : '';
    if (!info) { hoursBox.innerHTML = '<p class="v-hint">' + T.pickDay + '</p>'; updateSum(); return; }
    if (info.modo === 'solicitud') {
      var o = '<p class="v-hint">' + T.request + '</p><label class="l" for="v-franja">' + T.franja + '</label><select id="v-franja" name="franja">';
      T.fr.forEach(function (x) { o += '<option>' + x + '</option>'; });
      hoursBox.innerHTML = o + '</select>';
      updateSum(); return;
    }
    if (!info.horas.length) { hoursBox.innerHTML = '<p class="v-hint">' + T.noHours + '</p>'; updateSum(); return; }
    var h = '<div class="v-hours">';
    info.horas.forEach(function (x) { h += '<button type="button" class="v-hour' + (state.hora === x ? ' sel' : '') + '" data-h="' + x + '" aria-pressed="' + (state.hora === x) + '">' + x + '</button>'; });
    hoursBox.innerHTML = h + '</div>';
    updateSum();
  }
  hoursBox.addEventListener('click', function (e) {
    var b = e.target.closest('[data-h]'); if (!b) return;
    state.hora = b.getAttribute('data-h'); renderHours();
  });
  function updateSum() {
    if (!state.fecha) { sum.hidden = true; return; }
    sum.hidden = false;
    sum.textContent = T.summary(fmtLong(state.fecha), state.modo === 'horas' ? state.hora : '');
  }
  function getHuecos(intento) {
    var ctrl = new AbortController(), timer = setTimeout(function () { ctrl.abort(); }, 25000);
    return fetch(API + '?accion=huecos', {credentials: 'omit', signal: ctrl.signal}).then(function (r) { return r.json(); }).then(function (j) {
      clearTimeout(timer);
      if (!j || !j.ok || !j.dias || !j.dias.length) throw new Error('vacío');
      return j;
    }).catch(function (e) {
      clearTimeout(timer);
      // el servidor de Google a veces falla en el primer intento: se reintenta dos veces
      if (intento < 2) return new Promise(function (r) { setTimeout(r, 1500); }).then(function () { return getHuecos(intento + 1); });
      throw e;
    });
  }
  function load(keepDay) {
    cal.innerHTML = '<p class="v-hint">' + T.loading + '</p>';
    var timer = 0;
    return getHuecos(0).then(function (j) {
      if (!j || !j.ok || !j.dias || !j.dias.length) throw new Error('vacío');
      state.dias = {};
      j.dias.forEach(function (d) { state.dias[d.fecha] = d; });
      if (!keepDay || !state.dias[state.fecha] || state.dias[state.fecha].modo === 'cerrado') { state.fecha = ''; state.hora = ''; }
      var firstOpen = j.dias.filter(function (d) { return d.modo !== 'cerrado'; })[0] || j.dias[0];
      var p = (state.fecha || firstOpen.fecha).split('-');
      state.mes = [+p[0], p[1] - 1];
      renderCal(); renderHours();
    }).catch(function () {
      clearTimeout(timer);
      cal.innerHTML = '<p class="v-hint">' + T.loadFail + '</p>';
      hoursBox.innerHTML = '';
    });
  }
  load(false);

  /* ---------- ventana tras enviar ---------- */
  function money(n) { try { return n.toLocaleString(LANG === 'en' ? 'en-GB' : LANG, {maximumFractionDigits: 0}) + ' €'; } catch (e) { return n + ' €'; } }
  function similares(b) {
    var ref = b && b.price ? b.price : 0;
    return boats.filter(function (x) { return !b || (x.slug !== b.slug && (!b.kind || x.kind === b.kind)); })
      .sort(function (x, y) { return Math.abs((x.price || 0) - ref) - Math.abs((y.price || 0) - ref); })
      .slice(0, 3);
  }
  function popup(b) {
    var P = T.pop, last = document.activeElement;
    if (!document.getElementById('pm-pop-css')) {
      var st = document.createElement('style'); st.id = 'pm-pop-css';
      st.textContent = '.pm-pop{position:fixed;inset:0;z-index:9999;background:rgba(13,28,39,.55);display:flex;align-items:center;justify-content:center;padding:16px;animation:pmf .2s ease}' +
        '.pm-pop .bx{background:#fff;border-radius:12px;max-width:520px;width:100%;max-height:calc(100vh - 32px);overflow:auto;box-shadow:0 20px 60px rgba(0,0,0,.3);animation:pmu .25s ease}' +
        '.pm-pop .hd{position:relative}.pm-pop .hd img{display:block;width:100%;height:170px;object-fit:cover;border-radius:12px 12px 0 0}' +
        '.pm-pop .ok{display:flex;gap:12px;align-items:flex-start;padding:18px 20px 6px}.pm-pop .ok i{flex:0 0 34px;height:34px;border-radius:50%;background:#0B766B;color:#fff;font:700 18px/34px Arial;text-align:center;font-style:normal}' +
        '.pm-pop h2{margin:0 0 4px;font:700 19px/1.25 var(--display,Arial);color:var(--ink,#0E3042)}.pm-pop p{margin:0;font:14px/1.5 var(--display,Arial);color:var(--ink-2,#4A5D69)}' +
        '.pm-pop .sec{padding:12px 20px 0}.pm-pop .lab{font:700 11px var(--display,Arial);letter-spacing:.1em;text-transform:uppercase;color:var(--brass,#B58A2C);margin:8px 0 8px}' +
        '.pm-pop a.row{display:flex;gap:12px;align-items:center;padding:10px 12px;border:1px solid var(--plata-2,#D5DDE2);border-radius:8px;text-decoration:none;color:var(--ink,#0E3042);margin:0 0 8px;font:600 14px var(--display,Arial)}.pm-pop a.row small{display:block;font-weight:400;color:var(--ink-2,#4A5D69)}.pm-pop a.row:hover{border-color:var(--ink,#0E3042)}' +
        '.pm-pop .cards{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.pm-pop .cards a{text-decoration:none;color:var(--ink,#0E3042);font:600 12.5px/1.3 var(--display,Arial)}.pm-pop .cards img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:6px;margin:0 0 4px}.pm-pop .cards span{display:block;font-weight:400;color:var(--ink-2,#4A5D69)}.pm-pop .cards b.v{color:#c0392b;font-weight:700}' +
        '.pm-pop .ft{padding:14px 20px 18px;text-align:right}.pm-pop .x{position:absolute;top:10px;right:10px;width:36px;height:36px;border-radius:50%;border:0;background:rgba(255,255,255,.92);font-size:20px;cursor:pointer;color:#0E3042}' +
        '.pm-pop .btnc{border:1px solid var(--ink,#0E3042);background:#fff;color:var(--ink,#0E3042);border-radius:6px;padding:9px 16px;font:600 14px var(--display,Arial);cursor:pointer}' +
        '@keyframes pmf{from{opacity:0}}@keyframes pmu{from{transform:translateY(16px);opacity:0}}@media (prefers-reduced-motion:reduce){.pm-pop,.pm-pop .bx{animation:none}}@media (max-width:480px){.pm-pop .cards{grid-template-columns:repeat(2,1fr)}.pm-pop .cards a:nth-child(3){display:none}}';
      document.head.appendChild(st);
    }
    var img = b && b.slug ? '<img src="/' + b.slug + '-1-m.jpg" alt="' + esc(b.name) + '">' : '';
    var cards = similares(b && b.slug ? b : null).map(function (x) {
      return '<a href="' + PRE + '/barcos/' + x.slug + '.html"><img src="/' + x.slug + '-1-t.jpg" alt="" loading="lazy">' + esc(x.name) +
        '<span>' + (x.price ? money(x.price) + (x.vat ? ' <b class="v">' + P.vat + '</b>' : '') : '') + '</span></a>';
    }).join('');
    var w = document.createElement('div');
    w.className = 'pm-pop'; w.setAttribute('role', 'dialog'); w.setAttribute('aria-modal', 'true'); w.setAttribute('aria-labelledby', 'pmPopT');
    w.innerHTML = '<div class="bx"><div class="hd">' + img + '<button type="button" class="x" aria-label="' + P.close + '">×</button></div>' +
      '<div class="ok"><i aria-hidden="true">✓</i><div><h2 id="pmPopT">' + P.title + '</h2><p>' + T.ok.replace(/^[^.]+\.\s*/, '') + '</p></div></div>' +
      '<div class="sec"><p class="lab">' + P.meanwhile + '</p>' +
      '<a class="row" href="' + PRE + '/guias/que-mirar-comprar-barco-segunda-mano.html"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0E3042" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4h6v3H9zM9 12l2 2 4-4M9 17h6"/></svg><span>' + P.guide + '<small>' + P.guideSub + '</small></span></a>' +
      '<a class="row" href="' + PRE + '/alertas/"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0E3042" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15z"/><path d="M10 20a2 2 0 0 0 4 0"/></svg><span>' + P.alert + '<small>' + P.alertSub + '</small></span></a></div>' +
      (cards ? '<div class="sec"><p class="lab">' + P.similar + '</p><div class="cards">' + cards + '</div></div>' : '') +
      '<div class="ft"><button type="button" class="btnc">' + P.close + '</button></div></div>';
    document.body.appendChild(w);
    function cerrar() { w.remove(); document.removeEventListener('keydown', onKey); if (last && last.focus) last.focus(); }
    function onKey(e) { if (e.key === 'Escape') cerrar(); }
    w.addEventListener('click', function (e) { if (e.target === w || e.target.closest('.x,.btnc')) cerrar(); });
    w.addEventListener('click', function (e) { var a = e.target.closest('a'); if (a) { try { if (window.pmTrack) window.pmTrack('select_content', {form_id: 'visitaForm', label: a.getAttribute('href')}); } catch (x) {} } });
    document.addEventListener('keydown', onKey);
    w.querySelector('.x').focus();
  }

  /* ---------- envío ---------- */
  function val(n) { var x = f.querySelector('[name=' + n + ']'); if (!x) return ''; return x.type === 'checkbox' ? x.checked : (x.value || '').trim(); }
  function bad(t, n) {
    msg.className = 'msg'; msg.textContent = t;
    var x = n && f.querySelector('[name=' + n + ']'); if (x) { x.setAttribute('aria-invalid', 'true'); x.focus(); }
  }
  f.addEventListener('submit', function (ev) {
    ev.preventDefault();
    if (state.sent || state.busy) return;
    msg.className = 'msg'; msg.textContent = '';
    [].forEach.call(f.querySelectorAll('[aria-invalid]'), function (x) { x.removeAttribute('aria-invalid'); });
    if (!state.barco) { bad(T.errBoat, 'barco'); if (!f.querySelector('[name=barco]')) msg.textContent = T.errBoat; return; }
    if (!state.fecha) { bad(T.errDay); cal.scrollIntoView({block: 'center'}); return; }
    if (state.modo === 'horas' && !state.hora) { bad(T.errHour); hoursBox.scrollIntoView({block: 'center'}); return; }
    var nom = val('nombre'); if (!nom) { bad(T.errName, 'nombre'); return; }
    var tel = val('telefono'); if (!/^\+?[0-9 ().-]{6,20}$/.test(tel) || tel.replace(/\D/g, '').length < 6) { bad(T.errTel, 'telefono'); return; }
    var em = val('email'); if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)) { bad(T.errMail, 'email'); return; }
    if (!val('consent')) { bad(T.errConsent, 'consent'); return; }
    if (!window.submitConfirmed || API.indexOf('PENDIENTE') > 0) { msg.innerHTML = T.fail; return; }
    var p = {
      source: 'visita', barco: state.barco.name, barco_slug: state.barco.slug || '', fecha: state.fecha,
      hora: state.modo === 'horas' ? state.hora : '', franja: state.modo === 'solicitud' ? val('franja') : '',
      nombre: nom, telefono: tel, email: em, titulacion: val('titulacion'), notas: val('notas'),
      newsletter: !!val('newsletter'), consent: true, consent_v: '2026-10', consent_at: new Date().toISOString(),
      lang: LANG, page: path, ua: navigator.userAgent.slice(0, 120)
    };
    var btn = f.querySelector('button[type=submit]'), lbl = btn.textContent;
    btn.disabled = true; btn.textContent = T.sending; state.busy = true;
    var slug = state.barco.slug || '';
    window.submitConfirmed(API, p, 'json', f).then(function () {
      state.sent = true; state.busy = false;
      msg.className = 'msg ok'; msg.textContent = T.ok; btn.textContent = T.okBtn;
      try { popup(state.barco); } catch (e) {}
      try { if (window.pmTrack) window.pmTrack('generate_lead', {form_id: 'visitaForm', contact_purpose: 'visit', boat: slug}); } catch (e) {}
    }).catch(function (e) {
      state.busy = false; btn.disabled = false; btn.textContent = lbl;
      if (e && e.reason === 'ocupado') {
        msg.className = 'msg'; msg.textContent = T.taken;
        load(true);
      } else {
        msg.className = 'msg'; msg.innerHTML = T.fail;
      }
      try { if (window.pmTrack) window.pmTrack('contact_form_error', {form_id: 'visitaForm'}); } catch (x) {}
    });
  });
})();
