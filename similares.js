/* Plata Marine · "Barcos parecidos" en fichas, fichas vendidas y páginas de modelo.
   Elige hasta 3 barcos DISPONIBLES del inventario común (inventario.js) del mismo tipo (motor/vela),
   de eslora parecida, de generación parecida (±12 años) y de presupuesto parecido (también en vendidos). El HTML estático (generado por
   _tools/build_similares.js) sirve de respaldo; este script lo refresca al cambiar la cartera.
   Si no hay ninguno, se muestra el aviso .pm-empty con el enlace a alertas (nunca un bloque vacío). */
(function () {
  'use strict';
  function pick(INV, ref) {
    return INV.available().filter(function (b) {
      if (b.slug === ref.slug) return false;
      if (ref.kind && b.kind !== ref.kind) return false;
      if (Math.abs(b.length - ref.len) > (ref.dl || 2.5)) return false;
      if (ref.price && (b.price < ref.price * 0.5 || b.price > ref.price * 2)) return false;
      if (ref.year && Math.abs(b.year - ref.year) > 12) return false;
      /* En fichas, mismo tipo de barco obligatorio (una semirrígida no es alternativa a un pilothouse). */
      if (ref.slug && ref.types && ref.types.length && !ref.types.some(function (t) { return (b.types || []).indexOf(t) >= 0; })) return false;
      return true;
    }).sort(function (a, b) {
      function s(x) {
        var shared = (ref.types || []).some(function (t) { return (x.types || []).indexOf(t) >= 0; });
        return Math.abs(x.length - ref.len) / ref.len + (ref.price ? Math.abs(x.price - ref.price) / ref.price : 0) + (ref.types && !shared ? 0.6 : 0) + (ref.year ? Math.abs(x.year - ref.year) / 20 : 0);
      }
      return s(a) - s(b);
    }).slice(0, 3);
  }
  function run() {
    var INV = window.PM_INV;
    if (!INV) return;
    var lang = INV.lang();
    var T = {es: 'Ver ficha', ca: 'Veure fitxa', en: 'See details', fr: 'Voir la fiche'}[lang];
    var IMG = {'ranieri-azzurra-5m': '/ranieri-azzurra-1.jpg'};
    function price(n) { var s = String(n).replace(/\B(?=(\d{3})+(?!\d))/g, lang === 'en' ? ',' : lang === 'fr' ? '\u202f' : '.'); return lang === 'en' ? '€' + s : s + ' €'; }
    function esc(s) { return String(s).replace(/[&<>"]/g, function (m) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[m]; }); }
    [].forEach.call(document.querySelectorAll('.pm-sim[data-ref]'), function (box) {
      var ref = {};
      try { ref = JSON.parse(box.getAttribute('data-ref')); } catch (e) { return; }
      if (ref.slug) {
        var me = INV.get(ref.slug);
        /* El precio de un vendido no se muestra en ningún sitio, pero se usa como presupuesto de referencia
           para no recomendar barcos de otro segmento (6 oct 2026). */
        if (me) { ref.kind = me.kind; ref.len = me.length; ref.price = me.price; ref.types = me.types; ref.year = me.year; }
      }
      if (!ref.len) return;
      var list = pick(INV, ref);
      var empty = box.parentNode.querySelector('.pm-empty');
      if (empty) {
        empty.hidden = list.length > 0;
        /* Sin alternativa razonable: la alerta se abre ya rellenada con los datos de este barco. */
        var al = empty.querySelector('a[href*="/alertas/"]');
        if (al && ref.slug && al.getAttribute('href').indexOf('?ref=') < 0) al.setAttribute('href', al.getAttribute('href') + '?ref=' + encodeURIComponent(ref.slug));
      }
      box.hidden = list.length === 0;
      box.innerHTML = list.map(function (b) {
        var u = INV.url(b, lang), img = (IMG[b.slug] || '/' + b.slug + '-1.jpg').replace(/\.jpg$/, '');
        return '<a class="pcard" href="' + u + '"><img src="' + img + '-m.jpg" srcset="' + img + '-m.jpg 1000w, ' + img + '.jpg 1600w" sizes="(max-width: 640px) 100vw, 360px" alt="' + esc(b.name) + '" loading="lazy" width="1600" height="900">' +
          '<span class="pc-b"><strong>' + esc(b.name) + '</strong><span class="pc-p">' + price(b.price) + (b.vat ? ' <span class="vat">' + (lang === 'en' ? '+VAT' : lang === 'fr' ? '+TVA' : '+IVA') + '</span>' : '') + '</span>' +
          '<span class="pc-d">' + b.year + ' · ' + esc(b.d[lang]) + '</span><span class="pc-t">' + esc(INV.titleFor(b, lang)) + '</span>' +
          '<span class="pc-l">' + T + ' →</span></span></a>';
      }).join('');
    });
  }
  window.PM_SIM_PICK = pick;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
