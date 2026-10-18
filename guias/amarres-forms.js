/* Plata Marine · formularios de la guía de amarres y de /servicios/amarres (ES/CA/EN/FR).
   - #pmAmDl: descarga de la tabla de precios en PDF (source 'descarga'); el enlace al PDF aparece solo si el servidor confirma.
   - #pmAmPub: "¿Tienes un amarre que alquilar o traspasar?" (source 'amarre').
   - Antispam: campo trampa y espera mínima de submit-confirmed.js; nombre y teléfono los valida submit-confirmed.js; aquí email, campos y casilla. */
(function(){
  'use strict';
  var LEADS_URL='https://script.google.com/macros/s/AKfycbwJtBkktakE0qgmu_b8oHOOopCDnG6BDpBjg2zBUsZKi8l3_OBEuez_OHWmE9j8qCBF/exec';
  var m=/^\/(ca|en|fr)\//.exec(location.pathname), LANG=m?m[1]:'es';
  var PDF={es:'/guias/precios-amarres-cataluna-2026.pdf',ca:'/guias/precios-amarres-cataluna-2026-ca.pdf',en:'/guias/precios-amarres-cataluna-2026-en.pdf',fr:'/guias/precios-amarres-cataluna-2026-fr.pdf'}[LANG];
  var T={
    es:{consent:'Marca la casilla de privacidad para poder enviarlo.',req:'Completa este campo.',email:'Revisa el email, por ejemplo nombre@gmail.com.',sending:'Enviando…',send:'Enviar',
        dlOk:'Listo. Aquí tienes la tabla:',dlBtn:'Abrir el PDF',pubOk:'Recibido. Te escribo en 24 horas laborables.',okBtn:'Enviado ✓',
        fail:'No he podido confirmar que ha llegado. Tus datos siguen aquí: vuelve a intentarlo en unos minutos o escríbeme a juan@platamarine.com.'},
    ca:{consent:'Marca la casella de privacitat per poder enviar-ho.',req:'Completa aquest camp.',email:'Revisa el correu, per exemple nom@gmail.com.',sending:'Enviant…',send:'Enviar',
        dlOk:'Fet. Aquí tens la taula:',dlBtn:'Obrir el PDF',pubOk:'Rebut. T’escric en 24 hores laborables.',okBtn:'Enviat ✓',
        fail:'No he pogut confirmar que ha arribat. Les teves dades segueixen aquí: torna-ho a provar d’aquí a uns minuts o escriu-me a juan@platamarine.com.'},
    en:{consent:'Please tick the privacy box so I can receive it.',req:'Please fill in this field.',email:'Please check the email, e.g. name@gmail.com.',sending:'Sending…',send:'Send',
        dlOk:'Done. Here is the table:',dlBtn:'Open the PDF',pubOk:'Received. I will reply within 24 working hours.',okBtn:'Sent ✓',
        fail:'I could not confirm that it arrived. Your details are still here: please try again in a few minutes or write to juan@platamarine.com.'},
    fr:{consent:'Cochez la case de confidentialité pour pouvoir l’envoyer.',req:'Veuillez remplir ce champ.',email:'Vérifiez l’e-mail, par exemple nom@gmail.com.',sending:'Envoi…',send:'Envoyer',
        dlOk:'C’est fait. Voici le tableau :',dlBtn:'Ouvrir le PDF',pubOk:'Bien reçu. Je vous réponds sous 24 heures ouvrées.',okBtn:'Envoyé ✓',
        fail:'Je n’ai pas pu confirmer la réception. Vos informations sont toujours là : réessayez dans quelques minutes ou écrivez à juan@platamarine.com.'}
  }[LANG];
  function okEmail(s){ return /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(s); }
  function q(f,n){ var e=f.querySelector('[name="'+n+'"]'); return e?e.value.trim():''; }
  function check(f){
    var first=null;
    f.querySelectorAll('input,select,textarea').forEach(function(e){
      if(e.type==='checkbox'||e.name==='pm_hp_x'||!e.setCustomValidity) return;
      var v=e.value.trim(), bad=(e.required&&!v)||(e.type==='email'&&v&&!okEmail(v));
      e.setCustomValidity(bad?(v?T.email:T.req):''); if(bad&&!first) first=e;
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
    f.addEventListener('submit',function(e){
      e.preventDefault();
      if(sent||busy||!check(f)) return;
      if(!window.submitConfirmed){ st.hidden=false; st.textContent=T.fail; return; }
      var nl=f.querySelector('input[name=novedades]'), detail;
      if(kind==='descarga') detail='DESCARGA: tabla de precios de amarres 2026 ('+LANG+')';
      else detail='AMARRE: Puerto: '+q(f,'puerto')+' | Medidas: '+q(f,'medidas')+' | Modalidad: '+q(f,'modalidad')+(q(f,'concesion')?' | Concesión hasta: '+q(f,'concesion'):'')+(q(f,'precio')?' | Precio: '+q(f,'precio'):'')+(q(f,'mensaje')?' | Mensaje: '+q(f,'mensaje'):'');
      var payload={source:kind,nombre:q(f,'nombre'),telefono:q(f,'telefono'),email:q(f,'email'),detail:detail,lang:LANG,page:location.pathname,ua:navigator.userAgent.slice(0,120),consent:true,newsletter:!!(nl&&nl.checked),consent_v:'2026-10',consent_at:new Date().toISOString()};
      busy=true; btn.disabled=true; btn.textContent=T.sending; st.hidden=false; st.textContent=T.sending;
      window.submitConfirmed(LEADS_URL,payload,'json',f).then(function(){
        sent=true; busy=false; btn.textContent=T.okBtn;
        if(kind==='descarga'){
          st.innerHTML=''; st.appendChild(document.createTextNode(T.dlOk+' '));
          var a=document.createElement('a'); a.href=PDF; a.target='_blank'; a.rel='noopener'; a.className='btn btn-wa'; a.textContent=T.dlBtn; st.appendChild(a);
        } else st.textContent=T.pubOk;
        if(window.pmTrack) window.pmTrack('generate_lead',{form_id:kind==='descarga'?'descarga_amarres':'amarre',placement:location.pathname.indexOf('/servicios/')>-1?'servicios_amarres':'guia_amarres'});
        if(nl&&nl.checked&&window.pmTrack) window.pmTrack('newsletter_signup',{form_id:'descarga_amarres'});
      }).catch(function(){
        busy=false; st.textContent=T.fail; btn.disabled=false; btn.textContent=T.send;
        if(window.pmTrack) window.pmTrack('contact_form_error',{form_id:kind});
      });
    });
  }
  wire(document.getElementById('pmAmDl'),'descarga');
  wire(document.getElementById('pmAmPub'),'amarre');
})();
