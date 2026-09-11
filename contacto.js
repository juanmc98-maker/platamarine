/* Plata Marine: preparar un contacto no equivale a enviarlo. */
(function(){
  'use strict';
  var f=document.getElementById('valoracion'); if(!f) return;
  var TEL='34633742973', MAIL='juan@platamarine.com';
  var status=document.getElementById('contactoEstado');
  var fallback=document.getElementById('contactoAlternativa');
  var link=document.getElementById('continuarContacto');
  function v(id){var el=document.getElementById(id);return el?el.value.trim():'';}
  function track(name,method){if(window.pmTrack) window.pmTrack(name,{form_id:'valoracion',contact_method:method,contact_purpose:'seller',placement:'valora'});}
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
    ['modelo','puerto','nombre'].forEach(function(id){var el=document.getElementById(id);el.setCustomValidity(el.value.trim()?'':'Completa este campo.');});
    if(f.checkValidity()) return true;
    track('contact_form_error',method); f.reportValidity(); return false;
  }
  f.addEventListener('input',function(e){if(e.target.setCustomValidity) e.target.setCustomValidity('');});
  function openContact(method){
    if(!valid(method)) return;
    var message=build();
    var url=method==='whatsapp'?'https://wa.me/'+TEL+'?text='+encodeURIComponent(message):'mailto:'+MAIL+'?subject='+encodeURIComponent('Mi barco: '+v('modelo'))+'&body='+encodeURIComponent(message);
    link.href=url;
    link.textContent=method==='whatsapp'?'Abrir WhatsApp de nuevo':'Abrir mi aplicación de correo';
    status.textContent=method==='whatsapp'?'Mensaje preparado. Pulsa enviar en WhatsApp para que Juan lo reciba.':'Mensaje preparado para juan@platamarine.com. Pulsa enviar en tu aplicación de correo. Si no se abre, comprueba que tienes una aplicación de correo configurada.';
    status.hidden=false; fallback.hidden=false;
    track('contact_intent',method);
    window.location.href=url;
  }
  f.addEventListener('submit',function(e){e.preventDefault();openContact('whatsapp');});
  document.getElementById('porEmail').addEventListener('click',function(){openContact('email');});
})();
