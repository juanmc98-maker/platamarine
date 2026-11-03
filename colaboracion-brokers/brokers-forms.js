/* Plata Marine · formulario de /colaboracion-brokers/ (ES/CA/EN/FR), source 'broker'.
   - Antispam: campo trampa y espera mínima de 3 s de submit-confirmed.js; nombre y teléfono (si se rellena) los valida submit-confirmed.js.
   - Aquí: obligatorios, email, web (si se rellena) y casilla de privacidad. */
(function(){
  'use strict';
  var LEADS_URL='https://script.google.com/macros/s/AKfycbwJtBkktakE0qgmu_b8oHOOopCDnG6BDpBjg2zBUsZKi8l3_OBEuez_OHWmE9j8qCBF/exec';
  var m=/^\/(ca|en|fr)\//.exec(location.pathname), LANG=m?m[1]:'es';
  var T={
    es:{consent:'Marca la casilla de privacidad para poder enviarlo.',req:'Completa este campo.',email:'Revisa el email, por ejemplo nombre@empresa.com.',web:'Revisa la web, por ejemplo www.empresa.com.',sending:'Enviando…',send:'Enviar',
        ok:'Recibido. Te escribo en 24 horas laborables.',okBtn:'Enviado ✓',
        fail:'No he podido confirmar que ha llegado. Tus datos siguen aquí: vuelve a intentarlo en unos minutos o escríbeme a juan@platamarine.com.'},
    ca:{consent:'Marca la casella de privacitat per poder enviar-ho.',req:'Completa aquest camp.',email:'Revisa el correu, per exemple nom@empresa.com.',web:'Revisa la web, per exemple www.empresa.com.',sending:'Enviant…',send:'Enviar',
        ok:'Rebut. T’escric en 24 hores laborables.',okBtn:'Enviat ✓',
        fail:'No he pogut confirmar que ha arribat. Les teves dades segueixen aquí: torna-ho a provar d’aquí a uns minuts o escriu-me a juan@platamarine.com.'},
    en:{consent:'Please tick the privacy box so I can receive it.',req:'Please fill in this field.',email:'Please check the email, e.g. name@company.com.',web:'Please check the website, e.g. www.company.com.',sending:'Sending…',send:'Send',
        ok:'Received. I will reply within 24 working hours.',okBtn:'Sent ✓',
        fail:'I could not confirm that it arrived. Your details are still here: please try again in a few minutes or write to juan@platamarine.com.'},
    fr:{consent:'Cochez la case de confidentialité pour pouvoir l’envoyer.',req:'Veuillez remplir ce champ.',email:'Vérifiez l’e-mail, par exemple nom@societe.fr.',web:'Vérifiez le site, par exemple www.societe.fr.',sending:'Envoi…',send:'Envoyer',
        ok:'Bien reçu. Je vous réponds sous 24 heures ouvrées.',okBtn:'Envoyé ✓',
        fail:'Je n’ai pas pu confirmer la réception. Vos informations sont toujours là : réessayez dans quelques minutes ou écrivez à juan@platamarine.com.'}
  }[LANG];
  function okEmail(s){ return /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(s); }
  function okWeb(s){ return /^(https?:\/\/)?([a-z0-9-]+\.)+[a-z]{2,}(\/\S*)?$/i.test(s); }
  function q(f,n){ var e=f.querySelector('[name="'+n+'"]'); return e?e.value.trim():''; }
  function check(f){
    var first=null;
    f.querySelectorAll('input,select,textarea').forEach(function(e){
      if(e.type==='checkbox'||e.name==='pm_hp_x'||!e.setCustomValidity) return;
      var v=e.value.trim(), msg='';
      if(e.required&&!v) msg=T.req;
      else if(e.type==='email'&&v&&!okEmail(v)) msg=T.email;
      else if(e.name==='web'&&v&&!okWeb(v)) msg=T.web;
      e.setCustomValidity(msg); if(msg&&!first) first=e;
    });
    var c=f.querySelector('input[name=privacidad]');
    if(c){ c.setCustomValidity(c.checked?'':T.consent); if(!c.checked&&!first) first=c; }
    if(first){ first.reportValidity(); return false; }
    return true;
  }
  function wire(f,kind){
    if(!f) return;
    var btn=f.querySelector('button[type=submit]'), st=f.querySelector('.pm-amst'), sent=false, busy=false;
    f.addEventListener('input',function(e){ if(e.target.setCustomValidity) e.target.setCustomValidity(''); });
    f.addEventListener('change',function(e){ if(e.target.setCustomValidity) e.target.setCustomValidity(''); });
    f.addEventListener('submit',function(e){
      e.preventDefault();
      if(sent||busy||!check(f)) return;
      if(!window.submitConfirmed){ st.hidden=false; st.textContent=T.fail; return; }
      var detail='BROKER: '+q(f,'tipo')+' | Empresa: '+q(f,'empresa')+(q(f,'web')?' | Web: '+q(f,'web'):'')+(q(f,'zona')?' | Zona: '+q(f,'zona'):'')+(q(f,'mensaje')?' | Mensaje: '+q(f,'mensaje'):'');
      var payload={source:kind,nombre:q(f,'nombre'),telefono:q(f,'telefono'),email:q(f,'email'),detail:detail,lang:LANG,page:location.pathname,ua:navigator.userAgent.slice(0,120),consent:true,newsletter:false,consent_v:'2026-10',consent_at:new Date().toISOString()};
      busy=true; btn.disabled=true; btn.textContent=T.sending; st.hidden=false; st.textContent=T.sending;
      window.submitConfirmed(LEADS_URL,payload,'json',f).then(function(){
        sent=true; busy=false; btn.textContent=T.okBtn; st.textContent=T.ok;
        if(window.pmTrack) window.pmTrack('generate_lead',{form_id:'broker',placement:'colaboracion_brokers'});
      }).catch(function(){
        busy=false; st.textContent=T.fail; btn.disabled=false; btn.textContent=T.send;
        if(window.pmTrack) window.pmTrack('contact_form_error',{form_id:kind});
      });
    });
  }
  wire(document.getElementById('pmBroker'),'broker');
})();
