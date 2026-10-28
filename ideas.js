/* Buzón "¿De qué quieres que hablemos?" (Actualidad, ES/CA/EN/FR). La sugerencia llega a la hoja de leads como Novedades, con el texto "IDEA PARA ARTÍCULO". El email es obligatorio (el servidor pide un contacto). */
(function () {
  'use strict';
  var f = document.getElementById('pm-ideas');
  if (!f) return;
  var URL = 'https://script.google.com/macros/s/AKfycbwJtBkktakE0qgmu_b8oHOOopCDnG6BDpBjg2zBUsZKi8l3_OBEuez_OHWmE9j8qCBF/exec';
  var LANG = (document.documentElement.lang || 'es').slice(0, 2);
  var T = {
    es: { req: 'Cuéntame el tema en unas palabras.', mail: 'Revisa el email.', consent: 'Marca la casilla de privacidad para poder enviarlo.', sending: 'Enviando…', ok: '¡Gracias! Lo tengo apuntado. Si escribo sobre ello, lo verás aquí.', fail: 'No he podido confirmar el envío. Escríbeme a juan@platamarine.com y lo apunto.' },
    ca: { req: 'Explica\'m el tema en poques paraules.', mail: 'Revisa el correu.', consent: 'Marca la casella de privacitat per poder enviar-ho.', sending: 'Enviant…', ok: 'Gràcies! Ho tinc apuntat. Si n\'escric, ho veuràs aquí.', fail: 'No he pogut confirmar l\'enviament. Escriu-me a juan@platamarine.com i ho apunto.' },
    en: { req: 'Tell me the topic in a few words.', mail: 'Please check the email.', consent: 'Please tick the privacy box to send it.', sending: 'Sending…', ok: 'Thanks! It\'s noted. If I write about it, you\'ll see it here.', fail: 'I couldn\'t confirm it was sent. Email me at juan@platamarine.com and I\'ll note it.' },
    fr: { req: 'Dites-moi le sujet en quelques mots.', mail: 'Vérifiez l\'e-mail.', consent: 'Cochez la case de confidentialité pour l\'envoyer.', sending: 'Envoi…', ok: 'Merci ! C\'est noté. Si j\'écris dessus, vous le verrez ici.', fail: 'Je n\'ai pas pu confirmer l\'envoi. Écrivez-moi à juan@platamarine.com et je le note.' }
  }[LANG] || null;
  if (!T) return;
  var st = f.querySelector('.pmi-st'), btn = f.querySelector('button[type=submit]'), busy = false, sent = false;
  function val(n) { var e = f.elements[n]; return e ? String(e.value || '').trim() : ''; }
  function say(t) { if (st) { st.hidden = false; st.textContent = t; } }
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    if (busy || sent) return;
    var tema = val('tema'), em = val('email');
    if (tema.length < 4) { say(T.req); f.elements.tema.focus(); return; }
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)) { say(T.mail); f.elements.email.focus(); return; }
    if (!f.elements.consent.checked) { say(T.consent); return; }
    if (!window.submitConfirmed) { say(T.fail); return; }
    busy = true; if (btn) btn.disabled = true; say(T.sending);
    var p = { source: 'novedades', email: em, newsletter: false, consent: true, consent_v: '2026-09', consent_at: new Date().toISOString(), detail: 'IDEA PARA ARTÍCULO: ' + tema + (val('alias') ? ' · De: ' + val('alias') : '') + ' · Idioma: ' + LANG, page: location.pathname, ua: navigator.userAgent.slice(0, 120) };
    window.submitConfirmed(URL, p, 'json', f).then(function () {
      sent = true; busy = false; say(T.ok); f.reset();
      if (window.pmTrack) window.pmTrack('idea_sugerida', { form_id: 'ideas' });
    }).catch(function () { busy = false; if (btn) btn.disabled = false; say(T.fail); });
  });
})();
