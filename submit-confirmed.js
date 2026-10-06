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
    try { if (window.pmTrack) window.pmTrack('form_blocked_local', {reason: 'hp'}); } catch (x) {}
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
        if (payload && typeof payload === 'object') {
          payload = Object.assign({}, payload, {_t: Math.round((Date.now() - window.__pmT0) / 1000), _sid: sid});
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
      if (!result || result.ok !== true) throw err('unconfirmed');
      return result;
    } finally { clearTimeout(timer); }
  })();
  window.__pmInflight[key] = p;
  p.then(function () { delete window.__pmInflight[key]; }, function () { delete window.__pmInflight[key]; });
  return p;
};
