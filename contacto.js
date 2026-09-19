/* Plata Marine: formulario de venta con envío directo. Confirmación solo cuando el servidor la confirma. */
(function(){
  'use strict';
  var f=document.getElementById('valoracion'); if(!f) return;
  var TEL='34633742973', MAIL='juan@platamarine.com';
  var LEADS_URL='https://script.google.com/macros/s/AKfycbwJtBkktakE0qgmu_b8oHOOopCDnG6BDpBjg2zBUsZKi8l3_OBEuez_OHWmE9j8qCBF/exec';
  var status=document.getElementById('contactoEstado');
  var fallback=document.getElementById('contactoAlternativa');
  var link=document.getElementById('continuarContacto');
  var submitBtn=document.getElementById('enviarConsulta');
  var sent=false;
  function v(id){var el=document.getElementById(id);return el?el.value.trim():'';}
  function track(name,method){if(window.pmTrack) window.pmTrack(name,{form_id:'valoracion',contact_method:method||'',contact_purpose:'seller',placement:'valora'});}
  function build(){
    var lines=['Hola Juan, estoy pensando en vender mi barco.'];
    var barco=v('modelo'); if(v('anio')) barco+=' ('+v('anio')+')';
    lines.push('Barco: '+barco);
    lines.push('Puerto: '+v('puerto'));
    if(v('anuncio')) lines.push('Anuncio: '+v('anuncio'));
    lines.push('Soy '+v('nombre')+(v('telefono')?', tel. '+v('telefono'):'')+'.');
    return lines.join('\n');
  }
  function valid(method){
    ['modelo','puerto','nombre','telefono'].forEach(function(id){
      var el=document.getElementById(id);
      if(el) el.setCustomValidity(el.value.trim()?'':'Completa este campo.');
    });
    if(f.checkValidity()) return true;
    track('contact_form_error',method); f.reportValidity(); return false;
  }
  f.addEventListener('input',function(e){if(e.target.setCustomValidity) e.target.setCustomValidity('');});

  /* WhatsApp / email: alternativas siempre visibles. Abren la app con el mensaje listo;
     no afirman que la consulta ha llegado, solo que se ha abierto la app. */
  function openContact(method){
    if(!valid(method)) return;
    var message=build();
    var url=method==='whatsapp'?'https://wa.me/'+TEL+'?text='+encodeURIComponent(message):'mailto:'+MAIL+'?subject='+encodeURIComponent('Mi barco: '+v('modelo'))+'&body='+encodeURIComponent(message);
    if(link){ link.href=url; link.textContent=method==='whatsapp'?'Abrir WhatsApp de nuevo':'Abrir mi aplicación de correo otra vez'; }
    if(status){
      status.textContent=method==='whatsapp'?'Se ha abierto WhatsApp con el mensaje preparado. Pulsa enviar allí para que me llegue.':'Mensaje preparado para juan@platamarine.com. Pulsa enviar en tu aplicación de correo. Si no se abre, comprueba que tienes una aplicación de correo configurada.';
      status.hidden=false;
    }
    if(fallback) fallback.hidden=false;
    track('contact_intent',method);
    window.location.href=url;
  }

  /* Envío directo: botón principal. Solo se muestra confirmación cuando el
     servidor (Apps Script) devuelve ok:true. Si falla, no se limpia el
     formulario y se ofrecen WhatsApp/email como alternativa explícita. */
  function sendDirect(){
    if(sent) return;
    if(!valid('web')) return;
    if(!window.submitConfirmed){
      // Sin backend disponible: no simulamos un envío, vamos directos a la alternativa.
      openContact('whatsapp');
      return;
    }
    var detail='Modelo: '+v('modelo')+(v('anio')?' ('+v('anio')+')':'')+' | Puerto: '+v('puerto')+(v('anuncio')?' | Anuncio: '+v('anuncio'):'');
    var payload={source:'venta',nombre:v('nombre'),telefono:v('telefono'),detail:detail,page:location.pathname,ua:navigator.userAgent.slice(0,120)};
    if(submitBtn){ submitBtn.disabled=true; submitBtn.dataset.lbl=submitBtn.textContent; submitBtn.textContent='Enviando…'; }
    if(status){ status.hidden=false; status.textContent='Enviando tu consulta…'; }
    if(fallback) fallback.hidden=true;
    window.submitConfirmed(LEADS_URL,payload,'json').then(function(){
      sent=true;
      if(status) status.textContent='Consulta enviada. La he recibido y te contesto en cuanto pueda.';
      if(submitBtn) submitBtn.textContent='Consulta enviada ✓';
      track('generate_lead',null);
    }).catch(function(){
      if(status) status.textContent='No he podido confirmar que la consulta ha llegado. Tus datos siguen aquí, no se han borrado: puedes escribirme por WhatsApp o email con los botones de arriba, o volver a intentarlo en unos minutos.';
      if(fallback) fallback.hidden=false;
      if(submitBtn){ submitBtn.disabled=false; submitBtn.textContent=submitBtn.dataset.lbl||'Enviar consulta'; }
      track('contact_form_error','web');
    });
  }

  f.addEventListener('submit',function(e){ e.preventDefault(); sendDirect(); });
  var porWa=document.getElementById('porWhatsapp'); if(porWa) porWa.addEventListener('click',function(){ openContact('whatsapp'); });
  var porEm=document.getElementById('porEmail'); if(porEm) porEm.addEventListener('click',function(){ openContact('email'); });
})();
