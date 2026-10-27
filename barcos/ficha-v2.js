/* Ficha v2: puntos sobre la foto e índice lateral. */
(function(){
  'use strict';
  var box = document.querySelector('.v2-spots');
  if (box) {
    var T = [];
    try { T = JSON.parse(box.getAttribute('data-spots')); } catch (e) {}
    var tip = document.createElement('div');
    tip.className = 'v2-tip'; tip.hidden = true; tip.setAttribute('role', 'status');
    box.appendChild(tip);
    var dots = box.querySelectorAll('.v2-dot');
    for (var i = 0; i < dots.length; i++) dots[i].addEventListener('click', function(){
      var d = this, open = d.getAttribute('aria-expanded') === 'true';
      for (var j = 0; j < dots.length; j++) dots[j].setAttribute('aria-expanded', 'false');
      if (open || !T[+d.getAttribute('data-t')]) { tip.hidden = true; return; }
      d.setAttribute('aria-expanded', 'true');
      var t = T[+d.getAttribute('data-t')];
      tip.innerHTML = ''; var b = document.createElement('b'); b.textContent = t[0]; tip.appendChild(b); tip.appendChild(document.createTextNode(t[1]));
      var l = parseFloat(d.style.left), tp = parseFloat(d.style.top);
      tip.style.top = 'calc(' + tp + '% + 24px)';
      if (l > 66) { tip.style.left = 'auto'; tip.style.right = '3%'; } else { tip.style.right = 'auto'; tip.style.left = Math.max(2, l - 6) + '%'; }
      tip.hidden = false;
    });
  }
  var side = document.querySelector('.v2-side');
  if (side && 'IntersectionObserver' in window) {
    var links = side.querySelectorAll('a');
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){
        if (!e.isIntersecting) return;
        for (var k = 0; k < links.length; k++) links[k].classList.toggle('on', links[k].getAttribute('href') === '#' + e.target.id);
        side.classList.toggle('dark', /v2-hero|v2-dark|v2-end/.test(e.target.className));
      });
    }, {rootMargin: '-45% 0px -50% 0px'});
    for (var k = 0; k < links.length; k++) { var s = document.getElementById(links[k].getAttribute('href').slice(1)); if (s) io.observe(s); }
  }
})();
/* Datos clave arriba de la ficha: se leen de la ficha técnica de la propia página (4 idiomas). */
(function(){
  'use strict';
  var hero = document.querySelector('.v2-hero'), dl = document.querySelector('dl.specs');
  if (!hero || !dl || document.querySelector('.v2-keybar')) return;
  var want = [
    [/^(Eslora|Eslora total|Length|Length overall|LOA|Longueur|Longueur hors tout)$/i, 1],
    [/^(Año|Any|Year|Année)$/i, 1],
    [/^(Motor|Motores|Motors|Engine|Engines|Moteur|Moteurs)$/i, 1],
    [/^(Horas|Hores|Hours|Heures)$/i, 1],
    [/^(Capacidad|Plazas|Capacitat|Places|Capacity|Capacité)$/i, 1],
    [/^(Titulación|Titulació|Licence|Permis)$/i, 0]
  ];
  var rows = dl.querySelectorAll(':scope > div'), out = [];
  want.forEach(function(w){
    for (var i = 0; i < rows.length; i++) {
      var dt = rows[i].querySelector('dt'), dd = rows[i].querySelector('dd');
      if (!dt || !dd || !w[0].test(dt.textContent.trim())) continue;
      var v = dd.textContent.replace(/\s+/g, ' ').trim().split(' (')[0].split(/,\s| · /)[0].trim();
      if (w[1] && !/\d/.test(v)) return;
      if (v.length > 34) v = v.slice(0, 33).replace(/\s+\S*$/, '') + '…';
      out.push([dt.textContent.trim(), v]); return;
    }
  });
  if (out.length < 3) return;
  var st = document.createElement('style');
  st.textContent = '.v2-keybar{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:0;margin:0 auto;padding:14px var(--pad,20px) 4px;max-width:var(--max,1120px)}.v2-keybar div{padding:8px 12px 8px 0;border-bottom:1px solid rgba(127,146,158,.25)}.v2-keybar span{display:block;font:600 11px/1.3 "Archivo","Helvetica Neue",Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#7F929E}.v2-keybar b{display:block;font:600 15px/1.35 "Archivo","Helvetica Neue",Arial,sans-serif;color:#0D1C27;margin-top:2px}';
  document.head.appendChild(st);
  var bar = document.createElement('div'); bar.className = 'v2-keybar';
  out.forEach(function(o){ var d = document.createElement('div'), s = document.createElement('span'), b = document.createElement('b'); s.textContent = o[0]; b.textContent = o[1]; d.appendChild(s); d.appendChild(b); bar.appendChild(d); });
  hero.parentNode.insertBefore(bar, hero.nextSibling);
})();
