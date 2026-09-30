/* Plata Marine · listas de barcos en las páginas de compra (/comprar/).
   Pinta los barcos disponibles del inventario común (inventario.js) según el filtro de cada página,
   para que se actualicen solos al cambiar la cartera. El HTML estático sirve de respaldo. */
(function () {
  'use strict';
  function run() {
    var INV = window.PM_INV;
    if (!INV) return;
    var lang = INV.lang();
    var IMG = {'ranieri-azzurra-5m': '/ranieri-azzurra-1.jpg'};
    var T = {es: {see: 'Ver ficha'}, ca: {see: 'Veure fitxa'}, en: {see: 'See details'}}[lang];
    function price(n) { var s = String(n).replace(/\B(?=(\d{3})+(?!\d))/g, lang === 'en' ? ',' : '.'); return lang === 'en' ? '€' + s : s + ' €'; }
    function esc(s) { return String(s).replace(/[&<>"]/g, function (m) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[m]; }); }
    [].forEach.call(document.querySelectorAll('.pm-list[data-f]'), function (box) {
      var f = {};
      try { f = JSON.parse(box.getAttribute('data-f')); } catch (e) {}
      var list = INV.available().filter(function (b) {
        if (f.zone && b.zone !== f.zone) return false;
        if (f.area && b.area !== f.area) return false;
        if (f.kind && b.kind !== f.kind) return false;
        if (f.maxTitle && b.title > f.maxTitle) return false;
        if (f.q && !new RegExp(f.q, 'i').test(b.name)) return false;
        return true;
      }).sort(function (a, b) { return (b.price || 0) - (a.price || 0); });
      var empty = box.parentNode.querySelector('.pm-empty');
      if (empty) empty.hidden = list.length > 0;
      box.innerHTML = list.map(function (b) {
        var u = INV.url(b, lang), img = (IMG[b.slug] || '/' + b.slug + '-1.jpg').replace(/\.jpg$/, '');
        return '<a class="pcard" href="' + u + '"><img src="' + img + '-m.jpg" srcset="' + img + '-m.jpg 1000w, ' + img + '.jpg 1600w" sizes="(max-width: 640px) 100vw, 360px" alt="' + esc(b.name) + '" loading="lazy" width="1600" height="900">' +
          '<span class="pc-b"><strong>' + esc(b.name) + '</strong><span class="pc-p">' + price(b.price) + '</span>' +
          '<span class="pc-d">' + b.year + ' · ' + esc(b.d[lang]) + '</span><span class="pc-t">' + esc(INV.titleFor(b, lang)) + '</span>' +
          '<span class="pc-l">' + T.see + ' →</span></span></a>';
      }).join('');
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
