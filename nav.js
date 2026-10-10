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
(function(){if(document.querySelector("script[src^=\"/search.js\"]"))return;var s=document.createElement("script");s.src="/search.js?v=20261007";s.defer=true;document.head.appendChild(s);})();

/* Menú · ¿Cuánto vale mi barco? (7 oct 2026): primer enlace de Recursos › Vender, antes de valora-tu-barco. */
(function(){
  var p=location.pathname,pre=p.indexOf('/ca/')===0?'/ca':p.indexOf('/en/')===0?'/en':p.indexOf('/fr/')===0?'/fr':'';
  var T={'':'¿Cuánto vale mi barco?','/ca':'Quant val el meu vaixell?','/en':'How much is my boat worth?','/fr':'Combien vaut mon bateau ?'}[pre],h=pre+'/cuanto-vale-mi-barco/';
  var as=document.querySelectorAll('.pmx-col a[href$="/herramientas/valora-tu-barco.html"], .pmx-grp a[href$="/herramientas/valora-tu-barco.html"]');
  for(var i=0;i<as.length;i++){if(as[i].parentNode.querySelector('a[href="'+h+'"]'))continue;var a=document.createElement('a');a.href=h;a.textContent=T;if(p===h)a.setAttribute('aria-current','page');as[i].parentNode.insertBefore(a,as[i]);}
})();
