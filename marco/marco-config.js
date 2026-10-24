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
function render(){
  var s=state(),b=base(s),sum=0;
  var ul=$('mm-sl');ul.innerHTML='';
  s.o.forEach(function(i){var o=C.opts[i];sum+=o[1]||0;var li=document.createElement('li');var a=document.createElement('span');a.textContent=o[0];var p=document.createElement('span');p.textContent='+'+eur(o[1]||0);li.appendChild(a);li.appendChild(p);ul.appendChild(li);});
  $('mm-sb').textContent=eur(b);
  $('mm-se').textContent=C.eng[s.e];
  $('mm-so').textContent=s.o.length?(s.o.length+' · '+eur(sum)):L.sum_none;
  $('mm-st').textContent=eur(b+sum);
  $('mm-si').textContent=eur((b+sum)*1.21);
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
  t.push(L.sum_tot+': '+eur(b+sum)+' '+L.vat);
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
$('mm-print').addEventListener('click',function(){
  var s=render(),b=base(s),sum=0,tb=$('mm-pt');tb.innerHTML='';
  function row(a,p,cl){var tr=document.createElement('tr');if(cl)tr.className=cl;var x=document.createElement('td');x.textContent=a;var y=document.createElement('td');y.textContent=p;tr.appendChild(x);tr.appendChild(y);tb.appendChild(tr);}
  row(L.sum_base+' · '+(s.v&&C.inf?L.c_inf:L.c_std),eur(b));
  row(L.sum_eng,C.eng[s.e]);
  s.o.forEach(function(i){sum+=C.opts[i][1]||0;row(C.opts[i][0],'+'+eur(C.opts[i][1]||0));});
  row(L.sum_tot+' ('+L.vat.replace('+','').trim()+')',eur(b+sum),'t');
  row(L.sum_iva,eur((b+sum)*1.21));
  var d=document.querySelector('#mm-print-box [data-date]');if(d)d.textContent=new Date().toLocaleDateString(lg==='en'?'en-GB':lg+'-ES');
  window.print();
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
