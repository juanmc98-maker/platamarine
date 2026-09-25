/* Plata Marine · inventario común (fuente única de estados y datos básicos de cartera).
   Lo usan: el cuestionario "Qué barco necesito" (ES/CA/EN) y la sincronización de estados
   en portada, catálogo y fichas (elementos con data-pm-boat).
   Al cambiar el estado de un barco aquí, actualizar también en la misma subida:
   su ficha en los 3 idiomas (JSON-LD "availability"), su tarjeta del catálogo (data-sold)
   y regenerar sus PDF (ES/CA/EN).
   status: "available" | "reserved" | "sold"
   title: titulación mínima (1 Licencia de Navegación, 2 PNB, 3 PER, 4 Patrón de Yate)
   types: tipos del cuestionario (open, sundeck, walkaround, cabinado, pilothouse, fly, rib, velero) */
(function () {
  'use strict';
  var INV = {
    updated: '2026-09-25',
    boats: [
      {slug: 'oceanis-50', name: 'Beneteau Oceanis 50', year: 2008, kind: 'vela', types: ['velero'], length: 14.75, price: 155000, zone: 'valencia', title: 3, status: 'available',
        d: {es: 'Aprox. 14,75 m · Yanmar 110 cv · La Pobla de Farnals (Valencia)', ca: 'Aprox. 14,75 m · Yanmar 110 cv · La Pobla de Farnals (València)', en: 'Approx. 14.75 m · Yanmar 110 hp · La Pobla de Farnals (Valencia)'}},
      {slug: 'sealine-365', name: 'Sealine 365', year: 1989, kind: 'motor', types: ['cabinado'], length: 11.1, price: 75000, zone: 'cataluna', title: 3, status: 'available',
        d: {es: '11,10 m · 2 x Volvo Penta 200 cv · Roda de Berà (Tarragona)', ca: '11,10 m · 2 x Volvo Penta 200 cv · Roda de Berà (Tarragona)', en: '11.10 m · 2 x Volvo Penta 200 hp · Roda de Berà (Tarragona)'}},
      {slug: 'monte-carlo-27', name: 'Beneteau Monte Carlo 27', year: 2008, kind: 'motor', types: ['cabinado', 'sundeck'], length: 7.98, price: 64900, zone: 'cataluna', title: 2, status: 'available',
        d: {es: '7,98 m · Volvo Penta 350 cv · Costa Brava', ca: '7,98 m · Volvo Penta 350 cv · Costa Brava', en: '7.98 m · Volvo Penta 350 hp · Costa Brava'}},
      {slug: 'van-de-stadt-36', name: 'Van de Stadt Zeehond 36', year: 1981, kind: 'vela', types: ['velero'], length: 12, price: 72000, zone: 'valencia', title: 3, status: 'available',
        d: {es: 'Aprox. 12 m · acero · Solé Mini 62 cv · Alicante', ca: 'Aprox. 12 m · acer · Solé Mini 62 cv · Alacant', en: 'Approx. 12 m · steel · Solé Mini 62 hp · Alicante'}},
      {slug: 'monterey-278-ss', name: 'Monterey 278 SS', year: 2011, kind: 'motor', types: ['sundeck', 'cabinado'], length: 8.4, price: 49990, zone: 'cataluna', title: 3, status: 'available',
        d: {es: '8,40 m · Volvo Penta 320 cv · Costa Brava', ca: '8,40 m · Volvo Penta 320 cv · Costa Brava', en: '8.40 m · Volvo Penta 320 hp · Costa Brava'}},
      {slug: 'faeton-730-moraga', name: 'Faeton 730 Moraga', year: 2005, kind: 'motor', types: ['pilothouse', 'walkaround'], length: 7.39, price: 30000, zone: 'baleares', title: 2, status: 'available',
        d: {es: '7,39 m · Volvo Penta 170 cv · Mallorca', ca: '7,39 m · Volvo Penta 170 cv · Mallorca', en: '7.39 m · Volvo Penta 170 hp · Mallorca'}},
      {slug: 'sacs-535', name: 'Sacs 535', year: 2002, kind: 'motor', types: ['rib'], length: 5.35, price: 25000, zone: 'baleares', title: 1, status: 'available',
        d: {es: '5,35 m · semirrígida · Suzuki 115 cv · Mallorca', ca: '5,35 m · semirígida · Suzuki 115 cv · Mallorca', en: '5.35 m · RIB · Suzuki 115 hp · Mallorca'}},
      {slug: 'ranieri-azzurra-5m', name: 'Ranieri Azzurra 5 m', year: 2004, kind: 'motor', types: ['open'], length: 5, price: 11990, zone: 'cataluna', title: 1, status: 'sold',
        d: {es: '5,00 m · Johnson 60 cv · Torredembarra', ca: '5,00 m · Johnson 60 cv · Torredembarra', en: '5.00 m · Johnson 60 hp · Torredembarra'}}
    ],
    label: {
      es: {available: 'Disponible', reserved: 'Reservado', sold: 'Vendido'},
      ca: {available: 'Disponible', reserved: 'Reservat', sold: 'Venut'},
      en: {available: 'Available', reserved: 'Reserved', sold: 'Sold'}
    },
    titleLabel: {
      es: ['Sin título', 'Licencia de Navegación o superior', 'PNB o superior', 'PER o superior', 'Patrón de Yate o superior'],
      ca: ['Sense títol', 'Llicència de Navegació o superior', 'PNB o superior', 'PER o superior', 'Patró de Iot o superior'],
      en: ['No licence', 'Navigation Licence or higher', 'PNB or higher', 'PER or higher', 'Yacht Skipper or higher']
    },
    sailLabel: {es: 'PER con prácticas de vela o superior', ca: 'PER amb pràctiques de vela o superior', en: 'PER with sailing practice or higher'},
    titleFor: function (b, lang) { return b.kind === 'vela' && b.title === 3 ? INV.sailLabel[lang] : INV.titleLabel[lang][b.title]; },
    lang: function () { var p = location.pathname; return p.indexOf('/ca/') === 0 ? 'ca' : p.indexOf('/en/') === 0 ? 'en' : 'es'; },
    get: function (slug) { for (var i = 0; i < INV.boats.length; i++) if (INV.boats[i].slug === slug) return INV.boats[i]; return null; },
    url: function (b, lang) { return (lang === 'es' ? '' : '/' + lang) + '/barcos/' + b.slug + '.html'; },
    available: function () { return INV.boats.filter(function (b) { return b.status === 'available'; }); }
  };
  window.PM_INV = INV;

  /* Red de seguridad: si el HTML de una tarjeta o ficha se quedó con un estado antiguo,
     se corrige al cargar con el estado de este inventario. */
  function sync() {
    var lang = INV.lang(), L = INV.label[lang];
    var els = document.querySelectorAll('[data-pm-boat]');
    for (var i = 0; i < els.length; i++) {
      var el = els[i], b = INV.get(el.getAttribute('data-pm-boat'));
      if (!b) continue;
      if (el.hasAttribute('data-sold')) el.setAttribute('data-sold', b.status === 'sold' ? '1' : '0');
      var st = el.querySelectorAll('.status,.boat-status');
      for (var j = 0; j < st.length; j++) {
        st[j].textContent = L[b.status];
        st[j].classList.toggle('available', b.status === 'available');
        st[j].classList.toggle('sold', b.status === 'sold');
      }
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', sync); else sync();
})();
