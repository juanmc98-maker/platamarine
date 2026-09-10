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

