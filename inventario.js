/* Plata Marine · inventario común (fuente única de estados y datos básicos de cartera).
   Lo usan: el cuestionario "Qué barco necesito" (ES/CA/EN/FR) y la sincronización de estados
   en portada, catálogo y fichas (elementos con data-pm-boat).
   Al cambiar el estado de un barco aquí, actualizar también en la misma subida:
   su ficha en los 4 idiomas (JSON-LD "availability"), su tarjeta del catálogo (data-sold)
   y regenerar sus PDF (ES/CA/EN/FR).
   status: "available" | "reserved" | "sold"
   title: titulación mínima (1 Licencia de Navegación, 2 PNB, 3 PER, 4 Patrón de Yate)
   types: tipos del cuestionario (open, sundeck, walkaround, cabinado, pilothouse, fly, rib, velero) */
(function () {
  'use strict';
  var INV = {
    updated: '2026-09-30',
    boats: [
      {slug: 'antares-12-fly', name: 'Beneteau Antares 12 Fly', year: 2024, kind: 'motor', types: ['fly', 'cabinado'], length: 12.9, price: 499000, zone: 'cataluna', area: 'costa-daurada', title: 3, status: 'sold',
        d: {es: '12,9 m · 2 x Mercury 400 XL · Costa Daurada (Tarragona)', ca: '12,9 m · 2 x Mercury 400 XL · Costa Daurada (Tarragona)', en: '12.9 m · twin Mercury 400 XL · Costa Daurada (Tarragona)', fr: '12,9 m · 2 x Mercury 400 XL · Costa Daurada (Tarragone)'}},
      {slug: 'prestige-32', name: 'Jeanneau Prestige 32', year: 2006, kind: 'motor', types: ['fly', 'cabinado'], length: 10.65, price: 89000, zone: 'baleares', area: 'menorca', title: 3, status: 'available',
        d: {es: '10,65 m · Volvo Penta D4 260 cv · Menorca', ca: '10,65 m · Volvo Penta D4 260 cv · Menorca', en: '10.65 m · Volvo Penta D4 260 hp · Menorca', fr: '10,65 m · Volvo Penta D4 260 ch · Minorque'}},
      {slug: 'gallart-1050', name: 'Gallart 10.50 Fly', year: 1977, kind: 'motor', types: ['fly', 'cabinado'], length: 9.58, price: 29900, zone: 'cataluna', area: 'costa-brava', title: 3, status: 'available',
        d: {es: '9,58 m · 2 x Volvo Penta 192 cv · Costa Brava (Girona)', ca: '9,58 m · 2 x Volvo Penta 192 cv · Costa Brava (Girona)', en: '9.58 m · twin Volvo Penta 192 hp · Costa Brava (Girona)', fr: '9,58 m · 2 x Volvo Penta 192 ch · Costa Brava (Gérone)'}},
      {slug: 'tiger-marine-650', name: 'Tiger Marine Top Line 650', year: 2015, kind: 'motor', types: ['rib'], length: 6.5, price: 33000, zone: 'cataluna', area: 'costa-daurada', title: 2, status: 'available',
        d: {es: 'Aprox. 6,50 m · semirrígida · Suzuki 150 cv · Costa Daurada (Tarragona)', ca: 'Aprox. 6,50 m · semirígida · Suzuki 150 cv · Costa Daurada (Tarragona)', en: 'Approx. 6.50 m · RIB · Suzuki 150 hp · Costa Daurada (Tarragona)', fr: 'Env. 6,50 m · semi-rigide · Suzuki 150 ch · Costa Daurada (Tarragone)'}},
      {slug: 'oceanis-50', name: 'Beneteau Oceanis 50', year: 2008, kind: 'vela', types: ['velero'], length: 14.75, price: 155000, zone: 'valencia', title: 3, status: 'available',
        d: {es: 'Aprox. 14,75 m · Yanmar 110 cv · Valencia', ca: 'Aprox. 14,75 m · Yanmar 110 cv · València', en: 'Approx. 14.75 m · Yanmar 110 hp · Valencia', fr: 'Env. 14,75 m · Yanmar 110 ch · Valence'}},
      {slug: 'sealine-365', name: 'Sealine 365 Sport Bridge', year: 1989, kind: 'motor', types: ['cabinado'], length: 11.1, price: 75000, zone: 'cataluna', area: 'costa-daurada', title: 3, status: 'available',
        d: {es: '11,10 m · 2 x Volvo Penta 200 cv · Costa Daurada (Tarragona)', ca: '11,10 m · 2 x Volvo Penta 200 cv · Costa Daurada (Tarragona)', en: '11.10 m · 2 x Volvo Penta 200 hp · Costa Daurada (Tarragona)', fr: '11,10 m · 2 x Volvo Penta 200 ch · Costa Daurada (Tarragone)'}},
      {slug: 'cattleya-x6', name: 'Cattleya X6', year: 2021, kind: 'motor', types: ['open', 'sundeck'], length: 5.98, price: 55000, vat: true, zone: 'baleares', area: 'ibiza', title: 1, status: 'available',
        d: {es: '5,98 m · Tohatsu 150 cv, nuevo 2026 · Ibiza', ca: '5,98 m · Tohatsu 150 cv, nou 2026 · Eivissa', en: '5.98 m · Tohatsu 150 hp, new 2026 · Ibiza', fr: '5,98 m · Tohatsu 150 ch, neuf 2026 · Ibiza'}},
      {slug: 'monte-carlo-27', name: 'Beneteau Monte Carlo 27', year: 2008, kind: 'motor', types: ['cabinado', 'sundeck'], length: 7.98, price: 64900, zone: 'cataluna', area: 'costa-brava', title: 2, status: 'available',
        d: {es: '7,98 m · Volvo Penta 350 cv · Costa Brava', ca: '7,98 m · Volvo Penta 350 cv · Costa Brava', en: '7.98 m · Volvo Penta 350 hp · Costa Brava', fr: '7,98 m · Volvo Penta 350 ch · Costa Brava'}},
      {slug: 'van-de-stadt-36', name: 'Van de Stadt Zeehond 36', year: 1981, kind: 'vela', types: ['velero'], length: 12, price: 72000, zone: 'valencia', title: 3, status: 'available',
        d: {es: 'Aprox. 12 m · acero · Solé Mini 62 cv · Alicante', ca: 'Aprox. 12 m · acer · Solé Mini 62 cv · Alacant', en: 'Approx. 12 m · steel · Solé Mini 62 hp · Alicante', fr: 'Env. 12 m · acier · Solé Mini 62 ch · Alicante'}},
      {slug: 'monterey-278-ss', name: 'Monterey 278 SS', year: 2011, kind: 'motor', types: ['sundeck', 'cabinado'], length: 8.4, price: 49990, zone: 'cataluna', area: 'costa-brava', title: 3, status: 'available',
        d: {es: '8,40 m · Volvo Penta 320 cv · Costa Brava', ca: '8,40 m · Volvo Penta 320 cv · Costa Brava', en: '8.40 m · Volvo Penta 320 hp · Costa Brava', fr: '8,40 m · Volvo Penta 320 ch · Costa Brava'}},
      {slug: 'faeton-730-moraga', name: 'Faeton 730 Moraga', year: 2005, kind: 'motor', types: ['pilothouse', 'walkaround'], length: 7.39, price: 28900, zone: 'baleares', title: 2, status: 'available',
        d: {es: '7,39 m · Volvo Penta 170 cv · Mallorca', ca: '7,39 m · Volvo Penta 170 cv · Mallorca', en: '7.39 m · Volvo Penta 170 hp · Mallorca', fr: '7,39 m · Volvo Penta 170 ch · Majorque'}},
      {slug: 'faeton-730-top-moraga', name: 'Faeton 730 Top Moraga', year: 2003, kind: 'motor', types: ['pilothouse'], length: 7.39, price: 24000, zone: 'baleares', title: 2, status: 'available',
        d: {es: '7,39 m · Volvo Penta 150 cv · Mallorca', ca: '7,39 m · Volvo Penta 150 cv · Mallorca', en: '7.39 m · Volvo Penta 150 hp · Mallorca', fr: '7,39 m · Volvo Penta 150 ch · Majorque'}},
      {slug: 'starfisher-840', name: 'Starfisher 840 R', year: 2004, kind: 'motor', types: ['pilothouse', 'cabinado'], length: 8.4, price: 50900, zone: 'galicia', title: 3, status: 'available',
        d: {es: 'Aprox. 8,40 m · 2 x Yanmar 200 cv · Galicia', ca: 'Aprox. 8,40 m · 2 x Yanmar 200 cv · Galícia', en: 'Approx. 8.40 m · twin Yanmar 200 hp · Galicia', fr: 'Env. 8,40 m · 2 x Yanmar 200 ch · Galice'}},
      {slug: 'sacs-535', name: 'Sacs 535', year: 2002, kind: 'motor', types: ['rib'], length: 5.35, price: 25000, zone: 'baleares', title: 1, status: 'available',
        d: {es: '5,35 m · semirrígida · Suzuki 115 cv · Mallorca', ca: '5,35 m · semirígida · Suzuki 115 cv · Mallorca', en: '5.35 m · RIB · Suzuki 115 hp · Mallorca', fr: '5,35 m · semi-rigide · Suzuki 115 ch · Majorque'}},
      {slug: 'ranieri-azzurra-5m', name: 'Ranieri Azzurra 5 m', year: 2004, kind: 'motor', types: ['open'], length: 5, price: 11990, zone: 'cataluna', area: 'costa-daurada', title: 1, status: 'sold',
        d: {es: '5,00 m · Johnson 60 cv · Costa Daurada', ca: '5,00 m · Johnson 60 cv · Costa Daurada', en: '5.00 m · Johnson 60 hp · Costa Daurada', fr: '5,00 m · Johnson 60 ch · Costa Daurada'}}
    ],
    label: {
      es: {available: 'Disponible', reserved: 'Reservado', sold: 'Vendido'},
      ca: {available: 'Disponible', reserved: 'Reservat', sold: 'Venut'},
      en: {available: 'Available', reserved: 'Reserved', sold: 'Sold'},
      fr: {available: 'Disponible', reserved: 'Réservé', sold: 'Vendu'}
    },
    titleLabel: {
      es: ['Sin título', 'Licencia de Navegación o superior', 'PNB o superior', 'PER o superior', 'Patrón de Yate o superior'],
      ca: ['Sense títol', 'Llicència de Navegació o superior', 'PNB o superior', 'PER o superior', 'Patró de Iot o superior'],
      en: ['No licence', 'Navigation Licence or higher', 'PNB or higher', 'PER or higher', 'Yacht Skipper or higher'],
      fr: ['Sans permis', 'Licencia de Navegación ou supérieur', 'PNB ou supérieur', 'PER ou supérieur', 'Patrón de Yate ou supérieur']
    },
    sailLabel: {es: 'PER con prácticas de vela o superior', ca: 'PER amb pràctiques de vela o superior', en: 'PER with sailing practice or higher', fr: 'PER avec pratiques de voile ou supérieur'},
    titleFor: function (b, lang) { return b.kind === 'vela' && b.title === 3 ? INV.sailLabel[lang] : INV.titleLabel[lang][b.title]; },
    lang: function () { var p = location.pathname; return p.indexOf('/ca/') === 0 ? 'ca' : p.indexOf('/en/') === 0 ? 'en' : p.indexOf('/fr/') === 0 ? 'fr' : 'es'; },
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
  /* Mensajes de WhatsApp según el estado (6 oct 2026): en una ficha reservada o vendida, ningún enlace
     debe preparar un mensaje que la describa como disponible. Se reescriben los enlaces wa.me que nombran al barco. */
  var WA = {
    reserved: {
      es: function (b) { return 'Hola Juan, he visto que el ' + b.name + ' de ' + b.year + ' está reservado. Si la reserva no sigue adelante, ¿me avisas? Y si tienes algo parecido, también me interesa.'; },
      ca: function (b) { return 'Hola Juan, he vist que el ' + b.name + ' del ' + b.year + ' està reservat. Si la reserva no tira endavant, m\'avises? I si tens alguna cosa semblant, també m\'interessa.'; },
      en: function (b) { return 'Hi Juan, I see the ' + b.year + ' ' + b.name + ' is reserved. If the reservation falls through, could you let me know? I\'m also interested in anything similar.'; },
      fr: function (b) { return 'Bonjour Juan, je vois que le ' + b.name + ' de ' + b.year + ' est réservé. Si la réservation n\'aboutit pas, pouvez-vous me prévenir ? Je suis aussi intéressé par quelque chose de similaire.'; }
    },
    sold: {
      es: function (b) { return 'Hola Juan, he visto la ficha del ' + b.name + ' de ' + b.year + ', que ya está vendido. Busco algo parecido, ¿me ayudas?'; },
      ca: function (b) { return 'Hola Juan, he vist la fitxa del ' + b.name + ' del ' + b.year + ', que ja està venut. Busco alguna cosa semblant, m\'ajudes?'; },
      en: function (b) { return 'Hi Juan, I saw the listing for the ' + b.year + ' ' + b.name + ', which is already sold. I\'m looking for something similar, can you help?'; },
      fr: function (b) { return 'Bonjour Juan, j\'ai vu la fiche du ' + b.name + ' de ' + b.year + ', déjà vendu. Je cherche quelque chose de similaire, pouvez-vous m\'aider ?'; }
    }
  };
  function waByStatus() {
    var m = location.pathname.match(/\/barcos\/([a-z0-9-]+)\.html$/);
    var b = m && INV.get(m[1]);
    if (!b || !WA[b.status]) return;
    var text = encodeURIComponent(WA[b.status][INV.lang()](b));
    var links = document.querySelectorAll('a[href*="wa.me/34633742973"]');
    for (var i = 0; i < links.length; i++) {
      var h = links[i].getAttribute('href'), q = h.indexOf('?text=');
      if (q < 0) continue;
      var t = ''; try { t = decodeURIComponent(h.slice(q + 6)); } catch (e) { continue; }
      if (t.indexOf(b.name) < 0 && t.indexOf(b.name.replace(/^\S+\s/, '')) < 0) continue;
      links[i].setAttribute('href', h.slice(0, q) + '?text=' + text);
    }
  }
  INV.waText = function (b, lang) { return WA[b.status] ? WA[b.status][lang](b) : null; };
  function boot() { sync(); waByStatus(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
