/* Plata Marine · ficha-plus (30/09/2026)
   1) Franja de datos clave con iconos bajo la galería (se genera a partir de la tabla .specs)
   2) Descripción plegada con "Ver más"
   3) Barra fija en móvil con precio + "Consultar este barco"
   Funciona en ES/CA/EN sin tocar el HTML de cada ficha. */
(function(){
"use strict";
var lang = (document.documentElement.lang || 'es').slice(0,2);
var T = {
  es: {more:'Ver descripción completa', less:'Ver menos', ask:'Consultar este barco'},
  ca: {more:'Veure la descripció completa', less:'Veure menys', ask:'Consultar aquest vaixell'},
  en: {more:'Read the full description', less:'Show less', ask:'Ask about this boat'}
}[lang] || {more:'Ver descripción completa', less:'Ver menos', ask:'Consultar este barco'};

var ICO = {
  year:'<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
  length:'<svg viewBox="0 0 24 24"><path d="M3 12h18M3 12l3-3M3 12l3 3M21 12l-3-3M21 12l-3 3"/></svg>',
  engine:'<svg viewBox="0 0 24 24"><path d="M4 10h3l2-2h6l2 2h3v7H4zM9 17v3M15 17v3M12 5v3"/></svg>',
  hours:'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
  pax:'<svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 20c0-3.5 2.5-6 6-6s6 2.5 6 6M15 20c0-2.5 1-4.5 3-5.5 2 .5 3 2.5 3 5.5"/></svg>',
  title:'<svg viewBox="0 0 24 24"><rect x="3" y="6" width="18" height="13" rx="2"/><path d="M7 11h6M7 15h10"/></svg>',
  place:'<svg viewBox="0 0 24 24"><path d="M12 21s-6-5.5-6-11a6 6 0 0 1 12 0c0 5.5-6 11-6 11z"/><circle cx="12" cy="10" r="2.2"/></svg>'
};
var KEYS = [
  {k:'year',  dt:['año','any','year']},
  {k:'length',dt:['eslora','length']},
  {k:'engine',dt:['motor','motores','motors','engine','engines','power']},
  {k:'hours', dt:['horas','hores','hours']},
  {k:'pax',   dt:['capacidad','capacitat','capacity','personas','persones','people']},
  {k:'title', dt:['titulación','titulació','licence','license']},
  {k:'place', dt:['ubicación','ubicació','location','zona','zone']}
];

/* 1) Datos clave */
var specs = document.querySelector('.specs');
var gal = document.querySelector('.gal');
if(specs && gal){
  var rows = {};
  Array.prototype.forEach.call(specs.querySelectorAll('div'), function(d){
    var dt = d.querySelector('dt'), dd = d.querySelector('dd');
    if(!dt || !dd) return;
    rows[dt.textContent.trim().toLowerCase()] = {label: dt.textContent.trim(), value: dd.textContent.trim()};
  });
  var items = [];
  KEYS.forEach(function(K){
    for(var i=0;i<K.dt.length;i++){
      var r = rows[K.dt[i]];
      if(r){
        var v = r.value;
        if(K.k==='engine') v = v.split(/\s[·(]\s?/)[0].replace(/,\s*(diésel|dièsel|diesel|gasolina|petrol)\b.*$/i,'');
        if(K.k==='place') v = v.replace(/\s*\(.*\)\s*$/,'');
        if(K.k==='title'){ v = v.replace(/PER con pr[áa]cticas de vela/i,'PER (vela)').replace(/PER amb pr[àa]ctiques de vela/i,'PER (vela)').replace(/Spanish PER with sailing endorsement/i,'PER (sail)').replace(/PER with sailing (practice|endorsement)/i,'PER (sail)').replace(/Licencia de Navegaci[óo]n/i,'Licencia').replace(/Llic[èe]ncia de Navegaci[óo]/i,'Llicència').replace(/Patr[óo]n o Capit[áa]n de Yate/i,'PY o CY'); }
        if(K.k==='hours'){ v = v.replace(/^Sin contador de horas$/i,'Sin contador').replace(/^Sense comptador d'hores$/i,'Sense comptador').replace(/^No hour meter$/i,'No hour meter'); }
        if(v.length > 44) v = v.slice(0,42).replace(/\s\S*$/,'') + '…';
        items.push({k:K.k, label:r.label, value:v});
        break;
      }
    }
  });
  if(items.length >= 3){
    var strip = document.createElement('ul');
    strip.className = 'keyfacts';
    strip.setAttribute('aria-label', lang==='en' ? 'Key facts' : lang==='ca' ? 'Dades clau' : 'Datos clave');
    strip.innerHTML = items.map(function(it){
      return '<li><span class="kf-ico" aria-hidden="true">' + ICO[it.k] + '</span><span class="kf-txt"><span class="kf-l">' + it.label + '</span><span class="kf-v">' + it.value + '</span></span></li>';
    }).join('');
    var mainImg = gal.querySelector('.main');
    if(mainImg) gal.insertBefore(strip, mainImg.nextSibling); else gal.parentNode.insertBefore(strip, gal.nextSibling);
  }
}

/* 2) Descripción plegada */
var prose = document.querySelector('.prose');
if(prose){
  var ps = Array.prototype.filter.call(prose.children, function(el){ return el.tagName === 'P'; });
  if(ps.length > 2){
    var hidden = ps.slice(2);
    hidden.forEach(function(p){ p.classList.add('prose-more'); });
    var btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'prose-toggle'; btn.textContent = T.more; btn.setAttribute('aria-expanded','false');
    ps[1].parentNode.insertBefore(btn, ps[1].nextSibling);
    btn.addEventListener('click', function(){
      var open = prose.classList.toggle('open');
      btn.textContent = open ? T.less : T.more;
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
}

/* 3) Barra fija en móvil */
var ask = document.querySelector('.price-box .btn-ask');
var price = document.querySelector('.price-box .price');
var head = document.querySelector('.head');
if(ask && price && head && window.matchMedia('(max-width: 639px)').matches){
  var bar = document.createElement('div');
  bar.className = 'stickybar';
  bar.innerHTML = '<span class="sb-price">' + price.textContent.trim() + '</span>';
  var a = ask.cloneNode(true);
  a.className = 'btn btn-wa sb-btn';
  a.textContent = T.ask;
  a.setAttribute('data-wa-context','ficha_sticky');
  bar.appendChild(a);
  document.body.appendChild(bar);
  var show = function(){
    var r = head.getBoundingClientRect();
    var pc = document.getElementById('privacy-choice');
    var cookiesOpen = !!(pc && pc.offsetParent !== null);
    bar.classList.toggle('on', r.bottom < 0 && !cookiesOpen);
  };
  window.addEventListener('scroll', show, {passive:true});
  document.addEventListener('click', function(){ setTimeout(show, 50); });
  show();
}
})();

/* Enlace a "valora tu barco" al final de la descripción de cada ficha (ES/CA/EN). */
(function(){
  var lang=(document.documentElement.lang||'es').slice(0,2);
  var L={es:['¿Tienes un barco parecido y lo quieres vender? ','Mira qué influye en su precio (2 min)','/herramientas/valora-tu-barco.html'],
    ca:['Tens un vaixell semblant i el vols vendre? ','Mira què influeix en el seu preu (2 min)','/ca/herramientas/valora-tu-barco.html'],
    en:['Own a similar boat and thinking of selling? ','See what affects its price (2 min)','/en/herramientas/valora-tu-barco.html']}[lang]||null;
  var prose=document.querySelector('.prose'); if(!L||!prose||document.getElementById('pm-sell-hint'))return;
  var p=document.createElement('p'); p.id='pm-sell-hint';
  p.style.cssText='margin-top:22px;padding:12px 14px;border-left:3px solid var(--brass,#b8955a);background:rgba(127,146,158,.08);font-size:.95em';
  p.appendChild(document.createTextNode(L[0])); var a=document.createElement('a'); a.href=L[2]; a.textContent=L[1]; p.appendChild(a);
  prose.parentNode.insertBefore(p, prose.nextSibling);
})();
