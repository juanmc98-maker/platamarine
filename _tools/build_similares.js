// Plata Marine · inserta/actualiza el bloque "Barcos parecidos" (ES/CA/EN) en:
//  - cada ficha de /barcos/ (disponibles y vendidas), antes de </main>
//  - cada página de /modelos/ (antes de "Título, impuestos y gastos fijos")
//  - el botón "Ver similares" en las tarjetas vendidas del catálogo
// Idempotente: sustituye lo que haya entre <!--pm-sim--> y <!--/pm-sim-->.
// Uso: node _tools/build_similares.js  (desde la raíz del repo)
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
global.window = {}; global.location = {pathname: '/'};
global.document = {readyState: 'complete', querySelectorAll: () => []};
eval(fs.readFileSync(path.join(ROOT, 'inventario.js'), 'utf8'));
eval(fs.readFileSync(path.join(ROOT, 'similares.js'), 'utf8'));
const INV = window.PM_INV, pick = window.PM_SIM_PICK;
const LANGS = ['es', 'ca', 'en'];
const pre = l => (l === 'es' ? '' : '/' + l);
const esc = s => String(s).replace(/[&<>"]/g, m => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[m]));
const IMG = {'ranieri-azzurra-5m': '/ranieri-azzurra-1.jpg'};
const price = (n, l) => { const s = String(n).replace(/\B(?=(\d{3})+(?!\d))/g, l === 'en' ? ',' : '.'); return l === 'en' ? '€' + s : s + ' €'; };
const card = (b, l) => {
  const img = (IMG[b.slug] || '/' + b.slug + '-1.jpg').replace(/\.jpg$/, '');
  return `<a class="pcard" href="${INV.url(b, l)}"><img src="${img}-m.jpg" srcset="${img}-m.jpg 1000w, ${img}.jpg 1600w" sizes="(max-width: 640px) 100vw, 360px" alt="${esc(b.name)}" loading="lazy" width="1600" height="900"><span class="pc-b"><strong>${esc(b.name)}</strong><span class="pc-p">${price(b.price, l)}${b.vat ? ' <span class="vat">' + (l === 'en' ? '+VAT' : '+IVA') + '</span>' : ''}</span><span class="pc-d">${b.year} · ${esc(b.d[l])}</span><span class="pc-t">${esc(INV.titleFor(b, l))}</span><span class="pc-l">${{es: 'Ver ficha', ca: 'Veure fitxa', en: 'See details'}[l]} →</span></span></a>`;
};
const TX = {
  es: {avail: 'Otros barcos parecidos', sold: 'Barcos parecidos disponibles', model: 'En venta ahora, de eslora parecida',
       sub: 'Del mismo tipo, eslora y precio aproximados, de mi cartera.', subM: 'Barcos de mi cartera de un tamaño parecido. No son este modelo, pero pueden servirte de referencia.',
       empty: 'Ahora mismo no tengo otro barco disponible que se le parezca.', emptyA: 'Crea una alerta', emptyB: 'y te aviso en cuanto entre uno que encaje.',
       all: 'Ver todos los barcos en venta', btn: '¿Buscas algo similar?'},
  ca: {avail: 'Altres vaixells semblants', sold: 'Vaixells semblants disponibles', model: 'En venda ara, d’eslora semblant',
       sub: 'Del mateix tipus, eslora i preu aproximats, de la meva cartera.', subM: 'Vaixells de la meva cartera d’una mida semblant. No són aquest model, però et poden servir de referència.',
       empty: 'Ara mateix no tinc cap altre vaixell disponible que s’hi assembli.', emptyA: 'Crea una alerta', emptyB: 'i t’aviso tan bon punt n’entri un que encaixi.',
       all: 'Veure tots els vaixells en venda', btn: 'Busques alguna cosa semblant?'},
  en: {avail: 'Other similar boats', sold: 'Similar boats available', model: 'For sale now, of a similar length',
       sub: 'Same type, similar length and price, from my listings.', subM: 'Boats from my listings of a similar size. Not this model, but a useful reference.',
       empty: 'Right now I have no other boat available that is similar.', emptyA: 'Set up an alert', emptyB: 'and I will let you know as soon as one that fits comes in.',
       all: 'See all boats for sale', btn: 'Looking for something similar?'}
};
function block(l, ref, head, sub) {
  let r = ref; if (ref.slug) { const me = INV.get(ref.slug); r = {slug: me.slug, kind: me.kind, len: me.length, price: me.status === 'sold' ? 0 : me.price, types: me.types}; }
  const list = pick(INV, r), t = TX[l];
  return `<!--pm-sim--><section class="pm-simbox" id="similares" aria-labelledby="simh"><h2 id="simh">${head}</h2><p class="pm-sub">${sub}</p>` +
    `<div class="pm-sim" data-ref='${JSON.stringify(ref)}'${list.length ? '' : ' hidden'}>${list.map(b => card(b, l)).join('')}</div>` +
    `<p class="pm-empty"${list.length ? ' hidden' : ''}>${t.empty} <a href="${pre(l)}/alertas/">${t.emptyA}</a> ${t.emptyB}</p>` +
    `<p class="pm-more"><a href="${pre(l)}/barcos/">${t.all} →</a></p></section><!--/pm-sim-->`;
}
const RX = /<!--pm-sim-->[\s\S]*?<!--\/pm-sim-->\n?/g;
function assets(h, css) {
  if (!h.includes('/similares.css')) h = h.replace(/(<link rel="stylesheet" href="\/nav\.css[^"]*">)/, `$1\n<link rel="stylesheet" href="/similares.css?v=20260928">`);
  if (!h.includes('/inventario.js')) h = h.replace('</body>', '<script src="/inventario.js?v=20260928" defer></script>\n</body>');
  if (!h.includes('/similares.js')) h = h.replace(/(<script src="\/inventario\.js[^"]*" defer><\/script>)/, `$1\n<script src="/similares.js?v=20260928" defer></script>`);
  return h;
}
const MODEL = {'bavaria-27-sport': 8.35, 'beneteau-antares-8': 8.0, 'beneteau-flyer-6-6-spacedeck': 6.7, 'beneteau-flyer-7-7-sundeck': 7.64,
  'jeanneau-cap-camarat-6-5-cc': 6.86, 'jeanneau-cap-camarat-7-5-wa': 7.19, 'jeanneau-cap-camarat-8-5-wa': 8.4, 'jeanneau-merry-fisher-795': 7.43,
  'quicksilver-activ-605-open': 6.45, 'quicksilver-activ-675-sundeck': 7.16};
let n = 0; const report = [];
for (const l of LANGS) {
  const dir = path.join(ROOT, l === 'es' ? '' : l);
  for (const b of INV.boats) {
    const f = path.join(dir, 'barcos', b.slug + '.html');
    if (!fs.existsSync(f)) { report.push('FALTA ' + f); continue; }
    let h = fs.readFileSync(f, 'utf8').replace(RX, '');
    const sold = b.status === 'sold';
    const blk = `<div class="wrap">${block(l, {slug: b.slug}, sold ? TX[l].sold : TX[l].avail, TX[l].sub)}</div>\n`;
    const i = h.lastIndexOf('</main>'); if (i < 0) { report.push('SIN </main> ' + f); continue; }
    h = assets(h.slice(0, i) + blk + h.slice(i));
    fs.writeFileSync(f, h); n++;
    report.push(`${l} ${b.slug}: ${pick(INV, {slug: b.slug, kind: b.kind, len: b.length, price: b.price, types: b.types}).map(x => x.slug).join(', ') || '(sin parecidos → alerta)'}`);
  }
  const MT = {"bavaria-27-sport": ["cabinado", "sundeck"], "beneteau-antares-8": ["pilothouse", "cabinado"], "beneteau-flyer-6-6-spacedeck": ["open", "sundeck"], "beneteau-flyer-7-7-sundeck": ["sundeck", "open"], "jeanneau-cap-camarat-6-5-cc": ["open"], "jeanneau-cap-camarat-7-5-wa": ["walkaround"], "jeanneau-cap-camarat-8-5-wa": ["walkaround"], "jeanneau-merry-fisher-795": ["pilothouse"], "quicksilver-activ-605-open": ["open"], "quicksilver-activ-675-sundeck": ["sundeck", "open"]};
  for (const [slug, len] of Object.entries(MODEL)) {
    const f = path.join(dir, 'modelos', slug + '.html');
    let h = fs.readFileSync(f, 'utf8').replace(RX, '');
    const blk = block(l, {kind: 'motor', len, dl: 1.5, types: MT[slug]}, TX[l].model, TX[l].subM).replace('id="similares"', 'id="en-venta"').replace('<section class="pm-simbox"', '<section class="pm-simbox" style="margin-top:8px"') + '\n\n        ';
    h = h.replace('<h2 id="gastos">', blk + '<h2 id="gastos">');
    fs.writeFileSync(f, assets(h)); n++;
    report.push(`${l} modelo ${slug}: ${pick(INV, {kind: 'motor', len, dl: 1.5, types: MT[slug]}).map(x => x.slug).join(', ') || '(ninguno → alerta)'}`);
  }
  // Catálogo: botón "Ver similares" en tarjetas vendidas
  const cf = path.join(dir, 'barcos', 'index.html');
  let c = fs.readFileSync(cf, 'utf8');
  c = c.replace(/(<article data-pm-boat="([^"]+)" class="bcard is-sold"[\s\S]*?<div class="bcta">)([\s\S]*?)(<\/div>)/g, (m, a, slug, inner, z) =>
    inner.includes('#similares') ? m : a + inner + `<a class="btn btn-ghost" href="${slug}.html#similares">${TX[l].btn}</a>` + z);
  fs.writeFileSync(cf, c); n++;
}
console.log(report.join('\n')); console.log('archivos escritos:', n);
