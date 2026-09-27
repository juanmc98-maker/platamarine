(function(){
  var dds=document.querySelectorAll('.pmx-dd');
  function closeAll(except){for(var i=0;i<dds.length;i++){if(dds[i]!==except){dds[i].classList.remove('open');dds[i].firstElementChild.setAttribute('aria-expanded','false');}}}
  for(var i=0;i<dds.length;i++){(function(dd){
    var b=dd.firstElementChild;
    b.addEventListener('click',function(e){e.stopPropagation();var o=!dd.classList.contains('open');closeAll(dd);dd.classList.toggle('open',o);b.setAttribute('aria-expanded',o?'true':'false');});
  })(dds[i]);}
  document.addEventListener('click',function(e){if(!e.target.closest('.pmx-dd'))closeAll();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){closeAll();closeP();}});
  var btn=document.getElementById('pmxBtn'),p=document.getElementById('pmxPanel');
  function closeP(){if(!btn||!p)return;p.classList.remove('open');btn.setAttribute('aria-expanded','false');btn.setAttribute('aria-label',btn.getAttribute('data-open'));}
  if(btn&&p){
    btn.addEventListener('click',function(){var o=p.classList.toggle('open');btn.setAttribute('aria-expanded',o?'true':'false');btn.setAttribute('aria-label',btn.getAttribute(o?'data-close':'data-open'));});
    p.addEventListener('click',function(e){if(e.target.closest('a'))closeP();});
    window.addEventListener('resize',function(){if(window.innerWidth>=1120)closeP();});
  }
})();
/* Tablas en móvil: si una tabla no cabe, cada fila se muestra como una ficha con su etiqueta (sin scroll lateral). */
(function(){
  function prep(){
    var ts=document.querySelectorAll('main table');
    for(var i=0;i<ts.length;i++){
      var t=ts[i]; if(t.classList.contains('pm-stack')||t.closest('.specs')) continue;
      var head=t.querySelector('thead tr')||t.rows[0]; if(!head) continue;
      var hs=head.cells, isHead=true;
      for(var k=0;k<hs.length;k++) if(hs[k].tagName!=='TH') isHead=false;
      if(!isHead||hs.length<2) continue;
      var labels=[].map.call(hs,function(c){return c.textContent.trim();});
      for(var r=0;r<t.rows.length;r++){ var row=t.rows[r]; if(row===head){row.classList.add('pm-head');continue;}
        for(var c=0;c<row.cells.length;c++) if(labels[c]) row.cells[c].setAttribute('data-label',labels[c]); }
      t.classList.add('pm-stack');
    }
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',prep); else prep();
})();
/* Enlaces nuevos del menú Comprar (precios, compra por zona/tipo y calculadoras) en todas las páginas, sin tocar cada HTML. */
(function(){
  var p=location.pathname,pre=p.indexOf('/ca/')===0?'/ca':p.indexOf('/en/')===0?'/en':'';
  var L={'':[['/comprar/','Comprar barco: por zona y tipo'],['/precios/','Precios de barcos de ocasión'],['/herramientas/','Calculadoras: impuestos, costes, financiación']],
    '/ca':[['/comprar/','Comprar vaixell: per zona i tipus'],['/precios/','Preus de vaixells d’ocasió'],['/herramientas/','Calculadores: impostos, costos, finançament']],
    '/en':[['/comprar/','Buy a boat: by area and type'],['/precios/','Used boat prices'],['/herramientas/','Calculators: taxes, costs, finance']]}[pre];
  function add(box){
    if(!box)return;
    L.forEach(function(it){var h=pre+it[0];if(box.querySelector('a[href="'+h+'"]'))return;var a=document.createElement('a');a.href=h;a.textContent=it[1];if(p===h||p===h+'index.html')a.setAttribute('aria-current','page');box.appendChild(a);});
  }
  add(document.getElementById('pmxM2'));
  var g=document.querySelectorAll('#pmxPanel .pmx-grp');
  for(var i=0;i<g.length;i++){var a=g[i].querySelector('a[href$="/modelos/"]');if(a){add(g[i]);break;}}
})();
/* Enlace "Escuelas náuticas" en el menú Servicios de todas las páginas. */
(function(){
  var p=location.pathname,pre=p.indexOf('/ca/')===0?'/ca':p.indexOf('/en/')===0?'/en':'';
  var t={'':'Escuelas náuticas','/ca':'Escoles nàutiques','/en':'Boating schools'}[pre],h=pre+'/servicios/escuelas.html';
  function add(box){if(!box||box.querySelector('a[href="'+h+'"]'))return;var a=document.createElement('a');a.href=h;a.textContent=t;if(p===h)a.setAttribute('aria-current','page');box.appendChild(a);}
  add(document.getElementById('pmxM4'));
  var g=document.querySelectorAll('#pmxPanel .pmx-grp');
  for(var i=0;i<g.length;i++){if(g[i].querySelector('a[href$="/servicios/directorio.html"]')){add(g[i]);break;}}
})();
