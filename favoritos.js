/* Plata Marine · barcos guardados y comparador (catálogo ES/CA/EN).
   Guarda los slugs en localStorage (solo en el navegador del visitante; no se envía a ningún sitio). */
(function () {
  'use strict';
  var grid = document.querySelector('.bgrid');
  if (!grid) return;
  var lang = (document.documentElement.lang || 'es').slice(0, 2);
  var T = {
    es: {save: 'Guardar para comparar', saved: 'Guardado', bar: '{n} guardados', bar1: '1 guardado', cmp: 'Comparar', clear: 'Vaciar', close: 'Cerrar', title: 'Tus barcos guardados', one: 'Guarda al menos dos barcos para compararlos.', price: 'Precio', year: 'Año', len: 'Eslora', type: 'Tipo', fuel: 'Combustible', eng: 'Motor', hrs: 'Horas', zone: 'Zona', lic: 'Titulación', see: 'Ver ficha', rm: 'Quitar', motor: 'Motor', vela: 'Vela', diesel: 'Diésel', gasolina: 'Gasolina', note: 'Se guardan solo en este navegador.'},
    ca: {save: 'Desar per comparar', saved: 'Desat', bar: '{n} desats', bar1: '1 desat', cmp: 'Comparar', clear: 'Buidar', close: 'Tancar', title: 'Els teus vaixells desats', one: 'Desa almenys dos vaixells per comparar-los.', price: 'Preu', year: 'Any', len: 'Eslora', type: 'Tipus', fuel: 'Combustible', eng: 'Motor', hrs: 'Hores', zone: 'Zona', lic: 'Titulació', see: 'Veure fitxa', rm: 'Treure', motor: 'Motor', vela: 'Vela', diesel: 'Dièsel', gasolina: 'Gasolina', note: 'Només es desen en aquest navegador.'},
    en: {save: 'Save to compare', saved: 'Saved', bar: '{n} saved', bar1: '1 saved', cmp: 'Compare', clear: 'Clear', close: 'Close', title: 'Your saved boats', one: 'Save at least two boats to compare them.', price: 'Price', year: 'Year', len: 'Length', type: 'Type', fuel: 'Fuel', eng: 'Engine', hrs: 'Hours', zone: 'Area', lic: 'Licence', see: 'See details', rm: 'Remove', motor: 'Motor', vela: 'Sail', diesel: 'Diesel', gasolina: 'Petrol', note: 'Saved in this browser only.'}
  }[lang] || null;
  if (!T) return;
  var KEY = 'pm_favs';
  function load() { try { var v = JSON.parse(localStorage.getItem(KEY) || '[]'); return Array.isArray(v) ? v : []; } catch (e) { return []; } }
  function store(a) { try { localStorage.setItem(KEY, JSON.stringify(a)); } catch (e) {} }
  var favs = load();
  var cards = [].slice.call(grid.querySelectorAll('.bcard[data-pm-boat]'));
  favs = favs.filter(function (s) { return cards.some(function (c) { return c.getAttribute('data-pm-boat') === s; }); });

  var css = document.createElement('style');
  css.textContent = '.bcard{position:relative}' +
    '.pmfav{position:absolute;top:10px;right:10px;z-index:2;width:40px;height:40px;border-radius:50%;border:0;background:rgba(255,255,255,.92);box-shadow:0 1px 4px rgba(0,0,0,.18);cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0}' +
    '.pmfav svg{width:20px;height:20px;fill:none;stroke:#0d1c27;stroke-width:2}.pmfav[aria-pressed="true"] svg{fill:#C8322B;stroke:#C8322B}' +
    '.pmbar{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:50;background:#0d1c27;color:#fff;border-radius:999px;padding:8px 8px 8px 18px;display:flex;gap:10px;align-items:center;box-shadow:0 4px 18px rgba(0,0,0,.25);font-family:var(--display,inherit);font-size:.92rem;max-width:calc(100% - 32px)}' +
    '.pmbar[hidden]{display:none}.pmbar button{font:inherit;border:0;border-radius:999px;padding:8px 14px;cursor:pointer}.pmbar .go{background:#fff;color:#0d1c27;font-weight:600}.pmbar .clr{background:transparent;color:#D5DDE2;text-decoration:underline;padding:8px 6px}' +
    '.pmcmp{position:fixed;inset:0;z-index:60;background:rgba(13,28,39,.55);display:flex;align-items:flex-start;justify-content:center;padding:24px 12px;overflow:auto}.pmcmp[hidden]{display:none}' +
    '.pmcmp .in{background:#fff;color:#0d1c27;border-radius:10px;max-width:1000px;width:100%;padding:18px;font-family:var(--display,inherit)}' +
    '.pmcmp .hd{display:flex;justify-content:space-between;align-items:center;gap:12px;margin:0 0 12px}.pmcmp h2{font-size:1.15rem;margin:0}.pmcmp .x{font:inherit;border:1px solid rgba(127,146,158,.45);background:#fff;border-radius:999px;padding:6px 14px;cursor:pointer}' +
    '.pmcmp .sc{overflow-x:auto;-webkit-overflow-scrolling:touch}.pmcmp table{border-collapse:collapse;font-size:14px;min-width:100%}' +
    '.pmcmp th,.pmcmp td{padding:8px 10px;border-bottom:1px solid #e3e8eb;text-align:left;vertical-align:top;min-width:150px}.pmcmp th{color:#5b6b76;font-weight:600;min-width:90px;position:sticky;left:0;background:#fff}' +
    '.pmcmp img{width:100%;max-width:220px;aspect-ratio:16/9;object-fit:cover;border-radius:6px;display:block;margin:0 0 6px}.pmcmp .nm{font-weight:600}.pmcmp .rm{font:inherit;font-size:12px;background:none;border:0;color:#5b6b76;text-decoration:underline;cursor:pointer;padding:0}' +
    '.pmcmp .nt{font-size:12px;color:#5b6b76;margin:10px 0 0}';
  document.head.appendChild(css);

  var heart = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7.5-4.6-9.5-9.2C1.1 8.4 3.2 5 6.6 5c2 0 3.4 1.1 4.2 2.4h2.4C14 6.1 15.4 5 17.4 5c3.4 0 5.5 3.4 4.1 6.8C19.5 16.4 12 21 12 21z"/></svg>';
  cards.forEach(function (c) {
    var s = c.getAttribute('data-pm-boat'), b = document.createElement('button');
    b.type = 'button'; b.className = 'pmfav'; b.innerHTML = heart;
    b.setAttribute('data-slug', s);
    b.addEventListener('click', function () { toggle(s); });
    c.appendChild(b);
  });

  var bar = document.createElement('div');
  bar.className = 'pmbar'; bar.hidden = true;
  bar.innerHTML = '<span class="n"></span><button type="button" class="go">' + T.cmp + '</button><button type="button" class="clr">' + T.clear + '</button>';
  document.body.appendChild(bar);
  bar.querySelector('.go').addEventListener('click', openCmp);
  bar.querySelector('.clr').addEventListener('click', function () { favs = []; store(favs); render(); });

  var modal = document.createElement('div');
  modal.className = 'pmcmp'; modal.hidden = true; modal.setAttribute('role', 'dialog'); modal.setAttribute('aria-modal', 'true'); modal.setAttribute('aria-label', T.title);
  document.body.appendChild(modal);
  modal.addEventListener('click', function (e) { if (e.target === modal) closeCmp(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !modal.hidden) closeCmp(); });

  function toggle(s) {
    var i = favs.indexOf(s);
    if (i < 0) { favs.push(s); try { window.pmTrack && window.pmTrack('save_boat', {boat: s}); } catch (e) {} } else favs.splice(i, 1);
    store(favs); render();
  }
  function render() {
    cards.forEach(function (c) {
      var b = c.querySelector('.pmfav'), on = favs.indexOf(c.getAttribute('data-pm-boat')) >= 0;
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      b.setAttribute('aria-label', (on ? T.saved : T.save) + ': ' + (c.querySelector('h2') || {}).textContent);
      b.title = on ? T.saved : T.save;
    });
    bar.hidden = favs.length === 0;
    bar.querySelector('.n').textContent = favs.length === 1 ? T.bar1 : T.bar.replace('{n}', favs.length);
    if (!modal.hidden) fill();
  }
  function info(c) {
    var sub = ((c.querySelector('.sub') || {}).textContent || '').split(' · ');
    var hrs = '', eng = '';
    sub.forEach(function (p) { if (/\d\s?h$/.test(p.trim())) hrs = p.trim(); else if (/(cv|hp)\b/i.test(p)) eng = p.trim(); });
    var len = ''; sub.forEach(function (p) { if (/\d\s?m$/.test(p.trim()) && !len) len = p.trim(); });
    var a = c.querySelector('h2 a'), img = c.querySelector('img'), st = c.querySelector('.status');
    return {
      name: a ? a.textContent : '', href: a ? a.getAttribute('href') : '#', img: img ? img.getAttribute('src') : '',
      price: ((c.querySelector('.price') || {}).textContent || ''), year: c.dataset.anyo || '', len: len,
      type: T[c.dataset.tipo] || '', fuel: T[c.dataset.comb] || '', eng: eng, hrs: hrs, zone: sub.length > 1 ? sub[sub.length - 1].trim() : '',
      lic: ((c.querySelector('.tbadge') || {}).textContent || '').replace(/^[^:]*:\s*/, ''), status: st ? st.textContent : ''
    };
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (m) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[m]; }); }
  function fill() {
    var list = favs.map(function (s) { for (var i = 0; i < cards.length; i++) if (cards[i].getAttribute('data-pm-boat') === s) return [s, info(cards[i])]; return null; }).filter(Boolean);
    var h = '<div class="hd"><h2>' + T.title + '</h2><button type="button" class="x">' + T.close + '</button></div>';
    if (list.length < 2) h += '<p>' + T.one + '</p>';
    if (list.length) {
      var rows = [['', function (d, s) { return '<img src="' + esc(d.img) + '" alt=""><a class="nm" href="' + esc(d.href) + '">' + esc(d.name) + '</a><br><button type="button" class="rm" data-slug="' + esc(s) + '">' + T.rm + '</button>'; }],
        [T.price, 'price'], [T.year, 'year'], [T.len, 'len'], [T.type, 'type'], [T.eng, 'eng'], [T.hrs, 'hrs'], [T.fuel, 'fuel'], [T.zone, 'zone'], [T.lic, 'lic'],
        ['', function (d) { return '<a href="' + esc(d.href) + '">' + T.see + ' →</a>'; }]];
      h += '<div class="sc"><table>' + rows.map(function (r) {
        return '<tr><th scope="row">' + r[0] + '</th>' + list.map(function (x) { return '<td>' + (typeof r[1] === 'function' ? r[1](x[1], x[0]) : esc(x[1][r[1]] || '–')) + '</td>'; }).join('') + '</tr>';
      }).join('') + '</table></div>';
    }
    h += '<p class="nt">' + T.note + '</p>';
    modal.innerHTML = '<div class="in">' + h + '</div>';
    modal.querySelector('.x').addEventListener('click', closeCmp);
    [].forEach.call(modal.querySelectorAll('.rm'), function (b) { b.addEventListener('click', function () { toggle(b.getAttribute('data-slug')); }); });
  }
  var last = null;
  function openCmp() { last = document.activeElement; fill(); modal.hidden = false; document.body.style.overflow = 'hidden'; var x = modal.querySelector('.x'); if (x) x.focus(); }
  function closeCmp() { modal.hidden = true; document.body.style.overflow = ''; if (last && last.focus) last.focus(); }
  render();
})();
