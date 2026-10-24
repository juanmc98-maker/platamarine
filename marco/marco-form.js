/* Plata Marine · página de modelo Mar.Co: formulario de presupuesto (ES/CA/EN/FR), galería, vídeos y submenú.
   - Envío a la hoja de leads (source 'marco'), con la configuración si la hay; confirmación solo con ok:true del servidor (submit-confirmed.js).
   - Antispam: campo trampa y espera mínima de submit-confirmed.js + validación real de nombre, email y teléfono. */
(function(){
  'use strict';
  var f=document.getElementById('mcForm'); if(!f) return;
  var LEADS_URL='https://script.google.com/macros/s/AKfycbwJtBkktakE0qgmu_b8oHOOopCDnG6BDpBjg2zBUsZKi8l3_OBEuez_OHWmE9j8qCBF/exec';
  var LANG=(document.documentElement.lang||'es').slice(0,2);
  var T={
    es:{consent:'Marca la casilla de privacidad para poder enviarlo.',req:'Completa este campo.',name:'Escribe tu nombre (solo letras).',email:'Revisa el email, por ejemplo nombre@email.com.',tel:'Revisa el teléfono: con prefijo internacional, por ejemplo 612 345 678 o +33 6 12 34 56 78.',
        sending:'Enviando…',ok:'Solicitud recibida. Te contesto en 24 horas laborables.',okBtn:'Enviado ✓',send:'Solicitar presupuesto',
        fail:'No he podido confirmar que el mensaje ha llegado. Tus datos siguen aquí: vuelve a intentarlo en unos minutos o escríbeme a juan@platamarine.com.'},
    ca:{consent:'Marca la casella de privacitat per poder enviar-ho.',req:'Completa aquest camp.',name:'Escriu el teu nom (només lletres).',email:'Revisa el correu, per exemple nom@correu.com.',tel:'Revisa el telèfon: amb prefix internacional, per exemple 612 345 678 o +33 6 12 34 56 78.',
        sending:'Enviant…',ok:'Sol·licitud rebuda. Et contesto en 24 hores laborables.',okBtn:'Enviat ✓',send:'Sol·licitar pressupost',
        fail:"No he pogut confirmar que el missatge ha arribat. Les teves dades segueixen aquí: torna-ho a provar d'aquí a uns minuts o escriu-me a juan@platamarine.com."},
    en:{consent:'Please tick the privacy box so I can receive it.',req:'Please fill in this field.',name:'Please enter your name (letters only).',email:'Please check the email, e.g. name@email.com.',tel:'Please check the phone number, with the international code, e.g. +44 7700 900123.',
        sending:'Sending…',ok:'Request received. I will reply within 24 working hours.',okBtn:'Sent ✓',send:'Request a quote',
        fail:'I could not confirm that your message arrived. Your details are still here: please try again in a few minutes or write to juan@platamarine.com.'},
    fr:{consent:'Cochez la case de confidentialité pour pouvoir l’envoyer.',req:'Veuillez remplir ce champ.',name:'Indiquez votre nom (lettres uniquement).',email:"Vérifiez l'e-mail, par exemple nom@email.fr.",tel:"Vérifiez le numéro, avec l'indicatif international, par exemple +33 6 12 34 56 78.",
        sending:'Envoi…',ok:'Demande reçue. Je vous réponds sous 24 heures ouvrées.',okBtn:'Envoyé ✓',send:'Demander un devis',
        fail:"Je n'ai pas pu confirmer que votre message est bien arrivé. Vos informations sont toujours là : réessayez dans quelques minutes ou écrivez à juan@platamarine.com."}
  }[LANG]||null; if(!T) return;
  function el(id){return document.getElementById(id);}
  function v(id){var e=el(id);return e?e.value.trim():'';}
  var status=el('mc_status'), btn=el('mc_send'), sent=false, busy=false, model=f.getAttribute('data-model')||'Mar.Co';
  function okName(s){ return s.length>=2 && /\p{L}/u.test(s) && !/[0-9@]|https?:|www\./i.test(s); }
  function okEmail(s){ return /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(s); }
  function okTel(s){ var d=s.replace(/[\s().-]/g,''); return /^[6-9]\d{8}$/.test(d) || /^(\+|00)\d{8,15}$/.test(d); }
  function check(){
    var rules=[['mc_name',okName,T.name],['mc_email',okEmail,T.email],['mc_tel',okTel,T.tel]],first=null;
    rules.forEach(function(r){ var e=el(r[0]); var bad=!r[1](e.value.trim()); e.setCustomValidity(bad?(e.value.trim()?r[2]:T.req):''); if(bad&&!first) first=e; });
    var c=el('mc_consent'); c.setCustomValidity(c.checked?'':T.consent); if(!c.checked&&!first) first=c;
    if(first){ first.reportValidity(); return false; }
    return true;
  }
  f.addEventListener('input',function(e){ if(e.target.setCustomValidity) e.target.setCustomValidity(''); });
  f.addEventListener('submit',function(e){
    e.preventDefault();
    if(sent||busy||!check()) return;
    if(!window.submitConfirmed){ status.hidden=false; status.textContent=T.fail; return; }
    var cfg=(el('mc_cfg_w')&&!el('mc_cfg_w').hidden)?v('mc_cfg'):'';
    var detail=model+(cfg?' | Configuración: '+cfg.replace(/\n/g,' · '):'')+(v('mc_when')?' | Cuándo: '+v('mc_when'):'')+(v('mc_zone')?' | Zona: '+v('mc_zone'):'')+' | Email: '+v('mc_email')+(v('mc_msg')?' | Mensaje: '+v('mc_msg'):'')+(cfg?' | Enlace: '+location.href:'');
    var payload={source:'marco',barco:model,nombre:v('mc_name'),telefono:v('mc_tel'),email:v('mc_email'),detail:detail,lang:LANG,page:location.pathname,ua:navigator.userAgent.slice(0,120),consent:true,consent_v:'2026-10',consent_at:new Date().toISOString()};
    busy=true; btn.disabled=true; btn.textContent=T.sending; status.hidden=false; status.textContent=T.sending;
    window.submitConfirmed(LEADS_URL,payload,'json',f).then(function(){
      sent=true; busy=false; status.textContent=T.ok; btn.textContent=T.okBtn;
      if(window.pmTrack) window.pmTrack('generate_lead',{form_id:'marco',contact_purpose:'quote',placement:'marco',boat:model});
    }).catch(function(){
      busy=false; status.textContent=T.fail; btn.disabled=false; btn.textContent=T.send;
      if(window.pmTrack) window.pmTrack('contact_form_error',{form_id:'marco'});
    });
  });
})();
/* galería: ver todas (también al abrir una foto, para que el visor pase por todas) */
(function(){var b=document.getElementById('mm-more'),g=document.getElementById('mm-gal');if(!g)return;function all(){g.classList.remove('fold');if(b&&b.parentNode)b.parentNode.removeChild(b);}
if(b)b.addEventListener('click',all);window.addEventListener('click',function(e){if(e.target&&e.target.closest&&e.target.closest('#mm-gal'))all();},true);})();
/* vídeos: se cargan solo al dar al play (youtube-nocookie) */
(function(){[].forEach.call(document.querySelectorAll('.mm-video[data-yt]'),function(v){var b=v.querySelector('button');if(!b)return;b.addEventListener('click',function(){var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+v.getAttribute('data-yt')+'?autoplay=1&rel=0';f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';f.allowFullscreen=true;f.title=b.getAttribute('aria-label')||'';v.innerHTML='';v.appendChild(f);});});})();
/* submenú: marca la sección visible */
(function(){var a=[].slice.call(document.querySelectorAll('.mm-sub a'));if(!a.length||!('IntersectionObserver' in window))return;
a.forEach(function(x){var s=document.querySelector(x.getAttribute('href'));if(!s)return;new IntersectionObserver(function(en){if(en[0].isIntersecting){a.forEach(function(y){y.classList.remove('on');});x.classList.add('on');}},{rootMargin:'-45% 0px -50% 0px'}).observe(s);});})();
