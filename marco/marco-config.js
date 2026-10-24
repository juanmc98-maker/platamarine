/* Plata Marine · configurador Mar.Co (ES/CA/EN/FR).
   Versión + motores + opcionales de la tarifa oficial; total al momento, enlace para compartir (#cfg=…),
   resumen imprimible y paso de la configuración al formulario de presupuesto. */
(function(){
'use strict';
var C=window.MC_CFG, box=document.getElementById('mm-cfg'); if(!C||!box) return;
var L=C.L, lg=C.lang;
function eur(n){var s=Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g,lg==='en'?',':(lg==='fr'?' ':'.'));return lg==='en'?'€'+s:s+' €';}
function $(id){return document.getElementById(id);}
var opts=[].slice.call(box.querySelectorAll('input[name=mmo]'));
function state(){
  var v=+((box.querySelector('input[name=mmv]:checked')||{}).value||0);
  var e=(box.querySelector('input[name=mme]:checked')||{}).value||'adv';
  var sel=opts.filter(function(o){return o.checked;}).map(function(o){return +o.value;});
  return {v:v,e:e,o:sel};
}
function base(s){return s.v&&C.inf?C.inf:C.base;}
/* compatibilidades: lo que necesita cada opcional y con qué choca */
function enforce(){
  for(var it=0;it<6;it++){
    var prov={},changed=false;
    opts.forEach(function(o){if(o.checked&&o.dataset.pv)o.dataset.pv.split(' ').forEach(function(k){prov[k]=1;});});
    opts.forEach(function(o){
      var why=[];
      (o.dataset.rq||'').split(' ').forEach(function(k){if(k&&!prov[k])why.push(C.why[k]);});
      (o.dataset.nr||'').split(' ').forEach(function(k){if(k&&prov[k])why.push(C.why['x_'+k]);});
      var lab=o.closest('label'),n=lab&&lab.querySelector('.mm-why');
      if(why.length){if(o.checked){o.checked=false;changed=true;}o.disabled=true;if(lab)lab.classList.add('off');if(n){n.hidden=false;n.textContent=why[0];}}
      else{o.disabled=false;if(lab)lab.classList.remove('off');if(n)n.hidden=true;}
    });
    if(!changed)break;
  }
}
function render(){
  enforce();
  var s=state(),b=base(s),sum=0;
  var ul=$('mm-sl');ul.innerHTML='';
  s.o.forEach(function(i){var o=C.opts[i];sum+=o[1]||0;var li=document.createElement('li');var a=document.createElement('span');a.textContent=o[0];var p=document.createElement('span');p.textContent='+'+eur(o[1]||0);li.appendChild(a);li.appendChild(p);ul.appendChild(li);});
  $('mm-sb').textContent=eur(b);
  $('mm-se').textContent=C.eng[s.e];
  $('mm-so').textContent=s.o.length?(s.o.length+' · '+eur(sum)):L.sum_none;
  $('mm-st').textContent=eur(b+sum);
  $('mm-si').textContent=eur((b+sum)*1.21);
  if($('mm-ie')){$('mm-ie').textContent=eur((b+sum)*0.12);$('mm-ia').textContent=eur((b+sum)*1.33);}
  var bt=$('mm-bt'); if(bt) bt.textContent=eur(b+sum);
  [].forEach.call(box.querySelectorAll('.mm-cat'),function(d){var n=d.querySelectorAll('input:checked').length;var i=d.querySelector('summary i');i.hidden=!n;i.textContent=n;});
  var h='#cfg='+s.v+'-'+s.e+(s.o.length?'-'+s.o.join('.'):'');
  if(history.replaceState&&(s.v||s.e!=='adv'||s.o.length)) history.replaceState(null,'',h);
  window.MC_SUMMARY=text(s,b,sum);
  var ta=$('mc_cfg'); if(ta&&touched){ta.value=window.MC_SUMMARY;$('mc_cfg_w').hidden=false;}
  return s;
}
var touched=false;
function text(s,b,sum){
  var t=[C.name+' · '+(s.v&&C.inf?L.c_inf:L.c_std)+': '+eur(b)];
  t.push(L.sum_eng+': '+C.eng[s.e]);
  s.o.forEach(function(i){t.push('+ '+C.opts[i][0]+': '+eur(C.opts[i][1]||0));});
  t.push(L.sum_tot+': '+eur(b+sum)+' '+L.vat);t.push(L.sum_iva+': '+eur((b+sum)*1.21));if(C.iedmt){t.push(L.ie_l+': '+eur((b+sum)*0.12));t.push(L.ie_all+': '+eur((b+sum)*1.33));}
  return t.join('\n');
}
box.addEventListener('change',function(e){
  var t=e.target;touched=true;
  if(t.name==='mmo'&&t.checked&&t.dataset.x){opts.forEach(function(o){if(o!==t&&o.dataset.x===t.dataset.x)o.checked=false;});}
  render();
  if(window.pmTrack&&t.name) window.pmTrack('configurator_change',{brand:'marco',model:C.name});
});
/* restaurar desde el enlace */
var m=location.hash.match(/^#cfg=(\d)-(mer|oth|adv)(?:-([\d.]+))?$/);
if(m){touched=true;var r=box.querySelector('input[name=mmv][value="'+m[1]+'"]');if(r)r.checked=true;
  var e=box.querySelector('input[name=mme][value="'+m[2]+'"]');if(e)e.checked=true;
  (m[3]||'').split('.').forEach(function(i){var o=box.querySelector('input[name=mmo][value="'+i+'"]');if(o){o.checked=true;var d=o.closest('details');if(d)d.open=true;}});
  setTimeout(function(){var c=document.getElementById('configurar');if(c)c.scrollIntoView();},300);}
render();
$('mm-send').addEventListener('click',function(){touched=true;render();});
$('mm-share').addEventListener('click',function(){
  var s=render(),u=location.origin+location.pathname+'#cfg='+s.v+'-'+s.e+(s.o.length?'-'+s.o.join('.'):''),b=this;
  function ok(){b.textContent=L.b_copied;setTimeout(function(){b.textContent=L.b_share;},2200);}
  if(navigator.share&&/Mobi|Android/i.test(navigator.userAgent)){navigator.share({title:C.name,url:u}).catch(function(){});return;}
  if(navigator.clipboard)navigator.clipboard.writeText(u).then(ok,function(){prompt('',u);});else prompt('',u);
});
/* Oferta en PDF: pide nombre, teléfono y email, guarda el lead (con nº de oferta y configuración) y genera la ficha */
var LEADS_URL='https://script.google.com/macros/s/AKfycbwJtBkktakE0qgmu_b8oHOOopCDnG6BDpBjg2zBUsZKi8l3_OBEuez_OHWmE9j8qCBF/exec';
var client=null,dl=$('mm-dl'),dlf=$('mcDl'),last=null;
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function offerNo(){var d=new Date(),p=function(n){return (n<10?'0':'')+n;};var a='ABCDEFGHJKLMNPQRSTUVWXYZ23456789',r='';for(var i=0;i<4;i++)r+=a.charAt(Math.floor(Math.random()*a.length));return 'PM-MC-'+String(d.getFullYear()).slice(2)+p(d.getMonth()+1)+p(d.getDate())+'-'+r;}
function cfgUrl(s){return location.origin+location.pathname+'#cfg='+s.v+'-'+s.e+(s.o.length?'-'+s.o.join('.'):'');}
function loadQr(){return new Promise(function(ok){if(window.qrcode)return ok();var sc=document.createElement('script');sc.src='/marco/qr.js';sc.onload=ok;sc.onerror=ok;document.head.appendChild(sc);});}
function sheet(no,s){
  var b=base(s),sum=0,rows='';
  rows+='<tr><td>'+esc(L.sum_base+' · '+(s.v&&C.inf?L.c_inf:L.c_std))+' <span style="color:#6b7a84">('+esc(L.noeng)+')</span></td><td>'+eur(b)+'</td></tr>';
  rows+='<tr><td>'+esc(L.sum_eng)+'</td><td>'+esc(C.eng[s.e])+'</td></tr>';
  s.o.forEach(function(i){sum+=C.opts[i][1]||0;rows+='<tr><td>'+esc(C.opts[i][0])+'</td><td>+'+eur(C.opts[i][1]||0)+'</td></tr>';});
  var specs=C.specs.map(function(x){return '<dt>'+esc(x[0])+'</dt><dd>'+esc(x[1])+'</dd>';}).join('');
  var qr='';try{if(window.qrcode){var q=qrcode(0,'M');q.addData(cfgUrl(s));q.make();qr=q.createSvgTag({cellSize:4,margin:0,scalable:true});}}catch(e){}
  var dt=new Date().toLocaleDateString(lg==='en'?'en-GB':lg+'-ES',{day:'2-digit',month:'2-digit',year:'numeric'});
  var th=(C.thumbs||[]).map(function(u){return '<img src="'+u+'" alt="">';}).join('');
  var h='<div class="pg"><div class="hd"><img src="/logo-plata-marine.png" alt="Plata Marine"><img class="b" src="'+C.brandlogo+'" alt="Mar.Co"></div>'+
   '<div class="meta"><div><div class="k">'+esc(L.sh_offer)+' · '+esc(C.kind)+'</div><h1>'+esc(C.name)+'</h1><div class="s">'+esc(L.sh_for)+': <b>'+esc(client.n)+'</b></div></div>'+
   '<div class="ref"><span>'+esc(L.sh_offer)+' nº</span><b>'+no+'</b><span>'+esc(L.sh_date)+': '+dt+'</span></div></div>'+
   '<img class="hero" src="'+C.hero+'" alt="">'+(th?'<div class="th">'+th+'</div>':'')+
   '<div class="cols"><div><h2>'+esc(L.sh_cfg)+'</h2><table>'+rows+'</table></div><div><h2>'+esc(L.sh_specs)+'</h2><dl>'+specs+'</dl></div></div>'+
   '<div class="tot"><div><div class="l">'+esc(L.sum_tot)+'</div><div class="v">'+eur(b+sum)+'<span class="vat">'+esc(L.vat)+'</span></div></div><div class="iva">'+esc(L.sum_iva)+': <b style="color:#fff">'+eur((b+sum)*1.21)+'</b>'+(C.iedmt?'<br>'+esc(L.ie_l)+': <b style="color:#fff">'+eur((b+sum)*0.12)+'</b><br>'+esc(L.ie_all)+'<br><b style="color:#fff;font-size:12pt">'+eur((b+sum)*1.33)+'</b>':'<br><span style="font-size:7pt">'+esc(L.ie_unk)+'</span>')+'</div></div>'+
   '<div class="ft">'+(qr?'<div class="qr">'+qr+'</div>':'')+'<div class="c"><small>'+esc(L.sh_scan)+'</small><b>Juan Morante · Plata Marine</b>+34 633 742 973 · juan@platamarine.com · www.platamarine.com</div></div>'+
   '<p class="sm">'+esc(L.sh_valid)+'</p></div>';
  var el=$('mm-sheet');if(!el){el=document.createElement('div');el.id='mm-sheet';document.body.appendChild(el);}
  el.innerHTML=h;el.className=s.o.length>9?'many':'';
  var imgs=[].slice.call(el.querySelectorAll('img'));
  return Promise.all(imgs.map(function(i){return i.complete?1:new Promise(function(r){i.onload=i.onerror=r;});}));
}
function makePdf(){
  var s=render(),no=offerNo(),st=$('dl_status'),bt=$('dl_send');
  var b=base(s),sum=0;s.o.forEach(function(i){sum+=C.opts[i][1]||0;});
  var detail='Oferta PDF '+no+' · '+text(s,b,sum).replace(/\n/g,' · ')+' | Email: '+client.e+' | Enlace: '+cfgUrl(s);
  var payload={source:'marco',barco:C.name+' · oferta '+no,nombre:client.n,telefono:client.t,email:client.e,detail:detail,lang:lg,page:location.pathname,ua:navigator.userAgent.slice(0,120),consent:true,consent_v:'2026-10',consent_at:new Date().toISOString()};
  st.hidden=false;st.textContent=L.dl_wait;bt.disabled=true;
  return window.submitConfirmed(LEADS_URL,payload,'json',dlf).then(function(){
    if(window.pmTrack)window.pmTrack('generate_lead',{form_id:'marco_pdf',contact_purpose:'offer_pdf',placement:'marco',boat:C.name});
    return loadQr().then(function(){return sheet(no,s);}).then(function(){dl.hidden=true;bt.disabled=false;st.hidden=true;document.title=C.name+' · '+no;window.print();});
  });
}
$('mm-print').addEventListener('click',function(){
  if(client){makePdf().catch(function(){});dl.hidden=false;return;}
  last=document.activeElement;dl.hidden=false;var n=$('dl_name');if(n)n.focus();
});
dl.querySelector('.x').addEventListener('click',function(){dl.hidden=true;if(last)last.focus();});
dl.addEventListener('click',function(e){if(e.target===dl)dl.hidden=true;});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!dl.hidden)dl.hidden=true;});
var FT={es:['Escribe tu nombre (solo letras).','Revisa el email, por ejemplo nombre@email.com.','Revisa el teléfono, por ejemplo 612 345 678 o +33 6 12 34 56 78.','Marca la casilla de privacidad.','No he podido guardar tus datos. Vuelve a intentarlo en unos minutos o escríbeme a juan@platamarine.com.'],
 ca:['Escriu el teu nom (només lletres).','Revisa el correu, per exemple nom@correu.com.','Revisa el telèfon, per exemple 612 345 678 o +33 6 12 34 56 78.','Marca la casella de privacitat.','No he pogut desar les teves dades. Torna-ho a provar d’aquí a uns minuts o escriu-me a juan@platamarine.com.'],
 en:['Please enter your name (letters only).','Please check the email, e.g. name@email.com.','Please check the phone number, e.g. +44 7700 900123.','Please tick the privacy box.','I could not save your details. Please try again in a few minutes or write to juan@platamarine.com.'],
 fr:['Indiquez votre nom (lettres uniquement).','Vérifiez l’e-mail, par exemple nom@email.fr.','Vérifiez le numéro, par exemple +33 6 12 34 56 78.','Cochez la case de confidentialité.','Je n’ai pas pu enregistrer vos coordonnées. Réessayez dans quelques minutes ou écrivez à juan@platamarine.com.']}[lg]||[];
