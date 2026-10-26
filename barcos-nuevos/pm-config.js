/* Plata Marine · configurador de barcos nuevos (ES/CA/EN/FR), común a todas las marcas.
   Datos en window.PM_CFG = {brand, src, models:[{id,name,base,inc,eng:[[texto,precio]],opt:[[texto,precio|null]]}]}
   (precio null = a consultar; no suma). Total sin IVA "+ impuestos", enlace para compartir (#cfg=…)
   y solicitud de presupuesto a la hoja de leads con la configuración (submit-confirmed.js). */
(function(){
'use strict';
var C=window.PM_CFG,box=document.getElementById('pm-cfg');if(!C||!box)return;
var LG=(document.documentElement.lang||'es').slice(0,2);
var LEADS_URL='https://script.google.com/macros/s/AKfycbwJtBkktakE0qgmu_b8oHOOopCDnG6BDpBjg2zBUsZKi8l3_OBEuez_OHWmE9j8qCBF/exec';
var L={
 es:{model:'Modelo',eng:'Motorización',opt:'Opcionales',ask:'a consultar',tot:'Total',tax:'+ impuestos',base:'Barco',none:'Sin opcionales',askn:'Opcionales a consultar (no suman):',
  note:'Precio orientativo de la tarifa del astillero, sin IVA y en fábrica. No incluye transporte, matriculación ni el IEDMT cuando corresponda. El precio final es el del presupuesto por escrito.',
  fh:'Pídeme el presupuesto de esta configuración',fp:'Te lo paso por escrito, sin compromiso.',name:'Nombre',tel:'Teléfono',email:'Email',msg:'Cuéntame (opcional)',
  consent:'He leído la información de privacidad y acepto que uses estos datos para contestarme.',send:'Solicitar presupuesto',req:'Los campos con * son obligatorios.',
  e_name:'Escribe tu nombre (solo letras).',e_email:'Revisa el email, por ejemplo nombre@email.com.',e_tel:'Revisa el teléfono, por ejemplo 612 345 678 o +33 6 12 34 56 78.',e_c:'Marca la casilla de privacidad para poder enviarlo.',
  sending:'Enviando…',ok:'Solicitud recibida. Te contesto en 24 horas laborables.',okb:'Enviado ✓',fail:'No he podido confirmar que el mensaje ha llegado. Vuelve a intentarlo en unos minutos o escríbeme a juan@platamarine.com.',share:'Copiar enlace de esta configuración',copied:'Enlace copiado',priv:'/privacidad'},
 ca:{model:'Model',eng:'Motorització',opt:'Opcionals',ask:'a consultar',tot:'Total',tax:'+ impostos',base:'Vaixell',none:'Sense opcionals',askn:'Opcionals a consultar (no sumen):',
  note:'Preu orientatiu de la tarifa de la drassana, sense IVA i a fàbrica. No inclou transport, matriculació ni l’IEDMT quan correspongui. El preu final és el del pressupost per escrit.',
  fh:'Demana’m el pressupost d’aquesta configuració',fp:'Te’l passo per escrit, sense compromís.',name:'Nom',tel:'Telèfon',email:'Correu',msg:'Explica’m (opcional)',
  consent:'He llegit la informació de privacitat i accepto que facis servir aquestes dades per contestar-me.',send:'Sol·licitar pressupost',req:'Els camps amb * són obligatoris.',
  e_name:'Escriu el teu nom (només lletres).',e_email:'Revisa el correu, per exemple nom@correu.com.',e_tel:'Revisa el telèfon, per exemple 612 345 678 o +33 6 12 34 56 78.',e_c:'Marca la casella de privacitat per poder enviar-ho.',
  sending:'Enviant…',ok:'Sol·licitud rebuda. Et contesto en 24 hores laborables.',okb:'Enviat ✓',fail:'No he pogut confirmar que el missatge ha arribat. Torna-ho a provar d’aquí a uns minuts o escriu-me a juan@platamarine.com.',share:'Copiar l’enllaç d’aquesta configuració',copied:'Enllaç copiat',priv:'/ca/privacidad'},
 en:{model:'Model',eng:'Engines',opt:'Options',ask:'on request',tot:'Total',tax:'+ taxes',base:'Boat',none:'No options',askn:'Options on request (not added):',
  note:'Indicative price from the builder’s price list, ex-works, excluding VAT. It does not include transport, registration or Spanish IEDMT tax where it applies. The final price is the one in the written quote.',
  fh:'Ask me for a quote for this configuration',fp:'I will send it to you in writing, with no obligation.',name:'Name',tel:'Phone',email:'Email',msg:'Tell me more (optional)',
  consent:'I have read the privacy information and agree to you using these details to reply to me.',send:'Request a quote',req:'Fields marked * are required.',
  e_name:'Please enter your name (letters only).',e_email:'Please check the email, e.g. name@email.com.',e_tel:'Please check the phone number, with the international code, e.g. +44 7700 900123.',e_c:'Please tick the privacy box.',
  sending:'Sending…',ok:'Request received. I will reply within 24 working hours.',okb:'Sent ✓',fail:'I could not confirm that your message arrived. Please try again in a few minutes or write to juan@platamarine.com.',share:'Copy link to this configuration',copied:'Link copied',priv:'/en/privacidad'},
 fr:{model:'Modèle',eng:'Motorisation',opt:'Options',ask:'sur demande',tot:'Total',tax:'+ taxes',base:'Bateau',none:'Sans options',askn:'Options sur demande (non incluses) :',
  note:'Prix indicatif du tarif du chantier, départ usine, hors TVA. Hors transport, immatriculation et taxe espagnole IEDMT le cas échéant. Le prix final est celui du devis écrit.',
  fh:'Demandez-moi le devis de cette configuration',fp:'Je vous l’envoie par écrit, sans engagement.',name:'Nom',tel:'Téléphone',email:'E-mail',msg:'Précisez (facultatif)',
  consent:'J’ai lu les informations de confidentialité et j’accepte que vous utilisiez ces données pour me répondre.',send:'Demander un devis',req:'Les champs marqués * sont obligatoires.',
  e_name:'Indiquez votre nom (lettres uniquement).',e_email:'Vérifiez l’e-mail, par exemple nom@email.fr.',e_tel:'Vérifiez le numéro, avec l’indicatif, par exemple +33 6 12 34 56 78.',e_c:'Cochez la case de confidentialité.',
  sending:'Envoi…',ok:'Demande reçue. Je vous réponds sous 24 heures ouvrées.',okb:'Envoyé ✓',fail:'Je n’ai pas pu confirmer que votre message est arrivé. Réessayez dans quelques minutes ou écrivez à juan@platamarine.com.',share:'Copier le lien de cette configuration',copied:'Lien copié',priv:'/fr/privacidad'}
}[LG]||null;if(!L)return;
function eur(n){var s=Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g,LG==='en'?',':(LG==='fr'?' ':'.'));return LG==='en'?'€'+s:s+' €';}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
var css='.pc{display:grid;grid-template-columns:1.3fr 1fr;gap:28px;align-items:start}.pc fieldset{border:0;margin:0 0 22px;padding:0}.pc legend{font-weight:700;font-size:1.05rem;margin:0 0 10px;padding:0}'
+'.pc-ch{display:grid;gap:8px}.pc-ch label{display:flex;justify-content:space-between;gap:12px;align-items:center;background:#fff;border:1px solid rgba(14,48,66,.16);border-radius:10px;padding:10px 12px;cursor:pointer;font-size:15px;line-height:1.35}'
+'.pc-ch label:has(input:checked){border-color:var(--wa,#0B766B);box-shadow:0 0 0 1px var(--wa,#0B766B)}.pc-ch label span{display:flex;gap:10px;align-items:center}.pc-ch input{accent-color:var(--wa,#0B766B);width:18px;height:18px;flex:none}.pc-ch b{white-space:nowrap;font-weight:600}.pc-ch b.ask{color:var(--ink-2,#555);font-weight:500;font-style:italic}'
+'.pc-sum{position:sticky;top:90px;background:#0E3042;color:#fff;border-radius:14px;padding:20px}.pc-sum h3{margin:0 0 12px;font-size:1.15rem;color:#fff}.pc-sum ul{list-style:none;margin:0 0 10px;padding:0;font-size:14px}.pc-sum li{display:flex;justify-content:space-between;gap:10px;padding:5px 0;border-bottom:1px solid rgba(255,255,255,.12)}'
+'.pc-tot{display:flex;justify-content:space-between;align-items:baseline;font-size:1.5rem;font-weight:700;margin:12px 0 4px}.pc-tot .vat{color:#ff8a80;font-size:.55em;margin-left:4px}.pc-sum small{display:block;font-size:12.5px;line-height:1.45;color:rgba(255,255,255,.75)}.pc-ask{font-size:13px;color:rgba(255,255,255,.8);margin:8px 0 0}'
+'.pc-share{margin-top:12px;background:transparent;border:1px solid rgba(255,255,255,.5);color:#fff;border-radius:8px;padding:8px 12px;font:inherit;font-size:14px;cursor:pointer}'
+'.pc-form{margin-top:26px;display:grid;grid-template-columns:1fr 1fr;gap:12px}.pc-form h3{grid-column:1/-1;margin:0}.pc-form p{grid-column:1/-1;margin:0;color:var(--ink-2,#555)}.pc-form label{display:block;font-weight:600;font-size:14px;margin-bottom:4px}.pc-form input[type=text],.pc-form input[type=tel],.pc-form input[type=email],.pc-form textarea{width:100%;box-sizing:border-box;border:1px solid rgba(14,48,66,.25);border-radius:8px;padding:10px;font:inherit;font-size:16px}.pc-form .s2{grid-column:1/-1}.pc-form textarea{min-height:80px}.pc-form button{background:var(--wa,#0B766B);color:#fff;border:0;border-radius:10px;padding:13px 20px;font:inherit;font-weight:700;cursor:pointer}.pc-form .cs{display:flex;gap:10px;align-items:flex-start;font-weight:400;font-size:14px}.pc-form .cs input{width:20px;height:20px;accent-color:#0B766B;margin:1px 0 0}'
+'@media(max-width:820px){.pc{grid-template-columns:1fr}.pc-sum{position:static}.pc-form{grid-template-columns:1fr}}';
var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
var M=C.models,multi=M.length>1;
function radio(name,i,txt,price,chk,sub){return '<label><span><input type="radio" name="'+name+'" value="'+i+'"'+(chk?' checked':'')+'>'+esc(txt)+(sub?' <small style="color:var(--ink-2,#666)">'+esc(sub)+'</small>':'')+'</span><b>'+price+'</b></label>';}
function build(mi){
  var m=M[mi],h='<div class="pc"><div>';
  if(multi){h+='<fieldset><legend>'+L.model+'</legend><div class="pc-ch">';M.forEach(function(x,i){h+=radio('pcm',i,x.name,eur(x.base)+' <span style="font-weight:400;font-size:13px">'+esc(x.inc||'')+'</span>',i===mi);});h+='</div></fieldset>';}
  if(m.eng&&m.eng.length){h+='<fieldset><legend>'+L.eng+'</legend><div class="pc-ch">';m.eng.forEach(function(e,i){h+=radio('pce',i,e[0],e[1]==null?'<span class="ask">'+L.ask+'</span>':(e[1]?'+'+eur(e[1]):'—'),i===0);});h+='</div></fieldset>';}
  if(m.opt&&m.opt.length){h+='<fieldset><legend>'+L.opt+'</legend><div class="pc-ch">';m.opt.forEach(function(o,i){h+='<label><span><input type="checkbox" name="pco" value="'+i+'">'+esc(o[0])+'</span>'+(o[1]==null?'<b class="ask">'+L.ask+'</b>':'<b>+'+eur(o[1])+'</b>')+'</label>';});h+='</div></fieldset>';}
  h+='</div><aside class="pc-sum" aria-live="polite"><h3>'+esc(m.name)+'</h3><ul id="pc-l"></ul><div class="pc-tot"><span>'+L.tot+'</span><span><span id="pc-t"></span><span class="vat">'+L.tax+'</span></span></div><p class="pc-ask" id="pc-a" hidden></p><small>'+L.note+(C.note?' '+esc(C.note):'')+'</small><button type="button" class="pc-share" id="pc-sh">'+L.share+'</button></aside></div>';
  h+='<form class="pc-form" id="pcForm" novalidate data-contact-intent="config_'+esc(C.src)+'"><h3>'+L.fh+'</h3><p>'+L.fp+'</p>'
   +'<div><label for="pc_name">'+L.name+' *</label><input id="pc_name" type="text" required autocomplete="name" maxlength="60"></div>'
   +'<div><label for="pc_tel">'+L.tel+' *</label><input id="pc_tel" type="tel" required autocomplete="tel" inputmode="tel" maxlength="20" placeholder="+34 6xx xxx xxx"></div>'
   +'<div class="s2"><label for="pc_email">'+L.email+' *</label><input id="pc_email" type="email" required autocomplete="email" maxlength="100"></div>'
   +'<div class="s2"><label for="pc_msg">'+L.msg+'</label><textarea id="pc_msg" maxlength="1500"></textarea></div>'
   +'<div class="s2"><label class="cs"><input id="pc_c" type="checkbox" required><span>'+L.consent.replace('privacidad','<a href="'+L.priv+'" target="_blank" rel="noopener">privacidad</a>')+' *</span></label></div>'
   +'<div class="s2"><button type="submit" id="pc_send">'+L.send+'</button></div><p>'+L.req+'</p><p id="pc_st" role="status" aria-live="polite" hidden></p></form>';
  box.innerHTML=h;wire();
}
var cur=0;
function sel(){var m=M[cur],e=box.querySelector('input[name=pce]:checked'),ei=e?+e.value:-1;var o=[].map.call(box.querySelectorAll('input[name=pco]:checked'),function(x){return +x.value;});return{m:m,ei:ei,o:o};}
function summary(){
  var s=sel(),m=s.m,tot=m.base,lines=[[L.base+' ('+(m.inc||'')+')',eur(m.base)]],ask=[];
  if(s.ei>=0){var e=m.eng[s.ei];if(e[1]==null)ask.push(e[0]);else{tot+=e[1];if(e[1])lines.push([e[0],'+'+eur(e[1])]);}}
  s.o.forEach(function(i){var o=m.opt[i];if(o[1]==null)ask.push(o[0]);else{tot+=o[1];lines.push([o[0],'+'+eur(o[1])]);}});
  document.getElementById('pc-l').innerHTML=lines.map(function(l){return '<li><span>'+esc(l[0])+'</span><span>'+l[1]+'</span></li>';}).join('');
  document.getElementById('pc-t').textContent=eur(tot);
  var a=document.getElementById('pc-a');a.hidden=!ask.length;a.textContent=ask.length?L.askn+' '+ask.join(', '):'';
  var hash='#cfg='+cur+'-'+(s.ei<0?0:s.ei)+(s.o.length?'-'+s.o.join('.'):'');
  if(history.replaceState)history.replaceState(null,'',hash);
  return m.name+'\n'+lines.map(function(l){return l[0]+': '+l[1];}).join('\n')+(ask.length?'\n'+L.askn+' '+ask.join(', '):'')+'\n'+L.tot+': '+eur(tot)+' '+L.tax;
}
function wire(){
  document.getElementById('pc-sh').onclick=function(){var b=this;summary();var u=location.href;(navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).then(function(){b.textContent=L.copied;},function(){prompt('',u);});};
  var f=document.getElementById('pcForm'),btn=document.getElementById('pc_send'),stt=document.getElementById('pc_st'),busy=false,sent=false;
  function okName(s){return s.length>=2&&/\p{L}/u.test(s)&&!/[0-9@]|https?:|www\./i.test(s);}
  function okEmail(s){return /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(s);}
  function okTel(s){var d=s.replace(/[\s().-]/g,'');return /^[6-9]\d{8}$/.test(d)||/^(\+|00)\d{8,15}$/.test(d);}
  f.addEventListener('input',function(e){if(e.target.setCustomValidity)e.target.setCustomValidity('');});
  f.addEventListener('submit',function(e){
    e.preventDefault();if(sent||busy)return;
    var r=[['pc_name',okName,L.e_name],['pc_email',okEmail,L.e_email],['pc_tel',okTel,L.e_tel]],first=null;
    r.forEach(function(x){var el=document.getElementById(x[0]);var bad=!x[1](el.value.trim());el.setCustomValidity(bad?x[2]:'');if(bad&&!first)first=el;});
    var c=document.getElementById('pc_c');c.setCustomValidity(c.checked?'':L.e_c);if(!c.checked&&!first)first=c;
    if(first){first.reportValidity();return;}
    if(!window.submitConfirmed){stt.hidden=false;stt.textContent=L.fail;return;}
    var v=function(id){return document.getElementById(id).value.trim();},cfg=summary();
    var payload={source:'config_'+C.src,barco:sel().m.name,nombre:v('pc_name'),telefono:v('pc_tel'),email:v('pc_email'),
      detail:C.brand+' | Configuración: '+cfg.replace(/\n/g,' · ')+' | Email: '+v('pc_email')+(v('pc_msg')?' | Mensaje: '+v('pc_msg'):'')+' | Enlace: '+location.href,
      lang:LG,page:location.pathname,ua:navigator.userAgent.slice(0,120),consent:true,consent_v:'2026-10',consent_at:new Date().toISOString()};
    busy=true;btn.disabled=true;btn.textContent=L.sending;stt.hidden=false;stt.textContent=L.sending;
    window.submitConfirmed(LEADS_URL,payload,'json',f).then(function(){sent=true;busy=false;stt.textContent=L.ok;btn.textContent=L.okb;if(window.pmTrack)window.pmTrack('generate_lead',{form_id:'config_'+C.src,contact_purpose:'quote',placement:'config',boat:payload.barco});})
    .catch(function(){busy=false;stt.textContent=L.fail;btn.disabled=false;btn.textContent=L.send;});
  });
}
/* estado desde el enlace compartido */
var mh=/#cfg=(\d+)-(\d+)(?:-([\d.]+))?/.exec(location.hash);
if(mh&&M[+mh[1]])cur=+mh[1];
box.addEventListener('change',function(e){if(e.target.name==='pcm'){cur=+e.target.value;build(cur);summary();if(window.pmTrack)window.pmTrack('tool_use',{tool:'config_'+C.src});return;}summary();});
build(cur);
if(mh){var e=box.querySelector('input[name=pce][value="'+mh[2]+'"]');if(e)e.checked=true;(mh[3]||'').split('.').forEach(function(i){var o=box.querySelector('input[name=pco][value="'+i+'"]');if(o)o.checked=true;});}
summary();
})();
