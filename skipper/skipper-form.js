/* Plata Marine · formulario de presupuesto SKIPPER (ES/CA/EN/FR).
   - Envío a la hoja de leads (source 'skipper'); la confirmación solo aparece si el servidor responde ok:true (submit-confirmed.js).
   - Antispam: campo trampa y espera mínima de submit-confirmed.js + validación real de nombre, email y teléfono. */
(function(){
  'use strict';
  var f=document.getElementById('skForm'); if(!f) return;
  var LEADS_URL='https://script.google.com/macros/s/AKfycbwJtBkktakE0qgmu_b8oHOOopCDnG6BDpBjg2zBUsZKi8l3_OBEuez_OHWmE9j8qCBF/exec';
  var LANG=location.pathname.indexOf('/ca/')===0?'ca':location.pathname.indexOf('/en/')===0?'en':location.pathname.indexOf('/fr/')===0?'fr':'es';
  var T={
    es:{consent:'Marca la casilla de privacidad para poder enviarlo.',req:'Completa este campo.',name:'Escribe tu nombre (solo letras).',email:'Revisa el email, por ejemplo nombre@email.com.',tel:'Revisa el teléfono: con prefijo internacional, por ejemplo 612 345 678 o +33 6 12 34 56 78.',url:'El enlace no parece correcto. Si no lo tienes, déjalo en blanco.',
        sending:'Enviando…',ok:'Solicitud recibida. Te contesto en 24 horas laborables.',okBtn:'Enviado ✓',send:'Solicitar oferta personalizada',
        fail:'No he podido confirmar que el mensaje ha llegado. Tus datos siguen aquí: vuelve a intentarlo en unos minutos o escríbeme a juan@platamarine.com.'},
    ca:{consent:'Marca la casella de privacitat per poder enviar-ho.',req:'Completa aquest camp.',name:'Escriu el teu nom (només lletres).',email:'Revisa el correu, per exemple nom@correu.com.',tel:'Revisa el telèfon: amb prefix internacional, per exemple 612 345 678 o +33 6 12 34 56 78.',url:"L'enllaç no sembla correcte. Si no el tens, deixa-ho en blanc.",
        sending:'Enviant…',ok:'Sol·licitud rebuda. Et contesto en 24 hores laborables.',okBtn:'Enviat ✓',send:'Sol·licitar oferta personalitzada',
        fail:"No he pogut confirmar que el missatge ha arribat. Les teves dades segueixen aquí: torna-ho a provar d'aquí a uns minuts o escriu-me a juan@platamarine.com."},
    en:{consent:'Please tick the privacy box so I can receive it.',req:'Please fill in this field.',name:'Please enter your name (letters only).',email:'Please check the email, e.g. name@email.com.',tel:'Please check the phone number, with the international code, e.g. +44 7700 900123.',url:"That link doesn't look right. If you don't have it, leave it blank.",
        sending:'Sending…',ok:'Request received. I will reply within 24 working hours.',okBtn:'Sent ✓',send:'Request a personalised offer',
        fail:'I could not confirm that your message arrived. Your details are still here: please try again in a few minutes or write to juan@platamarine.com.'},
    fr:{consent:'Cochez la case de confidentialité pour pouvoir l’envoyer.',req:'Veuillez remplir ce champ.',name:'Indiquez votre nom (lettres uniquement).',email:"Vérifiez l'e-mail, par exemple nom@email.fr.",tel:"Vérifiez le numéro, avec l'indicatif international, par exemple +33 6 12 34 56 78.",url:"Le lien ne semble pas correct. Si vous ne l'avez pas, laissez ce champ vide.",
        sending:'Envoi…',ok:'Demande reçue. Je vous réponds sous 24 heures ouvrées.',okBtn:'Envoyé ✓',send:'Demander une offre personnalisée',
        fail:"Je n'ai pas pu confirmer que votre message est bien arrivé. Vos informations sont toujours là : réessayez dans quelques minutes ou écrivez à juan@platamarine.com."},
  }[LANG];
  function el(id){return document.getElementById(id);}
  function v(id){var e=el(id);return e?e.value.trim():'';}
  var status=el('sk_status'), btn=el('sk_send'), sent=false, busy=false;
  function okName(s){ return s.length>=2 && /\p{L}/u.test(s) && !/[0-9@]|https?:|www\./i.test(s); }
  function okEmail(s){ return /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(s); }
  function okTel(s){ var d=s.replace(/[\s().-]/g,''); return /^[6-9]\d{8}$/.test(d) || /^(\+|00)\d{8,15}$/.test(d); }
  function okUrl(s){ return !s || /^(https?:\/\/)?[^\s.]+\.[^\s]{2,}$/i.test(s); }
  function check(){
    var rules=[['sk_name',okName,T.name],['sk_email',okEmail,T.email],['sk_tel',okTel,T.tel]];
    var first=null;
    rules.forEach(function(r){ var e=el(r[0]); if(!e) return; var bad=!r[1](e.value.trim()); e.setCustomValidity(bad?(e.value.trim()?r[2]:T.req):''); if(bad&&!first) first=e; });
    var c=el('sk_consent'); if(c){ c.setCustomValidity(c.checked?'':T.consent); if(!c.checked&&!first) first=c; }
    if(first){ first.reportValidity(); return false; }
    return true;
  }
  f.addEventListener('input',function(e){ if(e.target.setCustomValidity) e.target.setCustomValidity(''); });
  f.addEventListener('submit',function(e){
    e.preventDefault();
    if(sent||busy||!check()) return;
    if(!window.submitConfirmed){ status.hidden=false; status.textContent=T.fail; return; }
    var detail='SKIPPER '+v('sk_model')+(v('sk_when')?' | Cuándo: '+v('sk_when'):'')+(v('sk_zone')?' | Zona: '+v('sk_zone'):'')+' | Email: '+v('sk_email')+(v('sk_msg')?' | Mensaje: '+v('sk_msg'):'');
    var payload={source:'skipper',barco:'SKIPPER '+v('sk_model'),nombre:v('sk_name'),telefono:v('sk_tel'),email:v('sk_email'),detail:detail,lang:LANG,page:location.pathname,ua:navigator.userAgent.slice(0,120),consent:true,consent_v:'2026-10',consent_at:new Date().toISOString()};
    busy=true; btn.disabled=true; btn.textContent=T.sending; status.hidden=false; status.textContent=T.sending;
    window.submitConfirmed(LEADS_URL,payload,'json',f).then(function(){
      sent=true; busy=false; status.textContent=T.ok; btn.textContent=T.okBtn;
      if(window.pmTrack) window.pmTrack('generate_lead',{form_id:'skipper',contact_purpose:'quote',placement:'skipper',boat:'SKIPPER '+v('sk_model')});
    }).catch(function(){
      busy=false; status.textContent=T.fail; btn.disabled=false; btn.textContent=T.send;
      if(window.pmTrack) window.pmTrack('contact_form_error',{form_id:'skipper'});
    });
  });
})();
