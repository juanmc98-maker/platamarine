// Regenera el HTML estático de las listas .pm-list[data-f] de /comprar/ (ES/CA/EN/FR) desde inventario.js (mismo criterio que portal.js).
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
global.window = {}; global.location = {pathname: '/'}; global.document = {readyState: 'complete', querySelectorAll: () => []};
eval(fs.readFileSync(path.join(ROOT, 'inventario.js'), 'utf8'));
const INV = window.PM_INV;
const esc = s => String(s).replace(/[&<>"]/g, m => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[m]));
const price = (n, l) => { const s = String(n).replace(/\B(?=(\d{3})+(?!\d))/g, l === 'en' ? ',' : l === 'fr' ? '\u202f' : '.'); return l === 'en' ? '€' + s : s + ' €'; };
const IMG = {'ranieri-azzurra-5m': '/ranieri-azzurra-1.jpg'};
const SEE = {es: 'Ver ficha', ca: 'Veure fitxa', en: 'See details', fr: 'Voir la fiche'};
const card = (b, l) => { const img = (IMG[b.slug] || '/' + b.slug + '-1.jpg').replace(/\.jpg$/, '');
  return `<a class="pcard" href="${INV.url(b, l)}"><img src="${img}-m.jpg" srcset="${img}-m.jpg 1000w, ${img}.jpg 1600w" sizes="(max-width: 640px) 100vw, 360px" alt="${esc(b.name)}" loading="lazy" width="1600" height="900"><span class="pc-b"><strong>${esc(b.name)}</strong><span class="pc-p">${price(b.price, l)}${b.vat ? ' <span class="vat">' + (l === 'en' ? '+VAT' : l === 'fr' ? '+TVA' : '+IVA') + '</span>' : ''}</span><span class="pc-d">${b.year} · ${esc(b.d[l])}</span><span class="pc-t">${esc(INV.titleFor(b, l))}</span><span class="pc-l">${SEE[l]} →</span></span></a>`; };
let n = 0;
for (const l of ['es', 'ca', 'en', 'fr']) {
  const dir = path.join(ROOT, l === 'es' ? '' : l, 'comprar');
  for (const f of fs.readdirSync(dir).filter(x => x.endsWith('.html'))) {
    const p = path.join(dir, f); let h = fs.readFileSync(p, 'utf8'); const o = h;
    h = h.replace(/<div class="pm-list" data-f='([^']*)'>[\s\S]*?<\/div>/g, (m, jf) => {
      const F = JSON.parse(jf);
      const list = INV.available().filter(b => !(F.zone && b.zone !== F.zone) && !(F.area && b.area !== F.area) && !(F.kind && b.kind !== F.kind) && !(F.maxTitle && b.title > F.maxTitle) && !(F.q && !new RegExp(F.q, 'i').test(b.name))).sort((a, b) => b.price - a.price);
      return `<div class="pm-list" data-f='${jf}'>` + list.map(b => card(b, l)).join('') + '</div>';
    });
    if (h !== o) { fs.writeFileSync(p, h); n++; console.log('actualizado', path.relative(ROOT, p)); }
  }
}
console.log(n, 'archivos');
