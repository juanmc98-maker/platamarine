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
    window.addEventListener('resize',function(){if(window.innerWidth>=1240)closeP();});
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
  var p=location.pathname,pre=p.indexOf('/ca/')===0?'/ca':p.indexOf('/en/')===0?'/en':p.indexOf('/fr/')===0?'/fr':'';
  var L={'':[['/comprar/','Comprar barco: por zona y tipo'],['/precios/','Precios de barcos de ocasión'],['/herramientas/','Calculadoras: impuestos, costes, financiación']],
    '/ca':[['/comprar/','Comprar vaixell: per zona i tipus'],['/precios/','Preus de vaixells d’ocasió'],['/herramientas/','Calculadores: impostos, costos, finançament']],
    '/en':[['/comprar/','Buy a boat: by area and type'],['/precios/','Used boat prices'],['/herramientas/','Calculators: taxes, costs, finance']],
    '/fr':[['/comprar/','Acheter un bateau : par zone et par type'],['/precios/','Prix des bateaux d’occasion'],['/herramientas/','Calculatrices : taxes, coûts, financement']]}[pre];
  function add(box){
    if(!box)return;
    L.forEach(function(it){var h=pre+it[0];if(box.querySelector('a[href="'+h+'"]'))return;var a=document.createElement('a');a.href=h;a.textContent=it[1];if(p===h||p===h+'index.html')a.setAttribute('aria-current','page');box.appendChild(a);});
  }
  add(document.getElementById('pmxM2'));
  var g=document.querySelectorAll('#pmxPanel .pmx-grp');
  for(var i=0;i<g.length;i++){var a=g[i].querySelector('a[href$="/modelos/"]');if(a){add(g[i]);break;}}
})();
/* Enlace "Barcos nuevos" (índice de marcas nuevas) en el menú Comprar de todas las páginas. */
(function(){
  var p=location.pathname,pre=p.indexOf('/ca/')===0?'/ca':p.indexOf('/en/')===0?'/en':p.indexOf('/fr/')===0?'/fr':'';
  var t={'':'Barcos nuevos','/ca':'Vaixells nous','/en':'New boats','/fr':'Bateaux neufs'}[pre],h=pre+'/barcos-nuevos/';
  function add(box){if(!box||box.querySelector('a[href="'+h+'"]'))return;var a=document.createElement('a');a.href=h;a.textContent=t;if(p===h||p===h+'index.html')a.setAttribute('aria-current','page');box.appendChild(a);}
  add(document.getElementById('pmxM2'));
  var g=document.querySelectorAll('#pmxPanel .pmx-grp');
  for(var i=0;i<g.length;i++){if(g[i].querySelector('a[href$="/modelos/"]')){add(g[i]);break;}}
})();
/* "Barcos en venta" con dos accesos: Barcos nuevos (/barcos-nuevos/, todas las marcas juntas) y Segunda mano.
   Escritorio: desplegable al pasar el ratón o al llegar con el teclado. Móvil: dos enlaces sangrados debajo. */
