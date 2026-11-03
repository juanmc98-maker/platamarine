/* Plata Marine · formulario «Te busco barco» de la portada (ES/CA/EN/FR).
   Envío a la hoja de leads (source 'busqueda') con submit-confirmed.js; la confirmación solo
   aparece si el servidor responde ok. Incluye cualificación: para cuándo y cómo pagará. */
(function(){
  'use strict';
  var f=document.getElementById('tbForm'); if(!f) return;
  var LEADS_URL='https://script.google.com/macros/s/AKfycbwJtBkktakE0qgmu_b8oHOOopCDnG6BDpBjg2zBUsZKi8l3_OBEuez_OHWmE9j8qCBF/exec';
  var p=location.pathname, L=p.indexOf('/ca/')===0?'ca':p.indexOf('/en/')===0?'en':p.indexOf('/fr/')===0?'fr':'es';
  var T={
    es:{consent:'Marca la casilla de privacidad para poder enviarlo.',req:'Completa este campo.',name:'Escribe tu nombre (solo letras).',email:'Revisa el email, por ejemplo nombre@email.com.',tel:'Revisa el teléfono: con prefijo internacional, por ejemplo 612 345 678 o +33 6 12 34 56 78.',sending:'Enviando…',ok:'Búsqueda recibida. Te contesto en 24 horas laborables.',okBtn:'Enviado ✓',send:'Envíame tu búsqueda',fail:'No he podido confirmar que el mensaje ha llegado. Tus datos siguen aquí: vuelve a intentarlo en unos minutos o escríbeme a juan@platamarine.com.'},
    ca:{consent:'Marca la casella de privacitat per poder enviar-ho.',req:'Completa aquest camp.',name:'Escriu el teu nom (només lletres).',email:'Revisa el correu, per exemple nom@correu.com.',tel:'Revisa el telèfon: amb prefix internacional, per exemple 612 345 678 o +33 6 12 34 56 78.',sending:'Enviant…',ok:'Cerca rebuda. Et contesto en 24 hores laborables.',okBtn:'Enviat ✓',send:'Envia’m la teva cerca',fail:"No he pogut confirmar que el missatge ha arribat. Les teves dades segueixen aquí: torna-ho a provar d'aquí a uns minuts o escriu-me a juan@platamarine.com."},
    en:{consent:'Please tick the privacy box so I can receive it.',req:'Please fill in this field.',name:'Please enter your name (letters only).',email:'Please check the email, e.g. name@email.com.',tel:'Please check the phone number, with the international code, e.g. +44 7700 900123.',sending:'Sending…',ok:'Search received. I will reply within 24 working hours.',okBtn:'Sent ✓',send:'Send me your search',fail:'I could not confirm that your message arrived. Your details are still here: please try again in a few minutes or write to juan@platamarine.com.'},
    fr:{consent:'Cochez la case de confidentialité pour pouvoir l’envoyer.',req:'Veuillez remplir ce champ.',name:'Indiquez votre nom (lettres uniquement).',email:"Vérifiez l'e-mail, par exemple nom@email.fr.",tel:"Vérifiez le numéro, avec l'indicatif international, par exemple +33 6 12 34 56 78.",sending:'Envoi…',ok:'Recherche reçue. Je vous réponds sous 24 heures ouvrées.',okBtn:'Envoyé ✓',send:'Envoyez-moi votre recherche',fail:"Je n'ai pas pu confirmer que votre message est bien arrivé. Vos informations sont toujours là : réessayez dans quelques minutes ou écrivez à juan@platamarine.com."}
  }[L];
  function $(id){return document.getElementById(id);}
  function v(id){var e=$(id);return e?e.value.trim():'';}
  var status=$('tb_status'), btn=$('tb_send'), sent=false, busy=false, started=false;
  function okName(s){ return s.length>=2 && /\p{L}/u.test(s) && !/[0-9@]|https?:|www\./i.test(s); }
  function okEmail(s){ return /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(s); }
  function okTel(s){ var d=s.replace(/[\s().-]/g,''); return /^[6-9]\d{8}$/.test(d) || /^(\+|00)\d{8,15}$/.test(d); }
  function check(){
    var first=null;
    [['tb_name',okName,T.name],['tb_tel',okTel,T.tel],['tb_email',okEmail,T.email]].forEach(function(r){ var e=$(r[0]); var bad=!r[1](e.value.trim()); e.setCustomValidity(bad?(e.value.trim()?r[2]:T.req):''); if(bad&&!first) first=e; });
    var b=$('tb_bud'); b.setCustomValidity(b.value?'':T.req); if(!b.value&&!first) first=b;
    var c=$('tb_consent'); c.setCustomValidity(c.checked?'':T.consent); if(!c.checked&&!first) first=c;
    if(first){ first.reportValidity(); return false; }
    return true;
  }
  f.addEventListener('input',function(e){ if(e.target.setCustomValidity) e.target.setCustomValidity(''); if(!started){ started=true; if(window.pmTrack) window.pmTrack('quote_start',{placement:'te_busco_barco'}); } });
  f.addEventListener('change',function(e){ if(e.target.setCustomValidity) e.target.setCustomValidity(''); });
  f.addEventListener('submit',function(e){
    e.preventDefault();
    if(sent||busy||!check()) return;
    if(!window.submitConfirmed){ status.hidden=false; status.textContent=T.fail; return; }
    var detail='Te busco barco | Tipo: '+v('tb_type')+' | Presupuesto: '+v('tb_bud')+' | '+v('tb_new')+(v('tb_zone')?' | Zona: '+v('tb_zone'):'')+(v('tb_when')?' | Cuándo: '+v('tb_when'):'')+(v('tb_pay')?' | Pago: '+v('tb_pay'):'')+' | Email: '+v('tb_email')+(v('tb_msg')?' | Mensaje: '+v('tb_msg'):'');
    var payload={source:'busqueda',barco:'Busca: '+v('tb_type')+' ('+v('tb_bud')+')',nombre:v('tb_name'),telefono:v('tb_tel'),email:v('tb_email'),detail:detail,lang:L,page:location.pathname,ua:navigator.userAgent.slice(0,120),consent:true,consent_v:'2026-10',consent_at:new Date().toISOString()};
    busy=true; btn.disabled=true; btn.textContent=T.sending; status.hidden=false; status.textContent=T.sending;
    window.submitConfirmed(LEADS_URL,payload,'json',f).then(function(){
      sent=true; busy=false; status.textContent=T.ok; btn.textContent=T.okBtn;
      if(window.pmTrack) window.pmTrack('generate_lead',{form_id:'busqueda',contact_purpose:'search',placement:'portada'});
    }).catch(function(){
      busy=false; status.textContent=T.fail; btn.disabled=false; btn.textContent=T.send;
      if(window.pmTrack) window.pmTrack('contact_form_error',{form_id:'busqueda'});
    });
  });
})();
