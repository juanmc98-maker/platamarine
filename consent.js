/* Consentimiento de analítica y marketing. Versión 2026-09-28 (Configurar por finalidad, atribución borrada al retirar). i18n ES/CA/EN/FR. */
(function () {
'use strict';
var GID = 'G-MJ6S489CXQ', FID = '1618955459947483', KEY = 'pm_privacy_v3', OLD = 'pm_cookies', OLD2 = 'pm_privacy_v2';
var VERSION = '2026-09-16', MAX_AGE = 365 * 86400000;
var allowedA = false, allowedM = false, loadedGA = false, loadedFB = false, box, opener;
var AKEY = 'pm_attr', AMAX = 90 * 86400000;
var LANG = location.pathname.indexOf('/ca/') === 0 ? 'ca' : (location.pathname.indexOf('/en/') === 0 ? 'en' : (location.pathname.indexOf('/fr/') === 0 ? 'fr' : 'es'));
var T = {
es: {
aria: 'Preferencias de cookies',
cfg: '<p><strong>Configurar cookies</strong></p><label class="opt"><input type="checkbox" data-opt="analytics"> <span><b>Analítica</b> (Google Analytics): cuántas visitas tiene la web y qué páginas se leen.</span></label><label class="opt"><input type="checkbox" data-opt="marketing"> <span><b>Publicidad</b> (Google Ads y Meta): medir si nuestros anuncios funcionan.</span></label><div class="choices"><button type="button" data-choice="back">Volver</button><button type="button" data-choice="save">Guardar mi elección</button></div>',
html: '<p><strong>Tú decides sobre las cookies.</strong> Con tu permiso, Google Analytics mide las visitas a esta web y Meta (Facebook/Instagram) nos ayuda a medir y mejorar nuestros anuncios. Puedes rechazarlas y usar todos los servicios igualmente. Guardamos tu elección durante 12 meses. <a href="/cookies.html">Política de cookies</a>.</p><div class="choices"><button type="button" data-choice="no">Rechazar todo</button><button type="button" data-choice="config">Configurar</button><button type="button" data-choice="all">Aceptar todo</button></div>'
},
ca: {
aria: 'Preferències de galetes',
cfg: '<p><strong>Configurar galetes</strong></p><label class="opt"><input type="checkbox" data-opt="analytics"> <span><b>Analítica</b> (Google Analytics): quantes visites té la web i quines pàgines es llegeixen.</span></label><label class="opt"><input type="checkbox" data-opt="marketing"> <span><b>Publicitat</b> (Google Ads i Meta): mesurar si els nostres anuncis funcionen.</span></label><div class="choices"><button type="button" data-choice="back">Tornar</button><button type="button" data-choice="save">Desar la meva elecció</button></div>',
html: '<p><strong>Tu decideixes sobre les galetes.</strong> Amb el teu permís, Google Analytics mesura les visites d\'aquesta web i Meta (Facebook/Instagram) ens ajuda a mesurar i millorar els nostres anuncis. Pots rebutjar-les i fer servir tots els serveis igualment. Guardem la teva elecció durant 12 mesos. <a href="/ca/cookies.html">Política de galetes</a>.</p><div class="choices"><button type="button" data-choice="no">Rebutjar-ho tot</button><button type="button" data-choice="config">Configurar</button><button type="button" data-choice="all">Acceptar-ho tot</button></div>'
},
en: {
aria: 'Cookie preferences',
cfg: '<p><strong>Cookie settings</strong></p><label class="opt"><input type="checkbox" data-opt="analytics"> <span><b>Analytics</b> (Google Analytics): how many visits the site gets and which pages are read.</span></label><label class="opt"><input type="checkbox" data-opt="marketing"> <span><b>Advertising</b> (Google Ads and Meta): measuring whether our ads work.</span></label><div class="choices"><button type="button" data-choice="back">Back</button><button type="button" data-choice="save">Save my choice</button></div>',
html: '<p><strong>You decide about cookies.</strong> With your permission, Google Analytics measures visits to this site and Meta (Facebook/Instagram) helps us measure and improve our ads. You can reject them and still use every service. We keep your choice for 12 months. <a href="/en/cookies.html">Cookie policy</a>.</p><div class="choices"><button type="button" data-choice="no">Reject all</button><button type="button" data-choice="config">Settings</button><button type="button" data-choice="all">Accept all</button></div>'
},
fr: {
aria: 'Préférences de cookies',
cfg: '<p><strong>Paramètres des cookies</strong></p><label class="opt"><input type="checkbox" data-opt="analytics"> <span><b>Mesure d\'audience</b> (Google Analytics) : combien de visites reçoit le site et quelles pages sont lues.</span></label><label class="opt"><input type="checkbox" data-opt="marketing"> <span><b>Publicité</b> (Google Ads et Meta) : mesurer si nos annonces fonctionnent.</span></label><div class="choices"><button type="button" data-choice="back">Retour</button><button type="button" data-choice="save">Enregistrer mon choix</button></div>',
html: '<p><strong>C\'est vous qui décidez pour les cookies.</strong> Avec votre accord, Google Analytics mesure les visites de ce site et Meta (Facebook/Instagram) nous aide à mesurer et à améliorer nos annonces. Vous pouvez les refuser et utiliser tous les services quand même. Nous conservons votre choix pendant 12 mois. <a href="/fr/cookies.html">Politique de cookies</a>.</p><div class="choices"><button type="button" data-choice="no">Tout refuser</button><button type="button" data-choice="config">Paramétrer</button><button type="button" data-choice="all">Tout accepter</button></div>'
}
};
/* Atribución de origen (UTM/gclid/referrer), solo con consentimiento de analítica.
No es publicidad ni remarketing: es texto de la propia URL/referrer, guardado en
local para saber por qué canal llegó cada lead. No se comparte con terceros. */
function captureAttribution() {
try {
var q = new URLSearchParams(location.search), data = {}, campaignKeys =
['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid'];
campaignKeys.forEach(function (k) { var v = q.get(k); if (v) data[k] = v.slice(0, 150); });
var hasCampaign = Object.keys(data).length > 0;
var ref = document.referrer, extRef = '';
try { if (ref && ref.indexOf(location.origin) !== 0) extRef = new URL(ref).origin; } catch (_) {}
if (hasCampaign) {
if (extRef) data.referrer = extRef;
data.landing = location.pathname; data.at = Date.now();
localStorage.setItem(AKEY, JSON.stringify(data));
return;
}
var existing = null;
try { existing = JSON.parse(localStorage.getItem(AKEY)); } catch (_) {}
if (existing && existing.at && Date.now() - existing.at < AMAX) return;
if (extRef) localStorage.setItem(AKEY, JSON.stringify({ referrer: extRef, landing: location.pathname, at: Date.now() }));
else if (!existing) localStorage.setItem(AKEY, JSON.stringify({ source: 'direct', landing: location.pathname, at: Date.now() }));
} catch (_) {}
}
window.pmAttribution = function () {
if (!allowedA) return null;
try { var a = JSON.parse(localStorage.getItem(AKEY)); return a && a.at && Date.now() - a.at < AMAX ? a : null; } catch (_) { return null; }
};
function dropAttribution() { try { localStorage.removeItem(AKEY); } catch (_) {} }
function cleanUrl() {
var q = new URLSearchParams(location.search), keep = new URLSearchParams();
['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid'].forEach(function (k) { var v = q.get(k); if (v) keep.set(k, v.slice(0, 150)); });
var k = keep.toString(); return location.origin + location.pathname + (k ? '?' + k : '');
}
function refOrigin() { try { return document.referrer ? new URL(document.referrer).origin : ''; } catch (_) { return ''; } }
window.dataLayer = window.dataLayer || [];
window.gtag = function () { window.dataLayer.push(arguments); };
window.gtag('consent', 'default', {analytics_storage:'denied', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'});
window['ga-disable-' + GID] = true;
function read() {
try {
var v = JSON.parse(localStorage.getItem(KEY));
if (v && v.version === VERSION && typeof v.analytics === 'boolean' && typeof v.marketing === 'boolean' && typeof v.at === 'number' && v.at <= Date.now() && Date.now() - v.at < MAX_AGE) return v;
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
function enableAnalytics() {
allowedA = true; window.__pmAnalyticsAllowed = true; window['ga-disable-' + GID] = false;
window.gtag('consent', 'update', {analytics_storage:'granted'});
captureAttribution();
if (loadedGA) return;
loadedGA = true; window.__pmga = true;
var s = document.createElement('script'); s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GID; document.head.appendChild(s);
window.gtag('js', new Date());
window.gtag('config', GID, {send_page_view:false, allow_google_signals:false, allow_ad_personalization_signals:false, cookie_expires:31536000, cookie_update:false});
window.gtag('event', 'page_view', {page_location:cleanUrl(), page_referrer:refOrigin(), page_title:document.title});
}
function enableMarketing() {
allowedM = true; window.__pmMarketingAllowed = true;
window.gtag('consent', 'update', {ad_storage:'granted', ad_user_data:'granted', ad_personalization:'granted'});
if (loadedFB) return;
loadedFB = true;
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
window.fbq('init', FID);
window.fbq('track', 'PageView');
}
function hide() { if (box) box.hidden = true; if (opener && opener.isConnected) opener.focus(); }
function save(choice, a, m) {
var hadGA = loadedGA, hadFB = loadedFB;
var analytics = choice === 'custom' ? !!a : (choice === 'analytics' || choice === 'all');
var marketing = choice === 'custom' ? !!m : choice === 'all';
try { localStorage.setItem(KEY, JSON.stringify({version:VERSION, analytics:analytics, marketing:marketing, at:Date.now()})); localStorage.removeItem(OLD); localStorage.removeItem(OLD2); } catch (_) {}
if (analytics) enableAnalytics(); else { allowedA = false; window.__pmAnalyticsAllowed = false; window['ga-disable-' + GID] = true; window.gtag('consent', 'update', {analytics_storage:'denied'}); dropAttribution(); }
if (marketing) enableMarketing(); else { allowedM = false; window.__pmMarketingAllowed = false; window.gtag('consent', 'update', {ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'}); }
if (!analytics || !marketing) clearCookies();
hide();
if ((!analytics && hadGA) || (!marketing && hadFB)) location.reload();
}
function show() {
opener = document.activeElement;
if (!box) {
var style = document.createElement('style');
style.textContent = '#privacy-choice[hidden]{display:none!important}#privacy-choice{position:fixed;bottom:16px;left:16px;right:16px;z-index:10000;max-width:560px;margin:auto;padding:20px;background:#fff;color:#171512;border:2px solid #171512;border-radius:8px;box-shadow:0 8px 35px #0003;font:15px/1.5 system-ui,sans-serif;max-height:85vh;overflow:auto}#privacy-choice p{margin:0 0 14px;color:#171512}#privacy-choice a{color:#171512;text-decoration:underline}#privacy-choice .choices{display:flex;gap:10px;flex-wrap:wrap}#privacy-choice button{flex:1;min-width:120px;background:#fff;color:#171512;border:2px solid #171512;border-radius:4px;padding:12px 10px;cursor:pointer;font:600 14px system-ui,sans-serif}#privacy-choice button:focus-visible{outline:3px solid #0067c0;outline-offset:3px}#privacy-choice .opt{display:flex;gap:10px;align-items:flex-start;margin:0 0 12px;cursor:pointer}#privacy-choice .opt input{width:20px;height:20px;margin-top:2px;flex:none}';
document.head.appendChild(style);
box = document.createElement('div'); box.id = 'privacy-choice'; box.setAttribute('role','dialog'); box.setAttribute('aria-label', T[LANG].aria);
document.body.appendChild(box);
}
mainView();
box.hidden = false;
box.querySelector('button').focus({preventScroll:true});
}
function mainView() {
box.innerHTML = T[LANG].html;
box.querySelector('[data-choice="no"]').onclick = function () { save('no'); };
box.querySelector('[data-choice="config"]').onclick = cfgView;
box.querySelector('[data-choice="all"]').onclick = function () { save('all'); };
}
function cfgView() {
var cur = read();
box.innerHTML = T[LANG].cfg;
box.querySelector('[data-opt="analytics"]').checked = !!(cur && cur.analytics);
box.querySelector('[data-opt="marketing"]').checked = !!(cur && cur.marketing);
box.querySelector('[data-choice="back"]').onclick = function () { mainView(); box.querySelector('button').focus(); };
box.querySelector('[data-choice="save"]').onclick = function () { save('custom', box.querySelector('[data-opt="analytics"]').checked, box.querySelector('[data-opt="marketing"]').checked); };
box.querySelector('input').focus();
}
window.siteConsent = {open:show, reject:function () { save('no'); }, analyticsAllowed:function () { return allowedA; }, marketingAllowed:function () { return allowedM; }};
document.addEventListener('click', function (e) {
var el = e.target.closest('[data-cookie-settings],#reset-ck,#ck-open');
if (el) { e.preventDefault(); show(); }
});
window.addEventListener('storage', function (e) {
if (e.key !== KEY) return;
var v = read(), newA = !!(v && v.analytics), newM = !!(v && v.marketing);
var reload = (!newA && loadedGA) || (!newM && loadedFB);
if (newA) enableAnalytics(); else { allowedA = false; window.__pmAnalyticsAllowed = false; window['ga-disable-' + GID] = true; dropAttribution(); }
if (newM) enableMarketing(); else { allowedM = false; window.__pmMarketingAllowed = false; }
if (reload) location.reload();
});
window.addEventListener('pageshow', function () {
var v = read(), newA = !!(v && v.analytics), newM = !!(v && v.marketing);
if ((!newA && allowedA) || (!newM && allowedM)) location.reload();
});
var initial = read();
if (!initial || !initial.analytics) dropAttribution();
if (initial) { if (initial.analytics) enableAnalytics(); if (initial.marketing) enableMarketing(); }
function init() { if (!initial) show(); }
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