(function(){
  var p=location.pathname,pre=p.indexOf('/ca/')===0?'/ca':p.indexOf('/en/')===0?'/en':p.indexOf('/fr/')===0?'/fr':'';
  var T={'':['Barcos nuevos','Segunda mano'],'/ca':['Vaixells nous','Segona mà'],'/en':['New boats','Pre-owned'],'/fr':['Bateaux neufs','Occasion']}[pre];
  var h=pre+'/barcos/',hn=pre+'/barcos-nuevos/',onN=(p===hn||p===hn+'index.html');
  var L=[[hn,T[0]],[h+'#segunda-mano',T[1]]];
  function fill(box){L.forEach(function(it){var a=document.createElement('a');a.href=it[0];a.textContent=it[1];if(it[0]===hn&&onN)a.setAttribute('aria-current','page');box.appendChild(a);});}
  var top=document.querySelector('header.top .pmx-nav>a[href="'+h+'"]');
  if(top){
    var dd=document.createElement('div');dd.className='pmx-dd pmx-bev'+(onN?' cur':'');
    top.parentNode.insertBefore(dd,top);dd.appendChild(top);
    var m=document.createElement('div');m.className='pmx-menu';m.id='pmxBev';fill(m);dd.appendChild(m);
    dd.addEventListener('keydown',function(e){if(e.key==='Escape'){dd.classList.add('shut');top.focus();}});
    dd.addEventListener('mouseleave',function(){dd.classList.remove('shut');});
    dd.addEventListener('focusout',function(e){if(!dd.contains(e.relatedTarget))dd.classList.remove('shut');});
  }
  var mt=document.querySelector('#pmxPanel .pmx-main a[href="'+h+'"]');
  if(mt&&!mt.parentNode.querySelector('.pmx-bevsub')){
    var s=document.createElement('div');s.className='pmx-bevsub';fill(s);mt.parentNode.insertBefore(s,mt.nextSibling);
  }
})();
/* Enlace "Broker en Barcelona y Maresme" en el menú Vender de todas las páginas. */
(function(){
  var p=location.pathname,pre=p.indexOf('/ca/')===0?'/ca':p.indexOf('/en/')===0?'/en':p.indexOf('/fr/')===0?'/fr':'';
  var t={'':'Vender en Barcelona y Maresme','/ca':'Vendre a Barcelona i Maresme','/en':'Selling in Barcelona and Maresme','/fr':'Vendre à Barcelone et dans le Maresme'}[pre],h=pre+'/vender/broker-nautico-barcelona-maresme.html';
  function add(box){if(!box||box.querySelector('a[href="'+h+'"]'))return;var a=document.createElement('a');a.href=h;a.textContent=t;if(p===h)a.setAttribute('aria-current','page');box.appendChild(a);}
  add(document.getElementById('pmxM1'));
  var g=document.querySelectorAll('#pmxPanel .pmx-grp');
  for(var i=0;i<g.length;i++){if(g[i].querySelector('a[href$="/herramientas/valora-tu-barco.html"]')){add(g[i]);break;}}
})();
/* Enlace "Escuelas náuticas" en el menú Servicios de todas las páginas. */
(function(){
  var p=location.pathname,pre=p.indexOf('/ca/')===0?'/ca':p.indexOf('/en/')===0?'/en':p.indexOf('/fr/')===0?'/fr':'';
  var t={'':'Escuelas náuticas','/ca':'Escoles nàutiques','/en':'Boating schools','/fr':'Écoles nautiques'}[pre],h=pre+'/servicios/escuelas.html';
  function add(box){if(!box||box.querySelector('a[href="'+h+'"]'))return;var a=document.createElement('a');a.href=h;a.textContent=t;if(p===h)a.setAttribute('aria-current','page');box.appendChild(a);}
  add(document.getElementById('pmxM4'));
  var g=document.querySelectorAll('#pmxPanel .pmx-grp');
  for(var i=0;i<g.length;i++){if(g[i].querySelector('a[href$="/servicios/directorio.html"]')){add(g[i]);break;}}
})();
/* Enlace "Amarres" en el menú Servicios de todas las páginas. */
(function(){
  var p=location.pathname,pre=p.indexOf('/ca/')===0?'/ca':p.indexOf('/en/')===0?'/en':p.indexOf('/fr/')===0?'/fr':'';
  var t={'':'Amarres','/ca':'Amarradors','/en':'Moorings','/fr':'Places de port'}[pre],h=pre+'/servicios/amarres.html';
  function add(box){if(!box||box.querySelector('a[href="'+h+'"]'))return;var a=document.createElement('a');a.href=h;a.textContent=t;if(p===h)a.setAttribute('aria-current','page');box.appendChild(a);}
  add(document.getElementById('pmxM4'));
  var g=document.querySelectorAll('#pmxPanel .pmx-grp');
  for(var i=0;i<g.length;i++){if(g[i].querySelector('a[href$="/servicios/directorio.html"]')){add(g[i]);break;}}
})();
/* Barra "Compartir" en el pie de todas las páginas: WhatsApp, Facebook, X, Telegram, copiar enlace y el menú nativo del móvil (Instagram, etc.). */
(function(){
  function run(){
    var foot=document.querySelector('footer.foot .wrap'); if(!foot||document.getElementById('pmShare'))return;
    var p=location.pathname,pre=p.indexOf('/ca/')===0?'/ca':p.indexOf('/en/')===0?'/en':p.indexOf('/fr/')===0?'/fr':'';
    var T={'':{t:'Comparte esta página',c:'Copiar enlace',ok:'Enlace copiado',m:'Compartir…',a:'Compartir en '},
      '/ca':{t:'Comparteix aquesta pàgina',c:'Copia l’enllaç',ok:'Enllaç copiat',m:'Compartir…',a:'Compartir a '},
      '/en':{t:'Share this page',c:'Copy link',ok:'Link copied',m:'Share…',a:'Share on '},
      '/fr':{t:'Partagez cette page',c:'Copier le lien',ok:'Lien copié',m:'Partager…',a:'Partager sur '}}[pre];
    var can=document.querySelector('link[rel="canonical"]'),url=(can&&can.href)||location.href.split('#')[0],title=document.title;
    var ogd=document.querySelector('meta[property="og:description"]'),txt=title+(ogd?' — '+ogd.content:'');
    var e=encodeURIComponent,eu=e(url);
    var I={wa:'<svg viewBox="0 0 24 24"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.5-.5.3-.5c.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5 2.5 1 3 .8 3.6.8.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.3-.7-.5zM12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2z"/></svg>',
      fb:'<svg viewBox="0 0 24 24"><path d="M13.5 22v-8h2.7l.4-3.2h-3.1V8.8c0-.9.3-1.6 1.6-1.6h1.7V4.4c-.3 0-1.3-.1-2.5-.1-2.5 0-4.1 1.5-4.1 4.2v2.3H7.4V14h2.8v8h3.3z"/></svg>',
      x:'<svg viewBox="0 0 24 24"><path d="M17.8 3h3l-6.7 7.7L22 21h-6.2l-4.8-6.3L5.4 21h-3l7.2-8.2L2 3h6.3l4.4 5.8L17.8 3zm-1.1 16.2h1.7L7.4 4.7H5.6l11.1 14.5z"/></svg>',
      tg:'<svg viewBox="0 0 24 24"><path d="M21.9 4.6 18.7 19.4c-.2 1-.9 1.3-1.8.8l-4.8-3.6-2.3 2.3c-.3.3-.5.5-1 .5l.3-4.9 8.9-8c.4-.3-.1-.5-.6-.2L6.4 13.2 1.7 11.7c-1-.3-1-1 .2-1.5L20.6 3c.9-.3 1.6.2 1.3 1.6z"/></svg>',
      cp:'<svg viewBox="0 0 24 24"><path d="M16 1H4a2 2 0 0 0-2 2v14h2V3h12V1zm3 4H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2zm0 16H8V7h11v14z"/></svg>',
      sh:'<svg viewBox="0 0 24 24"><path d="M18 16.1c-.8 0-1.5.3-2 .8l-7.1-4.2c.1-.2.1-.5.1-.7s0-.5-.1-.7L16 7.2c.6.5 1.3.8 2.1.8a3 3 0 1 0-3-3c0 .2 0 .5.1.7L8.1 9.8A3 3 0 1 0 6 15c.8 0 1.5-.3 2.1-.8l7.1 4.2c-.1.2-.1.4-.1.6a2.9 2.9 0 1 0 2.9-2.9z"/></svg>'};
    var links=[['wa','WhatsApp','https://api.whatsapp.com/send?text='+e(txt+' '+url)],['fb','Facebook','https://www.facebook.com/sharer/sharer.php?u='+eu],['x','X','https://twitter.com/intent/tweet?url='+eu+'&text='+e(title)],['tg','Telegram','https://t.me/share/url?url='+eu+'&text='+e(title)]];
    var box=document.createElement('div');box.id='pmShare';box.className='pm-share';
    var h='<p>'+T.t+'</p><div class="pm-share-row">';
    links.forEach(function(l){h+='<a href="'+l[2]+'" target="_blank" rel="noopener" data-no-track data-share data-net="'+l[0]+'" aria-label="'+T.a+l[1]+'">'+I[l[0]]+'<span>'+l[1]+'</span></a>';});
    h+='<button type="button" data-net="copy">'+I.cp+'<span>'+T.c+'</span></button>';
    if(navigator.share)h+='<button type="button" data-net="native">'+I.sh+'<span>'+T.m+'</span></button>';
    box.innerHTML=h+'</div>';
    foot.insertBefore(box,foot.firstChild);
    function track(n){if(window.pmTrack)window.pmTrack('share',{method:n});}
    box.addEventListener('click',function(ev){
      var el=ev.target.closest('[data-net]');if(!el)return;var n=el.getAttribute('data-net');
      if(n==='copy'){ev.preventDefault();var done=function(){var s=el.querySelector('span'),o=s.textContent;s.textContent=T.ok;el.classList.add('ok');setTimeout(function(){s.textContent=o;el.classList.remove('ok');},1800);};
        if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(url).then(done,function(){prompt(T.c,url);});else prompt(T.c,url);}
      else if(n==='native'){ev.preventDefault();navigator.share({title:title,text:txt,url:url}).catch(function(){});}
      track(n);
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
})();

/* "Síguenos" en el pie de todas las páginas: Instagram y página de Facebook de Plata Marine (enlaces simples, sin widgets ni cookies de terceros). */
(function(){
  function run(){
    var foot=document.querySelector('footer.foot .wrap'); if(!foot||document.getElementById('pmFollow'))return;
    var p=location.pathname,pre=p.indexOf('/ca/')===0?'/ca':p.indexOf('/en/')===0?'/en':p.indexOf('/fr/')===0?'/fr':'';
    var t={'':'Síguenos','/ca':'Segueix-nos','/en':'Follow us','/fr':'Suivez-nous'}[pre];
    var I={ig:'<svg viewBox="0 0 24 24"><path d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10zm0 8.2a3.2 3.2 0 1 1 0-6.4 3.2 3.2 0 0 1 0 6.4zM17.3 5.5a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4zM21.9 7.9c-.1-1.6-.4-3-1.6-4.2S17.7 2.2 16.1 2.1C14.5 2 9.5 2 7.9 2.1 6.3 2.2 4.9 2.5 3.7 3.7S2.2 6.3 2.1 7.9C2 9.5 2 14.5 2.1 16.1c.1 1.6.4 3 1.6 4.2s2.6 1.5 4.2 1.6c1.6.1 6.6.1 8.2 0 1.6-.1 3-.4 4.2-1.6s1.5-2.6 1.6-4.2c.1-1.6.1-6.6 0-8.2zm-2.1 10c-.3.9-1 1.5-1.9 1.9-1.3.5-4.4.4-5.9.4s-4.6.1-5.9-.4c-.9-.3-1.5-1-1.9-1.9-.5-1.3-.4-4.4-.4-5.9s-.1-4.6.4-5.9c.3-.9 1-1.5 1.9-1.9C7.4 3.7 10.5 3.8 12 3.8s4.6-.1 5.9.4c.9.3 1.5 1 1.9 1.9.5 1.3.4 4.4.4 5.9s.1 4.6-.4 5.9z"/></svg>',
      fb:'<svg viewBox="0 0 24 24"><path d="M13.5 22v-8h2.7l.4-3.2h-3.1V8.8c0-.9.3-1.6 1.6-1.6h1.7V4.4c-.3 0-1.3-.1-2.5-.1-2.5 0-4.1 1.5-4.1 4.2v2.3H7.4V14h2.8v8h3.3z"/></svg>'};
    var L=[['ig','Instagram','https://www.instagram.com/platamarine/'],['fb','Facebook','https://www.facebook.com/platamarine/']];
    if(!document.getElementById('pmFollowCss')){var st=document.createElement('style');st.id='pmFollowCss';st.textContent='.pm-follow{border-bottom:1px solid rgba(183,195,203,.22);padding:16px 0 18px}.pm-follow p{font-family:"Archivo","Helvetica Neue",Arial,sans-serif;font-size:11.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#7F929E;margin:0 0 10px}.pm-follow-row{display:flex;flex-wrap:wrap;gap:8px}.pm-follow-row a{display:inline-flex;align-items:center;gap:8px;font-family:"Archivo","Helvetica Neue",Arial,sans-serif;font-size:13.5px;font-weight:600;color:#fff;text-decoration:none;background:rgba(255,255,255,.08);border:1px solid rgba(183,195,203,.35);border-radius:999px;padding:9px 15px 9px 12px;line-height:1;transition:background .15s}.pm-follow-row a:hover{background:rgba(255,255,255,.16)}.pm-follow-row svg{width:16px;height:16px;fill:currentColor;flex:none}';document.head.appendChild(st);}
    var box=document.createElement('div');box.id='pmFollow';box.className='pm-follow';
    var h='<p>'+t+'</p><div class="pm-follow-row">';
    L.forEach(function(l){h+='<a href="'+l[2]+'" target="_blank" rel="noopener" data-no-track data-follow="'+l[0]+'">'+I[l[0]]+'<span>'+l[1]+'</span></a>';});
    box.innerHTML=h+'</div>';
    var sh=document.getElementById('pmShare');
    if(sh&&sh.parentNode===foot)foot.insertBefore(box,sh.nextSibling);else foot.insertBefore(box,foot.firstChild);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
})();

/* Enlace "Cómo hacer las fotos de tu barco" en el menú Vender de todas las páginas. */
(function(){
  var p=location.pathname,pre=p.indexOf('/ca/')===0?'/ca':p.indexOf('/en/')===0?'/en':p.indexOf('/fr/')===0?'/fr':'';
  var t={'':'Cómo hacer las fotos de tu barco','/ca':'Com fer les fotos del teu vaixell','/en':'How to photograph your boat','/fr':'Comment photographier votre bateau'}[pre],h=pre+'/vender/guia-fotos-barco.html';
  function add(box){if(!box||box.querySelector('a[href="'+h+'"]'))return;var a=document.createElement('a');a.href=h;a.textContent=t;if(p===h)a.setAttribute('aria-current','page');box.appendChild(a);}
  add(document.getElementById('pmxM1'));
  var g=document.querySelectorAll('#pmxPanel .pmx-grp');
  for(var i=0;i<g.length;i++){if(g[i].querySelector('a[href$="/herramientas/valora-tu-barco.html"]')){add(g[i]);break;}}
})();

/* Aviso en letra pequeña al pie de todas las páginas: información orientativa, podemos equivocarnos y nada es vinculante. */
(function(){
  function run(){
    var foot=document.querySelector('footer.foot .wrap'); if(!foot||document.getElementById('pmDisc'))return;
    var p=location.pathname,pre=p.indexOf('/ca/')===0?'/ca':p.indexOf('/en/')===0?'/en':p.indexOf('/fr/')===0?'/fr':'';
    var t={'':'La información de esta web es orientativa y se revisa con cuidado, pero podemos equivocarnos: compruébala siempre con la documentación del barco, el vendedor o un profesional. Nada de lo que aparece en esta web es vinculante.',
      '/ca':'La informació d’aquest web és orientativa i es revisa amb cura, però ens podem equivocar: comprova-la sempre amb la documentació del vaixell, el venedor o un professional. Res del que apareix en aquest web és vinculant.',
      '/en':'The information on this website is for guidance and is reviewed carefully, but we can get things wrong: always check it against the boat’s papers, the seller or a professional. Nothing on this website is binding.',
      '/fr':'Les informations de ce site sont indicatives et vérifiées avec soin, mais nous pouvons nous tromper : vérifiez-les toujours avec les papiers du bateau, le vendeur ou un professionnel. Rien de ce qui figure sur ce site n’est contractuel.'}[pre];
    var el=document.createElement('p');el.id='pmDisc';el.textContent=t;
    el.style.cssText='font-size:11.5px;line-height:1.5;opacity:.75;margin:14px 0 0;max-width:820px;flex-basis:100%';
    foot.appendChild(el);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
})();

/* Menú: "Vender mi barco" lleva a la página de venta (/vender-barco/) y el enlace a la herramienta no promete una tasación que no da. */
(function(){
  var p=location.pathname,pre=p.indexOf('/ca/')===0?'/ca':p.indexOf('/en/')===0?'/en':p.indexOf('/fr/')===0?'/fr':'';
  var lab={'':'¿Qué influye en el precio de mi barco?','/ca':'Què influeix en el preu del meu vaixell?','/en':'What affects my boat’s price?','/fr':'Qu’est-ce qui influe sur le prix de mon bateau ?'}[pre];
  var old=['¿Cuánto vale mi barco?','Quant val el meu vaixell?','How much is my boat worth?'];
  var as=document.querySelectorAll('.pmx-menu a, .pmx-grp a');
  for(var i=0;i<as.length;i++){
    var a=as[i],h=a.getAttribute('href');
    if(h===pre+'/#vender'||h==='/#vender'){a.setAttribute('href',pre+'/vender-barco/');}
    if(old.indexOf(a.textContent.trim())>-1){a.textContent=lab;}
  }
})();

/* Versión francesa: aviso al pie de que Juan no habla francés y usa un traductor. */
(function(){
  if(location.pathname.indexOf('/fr/')!==0)return;
  function run(){
    var foot=document.querySelector('footer.foot .wrap'); if(!foot||document.getElementById('pmFrNote'))return;
    var el=document.createElement('p');el.id='pmFrNote';
    el.textContent='Nous ne parlons pas français : ce site a été traduit et, pour vous répondre, nous utilisons un traducteur. N’hésitez pas à nous écrire en français, en anglais ou en espagnol. Merci de votre compréhension.';
    el.style.cssText='font-size:12.5px;line-height:1.5;margin:14px 0 0;max-width:820px;flex-basis:100%;font-weight:600';
    var d=document.getElementById('pmDisc'); if(d)foot.insertBefore(el,d); else foot.appendChild(el);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
})();

/* Solo en francés: enlaces para quien vive en Francia en el menú Comprar. */
(function(){
  if(location.pathname.indexOf('/fr/')!==0)return;
  var L=[['/fr/comprar/barcos-ocasion-espana-compradores-franceses.html','Vous vivez en France ? Bateaux en Espagne'],['/fr/guias/comprar-barco-espana-matricular-francia.html','Acheter en Espagne, immatriculer en France'],['/fr/guias/barco-frances-en-cataluna.html','Votre bateau en Catalogne']];
  function add(box){if(!box)return;L.forEach(function(it){if(box.querySelector('a[href="'+it[0]+'"]'))return;var a=document.createElement('a');a.href=it[0];a.textContent=it[1];if(location.pathname===it[0])a.setAttribute('aria-current','page');box.appendChild(a);});}
  add(document.getElementById('pmxM2'));
  var g=document.querySelectorAll('#pmxPanel .pmx-grp');
  for(var i=0;i<g.length;i++){if(g[i].querySelector('a[href$="/modelos/"]')){add(g[i]);break;}}
})();

/* Menú · Vender por zona (7 oct 2026): sustituye el enlace de Barcelona-Maresme por la línea de zonas
   (Costa Brava · Barcelona y Maresme · Tarragona · Baleares). Si el HTML ya trae .pmx-zonas no hace nada. */
(function(){
  var p=location.pathname,pre=p.indexOf('/ca/')===0?'/ca':p.indexOf('/en/')===0?'/en':p.indexOf('/fr/')===0?'/fr':'';
  if(document.querySelector('.pmx-zonas'))return;
  var L={'':'Vender por zona','/ca':'Vendre per zona','/en':'Selling by area','/fr':'Vendre par zone'}[pre];
  var N={'':['Costa Brava','Barcelona y Maresme','Tarragona','Baleares'],'/ca':['Costa Brava','Barcelona i Maresme','Tarragona','Balears'],'/en':['Costa Brava','Barcelona & Maresme','Tarragona','Balearics'],'/fr':['Costa Brava','Barcelone et Maresme','Tarragone','Baléares']}[pre];
  var S=['broker-nautico-costa-brava.html','broker-nautico-barcelona-maresme.html','broker-nautico-tarragona-costa-daurada.html','broker-nautico-baleares.html'];
  function make(){var d=document.createElement('div');d.className='pmx-zonas';var s=document.createElement('span');s.textContent=L;d.appendChild(s);
    for(var i=0;i<S.length;i++){var a=document.createElement('a');a.href=pre+'/vender/'+S[i];a.textContent=N[i];if(p===a.getAttribute('href'))a.setAttribute('aria-current','page');d.appendChild(a);}return d;}
  var as=document.querySelectorAll('.pmx-col a[href$="/vender/broker-nautico-barcelona-maresme.html"], .pmx-grp a[href$="/vender/broker-nautico-barcelona-maresme.html"]');
  for(var i=0;i<as.length;i++){as[i].parentNode.replaceChild(make(),as[i]);}
})();

/* Buscador de la web (lupa en la cabecera): ver /search.js */
(function(){if(document.querySelector("script[src^=\"/search.js\"]"))return;var s=document.createElement("script");s.src="/search.js?v=20261014";s.defer=true;document.head.appendChild(s);})();

/* Menú · ¿Cuánto vale mi barco? (7 oct 2026): primer enlace de Recursos › Vender, antes de valora-tu-barco. */
(function(){
  var p=location.pathname,pre=p.indexOf('/ca/')===0?'/ca':p.indexOf('/en/')===0?'/en':p.indexOf('/fr/')===0?'/fr':'';
  var T={'':'¿Cuánto vale mi barco?','/ca':'Quant val el meu vaixell?','/en':'How much is my boat worth?','/fr':'Combien vaut mon bateau ?'}[pre],h=pre+'/cuanto-vale-mi-barco/';
  var as=document.querySelectorAll('.pmx-col a[href$="/herramientas/valora-tu-barco.html"], .pmx-grp a[href$="/herramientas/valora-tu-barco.html"]');
  for(var i=0;i<as.length;i++){if(as[i].parentNode.querySelector('a[href="'+h+'"]'))continue;var a=document.createElement('a');a.href=h;a.textContent=T;if(p===h)a.setAttribute('aria-current','page');as[i].parentNode.insertBefore(a,as[i]);}
})();

/* Menú · Remolques (27 oct 2026): último enlace de Recursos › Comprar. */
(function(){
  var p=location.pathname,pre=p.indexOf('/ca/')===0?'/ca':p.indexOf('/en/')===0?'/en':p.indexOf('/fr/')===0?'/fr':'';
  var T={'':'Remolques para barcos','/ca':'Remolcs per a vaixells','/en':'Boat trailers','/fr':'Remorques pour bateaux'}[pre],h=pre+'/remolques/';
  var as=document.querySelectorAll('.pmx-col a[href$="/herramientas/"], .pmx-grp a[href$="/herramientas/"]');
  for(var i=0;i<as.length;i++){if(as[i].parentNode.querySelector('a[href="'+h+'"]'))continue;var a=document.createElement('a');a.href=h;a.textContent=T;if(p===h)a.setAttribute('aria-current','page');as[i].parentNode.insertBefore(a,as[i].nextSibling);}
})();

/* firma */
(function(){
  var SVG='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3140 1020" aria-hidden="true" focusable="false"><path fill="currentColor" transform="translate(0.000000,1020.000000) scale(1.000000,-1.000000)" d="M502 942 c-18 -1 -64 -8 -81 -11 -3 -1 -7 -1 -8 -2 -15 -2 -52 -11 -61 -14 -1 0 -5 -1 -7 -2 -2 -1 -5 -2 -6 -2 -1 -1 -3 -1 -3 -1 -1 0 -26 -7 -29 -9 -2 0 -4 -1 -6 -2 -3 -1 -5 -2 -6 -2 -2 0 -5 -2 -9 -3 -4 -1 -7 -3 -8 -3 -2 0 -5 -2 -8 -3 -4 -1 -7 -3 -8 -3 -2 0 -7 -2 -12 -4 -10 -4 -12 -5 -20 -9 -3 -1 -5 -2 -5 -2 -1 0 -3 -1 -6 -2 -2 -1 -5 -3 -6 -3 -2 0 -8 -3 -14 -6 -6 -3 -15 -8 -20 -10 -5 -2 -12 -6 -17 -9 -5 -2 -11 -6 -14 -7 -3 -2 -7 -4 -10 -6 -2 -2 -4 -3 -5 -3 0 0 -14 -8 -18 -12 -34 -26 -44 -35 -50 -48 -6 -12 -7 -29 -2 -41 16 -39 30 -44 66 -26 13 7 15 8 33 18 5 3 16 9 24 13 7 4 14 8 15 8 0 1 1 1 2 1 0 -1 -7 -34 -11 -49 -3 -10 -5 -21 -13 -56 -4 -19 -15 -72 -19 -89 -1 -5 -4 -19 -6 -31 -5 -22 -15 -74 -18 -92 -1 -12 -7 -47 -8 -55 0 -4 -1 -8 -1 -9 -1 -1 -2 -10 -3 -20 -1 -10 -3 -23 -4 -29 0 -7 -1 -17 -2 -22 -1 -6 -1 -12 -1 -13 -3 -26 -3 -71 -1 -85 6 -26 27 -48 52 -54 2 -1 6 -2 7 -2 5 -2 19 -1 27 2 10 5 19 16 22 29 3 10 5 21 8 33 1 7 2 14 3 16 3 12 5 23 16 85 1 8 3 17 3 19 1 8 3 16 4 24 1 3 1 9 2 12 1 3 2 9 2 13 1 4 2 10 2 13 0 3 1 9 2 13 1 9 2 16 4 25 1 4 3 13 4 21 1 8 3 16 3 19 1 2 1 5 1 7 0 9 7 13 13 9 3 -2 10 -11 13 -16 1 -2 4 -7 6 -10 6 -10 12 -21 24 -45 8 -14 12 -22 18 -31 2 -4 6 -12 9 -18 6 -12 12 -21 23 -38 15 -23 22 -32 31 -44 4 -5 11 -13 16 -20 5 -6 11 -13 14 -17 3 -3 8 -9 11 -13 10 -12 37 -40 49 -50 6 -6 13 -12 15 -13 6 -6 12 -11 18 -15 3 -2 6 -4 6 -4 0 0 3 -2 6 -4 2 -2 5 -4 7 -5 9 -9 53 -31 75 -37 24 -8 54 -9 75 -3 2 1 6 2 8 3 2 1 5 2 6 2 0 0 3 2 7 3 28 10 47 30 43 44 -3 10 -8 14 -21 17 -12 3 -27 7 -29 8 -2 0 -5 2 -8 3 -15 5 -32 15 -47 25 -23 16 -29 20 -45 35 -30 27 -46 46 -75 85 -7 8 -14 18 -16 20 -7 10 -17 25 -63 94 -31 47 -42 62 -58 78 l-7 8 17 8 c9 5 19 10 23 11 10 5 33 16 40 21 4 2 13 7 21 11 20 11 17 9 44 27 2 1 7 4 9 5 6 4 26 19 31 23 2 2 4 4 6 5 11 8 47 42 55 53 3 3 7 8 10 12 31 37 50 85 50 126 0 44 -28 87 -67 107 -15 8 -17 9 -41 15 -18 5 -71 8 -98 5z m80 -94 c8 -2 12 -6 14 -10 2 -10 -13 -34 -39 -63 -10 -11 -37 -36 -49 -46 -4 -3 -12 -10 -20 -16 -7 -6 -16 -13 -21 -16 -4 -4 -11 -9 -15 -12 -4 -4 -11 -9 -15 -11 -3 -3 -9 -7 -12 -10 -8 -6 -22 -16 -24 -18 -16 -11 -36 -24 -40 -27 -3 -3 -6 -5 -7 -5 -4 -3 -40 -28 -47 -33 -11 -7 -11 -7 -8 8 1 7 6 38 7 43 1 2 1 8 2 12 0 3 2 10 2 14 1 3 2 10 3 15 1 7 2 13 4 18 0 1 1 5 1 8 1 8 7 37 8 42 3 15 -2 28 -16 38 -5 4 -5 4 2 7 4 1 10 4 14 6 6 3 16 6 38 15 3 0 8 2 12 3 3 2 11 4 17 6 12 5 48 15 61 18 10 2 14 3 20 5 2 1 5 1 6 1 1 0 4 1 7 1 5 2 29 6 43 7 6 1 12 1 12 2 1 1 33 -1 40 -2z"/><path fill="currentColor" transform="translate(0.000000,1020.000000) scale(1.000000,-1.000000)" d="M1717 938 c-4 0 -6 -1 -12 -4 -11 -5 -18 -16 -23 -33 -2 -5 -5 -15 -8 -23 -2 -8 -5 -18 -6 -21 -1 -4 -3 -11 -4 -15 -3 -12 -4 -13 -9 -33 -3 -11 -5 -22 -6 -25 -1 -4 -2 -9 -3 -11 -2 -9 -18 -77 -20 -88 -2 -10 -6 -33 -9 -49 -2 -10 -3 -19 -4 -22 -1 -2 -1 -5 -1 -7 0 -1 -1 -7 -2 -12 -1 -5 -2 -14 -3 -18 -1 -5 -2 -12 -2 -14 -1 -3 -1 -9 -2 -14 -2 -20 -3 -25 -4 -30 -2 -9 -9 -97 -9 -106 0 -9 -18 -50 -37 -82 -2 -5 -5 -10 -6 -11 -1 -2 -4 -7 -7 -11 -2 -4 -8 -12 -12 -18 -8 -12 -27 -32 -30 -32 -7 2 -6 76 2 113 1 2 2 7 2 10 2 16 3 20 4 24 0 2 1 8 2 13 1 5 2 12 2 16 4 16 11 47 12 55 0 1 1 6 2 11 1 4 3 11 3 15 1 3 3 11 4 16 1 5 3 12 3 15 0 3 2 10 3 16 3 21 -4 34 -23 44 -14 6 -17 7 -33 7 -26 0 -31 -5 -44 -41 -2 -4 -4 -12 -7 -17 -2 -6 -4 -12 -5 -14 -2 -9 -23 -58 -31 -76 -1 -3 -4 -9 -6 -14 -8 -17 -28 -59 -38 -76 -3 -4 -5 -8 -5 -10 -15 -28 -54 -79 -59 -77 -2 1 -2 3 -4 17 0 6 3 41 5 54 0 2 1 8 2 12 1 10 5 32 6 39 1 3 2 14 4 24 2 11 4 22 5 26 1 8 5 32 7 45 1 4 2 11 2 13 3 9 2 30 -1 35 -10 20 -43 36 -69 34 -17 -1 -23 -8 -29 -32 -6 -21 -7 -26 -9 -36 -2 -6 -4 -17 -5 -24 -2 -7 -5 -23 -7 -34 -2 -12 -4 -24 -4 -26 -4 -33 -4 -33 -19 -61 -8 -16 -17 -32 -24 -42 -2 -3 -5 -9 -9 -13 -18 -29 -55 -67 -61 -63 -7 4 -6 65 1 116 1 4 1 9 1 12 1 2 1 6 1 8 1 1 1 6 2 10 1 3 1 9 2 12 1 4 6 32 7 43 1 1 1 4 2 7 2 7 3 12 4 18 1 4 2 10 3 15 1 5 3 13 4 20 3 13 10 41 14 54 1 5 3 14 5 21 5 18 13 44 14 45 0 1 7 3 16 5 8 2 17 5 21 5 3 1 9 3 13 4 4 1 17 5 28 8 11 3 22 6 25 7 15 4 24 7 42 16 16 7 24 17 26 29 1 10 -3 17 -12 20 -7 3 -42 2 -64 -1 -4 -1 -11 -1 -16 -2 -6 0 -20 -2 -31 -4 -11 -2 -21 -3 -21 -3 0 1 4 14 10 27 7 20 8 22 9 31 0 8 0 9 -2 14 -9 19 -41 38 -66 39 -20 1 -26 -3 -32 -20 -2 -6 -5 -13 -7 -17 -4 -10 -8 -22 -10 -28 -1 -4 -8 -21 -12 -31 0 -2 -1 -4 -2 -6 -1 -2 -2 -5 -2 -6 -2 -3 -2 -5 -5 -12 -6 -18 -6 -18 -9 -19 -1 0 -5 -1 -9 -2 -4 -1 -8 -2 -10 -3 -2 -1 -8 -2 -13 -4 -6 -2 -12 -4 -14 -4 -2 -1 -4 -2 -5 -2 -2 0 -9 -3 -16 -5 -7 -2 -17 -5 -21 -7 -5 -2 -20 -7 -33 -11 -26 -9 -29 -10 -31 -16 -2 -3 -2 -14 0 -18 0 -1 2 -4 3 -6 12 -25 32 -30 80 -17 2 0 8 2 15 4 6 1 14 3 18 4 10 3 11 3 11 0 -2 -6 -4 -13 -6 -18 -3 -15 -5 -22 -7 -29 -1 -4 -3 -10 -3 -12 -1 -2 -2 -6 -2 -8 -2 -9 -3 -13 -8 -36 l-5 -25 -6 -9 c-13 -22 -45 -58 -51 -58 0 0 -1 4 0 18 1 49 -10 87 -34 111 -11 12 -17 16 -39 26 -3 2 -8 5 -10 7 -20 17 -39 24 -60 21 -9 -1 -21 -4 -25 -6 -38 -16 -63 -37 -91 -72 -10 -13 -29 -46 -34 -58 0 -2 -2 -7 -4 -10 -21 -58 -23 -121 -4 -162 20 -44 61 -75 112 -85 69 -14 144 48 174 146 4 11 4 11 15 19 10 6 26 17 29 19 0 1 3 4 7 7 3 2 6 5 7 6 2 3 4 3 4 0 -1 -3 -3 -64 -3 -73 4 -64 14 -94 38 -118 29 -29 62 -37 89 -23 13 7 35 25 46 41 9 11 22 30 25 36 2 3 5 9 7 13 3 3 7 12 10 18 6 14 6 14 8 7 5 -20 12 -40 19 -49 24 -38 65 -54 100 -41 27 11 53 38 76 80 4 8 7 14 8 14 0 0 1 -4 1 -9 1 -18 5 -36 10 -48 11 -28 27 -45 52 -55 34 -14 71 -1 96 33 19 24 35 54 40 69 2 5 4 5 4 1 0 -2 1 -12 3 -22 13 -75 42 -120 85 -129 11 -2 28 -1 37 2 33 12 45 52 14 50 -9 -1 -11 0 -16 6 -25 27 -32 157 -16 305 0 8 2 18 2 23 1 5 3 13 3 20 2 11 6 36 10 59 1 6 3 16 4 22 2 5 4 17 6 26 4 14 8 29 13 48 1 4 4 14 6 24 2 10 5 20 6 24 2 7 3 12 6 25 2 9 3 14 5 20 1 1 1 4 1 5 0 2 0 4 1 5 0 1 2 8 3 15 1 6 3 13 3 15 4 16 5 61 2 64 0 1 -1 2 -1 3 0 4 -7 15 -11 20 -11 10 -29 16 -44 13z m-891 -430 c13 -24 14 -81 2 -125 -4 -15 -5 -20 -9 -29 -17 -43 -41 -74 -63 -81 -10 -4 -16 2 -21 18 -4 13 -4 54 1 73 1 2 1 5 2 6 0 3 3 14 6 21 8 25 29 66 40 78 1 1 4 4 6 8 7 9 13 16 23 25 10 9 11 9 13 6z"/><path fill="currentColor" transform="translate(0.000000,1020.000000) scale(1.000000,-1.000000)" d="M2134 868 c-8 -1 -15 -5 -18 -10 -4 -4 -16 -28 -16 -29 0 -1 -2 -5 -4 -10 -6 -13 -10 -21 -10 -22 0 0 -1 -2 -2 -4 -1 -3 -2 -6 -3 -8 -1 -4 -3 -7 -6 -14 -2 -4 -6 -16 -11 -27 0 -3 -2 -6 -2 -7 -1 -2 -3 -7 -5 -12 -2 -5 -4 -9 -4 -10 -4 -9 -7 -19 -7 -20 0 -2 -3 -3 -14 -7 -11 -4 -26 -9 -29 -11 -2 0 -7 -3 -13 -5 -7 -2 -15 -6 -20 -8 -4 -2 -8 -4 -9 -4 -2 0 -41 -20 -45 -23 -18 -17 3 -60 28 -59 7 1 18 4 30 8 4 2 12 4 17 6 4 1 11 3 14 4 3 1 6 2 6 2 0 -1 -2 -8 -8 -28 -14 -46 -27 -103 -32 -141 -2 -11 -9 -28 -24 -54 -9 -15 -30 -47 -34 -52 -1 -2 -4 -5 -6 -8 -15 -19 -40 -40 -48 -40 -7 0 -11 42 -6 68 1 3 1 11 2 17 1 10 2 18 5 37 1 3 3 14 5 25 3 17 6 29 14 66 7 34 8 38 9 50 0 17 -2 25 -12 36 -12 14 -46 26 -59 21 -7 -3 -9 -4 -12 -7 -5 -6 -19 -43 -25 -67 -1 -4 -2 -8 -3 -10 -1 -2 -2 -8 -3 -13 -2 -6 -3 -11 -3 -12 -1 -2 -4 -14 -5 -20 -1 -3 -2 -10 -3 -16 -4 -21 -7 -43 -10 -66 -2 -14 -2 -72 0 -84 6 -41 23 -67 57 -84 47 -24 92 -6 129 50 2 4 6 9 8 13 5 6 16 28 18 33 3 6 3 4 5 -10 5 -52 19 -87 45 -112 9 -10 16 -14 37 -23 12 -5 37 -9 47 -6 36 11 55 28 85 75 2 3 5 8 7 13 4 7 7 10 7 7 0 -2 10 -14 18 -22 39 -36 99 -48 144 -29 21 9 30 15 51 34 36 32 69 101 76 160 0 7 2 16 2 21 4 33 -4 81 -18 108 -18 34 -36 49 -69 57 -5 1 -11 4 -15 6 -7 4 -12 7 -19 10 -28 12 -69 -1 -108 -32 -18 -15 -19 -16 -30 -30 -19 -23 -29 -39 -41 -67 -8 -17 -9 -22 -17 -52 -3 -17 -6 -52 -5 -66 0 -5 0 -8 -1 -10 -2 -4 -16 -32 -19 -37 -1 -2 -5 -8 -8 -14 -22 -36 -51 -66 -62 -60 -15 7 -14 112 1 189 0 2 2 9 3 15 1 5 3 14 4 19 2 8 3 14 7 30 0 2 2 7 3 11 1 4 3 12 4 18 2 5 3 11 4 13 1 1 3 9 5 16 5 16 17 53 23 72 3 7 5 14 5 16 1 1 2 2 4 2 1 1 6 2 10 3 4 1 10 3 12 3 6 2 10 2 22 5 5 2 13 4 18 4 4 1 10 3 13 3 5 2 35 8 55 11 16 3 23 5 30 11 14 13 8 44 -10 52 -14 7 -35 6 -99 -2 -9 -1 -17 -2 -18 -3 -2 0 -3 2 -1 3 0 1 3 5 5 11 2 5 7 17 11 26 21 49 22 56 15 70 -10 21 -47 41 -69 37z m244 -343 c13 -19 16 -77 6 -119 -5 -21 -11 -38 -17 -53 -1 -2 -3 -6 -4 -8 -9 -24 -32 -59 -47 -72 -27 -23 -42 -16 -49 21 -2 17 0 46 6 67 0 1 2 6 3 10 6 21 20 57 27 69 0 1 3 5 5 10 4 7 7 13 17 27 11 15 46 50 51 51 0 0 1 -1 2 -3z"/><path fill="#d83d2a" transform="translate(0.000000,1020.000000) scale(1.000000,-1.000000)" d="M1869 805 c-29 -9 -57 -43 -62 -77 -5 -26 0 -44 14 -58 14 -14 32 -19 51 -14 45 11 80 83 59 120 -14 24 -39 36 -62 29z"/><path fill="currentColor" transform="translate(0.000000,1020.000000) scale(1.000000,-1.000000)" d="M2660 405 c-22 -8 -44 -30 -59 -57 -2 -4 -5 -9 -6 -11 -12 -22 -18 -60 -13 -83 8 -34 40 -54 71 -47 1 1 4 1 6 2 5 1 17 7 22 11 3 2 5 4 6 4 3 0 28 29 31 36 3 4 4 3 4 -3 2 -13 19 -35 33 -41 33 -16 69 2 89 45 9 18 12 28 15 45 1 8 1 38 0 44 -3 15 -12 31 -21 37 -4 3 -15 7 -18 7 -1 0 -3 1 -6 2 -30 15 -73 -18 -89 -69 -2 -6 -4 -12 -4 -12 0 -4 -11 -21 -19 -29 -30 -33 -43 -42 -58 -42 -23 0 -14 64 15 108 10 14 12 15 12 6 0 -15 8 -25 19 -21 9 3 14 13 14 31 0 22 -6 31 -25 39 -5 2 -12 1 -19 -2z m150 -45 c8 -14 4 -57 -8 -83 -7 -16 -20 -30 -24 -27 -3 3 -7 23 -5 32 0 3 1 9 2 13 4 23 14 45 29 63 4 5 4 5 6 2z"/><path fill="currentColor" transform="translate(0.000000,1020.000000) scale(1.000000,-1.000000)" d="M2899 403 c-6 -2 -8 -5 -12 -14 -2 -4 -7 -26 -8 -34 -1 -5 -1 -11 -2 -15 -4 -25 -5 -86 -2 -100 3 -15 9 -21 20 -21 12 0 15 4 21 28 7 28 15 55 22 73 2 5 3 10 4 11 0 0 0 1 1 1 1 0 1 -10 1 -27 1 -38 3 -48 9 -56 8 -9 21 -9 29 -1 4 4 11 20 21 50 2 4 4 10 4 11 1 1 1 3 2 4 0 1 1 4 2 5 0 1 2 5 3 8 1 3 4 9 6 12 2 4 4 8 4 8 0 1 1 1 1 1 1 0 1 -7 1 -34 0 -56 4 -76 19 -92 13 -14 34 -15 44 -2 2 2 3 5 3 5 0 1 0 2 1 3 4 2 -1 12 -7 12 -3 0 -7 4 -8 8 -4 10 -4 11 -5 58 0 46 0 54 -4 63 -7 23 -31 33 -53 23 -8 -3 -21 -19 -28 -33 -3 -8 -4 -9 -5 -3 -2 21 -9 34 -20 37 -13 5 -28 -3 -37 -19 -4 -7 -5 -6 -3 10 1 12 0 16 -6 20 -4 3 -13 3 -18 0z"/><path fill="#d83d2a" transform="translate(0.000000,1020.000000) scale(1.000000,-1.000000)" d="M2511 284 c-19 -7 -34 -29 -35 -50 -2 -47 58 -45 74 2 10 32 -12 59 -39 48z"/></svg>';
  function run(){
    var f=document.querySelector('footer');if(!f||f.querySelector('.rt-sign'))return;
    var old=f.querySelectorAll('a[href*="rotulito.com"]');
    for(var i=0;i<old.length;i++){var a=old[i],p=a.previousSibling;if(p&&p.nodeType===3)p.nodeValue=p.nodeValue.replace(/\s*·\s*$/,' ');a.parentNode.removeChild(a);}
    var l=(document.documentElement.lang||'es').slice(0,2);
    var T={es:'Web hecha por',ca:'Web feta per',en:'Website by',fr:'Site réalisé par'}[l]||'Web hecha por';
    var ref=f.querySelector('.legal-links a')||f;
    var st=document.createElement('style');
    st.textContent='.rt-sign{display:flex;justify-content:center;padding:22px 16px 96px;border-top:1px solid rgba(255,255,255,.12);margin-top:18px}.rt-sign a{display:inline-flex;align-items:center;gap:10px;color:#fff;text-decoration:none;font-size:15px;font-family:'+getComputedStyle(ref).fontFamily.replace(/'/g,'"')+';opacity:.92}.rt-sign a:hover{opacity:1}.rt-sign svg{height:30px;width:auto;display:block}';
    document.head.appendChild(st);
    var d=document.createElement('div');d.className='rt-sign';
    d.innerHTML='<a href="https://www.rotulito.com" target="_blank" rel="noopener" aria-label="'+T+' Rotulito"><span>'+T+'</span>'+SVG+'</a>';
    f.appendChild(d);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
})();

/* visor de fotos común */
(function(){if(document.querySelector('script[src^="/lightbox.js"]'))return;var s=document.createElement("script");s.src="/lightbox.js?v=20261024";s.defer=true;document.head.appendChild(s);})();
