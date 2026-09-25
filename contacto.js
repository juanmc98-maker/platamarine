/* Plata Marine: formulario "Quiero vender mi barco" (portada ES/CA/EN).
   - Envío directo: la confirmación solo aparece cuando el servidor responde ok:true.
   - WhatsApp / email: se pueden usar aunque el formulario esté incompleto; el mensaje lleva solo los datos escritos.
   - Medición: contact_intent (abrir WhatsApp/email) y generate_lead (formulario confirmado), sin datos personales. */
(function(){
  'use strict';
  var f=document.getElementById('valoracion'); if(!f) return;
  var TEL='34633742973', MAIL='juan@platamarine.com';
  var LEADS_URL='https://script.google.com/macros/s/AKfycbwJtBkktakE0qgmu_b8oHOOopCDnG6BDpBjg2zBUsZKi8l3_OBEuez_OHWmE9j8qCBF/exec';
  var LANG=location.pathname.indexOf('/ca/')===0?'ca':location.pathname.indexOf('/en/')===0?'en':'es';
  var T={
    es:{hello:'Hola Juan, estoy pensando en vender mi barco.',boat:'Barco',port:'Puerto',ad:'Anuncio',me:'Soy',tel:'tel.',subj:'Mi barco',
      req:'Completa este campo.',year:'Revisa el año: escríbelo con cuatro cifras, por ejemplo 1998.',phone:'Revisa el teléfono: puedes escribirlo con prefijo internacional, por ejemplo +34 600 000 000.',url:'El enlace no parece correcto. Si no lo tienes a mano, déjalo en blanco.',
      waOpen:'Se ha abierto WhatsApp con un mensaje preparado con los datos que has escrito. Pulsa enviar allí para que me llegue.',mailOpen:'Se ha preparado un correo para juan@platamarine.com con los datos que has escrito. Pulsa enviar en tu aplicación de correo; si no se abre, escríbeme directamente a esa dirección.',
      waAgain:'Abrir WhatsApp de nuevo',mailAgain:'Abrir el correo de nuevo',sending:'Enviando tu consulta…',sendingBtn:'Enviando…',
      ok:'Consulta recibida. Te contesto en cuanto pueda.',okBtn:'Consulta enviada ✓',
      fail:'No he podido confirmar que la consulta ha llegado. Tus datos siguen aquí, no se han borrado: puedes escribirme por WhatsApp o email con los botones de arriba o volver a intentarlo en unos minutos.',send:'Enviar consulta'},
    ca:{hello:'Hola Juan, estic pensant a vendre el meu vaixell.',boat:'Vaixell',port:'Port',ad:'Anunci',me:'Sóc',tel:'tel.',subj:'El meu vaixell',
      req:'Completa aquest camp.',year:"Revisa l'any: escriu-lo amb quatre xifres, per exemple 1998.",phone:'Revisa el telèfon: el pots escriure amb prefix internacional, per exemple +34 600 000 000.',url:"L'enllaç no sembla correcte. Si no el tens a mà, deixa-ho en blanc.",
      waOpen:"S'ha obert WhatsApp amb un missatge preparat amb les dades que has escrit. Prem enviar allà perquè m'arribi.",mailOpen:"S'ha preparat un correu per a juan@platamarine.com amb les dades que has escrit. Prem enviar a la teva aplicació de correu; si no s'obre, escriu-me directament a aquesta adreça.",
      waAgain:'Obrir WhatsApp de nou',mailAgain:'Obrir el correu de nou',sending:'Enviant la teva consulta…',sendingBtn:'Enviant…',
      ok:'Consulta rebuda. Et contesto tan aviat com pugui.',okBtn:'Consulta enviada ✓',
      fail:"No he pogut confirmar que la consulta ha arribat. Les teves dades segueixen aquí, no s'han esborrat: pots escriure'm per WhatsApp o correu amb els botons de dalt o tornar-ho a provar d'aquí a uns minuts.",send:'Enviar consulta'},
    en:{hello:"Hi Juan, I'm thinking of selling my boat.",boat:'Boat',port:'Port',ad:'Listing',me:"I'm",tel:'phone',subj:'My boat',
      req:'Please fill in this field.',year:'Please check the year: use four digits, e.g. 1998.',phone:'Please check the phone number: you can include the international code, e.g. +44 7700 900000.',url:"That link doesn't look right. If you don't have it to hand, leave it blank.",
      waOpen:'WhatsApp has opened with a message containing the details you entered. Press send there so it reaches me.',mailOpen:'An email to juan@platamarine.com has been prepared with the details you entered. Press send in your email app; if it does not open, write to that address directly.',
      waAgain:'Open WhatsApp again',mailAgain:'Open the email again',sending:'Sending your enquiry…',sendingBtn:'Sending…',
      ok:'Enquiry received. I will get back to you as soon as I can.',okBtn:'Enquiry sent ✓',
      fail:'I could not confirm that your enquiry arrived. Your details are still here and have not been deleted: you can message me on WhatsApp or by email with the buttons above, or try again in a few minutes.',send:'Send enquiry'}
  }[LANG];
  var status=document.getElementById('contactoEstado');
  var fallback=document.getElementById('contactoAlternativa');
  var link=document.getElementById('continuarContacto');
  var submitBtn=document.getElementById('enviarConsulta');
  var yearEl=document.getElementById('anio');
  var MAXY=new Date().getFullYear()+1;
  if(yearEl){ yearEl.removeAttribute('min'); yearEl.setAttribute('max',String(MAXY)); }
  if(link) link.setAttribute('data-no-track','');
  var sent=false;
  function v(id){var el=document.getElementById(id);return el?el.value.trim():'';}
  function track(name,method){if(window.pmTrack) window.pmTrack(name,{form_id:'valoracion',contact_method:method||'',contact_purpose:'seller',placement:'valora'});}
  function build(){
    var lines=[T.hello];
    var barco=v('modelo'); if(v('anio')) barco+=(barco?' ':'')+'('+v('anio')+')';
    if(barco) lines.push(T.boat+': '+barco);
    if(v('puerto')) lines.push(T.port+': '+v('puerto'));
    if(v('anuncio')) lines.push(T.ad+': '+v('anuncio'));
    if(v('nombre')||v('telefono')) lines.push(T.me+' '+v('nombre')+(v('telefono')?(v('nombre')?', ':'')+T.tel+' '+v('telefono'):'')+'.');
    return lines.join('\n');
  }
  function setMsg(el,msg){ if(el&&el.setCustomValidity) el.setCustomValidity(msg); }
  function valid(){
    ['modelo','puerto','nombre','telefono'].forEach(function(id){ var el=document.getElementById(id); if(el) setMsg(el, el.value.trim()?'':T.req); });
    var tel=document.getElementById('telefono');
    if(tel&&tel.value.trim()&&(!/^\+?[0-9 ().-]{6,20}$/.test(tel.value.trim())||tel.value.replace(/\D/g,'').length<6)) setMsg(tel,T.phone);
    if(yearEl&&yearEl.value.trim()){ var y=+yearEl.value; setMsg(yearEl,(y>=1900&&y<=MAXY)?'':T.year); } else if(yearEl) setMsg(yearEl,'');
    var ad=document.getElementById('anuncio'); if(ad) setMsg(ad, ad.value.trim()&&!/^https?:\/\/\S+\.\S+/.test(ad.value.trim())?T.url:'');
    if(f.checkValidity()) return true;
    track('contact_form_error','web'); f.reportValidity(); return false;
  }
  f.addEventListener('input',function(e){if(e.target.setCustomValidity) e.target.setCustomValidity('');});

  /* WhatsApp / email: no exigen el formulario completo ni afirman que la consulta ha llegado. */
  function openContact(method){
    var message=build();
    var url=method==='whatsapp'?'https://wa.me/'+TEL+'?text='+encodeURIComponent(message):'mailto:'+MAIL+'?subject='+encodeURIComponent(T.subj+(v('modelo')?': '+v('modelo'):''))+'&body='+encodeURIComponent(message);
    if(link){ link.href=url; link.textContent=method==='whatsapp'?T.waAgain:T.mailAgain; }
    if(status){ status.textContent=method==='whatsapp'?T.waOpen:T.mailOpen; status.hidden=false; }
    if(fallback) fallback.hidden=false;
    track('contact_intent',method);
    window.location.href=url;
  }

  /* Envío directo: confirmación solo con ok:true del servidor; si falla, no se borra nada. */
  function sendDirect(){
    if(sent) return;
    if(!valid()) return;
    if(!window.submitConfirmed){ if(status){status.hidden=false;status.textContent=T.fail;} if(fallback) fallback.hidden=false; return; }
    var detail='Modelo: '+v('modelo')+(v('anio')?' ('+v('anio')+')':'')+' | Puerto: '+v('puerto')+(v('anuncio')?' | Anuncio: '+v('anuncio'):'');
    var payload={source:'venta',nombre:v('nombre'),telefono:v('telefono'),detail:detail,lang:LANG,page:location.pathname,ua:navigator.userAgent.slice(0,120)};
    if(submitBtn){ submitBtn.disabled=true; submitBtn.dataset.lbl=submitBtn.dataset.lbl||submitBtn.textContent; submitBtn.textContent=T.sendingBtn; }
    if(status){ status.hidden=false; status.textContent=T.sending; }
    if(fallback) fallback.hidden=true;
    window.submitConfirmed(LEADS_URL,payload,'json').then(function(){
      sent=true;
      if(status) status.textContent=T.ok;
      if(submitBtn) submitBtn.textContent=T.okBtn;
      track('generate_lead',null);
    }).catch(function(){
      if(status) status.textContent=T.fail;
      if(fallback) fallback.hidden=true;
      if(submitBtn){ submitBtn.disabled=false; submitBtn.textContent=submitBtn.dataset.lbl||T.send; }
      track('contact_form_error','web');
    });
  }

  f.addEventListener('submit',function(e){ e.preventDefault(); sendDirect(); });
  var porWa=document.getElementById('porWhatsapp'); if(porWa) porWa.addEventListener('click',function(){ openContact('whatsapp'); });
  var porEm=document.getElementById('porEmail'); if(porEm) porEm.addEventListener('click',function(){ openContact('email'); });
})();
