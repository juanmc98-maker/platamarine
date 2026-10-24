/* Portada: "Barcos en cartera" se monta solo a partir de /inventario.js.
   Muestra los 3 barcos disponibles más caros, de más caro a más barato.
   Si el barco ya tiene tarjeta escrita en la portada, se usa esa; si no, se crea una
   con los datos del inventario y sus fotos /<slug>-1..4. No hay que tocar la portada
   al cambiar la cartera: basta con actualizar inventario.js. */
(function () {
  'use strict';
  var MAX = 3;
  function run() {
    var INV = window.PM_INV, grid = document.querySelector('#venta .boats');
    if (!INV || !grid) return;
    var lang = INV.lang();
    var T = {
      es: {year: 'Año', len: 'Eslora', ask: 'Preguntar por WhatsApp', ficha: 'Ver ficha completa', vatPaid: 'IVA pagado', foto: 'Foto ',
        wa: function (b) { return 'Hola Juan, me interesa el ' + b.name + ' de ' + b.year + ' que tenéis en venta. ¿Podemos hablar?'; }},
      ca: {year: 'Any', len: 'Eslora', ask: 'Preguntar per WhatsApp', ficha: 'Veure fitxa completa', vatPaid: 'IVA pagat', foto: 'Foto ',
        wa: function (b) { return 'Hola Juan, m\'interessa el ' + b.name + ' del ' + b.year + ' que teniu en venda. Podem parlar?'; }},
      en: {year: 'Year', len: 'Length', ask: 'Ask on WhatsApp', ficha: 'View full listing', vatPaid: 'VAT paid', foto: 'Photo ',
        wa: function (b) { return 'Hi Juan, I\'m interested in the ' + b.year + ' ' + b.name + ' you have for sale. Can we talk?'; }},
      fr: {year: 'Année', len: 'Longueur', ask: 'Demander sur WhatsApp', ficha: 'Voir l’annonce complète', vatPaid: 'TVA payée', foto: 'Photo ',
        wa: function (b) { return 'Bonjour Juan, le ' + b.name + ' de ' + b.year + ' que vous avez à vendre m’intéresse. Pouvons-nous en parler ?'; }}
    }[lang];
    function num(n, dec) {
      var s = n.toFixed(dec || 0), p = s.split('.'), sep = lang === 'en' ? ',' : lang === 'fr' ? '\u202f' : '.';
      var i = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, sep);
      return p[1] ? i + (lang === 'en' ? '.' : ',') + p[1] : i;
    }
    function price(b) {
      var v = lang === 'en' ? '€' + num(b.price) : num(b.price) + ' €';
      if (b.vat) v += ' <span class="vat" style="color:#D93025;font-weight:700;font-size:.6em">+IVA</span>';
      else if (b.vatPaid) v += ' <small style="font-size:.6em;font-weight:600">' + T.vatPaid + '</small>';
      return v;
    }
    function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]; }); }
    function build(b) {
      var url = INV.url(b, lang), a = document.createElement('article');
      a.className = 'boat featured'; a.setAttribute('data-pm-boat', b.slug);
      var d = b.d && b.d[lang] ? b.d[lang] : '';
      var thumbs = '';
      for (var i = 1; i <= 4; i++) thumbs += '<button type="button" aria-label="' + T.foto + i + '"' + (i === 1 ? ' class="on"' : '') + '><img alt="" loading="lazy" src="/' + b.slug + '-' + i + '-t.jpg"></button>';
      a.innerHTML =
        '<div class="gal"><a class="main-link" href="' + url + '" aria-label="' + esc(T.ficha) + '"><img class="main" loading="lazy" width="1600" height="900" alt="' + esc(b.name) + '" src="/' + b.slug + '-1-m.jpg"></a>' +
        '<div class="thumbs">' + thumbs + '</div><span class="boat-status">' + esc(INV.label[lang][b.status]) + '</span></div>' +
        '<div class="boat-body"><div class="boat-head"><h3><a href="' + url + '" style="color:inherit;text-decoration:none">' + esc(b.name) + '</a></h3><p class="price">' + price(b) + '</p></div>' +
        '<dl class="specs"><div><dt>' + T.year + '</dt><dd>' + b.year + '</dd></div><div><dt>' + T.len + '</dt><dd>' + (b.length % 1 ? num(b.length, 2) : num(b.length)) + ' m</dd></div></dl>' +
        (d ? '<p class="desc">' + esc(d) + '</p>' : '') +
        '<div class="boat-cta"><a class="btn btn-wa" href="https://wa.me/34633742973?text=' + encodeURIComponent(T.wa(b)) + '" target="_blank" rel="noopener">' + T.ask + '</a>' +
        '<a class="btn btn-ghost" href="' + url + '">' + T.ficha + '</a></div></div>';
      var main = a.querySelector('img.main'), btns = a.querySelectorAll('.thumbs button');
      [].forEach.call(btns, function (bt, k) {
        bt.addEventListener('click', function () {
          main.src = '/' + b.slug + '-' + (k + 1) + '-m.jpg';
          [].forEach.call(btns, function (x) { x.className = ''; }); bt.className = 'on';
        });
      });
      return a;
    }
    var top = INV.boats.filter(function (b) { return b.status === 'available' && b.price > 0; })
      .sort(function (x, y) { return y.price - x.price; }).slice(0, MAX);
    if (!top.length) return;
    var have = {};
    [].forEach.call(grid.querySelectorAll('.boat[data-pm-boat]'), function (c) { have[c.getAttribute('data-pm-boat')] = c; });
    var frag = document.createDocumentFragment();
    top.forEach(function (b) { frag.appendChild(have[b.slug] || build(b)); delete have[b.slug]; });
    Object.keys(have).forEach(function (k) { have[k].parentNode.removeChild(have[k]); });
    grid.appendChild(frag);
    var VIEW = {es: 'Ver barco', ca: 'Veure el vaixell', en: 'View boat', fr: 'Voir le bateau'}[lang];
    [].forEach.call(grid.querySelectorAll('.boat'), function (c) {
      var dt = c.querySelectorAll('.specs dt'), dd = c.querySelectorAll('.specs dd');
      if (dd.length && !c.querySelector('.boat-meta')) {
        var parts = [dd[0].textContent, dd[1] ? dd[1].textContent : ''];
        [].forEach.call(dt, function (x, k) { if (/^(Ubicaci|Location|Emplacement|Localisation)/i.test(x.textContent.trim())) parts.push(dd[k].textContent); });
        var p = document.createElement('p'), h = c.querySelector('.boat-head');
        p.className = 'boat-meta'; p.textContent = parts.filter(Boolean).join(' · ');
        if (h) h.parentNode.insertBefore(p, h.nextSibling);
      }
      var g = c.querySelector('.boat-cta .btn-ghost'); if (g) g.textContent = VIEW;
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
