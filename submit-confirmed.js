/* One request, explicit server acknowledgement; never retry automatically. */
window.submitConfirmed = async function (url, body, encoding) {
  var controller = new AbortController();
  var timer = setTimeout(function () { controller.abort(); }, 45000);
  try {
    var options = {method:'POST', credentials:'omit', signal:controller.signal};
    if (encoding === 'json') {
      var attribution = (window.pmAttribution && window.pmAttribution()) || null;
      var payload = attribution ? Object.assign({}, body, {attribution:attribution}) : body;
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
