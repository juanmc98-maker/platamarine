/* Plata Marine · acciones de la ficha (ES/CA/EN/FR), solo en barcos disponibles:
   0) Contacto también arriba, junto al precio (visita + WhatsApp) y bloque "También te ayudo con"
      tras la descripción, que enlaza solo a servicios que ya existen en la web.
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

  /* 1a) Contacto también arriba, junto al precio: visita y WhatsApp a la vista (el de abajo se mantiene) */
  (function () {
    var ask = document.querySelector('.price-box .btn-ask');
    if (!ask || document.querySelector('.pm-topc')) return;
    var C = {es: ['Solicitar visita', 'o'], ca: ['Sol·licitar visita', 'o'], en: ['Book a viewing', 'or'], fr: ['Demander une visite', 'ou']}[lang];
    var st = document.createElement('style');
    st.textContent = '.pm-topc{margin:2px 0 0;font-family:var(--display);font-size:14px;line-height:1.5}.pm-topc a{color:inherit;text-decoration:underline;text-underline-offset:3px;font-weight:600}.pm-topc .sep{opacity:.7;margin:0 4px}';
    document.head.appendChild(st);
    var p = document.createElement('p');
    p.className = 'pm-topc';
    p.innerHTML = '<a href="' + PRE + '/visita/?barco=' + encodeURIComponent(b.slug) + '" data-wa-context="ficha_visita_arriba">' + C[0] + '</a><span class="sep">' + C[1] + '</span>' +
      '<a href="' + ask.getAttribute('href') + '" target="_blank" rel="noopener" data-wa-context="ficha_wa_arriba">WhatsApp +34 633 742 973</a>';
    var after = ask.parentNode.classList.contains('v2-ctas') ? ask.parentNode : ask;
    after.parentNode.insertBefore(p, after.nextSibling);
  })();

  /* 1c) "También te ayudo con": solo servicios que ya existen en la web */
  (function () {
    var prose = document.querySelector('.prose');
    if (!prose || document.querySelector('.pm-extra')) return;
    var S = {
      es: {h: 'También te ayudo con', o: [
        ['Verlo en persona', 'Eliges día y hora y lo vemos juntos.', PRE + '/visita/?barco=' + encodeURIComponent(b.slug)],
        ['Llevarlo a otro puerto', mar ? 'Te pido presupuesto de traslado por carretera o navegando.' : 'Te pido presupuesto de traslado por carretera.', '#pm-traslado'],
        ['Papeles e impuestos', 'Cambio de titularidad, impuestos de la compra y documentación.', PRE + '/papeles-fiscalidad/'],
        ['Amarre', 'Amarres en traspaso o alquiler de otros clientes.', PRE + '/servicios/amarres.html'],
        ['ITB, gestoría, varadero y seguro', 'Te pongo en contacto con quien lo haría yo.', PRE + '/servicios/']]},
      ca: {h: 'També t’ajudo amb', o: [
        ['Veure’l en persona', 'Tries dia i hora i el veiem junts.', PRE + '/visita/?barco=' + encodeURIComponent(b.slug)],
        ['Portar-lo a un altre port', mar ? 'Et demano pressupost de trasllat per carretera o navegant.' : 'Et demano pressupost de trasllat per carretera.', '#pm-traslado'],
        ['Papers i impostos', 'Canvi de titularitat, impostos de la compra i documentació.', PRE + '/papeles-fiscalidad/'],
        ['Amarratge', 'Amarradors en traspàs o lloguer d’altres clients.', PRE + '/servicios/amarres.html'],
        ['ITB, gestoria, varador i assegurança', 'Et poso en contacte amb qui ho faria jo.', PRE + '/servicios/']]},
      en: {h: 'I can also help you with', o: [
        ['Seeing it in person', 'Pick a day and time and we’ll see it together.', PRE + '/visita/?barco=' + encodeURIComponent(b.slug)],
        ['Moving it to another marina', mar ? 'I get you a delivery quote by road or by sea.' : 'I get you a delivery quote by road.', '#pm-traslado'],
        ['Paperwork and taxes', 'Change of ownership, purchase taxes and documents.', PRE + '/papeles-fiscalidad/'],
        ['A berth', 'Berths for transfer or rent from other clients.', PRE + '/servicios/amarres.html'],
        ['Inspection, paperwork, haul-out and insurance', 'I put you in touch with who I’d use.', PRE + '/servicios/']]},
      fr: {h: 'Je peux aussi vous aider pour', o: [
        ['Le voir sur place', 'Vous choisissez le jour et l’heure et on le voit ensemble.', PRE + '/visita/?barco=' + encodeURIComponent(b.slug)],
        ['L’emmener dans un autre port', mar ? 'Je vous obtiens un devis de transport par la route ou par la mer.' : 'Je vous obtiens un devis de transport par la route.', '#pm-traslado'],
        ['Papiers et fiscalité', 'Changement de propriétaire, taxes d’achat et documents.', PRE + '/papeles-fiscalidad/'],
        ['Une place de port', 'Places à céder ou à louer d’autres clients.', PRE + '/servicios/amarres.html'],
        ['Inspection, formalités, mise à sec et assurance', 'Je vous mets en contact avec ceux à qui je ferais appel.', PRE + '/servicios/']]}
    }[lang];
    if (!S) return;
    var st = document.createElement('style');
    st.textContent = '#pm-traslado{scroll-margin-top:84px}.pm-extra{margin:26px 0 0;padding:18px 18px 8px;border:1px solid var(--plata,#dde3e8);border-radius:var(--radius,10px);background:#fff}.pm-extra h3{margin:0 0 10px;font-size:1.15rem}.pm-extra ul{list-style:none;margin:0;padding:0}.pm-extra li{border-top:1px solid var(--plata,#dde3e8)}.pm-extra li:first-child{border-top:0}.pm-extra a{display:block;padding:10px 0;text-decoration:none;color:var(--ink,#0E3042)}.pm-extra b{display:block;font-family:var(--display);font-size:15px}.pm-extra span{display:block;font-size:14px;color:var(--ink-2,#44545F);line-height:1.4}.pm-extra a:hover b{text-decoration:underline}';
    document.head.appendChild(st);
    var box = document.createElement('div');
    box.className = 'pm-extra';
    box.innerHTML = '<h3>' + S.h + '</h3><ul>' + S.o.map(function (o) { return '<li><a href="' + o[2] + '"><b>' + o[0] + '</b><span>' + o[1] + '</span></a></li>'; }).join('') + '</ul>';
    prose.parentNode.appendChild(box);
    var tr = box.querySelector('a[href="#pm-traslado"]');
    tr.addEventListener('click', function (ev) {
      var t = document.getElementById('pm-traslado');
      if (!t) { tr.parentNode.style.display = 'none'; return; }
      ev.preventDefault();
      var tg = t.querySelector('button[aria-controls]');
      if (tg && tg.getAttribute('aria-expanded') !== 'true') tg.click();
      t.scrollIntoView({behavior: 'smooth', block: 'start'});
    });
  })();

  /* 1b) "¿Qué te falta para decidirte?": un toque, respuesta concreta y recuento anónimo (con consentimiento de analítica) */
  (function () {
    var host = document.querySelector('aside.aside .card');
    if (!host) return;
    var nm = b.name || (document.querySelector('h1') || {}).textContent || b.slug;
    var WA = function (t) { return 'https://wa.me/34633742973?text=' + encodeURIComponent(t); };
    var coste = document.getElementById('coste') ? '#coste' : PRE + '/herramientas/coste-mantener-barco.html';
    var F = {
      es: {h: '¿Qué te falta para decidirte?', s: 'Un toque y te ayudo con eso.', o: [
        ['precio', 'El precio', 'Cuéntame tu presupuesto y te digo si encaja o te busco alternativas.', 'Escribirme', WA('Hola Juan, me interesa el ' + nm + ' pero el precio se me va un poco. ¿Lo hablamos?')],
        ['verlo', 'Verlo en persona', 'Elige día y hora y lo vemos juntos.', 'Solicitar visita', PRE + '/visita/?barco=' + b.slug],
        ['gastos', 'Lo que cuesta mantenerlo', 'Aquí tienes una estimación de lo que cuesta al año.', 'Ver el coste', coste],
        ['titulo', 'Qué título necesito', 'Te explico qué titulación hace falta para cada barco.', 'Ver titulaciones', PRE + '/titulaciones/'],
        ['amarre', 'Dónde amarrarlo', 'Te oriento sobre amarres y precios por zona.', 'Ver amarres', PRE + '/servicios/amarres.html'],
        ['datos', 'Más fotos o datos', 'Pregúntame lo que quieras saber y te contesto.', 'Preguntar por WhatsApp', WA('Hola Juan, quería más información del ' + nm + '.')]]},
      ca: {h: 'Què et falta per decidir-te?', s: 'Un toc i t’hi ajudo.', o: [
        ['precio', 'El preu', 'Explica’m el teu pressupost i et dic si encaixa o et busco alternatives.', 'Escriure’m', WA('Hola Juan, m’interessa el ' + nm + ' però el preu se m’escapa una mica. En parlem?')],
        ['verlo', 'Veure’l en persona', 'Tria dia i hora i el veiem junts.', 'Sol·licitar visita', PRE + '/visita/?barco=' + b.slug],
        ['gastos', 'El que costa mantenir-lo', 'Aquí tens una estimació del que costa l’any.', 'Veure el cost', coste],
        ['titulo', 'Quin títol necessito', 'T’explico quina titulació cal per a cada vaixell.', 'Veure titulacions', PRE + '/titulaciones/'],
        ['amarre', 'On amarrar-lo', 'T’oriento sobre amarratges i preus per zona.', 'Veure amarratges', PRE + '/servicios/amarres.html'],
        ['datos', 'Més fotos o dades', 'Pregunta’m el que vulguis i et responc.', 'Preguntar per WhatsApp', WA('Hola Juan, voldria més informació del ' + nm + '.')]]},
      en: {h: 'What’s holding you back?', s: 'One tap and I’ll help you with it.', o: [
        ['precio', 'The price', 'Tell me your budget and I’ll tell you if it fits or find you alternatives.', 'Message me', WA('Hi Juan, I like the ' + nm + ' but the price is a bit above my budget. Can we talk?')],
        ['verlo', 'Seeing it in person', 'Pick a day and time and we’ll see it together.', 'Book a viewing', PRE + '/visita/?barco=' + b.slug],
        ['gastos', 'Running costs', 'Here is an estimate of what it costs per year.', 'See the costs', coste],
        ['titulo', 'Which licence I need', 'I explain which licence each boat requires in Spain.', 'See licences', PRE + '/titulaciones/'],
        ['amarre', 'Where to moor it', 'I can point you to berths and prices by area.', 'See berths', PRE + '/servicios/amarres.html'],
        ['datos', 'More photos or details', 'Ask me anything you want to know and I’ll reply.', 'Ask on WhatsApp', WA('Hi Juan, I’d like more information about the ' + nm + '.')]]},
      fr: {h: 'Qu’est-ce qui vous fait hésiter ?', s: 'Un clic et je vous aide.', o: [
        ['precio', 'Le prix', 'Dites-moi votre budget : je vous dis s’il convient ou je vous cherche des alternatives.', 'M’écrire', WA('Bonjour Juan, le ' + nm + ' m’intéresse mais le prix dépasse un peu mon budget. On en parle ?')],
        ['verlo', 'Le voir sur place', 'Choisissez un jour et une heure et on le voit ensemble.', 'Demander une visite', PRE + '/visita/?barco=' + b.slug],
        ['gastos', 'Ce qu’il coûte à l’entretien', 'Voici une estimation de son coût annuel.', 'Voir le coût', coste],
        ['titulo', 'Le permis nécessaire', 'Je vous explique quel permis il faut en Espagne pour chaque bateau.', 'Voir les permis', PRE + '/titulaciones/'],
        ['amarre', 'Où l’amarrer', 'Je vous oriente sur les places de port et leurs prix par zone.', 'Voir les places', PRE + '/servicios/amarres.html'],
        ['datos', 'Plus de photos ou d’infos', 'Posez-moi vos questions, je vous réponds.', 'Demander sur WhatsApp', WA('Bonjour Juan, je voudrais plus d’informations sur le ' + nm + '.')]]}
    }[lang];
    if (!F) return;
    var st = document.createElement('style');
    st.textContent = '.pm-ft{margin:16px 0 0}.pm-ft h3{margin:.2em 0 .3em}.pm-ft .ops{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0}.pm-ft .ops button{font:600 13px var(--display);padding:7px 11px;border-radius:999px;border:1px solid var(--plata-2,#c9d3da);background:#fff;color:var(--ink,#0E3042);cursor:pointer}.pm-ft .ops button[aria-pressed=true]{background:var(--ink,#0E3042);color:#fff;border-color:var(--ink,#0E3042)}.pm-ft .r{margin:12px 0 0;font-size:15px}.pm-ft .r a{display:inline-block;margin-top:8px}';
    document.head.appendChild(st);
    var box = document.createElement('div');
    box.className = 'card pm-ft';
    box.innerHTML = '<h3>' + F.h + '</h3><p>' + F.s + '</p><div class="ops">' + F.o.map(function (o) { return '<button type="button" aria-pressed="false" data-k="' + o[0] + '">' + o[1] + '</button>'; }).join('') + '</div><div class="r" aria-live="polite"></div>';
    host.parentNode.insertBefore(box, host.nextSibling);
    var r = box.querySelector('.r');
    box.querySelectorAll('.ops button').forEach(function (bt) {
      bt.addEventListener('click', function () {
        var o = F.o.filter(function (x) { return x[0] === bt.dataset.k; })[0];
        box.querySelectorAll('.ops button').forEach(function (x) { x.setAttribute('aria-pressed', String(x === bt)); });
        var ext = o[4].indexOf('http') === 0;
        r.innerHTML = o[2] + '<br><a class="btn ' + (ext ? 'btn-wa' : 'btn-ghost') + '" href="' + o[4] + '"' + (ext ? ' target="_blank" rel="noopener"' : '') + '>' + o[3] + '</a>';
        try { if (window.pmCount) window.pmCount({t: 'falta', m: o[0], b: b.slug}); } catch (e) {}
        try { if (window.gtag) window.gtag('event', 'que_falta', {reason: o[0], boat: b.slug}); } catch (e) {}
      });
    });
  })();
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
  box.id = 'pm-traslado';
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
