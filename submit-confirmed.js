/* Plata Marine · envío de formularios con confirmación explícita del servidor.
   Regla (6 oct 2026): una consulta solo se da por recibida si el servidor responde ok:true.
   Antispam:
   - Campo trampa invisible en cada formulario. Si está relleno EN EL FORMULARIO QUE SE ENVÍA,
     no se envía nada y la promesa se RECHAZA (code 'blocked'): el formulario muestra su aviso de
     "no he podido confirmar" con WhatsApp/email como alternativa. Nunca se simula un éxito.
   - Envío muy rápido (<3 s desde que cargó la página, p. ej. con autocompletado): ya no se bloquea;
     se espera a completar los 3 s y se envía marcado revisar=1 para revisarlo a mano.
   - Texto que parece aleatorio: se envía marcado revisar=1.
   Robustez: doble clic o reintento mientras hay un envío en curso → no se repite la petición ni la medición;
   cada consulta lleva un identificador (_sid) que se mantiene en los reintentos del mismo contenido,
   para poder detectar duplicados en la hoja si una respuesta se perdió por la red. Sin reintentos automáticos. */
(function () {
  var T0 = Date.now();
  window.__pmT0 = T0;
  function addHp() {
    document.querySelectorAll('form').forEach(function (f) {
      if (f.querySelector('input[name=pm_hp_x]')) return;
      var w = document.createElement('div');
      w.setAttribute('aria-hidden', 'true');
      w.style.cssText = 'position:absolute!important;left:-9999px!important;width:1px;height:1px;overflow:hidden';
      w.innerHTML = '<label>No rellenar<input type="text" name="pm_hp_x" tabindex="-1" autocomplete="off"></label>';
      f.appendChild(w);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', addHp); else addHp();
  window.addEventListener('load', addHp);
  /* Formulario que se está enviando: se anota en fase de captura, antes que el código de cada página. */
  window.__pmLastForm = null;
  document.addEventListener('submit', function (e) { window.__pmLastForm = e.target; }, true);
  function hpFilled(form) {
    var scope = form && form.querySelectorAll ? form : null;
    if (!scope) return false; // sin formulario identificable no se bloquea: se envía y decide el servidor
    return Array.prototype.some.call(scope.querySelectorAll('input[name=pm_hp_x]'), function (i) { return i.value.trim() !== ''; });
  }
  window.__pmSpam = function (form) { return hpFilled(form === undefined ? window.__pmLastForm : form); };
  window.__pmFast = function () { return (Date.now() - T0) < 3000; };
  window.__pmRaro = function (t) {
    t = String(t || '').trim();
    if (t.length < 10 || /\s/.test(t)) return false;
    var up = (t.match(/[A-Z]/g) || []).length, lo = (t.match(/[a-z]/g) || []).length, vw = (t.match(/[aeiouáéíóú]/gi) || []).length;
    return up >= 3 && lo >= 3 && vw / t.length < 0.25;
  };
})();
window.__pmInflight = window.__pmInflight || {};
window.__pmSids = window.__pmSids || {};
window.submitConfirmed = function (url, body, encoding, form) {
  function err(code) { var e = new Error(code); e.code = code; return e; }
  var f = form || window.__pmLastForm;
  if (window.__pmSpam && window.__pmSpam(f)) {
    try { if (window.pmTrack) window.pmTrack('form_blocked_local', {label: 'hp'}); } catch (x) {}
    return Promise.reject(err('blocked'));
  }
  var key = url;
  if (body && typeof body === 'object') {
    var k = {};
    Object.keys(body).sort().forEach(function (n) { if (n !== 'consent_at' && n !== 'ua' && n !== '_t') k[n] = body[n]; });
    key += '|' + JSON.stringify(k);
  } else key += '|' + String(body);
  // Doble clic / doble envío: el primer envío gestiona la respuesta; los duplicados no hacen nada.
  if (window.__pmInflight[key]) return new Promise(function () {});
  if (!window.__pmSids[key]) window.__pmSids[key] = Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
  var sid = window.__pmSids[key];
  var fast = window.__pmFast && window.__pmFast();
  var p = (async function () {
    if (fast) await new Promise(function (r) { setTimeout(r, Math.max(0, 3000 - (Date.now() - window.__pmT0))); });
    var controller = new AbortController();
    var timer = setTimeout(function () { controller.abort(); }, 45000);
    try {
      var options = {method: 'POST', credentials: 'omit', signal: controller.signal};
      if (encoding === 'json') {
        var attribution = (window.pmAttribution && window.pmAttribution()) || null;
        var payload = attribution ? Object.assign({}, body, {attribution: attribution}) : body;
        // Origen visible en la hoja de leads (columna Datos, junto a "Página"): de qué anuncio o web llega.
        // Sin consentimiento solo se lee la URL actual (no se guarda nada en el dispositivo).
        var origen = window.__pmOrigen ? window.__pmOrigen(attribution) : '';
        if (origen && payload && typeof payload === 'object' && typeof payload.page === 'string' && payload.page.indexOf(' · origen: ') < 0)
          payload = Object.assign({}, payload, {page: payload.page + ' · origen: ' + origen});
        if (payload && typeof payload === 'object') {
          payload = Object.assign({}, payload, {_t: Math.round((Date.now() - window.__pmT0) / 1000), _sid: sid});
          var pn = f && f.querySelector && f.querySelector('#pmNombre');
          if (pn && !payload.nombre) payload.nombre = pn.value.trim().replace(/\s+/g, ' ');
          if (fast || window.__pmRaro(payload.nombre) || window.__pmRaro(payload.mensaje)) payload.revisar = '1';
        }
        // La hoja de leads interpreta "+34…" como fórmula (#ERROR!): se envía con prefijo 00, mismo número
        if (payload && typeof payload.telefono === 'string' && /^\s*\+/.test(payload.telefono)) payload = Object.assign({}, payload, {telefono: payload.telefono.replace(/^\s*\+/, '00')});
        options.headers = {'Content-Type': 'text/plain;charset=UTF-8'}; options.body = JSON.stringify(payload);
      }
      else options.body = body;
      var response;
      try { response = await fetch(url, options); } catch (e) { throw err('network'); }
      if (!response.ok || response.type === 'opaque') throw err('unconfirmed');
      var result;
      try { result = await response.json(); } catch (e) { throw err('unconfirmed'); }
      if (!result || result.ok !== true) { var no = err('unconfirmed'); no.reason = result && result.error ? String(result.error) : ''; throw no; }
      return result;
    } finally { clearTimeout(timer); }
  })();
  window.__pmInflight[key] = p;
  p.then(function () { delete window.__pmInflight[key]; }, function () { delete window.__pmInflight[key]; });
  return p;
};

/* Nombre y teléfono comprobados en todos los formularios (regla 11 oct 2026).
   - Nombre: solo letras (con acentos, apóstrofo, guion o punto), 2-60 caracteres, con alguna vocal, sin números ni enlaces.
   - Teléfono: español de 9 cifras (6, 7, 8 o 9), o internacional con prefijo (+ o 00, 8-15 cifras),
     o nacional de 10 cifras empezando por 0 (Francia, Italia…). No se aceptan cifras repetidas ni secuencias.
   - Ventana de datos de "Qué barco necesito" y "Valora tu barco": se añade el nombre y el teléfono pasa a obligatorio.
     El test del PER se queda solo con email (y el campo trampa de arriba).
   Se comprueba en fase de captura, antes del código de cada formulario: si algo no cuadra, no se envía y se avisa junto al campo. */
(function () {
  var m = /^\/(ca|en|fr)\//.exec(location.pathname), L = m ? m[1] : 'es';
  var TX = {
    es: {n: 'Escribe tu nombre (solo letras).', t: 'Revisa el teléfono: 9 cifras, o con prefijo (+33…) si no es de España.', nl: 'Tu nombre', tl: 'Tu teléfono (para WhatsApp)'},
    ca: {n: 'Escriu el teu nom (només lletres).', t: 'Revisa el telèfon: 9 xifres, o amb prefix (+33…) si no és d’Espanya.', nl: 'El teu nom', tl: 'El teu telèfon (per a WhatsApp)'},
    en: {n: 'Please enter your name (letters only).', t: 'Please check the phone number: include the country code (+44…) if it is not Spanish.', nl: 'Your name', tl: 'Your phone (for WhatsApp)'},
    fr: {n: 'Indiquez votre nom (lettres uniquement).', t: 'Vérifiez le téléphone : avec l’indicatif du pays (+33…) s’il n’est pas espagnol.', nl: 'Votre nom', tl: 'Votre téléphone (pour WhatsApp)'}
  }[L];
  var isPer = /test-per/.test(location.pathname);
  function okName(v) {
    v = String(v || '').trim().replace(/\s+/g, ' ');
    if (v.length < 2 || v.length > 60) return false;
    if (!/^[A-Za-zÀ-ÖØ-öø-ÿ'’. -]+$/.test(v)) return false;
    if (!/[aeiouyáéíóúàèìòùâêîôûäëïöüAEIOUYÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÄËÏÖÜ]/.test(v)) return false;
    if (v.split(' ').length > 6 || /(.)\1\1\1/i.test(v)) return false;
    return !(window.__pmRaro && window.__pmRaro(v.replace(/ /g, '')));
  }
  function okTel(v) {
    v = String(v || '').trim();
    var intl = /^(\+|00)/.test(v), d = v.replace(/\D/g, '');
    if (/[A-Za-z]/.test(v)) return false;
    if (intl) d = d.replace(/^00/, '');
    var ok = intl ? (d.length >= 8 && d.length <= 15) :
      (/^[6789]\d{8}$/.test(d) || /^34[6789]\d{8}$/.test(d) || /^0[1-9]\d{8}$/.test(d));
    if (!ok) return false;
    var tail = d.slice(-9);
    return !/^(\d)\1+$/.test(tail) && tail !== '123456789' && tail !== '987654321';
  }
  function setup() {
    var lf = document.getElementById('pmLeadForm');
    if (lf && !isPer && !lf.querySelector('#pmNombre')) {
      var em = document.getElementById('pmEmail');
      var st = document.createElement('style');
      st.textContent = '#pmLeadForm #pmNombre{width:100%;font:16px var(--serif);padding:11px 12px;border:1px solid var(--plata-2);border-radius:6px;margin-bottom:10px;box-sizing:border-box}';
      document.head.appendChild(st);
      var n = document.createElement('input');
      n.type = 'text'; n.id = 'pmNombre'; n.required = true; n.maxLength = 60;
      n.setAttribute('autocomplete', 'name'); n.placeholder = TX.nl;
      if (em) em.parentNode.insertBefore(n, em); else lf.insertBefore(n, lf.firstChild);
      var t = document.getElementById('pmTel');
      if (t) { t.required = true; t.placeholder = TX.tl; }
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup); else setup();
  function clearErr(f) { f.querySelectorAll('.pm-fielderr').forEach(function (p) { p.remove(); }); }
  function showErr(el, msg) {
    var p = document.createElement('p');
    p.className = 'pm-fielderr'; p.setAttribute('role', 'alert'); p.textContent = msg;
    p.style.cssText = 'color:#b42318;font-size:.9rem;font-weight:600;margin:4px 0 8px';
    el.setAttribute('aria-invalid', 'true');
    el.parentNode.insertBefore(p, el.nextSibling);
    el.addEventListener('input', function h() { el.removeAttribute('aria-invalid'); p.remove(); el.removeEventListener('input', h); });
    el.focus();
  }
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f || !f.querySelector || (isPer && f.id === 'pmLeadForm')) return;
    var n = f.querySelector('input[name=nombre],input[name=ya_name],#pmNombre'), t = f.querySelector('input[type=tel]');
    if (!n && !t) return;
    clearErr(f);
    var bad = null, msg = '';
    if (n && !okName(n.value)) { bad = n; msg = TX.n; }
    else if (t && (t.required || t.value.trim()) && !okTel(t.value)) { bad = t; msg = TX.t; }
    if (bad) {
      e.preventDefault(); e.stopImmediatePropagation();
      try { if (window.pmTrack) window.pmTrack('form_invalid_local', {label: bad === n ? 'nombre' : 'telefono'}); } catch (x) {}
      showErr(bad, msg);
    }
  }, true);
})();

/* Origen del contacto en texto corto: "Google Ads · campaña · palabra", "Meta Ads · campaña · anuncio",
   "web: dominio" o "directo". Usa la atribución guardada (con consentimiento) o, si no la hay, los parámetros de la URL actual. */
window.__pmOrigen = function (a) {
  try {
    var q = new URLSearchParams(location.search), d = {};
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid'].forEach(function (k) {
      var v = (a && a[k]) || q.get(k); if (v) d[k] = String(v).replace(/[|=+]/g, ' ').slice(0, 60);
    });
    var src = (d.utm_source || '').toLowerCase(), med = (d.utm_medium || '').toLowerCase(), canal = '';
    if (d.gclid || (/google/.test(src) && /cpc|paid|ads/.test(med))) canal = 'Google Ads';
    else if (d.fbclid && !src) canal = 'Meta';
    else if (/facebook|instagram|meta|fb|ig/.test(src)) canal = /cpc|paid|ads/.test(med) ? 'Meta Ads' : 'Meta';
    else if (src) canal = d.utm_source + (med ? '/' + d.utm_medium : '');
    if (canal) return [canal, d.utm_campaign, d.utm_term || d.utm_content].filter(Boolean).join(' · ');
    if (a && a.referrer) return 'web: ' + String(a.referrer).replace(/^https?:\/\/(www\.)?/, '');
    if (a && a.source === 'direct') return 'directo';
    return '';
  } catch (_) { return ''; }
};
