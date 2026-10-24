/* Visor de fotos común: cualquier foto en miniatura se amplía al pulsarla
   y se pasa a la anterior/siguiente con las flechas (vuelve al principio al llegar al final).
   Teclado (← → Esc) y deslizar el dedo en el móvil. No toca fotos que ya son enlaces o botones
   (fichas con su propio visor, tarjetas que llevan a otra página), ni logos, iconos o banderas. */
(function(){
"use strict";
if(window.__pmLbx)return;window.__pmLbx=1;
var lang=(document.documentElement.lang||'es').slice(0,2);
var T={es:['Foto ampliada','Cerrar','Foto anterior','Foto siguiente'],
 ca:['Foto ampliada','Tancar','Foto anterior','Foto següent'],
 en:['Enlarged photo','Close','Previous photo','Next photo'],
 fr:['Photo agrandie','Fermer','Photo précédente','Photo suivante'],
 it:['Foto ingrandita','Chiudi','Foto precedente','Foto successiva']}[lang]||['Foto ampliada','Cerrar','Foto anterior','Foto siguiente'];
var SKIP='a,button,label,[onclick],[role=link],[role=button],header,nav,footer,form,dialog,[role=dialog],[data-lb],[data-nolb],.lb,.sk-lbx,.lbx,.thumbs,#main-photo,.no-lb,.ai,.ph6';
var BAD=/logo|icon|icono|flag|bandera|favicon|avatar|sprite|badge|sello|firma|qr[-_.]/i;
function ok(im){
 if(!im||im.tagName!=='IMG'||im.closest(SKIP))return false;
 if(im.closest('.pm-lbx')||im.id==='main')return false;
 if(!im.classList.contains('pm-zoom')){var cu=getComputedStyle(im).cursor;if(cu==='pointer'||cu==='zoom-in')return false;}
 var src=im.currentSrc||im.src||'';if(!src||/\.svg(\?|$)/i.test(src)||/^data:/.test(src))return false;
 if(BAD.test(src)||BAD.test(im.className||'')||BAD.test(im.alt||''))return false;
 if(im.getAttribute('role')==='presentation'||im.getAttribute('aria-hidden')==='true')return false;
 var w=im.clientWidth,h=im.clientHeight;if(w<60||h<45)return false;
 if(im.naturalWidth&&im.naturalWidth<180)return false;
 if(im.naturalWidth&&w>=im.naturalWidth*0.85&&w>window.innerWidth*0.6&&big(im)===(im.currentSrc||im.src)&&!alt2(src))return false;
 var cs=getComputedStyle(im);if(cs.position==='absolute'||cs.position==='fixed')return false;
 var hp=im.parentElement;for(var k=0;k<2&&hp;k++,hp=hp.parentElement){if(hp.querySelector&&hp.querySelector('h1'))return false;}
 if(cs.pointerEvents==='none'||cs.visibility==='hidden')return false;
 return true;}
function big(im){
 var f=im.getAttribute('data-full')||im.getAttribute('data-zoom')||im.getAttribute('data-large');if(f)return f;
 var ss=im.getAttribute('srcset'),best=null,bw=0;
 if(ss){ss.split(',').forEach(function(p){var a=p.trim().split(/\s+/);var v=parseFloat(a[1])||1;if(a[1]&&/x$/.test(a[1]))v*=1000;if(v>bw){bw=v;best=a[0];}});}
 return best||im.currentSrc||im.src;}
function alt2(u){var m=u.match(/^(.*)-(m|t|thumb|sm|small)(\.(jpe?g|webp|png))(\?.*)?$/i);return m?m[1]+m[3]:null;}
var css='.pm-lbx{position:fixed;inset:0;z-index:2147483000;background:#05070a!important;opacity:1!important;display:none;align-items:center;justify-content:center;touch-action:pan-y;-webkit-tap-highlight-color:transparent}'+
'.pm-lbx.on{display:flex}.pm-lbx img{max-width:94vw;max-height:84vh;width:auto;height:auto;object-fit:contain;border-radius:6px;user-select:none;-webkit-user-drag:none;box-shadow:0 10px 40px rgba(0,0,0,.5)}'+
'.pm-lbx button{position:absolute;border:0;background:rgba(255,255,255,.14);color:#fff;width:50px;height:50px;border-radius:50%;font:28px/1 system-ui,sans-serif;cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0;z-index:2}'+
'.pm-lbx button:hover,.pm-lbx button:focus-visible{background:rgba(255,255,255,.28);outline:none}'+
'.pm-lbx .x{top:14px;right:14px}.pm-lbx .p{left:12px;top:50%;margin-top:-25px}.pm-lbx .n{right:12px;top:50%;margin-top:-25px}'+
'.pm-lbx .c{position:absolute;bottom:14px;left:60px;right:60px;text-align:center;color:rgba(255,255,255,.8);font:14px/1.4 system-ui,sans-serif}'+
'.pm-lbx .c small{display:block;opacity:.7;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'+
'@media (max-width:640px){.pm-lbx img{max-width:100vw;max-height:76vh;border-radius:0}.pm-lbx .p,.pm-lbx .n{top:auto;bottom:10px;margin-top:0;width:46px;height:46px}}'+
'img.pm-zoom{cursor:zoom-in}';
var box,img,cap,list=[],idx=0,last=null,x0=null,y0=null;
function build(){
 if(box)return;var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
 box=document.createElement('div');box.className='pm-lbx';box.setAttribute('role','dialog');box.setAttribute('aria-modal','true');box.setAttribute('aria-label',T[0]);
 box.innerHTML='<img alt=""><button type="button" class="x" aria-label="'+T[1]+'">×</button><button type="button" class="p" aria-label="'+T[2]+'">‹</button><button type="button" class="n" aria-label="'+T[3]+'">›</button><div class="c" aria-live="polite"></div>';
 document.body.appendChild(box);img=box.querySelector('img');cap=box.querySelector('.c');
 box.querySelector('.x').onclick=close;
 box.querySelector('.p').onclick=function(e){e.stopPropagation();show(idx-1);};
 box.querySelector('.n').onclick=function(e){e.stopPropagation();show(idx+1);};
 box.addEventListener('click',function(e){if(e.target===box)close();});
 box.addEventListener('touchstart',function(e){x0=e.touches[0].clientX;y0=e.touches[0].clientY;},{passive:true});
 box.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;if(Math.abs(dx)>45&&Math.abs(dx)>Math.abs(dy))show(idx+(dx<0?1:-1));x0=null;});
 document.addEventListener('keydown',function(e){if(!box.classList.contains('on'))return;
  if(e.key==='Escape')close();else if(e.key==='ArrowLeft')show(idx-1);else if(e.key==='ArrowRight')show(idx+1);
  else if(e.key==='Tab'){var b=box.querySelectorAll('button'),f=b[0],l=b[b.length-1];if(e.shiftKey&&document.activeElement===f){e.preventDefault();l.focus();}else if(!e.shiftKey&&document.activeElement===l){e.preventDefault();f.focus();}}});
}
function collect(){var seen={},out=[];Array.prototype.forEach.call(document.images,function(im){if(!ok(im))return;var u=big(im);if(seen[u])return;seen[u]=1;out.push({u:u,lo:im.currentSrc||im.src,a:im.alt||'',el:im});});return out;}
function show(i){
 var n=list.length;idx=(i+n)%n;var it=list[idx];
 var multi=n>1;box.querySelector('.p').style.display=multi?'':'none';box.querySelector('.n').style.display=multi?'':'none';
 img.onerror=null;var a2=alt2(it.u);
 if(a2){img.onerror=function(){img.onerror=function(){img.onerror=null;img.src=it.lo;};img.src=it.u;};img.src=a2;}
 else{img.onerror=function(){img.onerror=null;img.src=it.lo;};img.src=it.u;}
 img.alt=it.a;cap.innerHTML=(multi?(idx+1)+' / '+n:'')+(it.a?'<small></small>':'');if(it.a)cap.querySelector('small').textContent=it.a;
 if(multi){var nx=list[(idx+1)%n];var pre=new Image();pre.src=alt2(nx.u)||nx.u;}
}
function open(el){
 build();list=collect();var i=-1;
 var th=el.parentElement&&el.parentElement.querySelector('.thumbs');
 if(th){var tl=Array.prototype.map.call(th.querySelectorAll('img'),function(t){return {u:big(t),lo:t.currentSrc||t.src,a:el.alt||'',el:t};});
  if(tl.length){list=tl;var cur=el.currentSrc||el.src;for(var q=0;q<tl.length;q++)if(tl[q].lo===cur){i=q;break;}if(i<0)i=0;}}
 if(i<0)for(var k=0;k<list.length;k++)if(list[k].el===el||list[k].u===big(el)){i=k;break;}
 if(i<0){list.unshift({u:big(el),lo:el.currentSrc||el.src,a:el.alt||'',el:el});i=0;}
 last=document.activeElement;box.classList.add('on');document.documentElement.style.overflow='hidden';show(i);box.querySelector('.x').focus({preventScroll:true});
}
function close(){box.classList.remove('on');document.documentElement.style.overflow='';img.removeAttribute('src');if(last&&last.focus)last.focus({preventScroll:true});}
document.addEventListener('click',function(e){var t=e.target;if(t&&t.tagName==='IMG'&&ok(t)){e.preventDefault();e.stopPropagation();open(t);}},true);
document.addEventListener('mouseover',function(e){var t=e.target;if(t&&t.tagName==='IMG'&&!t.classList.contains('pm-zoom')&&ok(t)){t.classList.add('pm-zoom');if(!box)build();}},{passive:true});
function mark(){if(!box)build();Array.prototype.forEach.call(document.images,function(im){if(ok(im))im.classList.add('pm-zoom');});}
function later(){mark();setTimeout(mark,1500);setTimeout(mark,4000);}
if(document.readyState==='complete')later();else window.addEventListener('load',later);
})();
