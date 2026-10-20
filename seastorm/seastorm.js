/* Plata Marine · página SeaStorm (ES/CA/EN/FR): formulario de presupuesto y vídeo con carga al pulsar.
   Formulario:
   - Envío a la hoja de leads (source 'seastorm'); la confirmación solo aparece si el servidor responde ok:true (submit-confirmed.js).
   - Antispam: campo trampa y espera mínima de submit-confirmed.js + validación real de nombre, email y teléfono.
   Vídeo:
   - Hasta que se pulsa el botón solo se muestra una foto propia: no se hace ninguna petición a YouTube.
   - Al pulsar se inserta el reproductor de youtube-nocookie.com. */
(function(){
  'use strict';
  var LANG=location.pathname.indexOf('/ca/')===0?'ca':location.pathname.indexOf('/en/')===0?'en':location.pathname.indexOf('/fr/')===0?'fr':'es';

  document.querySelectorAll('.ss-video[data-yt]').forEach(function(box){
    var b=box.querySelector('button'); if(!b) return;
    b.addEventListener('click',function(){
      var id=box.getAttribute('data-yt'); if(!/^[\w-]{6,20}$/.test(id)) return;
      var f=document.createElement('iframe');
      f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0&playsinline=1';
      f.title=box.getAttribute('data-title')||'SeaStorm';
      f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      f.allowFullscreen=true;
      f.referrerPolicy='strict-origin-when-cross-origin';
      box.replaceChild(f,b);
      if(window.pmTrack) window.pmTrack('video_start',{video_provider:'youtube',video_id:id,placement:'seastorm'});
    });
  });

  var f=document.getElementById('ssForm'); if(!f) return;
  var LEADS_URL='https://script.google.com/macros/s/AKfycbwJtBkktakE0qgmu_b8oHOOopCDnG6BDpBjg2zBUsZKi8l3_OBEuez_OHWmE9j8qCBF/exec';
  var T={
    es:{consent:'Marca la casilla de privacidad para poder enviarlo.',req:'Completa este campo.',name:'Escribe tu nombre (solo letras).',email:'Revisa el email, por ejemplo nombre@email.com.',tel:'Revisa el teléfono: por ejemplo 612 345 678 o +33 6 12 34 56 78.',
        sending:'Enviando…',ok:'Solicitud recibida. Te contesto en 24 horas laborables.',okBtn:'Enviado ✓',send:'Pedir presupuesto',
        fail:'No he podido confirmar que el mensaje ha llegado. Tus datos siguen aquí: vuelve a intentarlo en unos minutos o escríbeme a juan@platamarine.com.'},
    ca:{consent:'Marca la casella de privacitat per poder enviar-ho.',req:'Completa aquest camp.',name:'Escriu el teu nom (només lletres).',email:'Revisa el correu, per exemple nom@correu.com.',tel:'Revisa el telèfon: per exemple 612 345 678 o +33 6 12 34 56 78.',
        sending:'Enviant…',ok:'Sol·licitud rebuda. Et contesto en 24 hores laborables.',okBtn:'Enviat ✓',send:'Demanar pressupost',
        fail:"No he pogut confirmar que el missatge ha arribat. Les teves dades segueixen aquí: torna-ho a provar d'aquí a uns minuts o escriu-me a juan@platamarine.com."},
    en:{consent:'Please tick the privacy box so I can receive it.',req:'Please fill in this field.',name:'Please enter your name (letters only).',email:'Please check the email, e.g. name@email.com.',tel:'Please check the phone number, with the international code, e.g. +44 7700 900123.',
        sending:'Sending…',ok:'Request received. I will reply within 24 working hours.',okBtn:'Sent ✓',send:'Request a quote',
        fail:'I could not confirm that your message arrived. Your details are still here: please try again in a few minutes or write to juan@platamarine.com.'},
    fr:{consent:'Cochez la case de confidentialité pour pouvoir l’envoyer.',req:'Veuillez remplir ce champ.',name:'Indiquez votre nom (lettres uniquement).',email:"Vérifiez l'e-mail, par exemple nom@email.fr.",tel:"Vérifiez le numéro, avec l'indicatif international, par exemple +33 6 12 34 56 78.",
        sending:'Envoi…',ok:'Demande reçue. Je vous réponds sous 24 heures ouvrées.',okBtn:'Envoyé ✓',send:'Demander un devis',
        fail:"Je n'ai pas pu confirmer que votre message est bien arrivé. Vos informations sont toujours là : réessayez dans quelques minutes ou écrivez à juan@platamarine.com."}
  }[LANG];
  var NEED={barco:'Solo barco',motor:'Barco y motor',llave:'Llave en mano (barco, motor, remolque y matriculación)'};
  function el(id){return document.getElementById(id);}
  function v(id){var e=el(id);return e?e.value.trim():'';}
  var status=el('ss_status'), btn=el('ss_send'), sent=false, busy=false;
  function okName(s){ return s.length>=2 && /\p{L}/u.test(s) && !/[0-9@]|https?:|www\./i.test(s); }
  function okEmail(s){ return /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(s); }
  function okTel(s){ var d=s.replace(/[\s().-]/g,''); return /^[6-9]\d{8}$/.test(d) || /^(\+|00)\d{8,15}$/.test(d); }
  function check(){
    var rules=[['ss_name',okName,T.name],['ss_tel',okTel,T.tel],['ss_email',okEmail,T.email]];
    var first=null;
    rules.forEach(function(r){ var e=el(r[0]); if(!e) return; var val=e.value.trim(), bad=!r[1](val); e.setCustomValidity(bad?(val?r[2]:T.req):''); if(bad&&!first) first=e; });
    var c=el('ss_consent'); if(c){ c.setCustomValidity(c.checked?'':T.consent); if(!c.checked&&!first) first=c; }
    if(first){ first.reportValidity(); return false; }
    return true;
  }
  f.addEventListener('input',function(e){ if(e.target.setCustomValidity) e.target.setCustomValidity(''); });
  f.addEventListener('change',function(e){ if(e.target.setCustomValidity) e.target.setCustomValidity(''); });
  f.addEventListener('submit',function(e){
    e.preventDefault();
    if(sent||busy||!check()) return;
    if(!window.submitConfirmed){ status.hidden=false; status.textContent=T.fail; return; }
    var model=v('ss_model')==='?'?'SeaStorm (sin decidir)':v('ss_model');
    var detail=model+' | '+(NEED[v('ss_need')]||v('ss_need'))+(v('ss_color')?' | Color: '+v('ss_color'):'')+(v('ss_zone')?' | Zona: '+v('ss_zone'):'')+' | Email: '+v('ss_email')+(v('ss_msg')?' | Mensaje: '+v('ss_msg'):'');
    var payload={source:'seastorm',barco:model,nombre:v('ss_name'),telefono:v('ss_tel'),email:v('ss_email'),detail:detail,lang:LANG,page:location.pathname,ua:navigator.userAgent.slice(0,120),consent:true,consent_v:'2026-10',consent_at:new Date().toISOString()};
    busy=true; btn.disabled=true; btn.textContent=T.sending; status.hidden=false; status.textContent=T.sending;
    window.submitConfirmed(LEADS_URL,payload,'json',f).then(function(){
      sent=true; busy=false; status.textContent=T.ok; btn.textContent=T.okBtn;
      if(window.pmTrack) window.pmTrack('generate_lead',{form_id:'seastorm',contact_purpose:'quote',placement:'seastorm',boat:model});
    }).catch(function(){
      busy=false; status.textContent=T.fail; btn.disabled=false; btn.textContent=T.send;
      if(window.pmTrack) window.pmTrack('contact_form_error',{form_id:'seastorm'});
    });
  });
})();
