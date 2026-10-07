/* Plata Marine · buscador de la web (lupa en la cabecera). Busca en títulos, encabezados y descripciones
   de todas las páginas del idioma actual (/search/<idioma>.json, generado con _tools/build_search_index.py).
   Sin servicios externos ni cookies; la medición solo envía el número de resultados, nunca lo que se escribe. */
(function () {
  'use strict';
  var p = location.pathname, lang = p.indexOf('/ca/') === 0 ? 'ca' : p.indexOf('/en/') === 0 ? 'en' : p.indexOf('/fr/') === 0 ? 'fr' : 'es';
  var T = {
    es: {btn: 'Buscar en la web', ph: '¿Qué buscas? Ej.: motos de agua, ITP, amarres…', none: 'No he encontrado nada con esas palabras.', help: 'Escríbeme y te ayudo', close: 'Cerrar', results: 'resultados'},
    ca: {btn: 'Cercar al web', ph: 'Què busques? Ex.: motos d\'aigua, ITP, amarradors…', none: 'No he trobat res amb aquestes paraules.', help: 'Escriu-me i t\'ajudo', close: 'Tancar', results: 'resultats'},
    en: {btn: 'Search the site', ph: 'What are you looking for? E.g. jet skis, tax, berths…', none: 'Nothing found with those words.', help: 'Message me and I will help', close: 'Close', results: 'results'},
    fr: {btn: 'Rechercher sur le site', ph: 'Que cherchez-vous ? Ex. : jet-ski, ITP, places de port…', none: 'Aucun résultat avec ces mots.', help: 'Écrivez-moi, je vous aide', close: 'Fermer', results: 'résultats'}
  }[lang];
  var STOP = {de: 1, la: 1, el: 1, en: 1, y: 1, a: 1, para: 1, un: 1, una: 1, del: 1, los: 1, las: 1, que: 1, con: 1, por: 1, mi: 1, i: 1, les: 1, per: 1, amb: 1, the: 1, of: 1, for: 1, to: 1, and: 1, du: 1, des: 1, le: 1, et: 1, pour: 1, d: 1, l: 1};
  function norm(s) { return String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, ' ').trim(); }
  function stem(w) { return w.length > 4 && /es$/.test(w) ? w.slice(0, -2) : w.length > 3 && /s$/.test(w) ? w.slice(0, -1) : w; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (m) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[m]; }); }
  var data = null, loading = null;
  function load() {
    if (data) return Promise.resolve(data);
    if (!loading) loading = fetch('/search/' + lang + '.json?v=20261007').then(function (r) { return r.json(); }).then(function (d) {
      data = d.map(function (x) { return {x: x, t: norm(x.t), h: norm(x.h), d: norm(x.d), u: norm(x.u)}; }); return data;
    });
    return loading;
  }
  function search(q) {
    var toks = norm(q).split(' ').filter(function (w) { return w && !STOP[w]; }).map(stem);
    if (!toks.length) return [];
    var res = [];
    data.forEach(function (r) {
      var sc = 0;
      for (var i = 0; i < toks.length; i++) {
        var w = toks[i], s = 0;
        if (r.t.indexOf(w) >= 0) s += 3;
        if (r.h.indexOf(w) >= 0) s += 2;
        if (r.d.indexOf(w) >= 0) s += 1;
        if (r.u.indexOf(w) >= 0) s += 1;
        if (!s) return;
        sc += s;
      }
      var nq = norm(q);
      if (r.t.indexOf(nq) >= 0) sc += 4;
      res.push({r: r.x, s: sc - r.x.u.split('/').length * 0.1});
    });
    return res.sort(function (a, b) { return b.s - a.s; }).slice(0, 8).map(function (o) { return o.r; });
  }
  var css = '.pms-btn{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border:1px solid rgba(127,146,158,.45);border-radius:999px;background:transparent;color:inherit;cursor:pointer;flex:none;margin-right:6px}.pms-btn svg{width:18px;height:18px}.pms-btn:hover{background:rgba(127,146,158,.12)}@media(max-width:560px){header.top .pms-btn{display:none}}.pms-row{display:flex;align-items:center;gap:10px;width:100%;font:inherit;font-size:15px;color:#3E5462;background:#fff;border:1px solid #B7C3CB;border-radius:10px;padding:11px 14px;margin:0 0 12px;cursor:pointer;text-align:left}.pms-row svg{width:18px;height:18px;flex:none}' +
    '.pms{position:fixed;inset:0;z-index:9995;background:rgba(13,28,39,.45);display:flex;justify-content:center;align-items:flex-start;padding:70px 16px 16px}.pms[hidden]{display:none}' +
    '.pms-box{width:100%;max-width:640px;background:#fff;border-radius:12px;box-shadow:0 20px 50px rgba(13,28,39,.3);overflow:hidden;font-family:"Archivo","Helvetica Neue",Arial,sans-serif;color:#0D1C27}' +
    '.pms-top{display:flex;gap:8px;align-items:center;padding:12px 14px;border-bottom:1px solid #E3E8EB}.pms-top input{flex:1;font:inherit;font-size:17px;border:0;outline:0;padding:8px 4px;min-width:0}.pms-x{border:0;background:transparent;font-size:24px;line-height:1;cursor:pointer;color:#7F929E;padding:4px 8px}' +
    '.pms-list{list-style:none;margin:0;padding:6px 0;max-height:60vh;overflow-y:auto}.pms-list a{display:block;padding:10px 16px;text-decoration:none;color:inherit}.pms-list a:hover,.pms-list a:focus{background:#F3F5F6;outline:0}.pms-list strong{display:block;font-size:15px}.pms-list span{display:block;font-size:13px;color:#3E5462;margin-top:2px;line-height:1.4}' +
    '.pms-none{padding:14px 16px;font-size:15px;color:#3E5462}.pms-none a{color:#0E3042}';
  function init() {
    var wrap = document.querySelector('header.top .wrap');
    if (!wrap || document.querySelector('.pms-btn')) return;
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    var b = document.createElement('button'); b.type = 'button'; b.className = 'pms-btn'; b.setAttribute('aria-label', T.btn); b.title = T.btn;
    b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>';
    var anchor = wrap.querySelector('.langsw') || wrap.querySelector('.pmx-btn');
    if (anchor) anchor.parentNode.insertBefore(b, anchor); else wrap.appendChild(b);
    var panel = document.querySelector('.pmx-panel .pmx-in');
    var row = null;
    if (panel) { row = document.createElement('button'); row.type = 'button'; row.className = 'pms-row'; row.innerHTML = b.innerHTML + '<span>' + esc(T.btn) + '</span>'; panel.insertBefore(row, panel.firstChild); }
    var ov = document.createElement('div'); ov.className = 'pms'; ov.hidden = true; ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true'); ov.setAttribute('aria-label', T.btn);
    ov.innerHTML = '<div class="pms-box"><div class="pms-top"><input type="text" inputmode="search" enterkeyhint="search" autocomplete="off" aria-label="' + esc(T.btn) + '" placeholder="' + esc(T.ph) + '"><button type="button" class="pms-x" aria-label="' + esc(T.close) + '">×</button></div><ul class="pms-list" role="listbox"></ul></div>';
    document.body.appendChild(ov);
    var inp = ov.querySelector('input'), list = ov.querySelector('.pms-list'), timer = null, tracked = false;
    var wa = 'https://wa.me/34633742973';
    function render() {
      var q = inp.value.trim();
      if (q.length < 2) { list.innerHTML = ''; return; }
      load().then(function () {
        var r = search(q);
        list.innerHTML = r.length ? r.map(function (x) { return '<li><a href="' + esc(x.u) + '"><strong>' + esc(x.t) + '</strong>' + (x.d ? '<span>' + esc(x.d) + '</span>' : '') + '</a></li>'; }).join('')
          : '<li class="pms-none">' + esc(T.none) + ' <a href="' + wa + '" target="_blank" rel="noopener">' + esc(T.help) + '</a></li>';
        clearTimeout(timer); timer = setTimeout(function () { if (window.pmTrack) window.pmTrack('site_search', {label: r.length ? 'con_resultados' : 'sin_resultados'}); }, 1500);
      });
    }
    function open() { ov.hidden = false; document.documentElement.style.overflow = 'hidden'; load(); setTimeout(function () { inp.focus(); }, 30); }
    function close() { ov.hidden = true; document.documentElement.style.overflow = ''; if (b.offsetParent) b.focus(); }
    b.addEventListener('click', open);
    if (row) row.addEventListener('click', function () { var mb = document.getElementById('pmxBtn'); if (mb && mb.getAttribute('aria-expanded') === 'true') mb.click(); open(); });
    ov.querySelector('.pms-x').addEventListener('click', close);
    ov.addEventListener('click', function (e) { if (e.target === ov) close(); });
    inp.addEventListener('input', render);
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
      if (e.key === 'Enter') { var a = list.querySelector('a[href^="/"]'); if (a) location.href = a.getAttribute('href'); }
      if (e.key === 'ArrowDown') { var f = list.querySelector('a'); if (f) { e.preventDefault(); f.focus(); } }
    });
    list.addEventListener('keydown', function (e) {
      var a = e.target.closest('a'); if (!a) return;
      var li = a.parentNode;
      if (e.key === 'ArrowDown' && li.nextElementSibling) { e.preventDefault(); li.nextElementSibling.querySelector('a').focus(); }
      if (e.key === 'ArrowUp') { e.preventDefault(); if (li.previousElementSibling) li.previousElementSibling.querySelector('a').focus(); else inp.focus(); }
      if (e.key === 'Escape') close();
    });
    document.addEventListener('keydown', function (e) { if (e.key === '/' && ov.hidden && !/input|textarea|select/i.test((e.target.tagName || ''))) { e.preventDefault(); open(); } });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