dlf.addEventListener('input',function(e){if(e.target.setCustomValidity)e.target.setCustomValidity('');});
dlf.addEventListener('submit',function(e){
  e.preventDefault();
  var n=$('dl_name'),t=$('dl_tel'),m=$('dl_email'),c=$('dl_consent'),first=null;
  var okN=n.value.trim().length>=2&&/\p{L}/u.test(n.value)&&!/[0-9@]|https?:|www\./i.test(n.value);
  var d=t.value.replace(/[\s().-]/g,''),okT=/^[6-9]\d{8}$/.test(d)||/^(\+|00)\d{8,15}$/.test(d);
  var okE=/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(m.value.trim());
  [[n,okN,FT[0]],[m,okE,FT[1]],[t,okT,FT[2]],[c,c.checked,FT[3]]].forEach(function(r){r[0].setCustomValidity(r[1]?'':r[2]);if(!r[1]&&!first)first=r[0];});
  if(first){first.reportValidity();return;}
  if(!window.submitConfirmed){$('dl_status').hidden=false;$('dl_status').textContent=FT[4];return;}
  client={n:n.value.trim(),t:t.value.trim(),e:m.value.trim()};
  makePdf().catch(function(){client=null;$('dl_send').disabled=false;$('dl_status').hidden=false;$('dl_status').textContent=FT[4];});
});
$('mm-reset').addEventListener('click',function(){
  opts.forEach(function(o){o.checked=false;});
  var v=box.querySelector('input[name=mmv][value="0"]');if(v)v.checked=true;
  var e=box.querySelector('input[name=mme][value="adv"]');if(e)e.checked=true;
  touched=false;var w=$('mc_cfg_w');if(w)w.hidden=true;
  if(history.replaceState)history.replaceState(null,'',location.pathname);render();
});
/* barra inferior en el móvil: visible mientras el configurador está en pantalla */
var bar=$('mm-bar'),sec=document.getElementById('configurar');
if(bar&&sec&&'IntersectionObserver' in window){new IntersectionObserver(function(en){bar.classList.toggle('on',en[0].isIntersecting);},{rootMargin:'0px 0px -40% 0px'}).observe(sec);}
})();
