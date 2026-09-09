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
    var css='#pm-ck{position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;max-width:520px;margin:0 auto;background:#0E3042;color:#E3E9EC;border-top:3px solid #B7C3CB;border-radius:10px;padding:18px 20px;box-shadow:0 18px 45px rgba(13,28,39,.35);font-family:"Archivo","Helvetica Neue",Arial,sans-serif;font-size:14px;line-height:1.5}#pm-ck p{margin:0 0 12px}#pm-ck a{color:#fff}#pm-ck .b{display:flex;gap:10px;flex-wrap:wrap}#pm-ck button{font:600 14px "Archivo","Helvetica Neue",Arial,sans-serif;padding:10px 16px;border-radius:7px;cursor:pointer;border:1px solid rgba(255,255,255,.55);background:transparent;color:#fff}#pm-ck button.ok{background:#B58A2C;border-color:#B58A2C;color:#0D1C27}@media(min-width:820px){#pm-ck{left:auto;right:24px;bottom:24px;margin:0}}';
    var st=document.createElement('style'); st.textContent=css; document.head.appendChild(st);
    var d=document.createElement('div'); d.id='pm-ck'; d.setAttribute('role','dialog'); d.setAttribute('aria-label','Cookies');
    d.innerHTML='<p>Usamos cookies de Google Analytics solo para saber qué páginas se visitan y mejorar la web. No hay publicidad ni se venden datos. <a href="/#quien">Más información</a>.</p><div class="b"><button type="button" class="ok" id="pm-ck-all">Aceptar todas</button><button type="button" id="pm-ck-ess">Solo necesarias</button></div>';
    document.body.appendChild(d);
    document.getElementById('pm-ck-all').onclick=function(){set('all');accept();d.remove();};
    document.getElementById('pm-ck-ess').onclick=function(){set('essential');d.remove();};
  }
  if(document.body) show(); else document.addEventListener('DOMContentLoaded',show);
})();
