/* One request, explicit server acknowledgement; never retry automatically. */
window.submitConfirmed = async function (url, body, encoding) {
  var controller = new AbortController();
  var timer = setTimeout(function () { controller.abort(); }, 45000);
  try {
    var options = {method:'POST', credentials:'omit', signal:controller.signal};
    if (encoding === 'json') { options.headers = {'Content-Type':'text/plain;charset=UTF-8'}; options.body = JSON.stringify(body); }
    else options.body = body;
    var response = await fetch(url, options);
    if (!response.ok || response.type === 'opaque') throw new Error('unconfirmed');
    var result = await response.json();
    if (!result || result.ok !== true) throw new Error('unconfirmed');
    return result;
  } finally { clearTimeout(timer); }
};
