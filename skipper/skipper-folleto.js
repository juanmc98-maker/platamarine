/* Plata Marine · descarga del folleto PDF de cada SKIPPER (ES/CA/EN/FR).
   - Nombre, email y teléfono obligatorios con validación real (mismas reglas que skipper-form.js).
   - Envío a la hoja de leads (source 'skipper-folleto') con submit-confirmed.js: campo trampa y espera mínima.
   - El enlace al PDF solo se muestra cuando el servidor confirma el envío (ok:true). */
(function(){
  'use strict';
  var f=document.getElementById('skfForm'); if(!f) return;
  var LEADS_URL='https://script.google.com/macros/s/AKfycbwJtBkktakE0qgmu_b8oHOOopCDnG6BDpBjg2zBUsZKi8l3_OBEuez_OHWmE9j8qCBF/exec';
  var LANG=location.pathname.indexOf('/ca/')===0?'ca':location.pathname.indexOf('/en/')===0?'en':location.pathname.indexOf('/fr/')===0?'fr':'es';
  var T={
    es:{consent:'Marca la casilla de privacidad para poder descargarlo.',req:'Completa este campo.',name:'Escribe tu nombre (solo letras).',email:'Revisa el email, por ejemplo nombre@email.com.',tel:'Revisa el teléfono: con prefijo internacional, por ejemplo 612 345 678 o +33 6 12 34 56 78.',
        sending:'Un momento…',ok:'¡Listo! La descarga empieza ahora. Si no se abre, toca el botón.',okBtn:'Enviado ✓',send:'Descargar el folleto',
        fail:'No he podido confirmar el envío. Tus datos siguen aquí: vuelve a intentarlo en unos minutos o escríbeme a juan@platamarine.com y te lo mando.'},
    ca:{consent:'Marca la casella de privacitat per poder descarregar-lo.',req:'Completa aquest camp.',name:'Escriu el teu nom (només lletres).',email:'Revisa el correu, per exemple nom@correu.com.',tel:'Revisa el telèfon: amb prefix internacional, per exemple 612 345 678 o +33 6 12 34 56 78.',
        sending:'Un moment…',ok:'Fet! La descàrrega comença ara. Si no s’obre, toca el botó.',okBtn:'Enviat ✓',send:'Descarregar el fullet',
        fail:"No he pogut confirmar l'enviament. Les teves dades segueixen aquí: torna-ho a provar d'aquí a uns minuts o escriu-me a juan@platamarine.com i te l'envio."},
    en:{consent:'Please tick the privacy box to download it.',req:'Please fill in this field.',name:'Please enter your name (letters only).',email:'Please check the email, e.g. name@email.com.',tel:'Please check the phone number, with the international code, e.g. +44 7700 900123.',
        sending:'One moment…',ok:'Done! The download is starting. If it does not open, tap the button.',okBtn:'Sent ✓',send:'Download the brochure',
        fail:'I could not confirm your request. Your details are still here: please try again in a few minutes or write to juan@platamarine.com and I will send it to you.'},
    fr:{consent:'Cochez la case de confidentialité pour pouvoir la télécharger.',req:'Veuillez remplir ce champ.',name:'Indiquez votre nom (lettres uniquement).',email:"Vérifiez l'e-mail, par exemple nom@email.fr.",tel:"Vérifiez le numéro, avec l'indicatif international, par exemple +33 6 12 34 56 78.",
        sending:'Un instant…',ok:'C’est fait ! Le téléchargement commence. S’il ne s’ouvre pas, touchez le bouton.',okBtn:'Envoyé ✓',send:'Télécharger la brochure',
        fail:"Je n'ai pas pu confirmer votre demande. Vos informations sont toujours là : réessayez dans quelques minutes ou écrivez à juan@platamarine.com et je vous l'envoie."}
  }[LANG];
  function el(id){return document.getElementById(id);}
  function v(id){var e=el(id);return e?e.value.trim():'';}
  var status=el('skf_status'), btn=el('skf_send'), done=el('skf_done'), dl=el('skf_dl'), sent=false, busy=false;
  var MODEL=f.getAttribute('data-model')||'SKIPPER';
  function okName(s){ return s.length>=2 && /\p{L}/u.test(s) && !/[0-9@]|https?:|www\./i.test(s); }
  function okEmail(s){ return /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(s); }
  function okTel(s){ var d=s.replace(/[\s().-]/g,''); return /^[6-9]\d{8}$/.test(d) || /^(\+|00)\d{8,15}$/.test(d); }
  function check(){
    var rules=[['skf_name',okName,T.name],['skf_tel',okTel,T.tel],['skf_email',okEmail,T.email]];
    var first=null;
    rules.forEach(function(r){ var e=el(r[0]); if(!e) return; var bad=!r[1](e.value.trim()); e.setCustomValidity(bad?(e.value.trim()?r[2]:T.req):''); if(bad&&!first) first=e; });
    var c=el('skf_consent'); if(c){ c.setCustomValidity(c.checked?'':T.consent); if(!c.checked&&!first) first=c; }
    if(first){ first.reportValidity(); return false; }
    return true;
  }
  f.addEventListener('input',function(e){ if(e.target.setCustomValidity) e.target.setCustomValidity(''); });
  f.addEventListener('change',function(e){ if(e.target.setCustomValidity) e.target.setCustomValidity(''); });
  f.addEventListener('submit',function(e){
    e.preventDefault();
    if(sent||busy||!check()) return;
    if(!window.submitConfirmed){ status.hidden=false; status.textContent=T.fail; return; }
    var payload={source:'skipper-folleto',barco:MODEL,nombre:v('skf_name'),telefono:v('skf_tel'),email:v('skf_email'),detail:'Folleto '+MODEL,lang:LANG,page:location.pathname,ua:navigator.userAgent.slice(0,120),consent:true,consent_v:'2026-10',consent_at:new Date().toISOString()};
    busy=true; btn.disabled=true; btn.textContent=T.sending; status.hidden=false; status.textContent=T.sending;
    window.submitConfirmed(LEADS_URL,payload,'json',f).then(function(){
      sent=true; busy=false; status.textContent=T.ok; btn.textContent=T.okBtn;
      if(done) done.hidden=false;
      if(dl){ try{ dl.click(); }catch(x){} }
      if(window.pmTrack) window.pmTrack('generate_lead',{form_id:'skipper_folleto',contact_purpose:'brochure',placement:'skipper',boat:MODEL});
    }).catch(function(){
      busy=false; status.textContent=T.fail; btn.disabled=false; btn.textContent=T.send;
      if(window.pmTrack) window.pmTrack('contact_form_error',{form_id:'skipper_folleto'});
    });
  });
})();
