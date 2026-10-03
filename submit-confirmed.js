/* One request, explicit server acknowledgement; never retry automatically.
   Antispam (3 oct 2026): campo trampa invisible en cada formulario + tiempo mínimo en la página.
   Si salta, se responde "ok" sin enviar nada (el bot no insiste). Texto que parece aleatorio: se envía marcado revisar=1. */
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
  window.__pmSpam = function () {
    var hp = Array.prototype.some.call(document.querySelectorAll('input[name=pm_hp_x]'), function (i) { return i.value.trim() !== ''; });
    return hp || (Date.now() - T0) < 3000;
  };
  window.__pmRaro = function (t) {
    t = String(t || '').trim();
    if (t.length < 10 || /\s/.test(t)) return false;
    var up = (t.match(/[A-Z]/g) || []).length, lo = (t.match(/[a-z]/g) || []).length, vw = (t.match(/[aeiouáéíóú]/gi) || []).length;
    return up >= 3 && lo >= 3 && vw / t.length < 0.25;
  };
})();
window.submitConfirmed = async function (url, body, encoding) {
  if (window.__pmSpam && window.__pmSpam()) return {ok: true};
  var controller = new AbortController();
  var timer = setTimeout(function () { controller.abort(); }, 45000);
  try {
    var options = {method:'POST', credentials:'omit', signal:controller.signal};
    if (encoding === 'json') {
      var attribution = (window.pmAttribution && window.pmAttribution()) || null;
      var payload = attribution ? Object.assign({}, body, {attribution:attribution}) : body;
      if (payload && typeof payload === 'object') {
        payload = Object.assign({}, payload, {_t: Math.round((Date.now() - window.__pmT0) / 1000)});
        if (window.__pmRaro(payload.nombre) || window.__pmRaro(payload.mensaje)) payload.revisar = '1';
      }
      // La hoja de leads interpreta "+34…" como fórmula (#ERROR!): se envía con prefijo 00, mismo número
      if (payload && typeof payload.telefono === 'string' && /^\s*\+/.test(payload.telefono)) payload = Object.assign({}, payload, {telefono: payload.telefono.replace(/^\s*\+/, '00')});
      options.headers = {'Content-Type':'text/plain;charset=UTF-8'}; options.body = JSON.stringify(payload);
    }
    else options.body = body;
    var response = await fetch(url, options);
    if (!response.ok || response.type === 'opaque') throw new Error('unconfirmed');
    var result = await response.json();
    if (!result || result.ok !== true) throw new Error('unconfirmed');
    return result;
  } finally { clearTimeout(timer); }
};
