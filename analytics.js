/* Plata Marine · Google Analytics 4 con consentimiento (RGPD) */
(function(){
  var ID='G-MJ6S489CXQ', KEY='pm_cookies';
  window.dataLayer=window.dataLayer||[];
  function gtag(){dataLayer.push(arguments);}
  window.gtag=gtag;
  gtag('consent','default',{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',wait_for_update:500});
  function load(){
    if(window.__pmga) return; window.__pmga=true;
    var s=document.createElement('script'); s.async=true; s.src='https://www.googletagmanager.com/gtag/js?id='+ID; document.head.appendChild(s);
    gtag('js',new Date()); gtag('config',ID,{anonymize_ip:true});
  }
  function get(){try{return localStorage.getItem(KEY);}catch(e){return null;}}
  function set(v){try{localStorage.setItem(KEY,v);}catch(e){}}
  function accept(){gtag('consent','update',{analytics_storage:'granted'}); load();}
  var c=get();
  if(c==='all'){accept();return;}
  if(c==='essential'){return;}
  function show(){
    var css='#pm-ck{position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;max-width:520px;margin:0 auto;background:#0E3042;color:#E3E9EC;border-top:3px solid #B7C3CB;border-radius:10px;padding:18px 20px;box-shadow:0 18px 45px rgba(13,28,39,.35);font-family:"Archivo","Helvetica Neue",Arial,sans-serif;font-size:14px;line-height:1.5}#pm-ck p{margin:0 0 12px}#pm-ck a{color:#fff}#pm-ck .b{display:flex;gap:10px;flex-wrap:wrap}#pm-ck button{font:600 14px "Archivo","Helvetica Neue",Arial,sans-serif;padding:10px 16px;border-radius:7px;cursor:pointer;border:1px solid rgba(255,255,255,.55);background:transparent;color:#fff}#pm-ck button.ok{background:#B58A2C;border-color:#B58A2C;color:#0D1C27}@media(min-width:820px){#pm-ck{left:24px;right:auto;bottom:24px;margin:0}}';
    var st=document.createElement('style'); st.textContent=css; document.head.appendChild(st);
    var d=document.createElement('div'); d.id='pm-ck'; d.setAttribute('role','dialog'); d.setAttribute('aria-label','Cookies');
    d.innerHTML='<p>Usamos cookies de Google Analytics solo para saber qué páginas se visitan y mejorar la web. No hay publicidad ni se venden datos. <a href="/cookies.html">Política de cookies</a>.</p><div class="b"><button type="button" class="ok" id="pm-ck-all">Aceptar todas</button><button type="button" id="pm-ck-ess">Solo necesarias</button></div>';
    document.body.appendChild(d);
    document.getElementById('pm-ck-all').onclick=function(){set('all');accept();d.remove();};
    document.getElementById('pm-ck-ess').onclick=function(){set('essential');d.remove();};
  }
  if(document.body) show(); else document.addEventListener('DOMContentLoaded',show);
})();
/* Menú móvil en páginas interiores (la home ya trae el suyo) */
(function(){
  function init(){
    if(document.getElementById('menuBtn')) return;
    var top=document.querySelector('header.top'), wrap=top&&top.querySelector('.wrap'), nav=top&&top.querySelector('.nav');
    if(!top||!wrap||!nav) return;
    var css='.pm-mbtn{display:none;width:42px;height:42px;align-items:center;justify-content:center;border:1px solid #B7C3CB;background:rgba(255,255,255,.55);border-radius:7px;cursor:pointer;color:#0D1C27;padding:0;flex:none}.pm-mbtn span,.pm-mbtn span::before,.pm-mbtn span::after{display:block;width:19px;height:2px;background:currentColor;border-radius:2px;content:"";position:relative;transition:.2s ease}.pm-mbtn span::before{position:absolute;top:-6px}.pm-mbtn span::after{position:absolute;top:6px}.pm-mbtn[aria-expanded="true"] span{background:transparent}.pm-mbtn[aria-expanded="true"] span::before{top:0;transform:rotate(45deg)}.pm-mbtn[aria-expanded="true"] span::after{top:0;transform:rotate(-45deg)}.pm-mnav{display:none;position:absolute;left:0;right:0;top:64px;background:rgba(243,245,246,.985);border-bottom:1px solid #B7C3CB;box-shadow:0 14px 30px rgba(13,28,39,.08);max-height:calc(100dvh - 64px);overflow-y:auto;z-index:30}.pm-mnav.open{display:block}.pm-mnav .wrap{height:auto;display:grid;grid-template-columns:1fr 1fr;gap:0;padding-top:10px;padding-bottom:16px}.pm-mnav a{font-family:"Archivo","Helvetica Neue",Arial,sans-serif;font-size:14px;font-weight:600;text-decoration:none;color:#0D1C27;padding:12px 6px;border-bottom:1px solid rgba(127,146,158,.18)}.pm-mnav .pm-wide{grid-column:1/-1;margin-top:10px;border-bottom:0;padding:0}.pm-mnav .pm-wide .btn{width:100%;display:inline-flex}@media (max-width:819px){.pm-mbtn{display:inline-flex}header.top{position:sticky}}@media (max-width:480px){.pm-mnav .wrap{grid-template-columns:1fr}.pm-mnav .pm-wide{grid-column:1}}';
    var st=document.createElement('style'); st.textContent=css; document.head.appendChild(st);
    var btn=document.createElement('button'); btn.type='button'; btn.className='pm-mbtn'; btn.id='pmMenuBtn'; btn.setAttribute('aria-expanded','false'); btn.setAttribute('aria-controls','pmMobileNav'); btn.setAttribute('aria-label','Abrir menú'); btn.innerHTML='<span></span>';
    wrap.appendChild(btn);
    var m=document.createElement('nav'); m.className='pm-mnav'; m.id='pmMobileNav'; m.setAttribute('aria-label','Menú móvil');
    var inner=document.createElement('div'); inner.className='wrap';
    nav.querySelectorAll('a').forEach(function(a){var c=a.cloneNode(true); c.removeAttribute('aria-current'); inner.appendChild(c);});
    var wa=top.querySelector('a.btn-wa'); if(wa){var d=document.createElement('div'); d.className='pm-wide'; d.appendChild(wa.cloneNode(true)); inner.appendChild(d);}
    m.appendChild(inner); top.appendChild(m);
    btn.addEventListener('click',function(){var o=!m.classList.contains('open'); m.classList.toggle('open',o); btn.setAttribute('aria-expanded',o?'true':'false'); btn.setAttribute('aria-label',o?'Cerrar menú':'Abrir menú');});
    m.addEventListener('click',function(e){if(e.target.closest('a')){m.classList.remove('open');btn.setAttribute('aria-expanded','false');}});
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();
/* Medición de contactos (solo si hay consentimiento: gtag ignora eventos sin GA cargado) */
(function(){
  function ev(name,params){try{if(window.gtag) gtag('event',name,params||{});}catch(e){}}
  function where(el){var s=el.closest('section,header,footer,aside');return (s&&(s.id||s.className||s.tagName)||'').toString().slice(0,40);}
  document.addEventListener('click',function(e){
    var a=e.target.closest('a,button'); if(!a) return;
    var href=a.getAttribute('href')||'';
    if(href.indexOf('wa.me')>=0||href.indexOf('whatsapp')>=0){ev('click_whatsapp',{location:where(a),label:(a.textContent||'').trim().slice(0,60),page:location.pathname});}
    else if(href.indexOf('mailto:')===0){ev('click_email',{location:where(a),page:location.pathname});}
    else if(href.indexOf('tel:')===0){ev('click_phone',{location:where(a),page:location.pathname});}
    else if(a.matches('a[href*="/barcos/"],a[href*="barcos/"]')&&!a.matches('nav a')){ev('click_boat',{label:href.slice(0,80),page:location.pathname});}
  },true);
  document.addEventListener('submit',function(e){
    var f=e.target; if(!f||!f.id) return;
    ev('form_submit',{form:f.id,page:location.pathname});
  },true);
  window.pmTrack=ev;
})();
/* Aviso discreto de novedades (solo páginas de contenido, una vez cada 30 días) */
(function(){
  var KEY='pm_news', URL='https://script.google.com/macros/s/AKfycbwJtBkktakE0qgmu_b8oHOOopCDnG6BDpBjg2zBUsZKi8l3_OBEuez_OHWmE9j8qCBF/exec';
  var p=location.pathname;
  if(!/^\/(guias|actualidad|navegante|titulaciones)\//.test(p)) return;
  function get(){try{return JSON.parse(localStorage.getItem(KEY)||'null');}catch(e){return null;}}
  function set(v){try{localStorage.setItem(KEY,JSON.stringify({v:v,t:Date.now()}));}catch(e){}}
  var s=get(); if(s&&(s.v==='ok'||Date.now()-s.t<30*864e5)) return;
  var shown=false, timer=null;
  function ready(){ if(document.getElementById('pm-ck')) return false; var m=document.getElementById('pmModal'); if(m&&!m.classList.contains('hidden')) return false; return true; }
  function show(){
    if(shown) return; if(!ready()){ setTimeout(show,8000); return; } shown=true;
    var css='#pm-nl{position:fixed;right:16px;bottom:16px;left:16px;z-index:9990;max-width:360px;margin-left:auto;background:#fff;color:#0D1C27;border-top:3px solid #B58A2C;border-radius:10px;padding:18px 20px 16px;box-shadow:0 18px 45px rgba(13,28,39,.28);font-family:"Archivo","Helvetica Neue",Arial,sans-serif;font-size:14px;line-height:1.45;transform:translateY(20px);opacity:0;transition:.35s ease}#pm-nl.in{transform:none;opacity:1}#pm-nl h4{font-size:16px;margin:0 28px 6px 0;line-height:1.25}#pm-nl p{margin:0 0 10px;color:#3E5462}#pm-nl input[type=email]{width:100%;box-sizing:border-box;font:15px "Archivo","Helvetica Neue",Arial,sans-serif;padding:9px 11px;border:1px solid #B7C3CB;border-radius:6px;margin:0 0 8px}#pm-nl label{display:flex;gap:7px;align-items:flex-start;font-size:12px;color:#3E5462;margin:0 0 10px}#pm-nl label a{color:#0E3042}#pm-nl button.go{font:600 14px "Archivo","Helvetica Neue",Arial,sans-serif;padding:9px 16px;border-radius:7px;cursor:pointer;border:0;background:#128C7E;color:#fff}#pm-nl button.x{position:absolute;top:8px;right:8px;width:30px;height:30px;border:0;background:transparent;font-size:20px;line-height:1;cursor:pointer;color:#7F929E}#pm-nl .m{font-size:12.5px;color:#c0392b;margin:8px 0 0}#pm-nl .m.ok{color:#2e8b57}#pm-nl .lg{font-size:10.5px;color:#7F929E;margin:10px 0 0;line-height:1.4}@media(max-width:480px){#pm-nl{left:12px;right:12px;bottom:12px}}';
    var st=document.createElement('style'); st.textContent=css; document.head.appendChild(st);
    var d=document.createElement('aside'); d.id='pm-nl'; d.setAttribute('aria-label','Novedades de Plata Marine');
    d.innerHTML='<button type="button" class="x" aria-label="Cerrar">×</button><h4>¿Te aviso cuando publique una guía nueva?</h4><p>Un correo al mes como mucho, cuando haya algo que merezca la pena. Sin ofertas ni relleno.</p><form novalidate><input type="email" placeholder="tu@correo.com" autocomplete="email" required><label><input type="checkbox" required> <span>Acepto recibir novedades de Plata Marine según la <a href="/privacidad.html" target="_blank" rel="noopener">política de privacidad</a>. Baja cuando quieras.</span></label><button type="submit" class="go">Apuntarme</button><p class="m"></p><p class="lg">Responsable: Juan Morante Cruz (Plata Marine). Finalidad: enviarte artículos y guías. Derechos en juan@platamarine.com.</p></form>';
    document.body.appendChild(d); requestAnimationFrame(function(){d.classList.add('in');});
    d.querySelector('.x').onclick=function(){set('x');d.remove();};
    d.querySelector('form').onsubmit=function(e){
      e.preventDefault(); var em=d.querySelector('input[type=email]').value.trim(), ok=d.querySelector('input[type=checkbox]').checked, m=d.querySelector('.m'); m.className='m';
      if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)){m.textContent='Revisa el correo, no parece correcto.';return;}
      if(!ok){m.textContent='Marca la casilla para que pueda escribirte.';return;}
      var b=d.querySelector('.go'); b.disabled=true; b.textContent='Enviando…';
      fetch(URL,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain'},body:JSON.stringify({source:'novedades',email:em,consent:true,newsletter:true,consent_v:'2026-09',consent_at:new Date().toISOString(),page:p,ua:navigator.userAgent.slice(0,120)})}).then(function(){
        set('ok'); m.className='m ok'; m.textContent='Apuntado. Te llega un correo de bienvenida en unos minutos.'; b.textContent='Listo';
        try{if(window.gtag)gtag('event','newsletter_signup',{page:p});}catch(x){}
        setTimeout(function(){d.remove();},3000);
      }).catch(function(){m.textContent='No se ha podido enviar. Prueba otra vez más tarde.';b.disabled=false;b.textContent='Apuntarme';});
    };
  }
  function onScroll(){ var h=document.documentElement; var pct=(h.scrollTop+window.innerHeight)/h.scrollHeight; if(pct>0.6){ window.removeEventListener('scroll',onScroll); show(); } }
  function start(){ window.addEventListener('scroll',onScroll,{passive:true}); timer=setTimeout(show,45000); }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',start); else start();
})();

