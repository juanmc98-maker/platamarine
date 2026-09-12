/* Consentimiento de analítica. Publicidad desactivada. Versión 2026-09-12. */
(function () {
  'use strict';
  var ID = 'G-MJ6S489CXQ', KEY = 'pm_privacy_v2', OLD = 'pm_cookies';
  var VERSION = '2026-09-12', MAX_AGE = 365 * 86400000, allowed = false, loaded = false, box, opener;
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag('consent', 'default', {analytics_storage:'denied', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'});
  window['ga-disable-' + ID] = true;
  function read() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY));
      if (v && v.version === VERSION && typeof v.analytics === 'boolean' && typeof v.at === 'number' && v.at <= Date.now() && Date.now() - v.at < MAX_AGE) return v;
    } catch (_) {}
    return null;
  }
  function clearCookies() {
    var host = location.hostname, domains = ['', host, '.' + host];
    var parts = host.split('.');
    while (parts.length > 2) { parts.shift(); domains.push('.' + parts.join('.')); }
    var paths = ['/'], segments = location.pathname.split('/');
    for (var i = 1; i < segments.length; i++) paths.push(segments.slice(0, i + 1).join('/'));
    document.cookie.split(';').forEach(function (item) {
      var name = item.split('=')[0].trim();
      if (!/^(_ga(?:_|$)|_gid$|_gat|_gcl_|_fbp$|_fbc$|rt_consent$)/.test(name)) return;
      domains.forEach(function (domain) { paths.forEach(function (path) {
        document.cookie = name + '=; Max-Age=0; path=' + path + (domain ? '; domain=' + domain : '') + '; SameSite=Lax; Secure';
      }); });
    });
  }
  function enable() {
    allowed = true; window.__pmAnalyticsAllowed = true; window['ga-disable-' + ID] = false;
    window.gtag('consent', 'update', {analytics_storage:'granted', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'});
    if (loaded) return;
    loaded = true; window.__pmga = true;
    var s = document.createElement('script'); s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + ID; document.head.appendChild(s);
    window.gtag('js', new Date());
    // No query strings, fragment identifiers, form data or external link text in analytics.
    window.gtag('config', ID, {send_page_view:false, allow_google_signals:false, allow_ad_personalization_signals:false, cookie_expires:31536000, cookie_update:false, page_location:location.origin + location.pathname, page_referrer:'', ignore_referrer:true});
    window.gtag('event', 'page_view', {page_location:location.origin + location.pathname, page_referrer:'', page_title:document.title});
  }
  function disable() {
    allowed = false; window.__pmAnalyticsAllowed = false; window['ga-disable-' + ID] = true;
    window.gtag('consent', 'update', {analytics_storage:'denied', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'});
    clearCookies();
  }
  function hide() { if (box) box.hidden = true; if (opener && opener.isConnected) opener.focus(); }
  function save(value) {
    var hadTracker = loaded;
    try { localStorage.setItem(KEY, JSON.stringify({version:VERSION, analytics:value, at:Date.now()})); localStorage.removeItem(OLD); } catch (_) {}
    if (value) enable(); else disable();
    hide();
    // Unload the already running SDK after withdrawal; only the preference is retained.
    if (!value && hadTracker) location.reload();
  }
  function show() {
    opener = document.activeElement;
    if (!box) {
      var style = document.createElement('style');
      style.textContent = '#privacy-choice[hidden]{display:none!important}#privacy-choice{position:fixed;bottom:16px;left:16px;right:16px;z-index:10000;max-width:560px;margin:auto;padding:20px;background:#fff;color:#171512;border:2px solid #171512;border-radius:8px;box-shadow:0 8px 35px #0003;font:15px/1.5 system-ui,sans-serif;max-height:85vh;overflow:auto}#privacy-choice p{margin:0 0 14px;color:#171512}#privacy-choice a{color:#171512;text-decoration:underline}#privacy-choice .choices{display:flex;gap:12px;flex-wrap:wrap}#privacy-choice button{flex:1;min-width:130px;background:#fff;color:#171512;border:2px solid #171512;border-radius:4px;padding:12px 16px;cursor:pointer;font:600 15px system-ui,sans-serif}#privacy-choice button:focus-visible{outline:3px solid #0067c0;outline-offset:3px}';
      document.head.appendChild(style);
      box = document.createElement('div'); box.id = 'privacy-choice'; box.setAttribute('role','dialog'); box.setAttribute('aria-label','Preferencias de cookies');
      box.innerHTML = '<p><strong>Tú decides sobre las cookies.</strong> Con tu permiso, Google Analytics mide las visitas a esta web. No activamos cookies publicitarias. Puedes rechazar la analítica y usar todos los servicios. Guardamos tu elección durante 12 meses. <a href="/cookies.html">Política de cookies</a>.</p><div class="choices"><button type="button" data-choice="no">Rechazar analítica</button><button type="button" data-choice="yes">Aceptar analítica</button></div>';
      document.body.appendChild(box);
      box.querySelector('[data-choice="no"]').onclick = function () { save(false); };
      box.querySelector('[data-choice="yes"]').onclick = function () { save(true); };
    }
    box.hidden = false;
    box.querySelector('button').focus({preventScroll:true});
  }
  window.siteConsent = {open:show, reject:function () { save(false); }, analyticsAllowed:function () { return allowed; }};
  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-cookie-settings],#reset-ck,#ck-open');
    if (el) { e.preventDefault(); show(); }
  });
  window.addEventListener('storage', function (e) {
    if (e.key !== KEY) return;
    var v = read();
    if (!v || !v.analytics) { var wasLoaded=loaded; disable(); if (wasLoaded) location.reload(); }
    else enable();
  });
  window.addEventListener('pageshow', function () { var v=read(); if ((!v || !v.analytics) && allowed) { disable(); location.reload(); } });
  var initial = read();
  if (initial && initial.analytics) enable(); else disable();
  function init() { if (!initial) show(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
