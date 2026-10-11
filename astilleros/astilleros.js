/* Plata Marine · formulario "¿Eres astillero?" (ES/CA/EN/FR).
   - Envío a la hoja de leads (source 'astillero'); la confirmación solo aparece si el servidor responde ok:true (submit-confirmed.js).
   - Antispam: campo trampa y espera mínima de submit-confirmed.js + validación real de nombre, email y teléfono. */
(function(){
  'use strict';
  var f=document.getElementById('astilleroForm'); if(!f) return;
  var LEADS_URL='https://script.google.com/macros/s/AKfycbwJtBkktakE0qgmu_b8oHOOopCDnG6BDpBjg2zBUsZKi8l3_OBEuez_OHWmE9j8qCBF/exec';
  var LANG=location.pathname.indexOf('/ca/')===0?'ca':location.pathname.indexOf('/en/')===0?'en':location.pathname.indexOf('/fr/')===0?'fr':location.pathname.indexOf('/it/')===0?'it':'es';
  var T={
    es:{req:'Completa este campo.',name:'Escribe tu nombre (solo letras).',email:'Revisa el email, por ejemplo nombre@astillero.com.',tel:'Revisa el teléfono: con prefijo internacional, por ejemplo +39 333 123 4567.',url:'El enlace no parece correcto. Si no lo tienes, déjalo en blanco.',
        sending:'Enviando…',ok:'Mensaje recibido. Te contesto en 24 horas laborables.',okBtn:'Enviado ✓',send:'Enviar',
        fail:'No he podido confirmar que el mensaje ha llegado. Tus datos siguen aquí: vuelve a intentarlo en unos minutos o escríbeme a juan@platamarine.com.'},
    ca:{req:'Completa aquest camp.',name:'Escriu el teu nom (només lletres).',email:'Revisa el correu, per exemple nom@drassana.com.',tel:'Revisa el telèfon: amb prefix internacional, per exemple +39 333 123 4567.',url:"L'enllaç no sembla correcte. Si no el tens, deixa-ho en blanc.",
        sending:'Enviant…',ok:'Missatge rebut. Et contesto en 24 hores laborables.',okBtn:'Enviat ✓',send:'Enviar',
        fail:"No he pogut confirmar que el missatge ha arribat. Les teves dades segueixen aquí: torna-ho a provar d'aquí a uns minuts o escriu-me a juan@platamarine.com."},
    en:{req:'Please fill in this field.',name:'Please enter your name (letters only).',email:'Please check the email, e.g. name@yard.com.',tel:'Please check the phone number, with the international code, e.g. +39 333 123 4567.',url:"That link doesn't look right. If you don't have it, leave it blank.",
        sending:'Sending…',ok:'Message received. I will reply within 24 working hours.',okBtn:'Sent ✓',send:'Send',
        fail:'I could not confirm that your message arrived. Your details are still here: please try again in a few minutes or write to juan@platamarine.com.'},
    fr:{req:'Veuillez remplir ce champ.',name:'Indiquez votre nom (lettres uniquement).',email:"Vérifiez l'e-mail, par exemple nom@chantier.com.",tel:"Vérifiez le numéro, avec l'indicatif international, par exemple +33 6 12 34 56 78.",url:"Le lien ne semble pas correct. Si vous ne l'avez pas, laissez ce champ vide.",
        sending:'Envoi…',ok:'Message reçu. Je vous réponds sous 24 heures ouvrées.',okBtn:'Envoyé ✓',send:'Envoyer',
        fail:"Je n'ai pas pu confirmer que votre message est bien arrivé. Vos informations sont toujours là : réessayez dans quelques minutes ou écrivez à juan@platamarine.com."},
    it:{req:'Compilate questo campo.',name:'Scrivete il vostro nome (solo lettere).',email:"Controllate l'e-mail, ad esempio nome@cantiere.it.",tel:'Controllate il telefono, con il prefisso internazionale, ad esempio +39 333 123 4567.',url:'Il link non sembra corretto. Se non lo avete, lasciate il campo vuoto.',
        sending:'Invio in corso…',ok:'Messaggio ricevuto. Rispondo entro 24 ore lavorative.',okBtn:'Inviato ✓',send:'Invia',
        fail:'Non ho potuto confermare che il messaggio sia arrivato. I vostri dati sono ancora qui: riprovate tra qualche minuto o scrivete a juan@platamarine.com.'},
  }[LANG];
  function el(id){return document.getElementById(id);}
  function v(id){var e=el(id);return e?e.value.trim():'';}
  var status=el('ya_status'), btn=el('ya_send'), sent=false, busy=false;
  function okName(s){ return s.length>=2 && /\p{L}/u.test(s) && !/[0-9@]|https?:|www\./i.test(s); }
  function okEmail(s){ return /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(s); }
  function okTel(s){ var d=s.replace(/[\s().-]/g,''); return /^[6-9]\d{8}$/.test(d) || /^(\+|00)\d{8,15}$/.test(d); }
  function okUrl(s){ return !s || /^(https?:\/\/)?[^\s.]+\.[^\s]{2,}$/i.test(s); }
  function check(){
    var rules=[['ya_yard',function(s){return s.length>=2;},T.req],['ya_name',okName,T.name],['ya_email',okEmail,T.email],['ya_tel',okTel,T.tel],['ya_web',okUrl,T.url]];
    var first=null;
    rules.forEach(function(r){ var e=el(r[0]); if(!e) return; var bad=!r[1](e.value.trim()); e.setCustomValidity(bad?(e.value.trim()?r[2]:(r[0]==='ya_web'?'':T.req)):''); if(bad&&!first) first=e; });
    if(first){ first.reportValidity(); return false; }
    return true;
  }
  f.addEventListener('input',function(e){ if(e.target.setCustomValidity) e.target.setCustomValidity(''); });
  f.addEventListener('submit',function(e){
    e.preventDefault();
    if(sent||busy||!check()) return;
    if(!window.submitConfirmed){ status.hidden=false; status.textContent=T.fail; return; }
    var detail='ASTILLERO: '+v('ya_yard')+(v('ya_web')?' | Web: '+v('ya_web'):'')+(v('ya_country')?' | País: '+v('ya_country'):'')+(v('ya_role')?' | Cargo: '+v('ya_role'):'')+' | Email: '+v('ya_email')+(v('ya_msg')?' | Mensaje: '+v('ya_msg'):'');
    var payload={source:'astillero',nombre:v('ya_name'),telefono:v('ya_tel'),email:v('ya_email'),detail:detail,lang:LANG,page:location.pathname,ua:navigator.userAgent.slice(0,120)};
    busy=true; btn.disabled=true; btn.textContent=T.sending; status.hidden=false; status.textContent=T.sending;
    window.submitConfirmed(LEADS_URL,payload,'json',f).then(function(){
      sent=true; busy=false; status.textContent=T.ok; btn.textContent=T.okBtn;
      if(window.pmTrack) window.pmTrack('generate_lead',{form_id:'astillero',contact_purpose:'yard',placement:'astilleros'});
    }).catch(function(){
      busy=false; status.textContent=T.fail; btn.disabled=false; btn.textContent=T.send;
      if(window.pmTrack) window.pmTrack('contact_form_error',{form_id:'astillero'});
    });
  });
})();
