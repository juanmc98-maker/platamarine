/* Plata Marine · formulario de /recordatorios-barco/ (ES/CA/EN/FR), source 'recordatorio'.
   - Antispam: campo trampa y espera mínima de 3 s de submit-confirmed.js.
   - Al menos una fecha (tipo + fecha futura), email válido y casilla de avisos. Novedades: casilla aparte y opcional.
   - En la hoja de leads, el detalle va como "AVISOS: itb=2027-05-01; seguro=2027-02-10 | Barco: …". */
(function(){
  'use strict';
  var LEADS_URL='https://script.google.com/macros/s/AKfycbwJtBkktakE0qgmu_b8oHOOopCDnG6BDpBjg2zBUsZKi8l3_OBEuez_OHWmE9j8qCBF/exec';
  var m=/^\/(ca|en|fr)\//.exec(location.pathname), LANG=m?m[1]:'es';
  var T={
    es:{consent:'Marca la casilla de los avisos para poder activarlos.',req:'Completa este campo.',email:'Revisa el email, por ejemplo nombre@correo.com.',row:'Elige qué vence y pon una fecha futura.',sending:'Enviando…',send:'Activar mis avisos',
        ok:'Hecho. Te escribiré antes de cada fecha. Si quieres cambiar algo, contesta a cualquier aviso.',okBtn:'Avisos activados ✓',
        fail:'No he podido confirmar que ha llegado. Tus datos siguen aquí: vuelve a intentarlo en unos minutos o escríbeme a juan@platamarine.com.'},
    ca:{consent:'Marca la casella dels avisos per poder activar-los.',req:'Completa aquest camp.',email:'Revisa el correu, per exemple nom@correu.com.',row:'Tria què venç i posa una data futura.',sending:'Enviant…',send:'Activar els meus avisos',
        ok:'Fet. T’escriuré abans de cada data. Si vols canviar alguna cosa, contesta qualsevol avís.',okBtn:'Avisos activats ✓',
        fail:'No he pogut confirmar que ha arribat. Les teves dades segueixen aquí: torna-ho a provar d’aquí a uns minuts o escriu-me a juan@platamarine.com.'},
    en:{consent:'Please tick the reminders box to turn them on.',req:'Please fill in this field.',email:'Please check the email, e.g. name@mail.com.',row:'Choose what expires and enter a future date.',sending:'Sending…',send:'Turn on my reminders',
        ok:'Done. I will email you before each date. To change anything, just reply to any reminder.',okBtn:'Reminders on ✓',
        fail:'I could not confirm that it arrived. Your details are still here: please try again in a few minutes or write to juan@platamarine.com.'},
    fr:{consent:'Cochez la case des rappels pour les activer.',req:'Veuillez remplir ce champ.',email:'Vérifiez l’e-mail, par exemple nom@mail.fr.',row:'Choisissez ce qui expire et une date future.',sending:'Envoi…',send:'Activer mes rappels',
        ok:'C’est fait. Je vous écrirai avant chaque date. Pour modifier quelque chose, répondez à n’importe quel rappel.',okBtn:'Rappels activés ✓',
        fail:'Je n’ai pas pu confirmer la réception. Vos informations sont toujours là : réessayez dans quelques minutes ou écrivez à juan@platamarine.com.'}
  }[LANG];
  function okEmail(s){ return /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(s); }
  function q(f,n){ var e=f.querySelector('[name="'+n+'"]'); return e?e.value.trim():''; }
  function today(){ var d=new Date(); d.setHours(0,0,0,0); return d; }
  var f=document.getElementById('pmRecordatorio'); if(!f) return;
  var add=f.querySelector('.rc-add');
  if(add) add.addEventListener('click',function(){
    var h=f.querySelector('.rc-row[hidden]'); if(h){ h.hidden=false; var s=h.querySelector('select'); if(s) s.focus(); }
    if(!f.querySelector('.rc-row[hidden]')) add.hidden=true;
  });
  function rows(){
    var out=[], bad=null;
    f.querySelectorAll('.rc-row').forEach(function(r){
      if(r.hidden) return;
      var s=r.querySelector('select'), d=r.querySelector('input[type=date]');
      s.setCustomValidity(''); d.setCustomValidity('');
      var tv=s.value, dv=d.value;
      if(!tv&&!dv) return;
      var dt=dv?new Date(dv+'T00:00:00'):null;
      if(!tv){ if(!bad) bad=s; s.setCustomValidity(T.row); return; }
      if(!dt||isNaN(dt)||dt<today()){ if(!bad) bad=d; d.setCustomValidity(T.row); return; }
      out.push(tv+'='+dv);
    });
    if(!out.length&&!bad){ bad=f.querySelector('.rc-row select'); bad.setCustomValidity(T.row); }
    return {list:out,bad:bad};
  }
  function check(){
    var r=rows(), first=r.bad;
    var e=f.querySelector('input[name=email]'), v=e.value.trim();
    e.setCustomValidity(!v?T.req:(okEmail(v)?'':T.email)); if(e.validationMessage&&!first) first=e;
    var c=f.querySelector('input[name=privacidad]');
    c.setCustomValidity(c.checked?'':T.consent); if(!c.checked&&!first) first=c;
    if(first){ first.reportValidity(); return null; }
    return r.list;
  }
  var btn=f.querySelector('button[type=submit]'), st=f.querySelector('.pm-amst'), sent=false, busy=false;
  f.addEventListener('input',function(e){ if(e.target.setCustomValidity) e.target.setCustomValidity(''); });
  f.addEventListener('change',function(e){ if(e.target.setCustomValidity) e.target.setCustomValidity(''); });
  f.addEventListener('submit',function(e){
    e.preventDefault();
    if(sent||busy) return;
    var list=check(); if(!list) return;
    if(!window.submitConfirmed){ st.hidden=false; st.textContent=T.fail; return; }
    var nl=!!(f.querySelector('input[name=novedades]')||{}).checked;
    var detail='AVISOS: '+list.join('; ')+(q(f,'barco')?' | Barco: '+q(f,'barco'):'');
    var payload={source:'recordatorio',nombre:q(f,'su_nombre'),telefono:'',email:q(f,'email'),detail:detail,lang:LANG,page:location.pathname,ua:navigator.userAgent.slice(0,120),consent:true,newsletter:nl,consent_v:'2026-11',consent_at:new Date().toISOString()};
    busy=true; btn.disabled=true; btn.textContent=T.sending; st.hidden=false; st.textContent=T.sending;
    window.submitConfirmed(LEADS_URL,payload,'json',f).then(function(){
      sent=true; busy=false; btn.textContent=T.okBtn; st.textContent=T.ok;
      if(window.pmTrack) window.pmTrack('generate_lead',{form_id:'recordatorio',placement:'recordatorios_barco'});
      try{ if(window.pmCount) window.pmCount({t:'recordatorio',m:list.length+' fechas'}); }catch(x){}
    }).catch(function(){
      busy=false; st.textContent=T.fail; btn.disabled=false; btn.textContent=T.send;
      if(window.pmTrack) window.pmTrack('contact_form_error',{form_id:'recordatorio'});
    });
  });
})();
