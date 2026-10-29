/* Carrusel de marcas de la portada (ES/CA/EN/FR).
   Para añadir una marca: una línea más en MARCAS (logo en blanco con fondo transparente, h = alto en px). */
(function () {
  'use strict';
  var MARCAS = [
    { slug: 'skipper',   name: 'SKIPPER Powerboats',           logo: '/skipper/fotos/skipper-logo-blanco.png',       h: 22 },
    { slug: 'klasea',    name: 'Klase A',                      logo: '/barcos-nuevos/logos/klasea-blanco.png',       h: 48 },
    { slug: 'marco',     name: 'Mar.Co',                       logo: '/barcos-nuevos/logos/marco-blanco.png',        h: 40 },
    { slug: 'catharsis', name: 'Catharsis (Avila Marin)',      logo: '/barcos-nuevos/logos/avila-marin-blanco.png',  h: 54 },
    { slug: 'kattum',    name: 'Kattum Yachts',                logo: '/barcos-nuevos/logos/kattum-blanco.png',       h: 40 },
    { slug: 'squama',    name: 'Squama (Pičuljan Pro-Nautic)', logo: '/barcos-nuevos/logos/piculjan-blanco.png',     h: 34 },
    { slug: 'seastorm',  name: 'SeaStorm',                     logo: '/seastorm/fotos/seastorm-logo.png',            h: 18 }
  ];
  var box = document.querySelector('[data-marcas]');
  if (!box) return;
  var lang = (document.documentElement.lang || 'es').slice(0, 2);
  var pre = (lang === 'es') ? '' : '/' + lang;
  function lista(oculta) {
    var ul = document.createElement('ul');
    ul.className = 'pmb-set';
    if (oculta) ul.setAttribute('aria-hidden', 'true');
    MARCAS.forEach(function (m) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = pre + '/' + m.slug + '/';
      if (oculta) a.tabIndex = -1;
      var img = document.createElement('img');
      img.src = m.logo; img.alt = oculta ? '' : m.name; img.style.height = m.h + 'px';
      img.loading = 'lazy'; img.decoding = 'async';
      a.appendChild(img); li.appendChild(a); ul.appendChild(li);
    });
    return ul;
  }
  var track = document.createElement('div');
  track.className = 'pmb-track';
  // Cada mitad del carrusel repite la lista hasta tener al menos 10 logos, para que no queden huecos en pantallas anchas
  var rep = Math.max(1, Math.ceil(10 / MARCAS.length));
  for (var i = 0; i < rep * 2; i++) track.appendChild(lista(i > 0));
  track.style.animationDuration = (MARCAS.length * rep * 4) + 's';
  box.innerHTML = '';
  box.appendChild(track);
})();
