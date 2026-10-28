/* Plata Marine · configurador Catharsis 930 (ES/CA/EN/FR). Precios sin IVA, orientativos. */
(function(){
'use strict';
var lg=(document.documentElement.lang||'es').slice(0,2); if(['es','ca','en','fr'].indexOf(lg)<0) lg='es';
var BASE=103990;
var ENG=[
 {id:'none',p:0,es:['Sin motores','Los vemos juntos según el uso'],ca:['Sense motors','Els triem junts segons l’ús'],en:['No engines','We choose them together for your use'],fr:['Sans moteurs','Nous les choisissons ensemble selon l’usage']},
 {id:'2x250',p:49490,es:['2 × 250 CV','Mercury o Suzuki, montados'],ca:['2 × 250 CV','Mercury o Suzuki, muntats'],en:['2 × 250 hp','Mercury or Suzuki, fitted'],fr:['2 × 250 ch','Mercury ou Suzuki, installés']}
];
var OPT=[
 {id:'teca',p:4230,es:'Suelo de teca sintética',ca:'Terra de teca sintètica',en:'Synthetic teak decking',fr:'Pont en teck synthétique'},
 {id:'proa',p:3900,es:'Hélice de proa',ca:'Hèlix de proa',en:'Bow thruster',fr:'Propulseur d’étrave'},
 {id:'flaps',p:3900,es:'Flaps automáticos',ca:'Flaps automàtics',en:'Automatic trim tabs',fr:'Flaps automatiques'},
 {id:'plot12',p:5530,g:'plot',es:'Plotter de 12"',ca:'Plotter de 12"',en:'12" chartplotter',fr:'Traceur 12"'},
 {id:'plot9',p:3580,g:'plot',es:'Plotter de 9"',ca:'Plotter de 9"',en:'9" chartplotter',fr:'Traceur 9"'},
 {id:'vhf',p:1300,es:'Radio VHF',ca:'Ràdio VHF',en:'VHF radio',fr:'Radio VHF'},
 {id:'fusion',p:1560,es:'Equipo de música Fusion',ca:'Equip de música Fusion',en:'Fusion sound system',fr:'Système audio Fusion'},
 {id:'solar',p:1560,es:'Placas solares 420 W',ca:'Plaques solars 420 W',en:'420 W solar panels',fr:'Panneaux solaires 420 W'},
 {id:'calef',p:2860,es:'Calefacción diésel',ca:'Calefacció dièsel',en:'Diesel heating',fr:'Chauffage diesel'},
 {id:'calent',p:980,es:'Calentador de agua',ca:'Escalfador d’aigua',en:'Water heater',fr:'Chauffe-eau'},
 {id:'nevera',p:780,es:'Nevera de cajón',ca:'Nevera de calaix',en:'Drawer fridge',fr:'Réfrigérateur à tiroir'},
 {id:'verano',p:2280,es:'Toldo de verano',ca:'Tendal d’estiu',en:'Summer canopy',fr:'Taud d’été'},
 {id:'invierno',p:3580,es:'Toldo de invierno',ca:'Tendal d’hivern',en:'Winter cover',fr:'Taud d’hiver'},
 {id:'bimini',p:780,es:'Bimini de proa',ca:'Bimini de proa',en:'Bow bimini',fr:'Bimini avant'},
 {id:'cortinas',p:1040,g:'funda',es:'Cortinas y funda de parabrisas',ca:'Cortines i funda de parabrisa',en:'Curtains and windscreen cover',fr:'Rideaux et housse de pare-brise'},
 {id:'funda',p:390,g:'funda',es:'Funda de parabrisas',ca:'Funda de parabrisa',en:'Windscreen cover',fr:'Housse de pare-brise'},
 {id:'plataforma',p:1300,es:'Plataforma auxiliar',ca:'Plataforma auxiliar',en:'Auxiliary platform',fr:'Plateforme auxiliaire'},
 {id:'luces',p:980,es:'Luces subacuáticas',ca:'Llums subaquàtics',en:'Underwater lights',fr:'Éclairage sous-marin'},
 {id:'vivero',p:910,es:'Vivero',ca:'Viver',en:'Live bait well',fr:'Vivier'},
 {id:'vent',p:390,es:'Ventiladores',ca:'Ventiladors',en:'Fans',fr:'Ventilateurs'}
];
var T={
 es:{k:'Configurador',h:'Configura tu Catharsis 930',s:'Elige motores y opcionales. El total se actualiza al momento y me lo puedes enviar para que te prepare el presupuesto por escrito.',b:'Barco con equipamiento de serie',e:'1. Motores',o:'2. Equipamiento opcional',t:'Total orientativo',v:'+ impuestos',cta:'Enviarme esta configuración',n:'Precio orientativo sin IVA. No incluye transporte desde fábrica, impuesto de matriculación (IEDMT) ni matriculación. Puede cambiar y no es vinculante: el precio final es el del presupuesto por escrito.',wa:'Hola Juan, me interesa el Catharsis 930 con esta configuración:',we:'Motores',wo:'Opcionales',wn:'ninguno',wt:'Total orientativo'},
 ca:{k:'Configurador',h:'Configura el teu Catharsis 930',s:'Tria motors i opcionals. El total s’actualitza al moment i me’l pots enviar perquè et prepari el pressupost per escrit.',b:'Vaixell amb equipament de sèrie',e:'1. Motors',o:'2. Equipament opcional',t:'Total orientatiu',v:'+ impostos',cta:'Envia’m aquesta configuració',n:'Preu orientatiu sense IVA. No inclou el transport des de fàbrica, l’impost de matriculació (IEDMT) ni la matriculació. Pot canviar i no és vinculant: el preu final és el del pressupost per escrit.',wa:'Hola Juan, m’interessa el Catharsis 930 amb aquesta configuració:',we:'Motors',wo:'Opcionals',wn:'cap',wt:'Total orientatiu'},
 en:{k:'Configurator',h:'Configure your Catharsis 930',s:'Choose engines and options. The total updates instantly and you can send it to me so I prepare a written quote.',b:'Boat with standard equipment',e:'1. Engines',o:'2. Optional equipment',t:'Indicative total',v:'+ taxes',cta:'Send me this configuration',n:'Indicative price excluding VAT. It does not include transport from the factory, Spanish registration tax (IEDMT) or registration. It may change and is not binding: the final price is the one in the written quote.',wa:'Hello Juan, I am interested in the Catharsis 930 with this configuration:',we:'Engines',wo:'Options',wn:'none',wt:'Indicative total'},
 fr:{k:'Configurateur',h:'Configurez votre Catharsis 930',s:'Choisissez les moteurs et les options. Le total se met à jour instantanément et vous pouvez me l’envoyer pour que je prépare un devis écrit.',b:'Bateau avec équipement de série',e:'1. Moteurs',o:'2. Équipement en option',t:'Total indicatif',v:'HT',cta:'M’envoyer cette configuration',n:'Prix indicatif hors TVA. Il ne comprend pas le transport depuis l’usine, la taxe d’immatriculation espagnole (IEDMT) ni l’immatriculation. Il peut changer et n’est pas contractuel : le prix final est celui du devis écrit.',wa:'Bonjour Juan, le Catharsis 930 m’intéresse avec cette configuration :',we:'Moteurs',wo:'Options',wn:'aucune',wt:'Total indicatif'}
}[lg];
function eur(n){var s=String(Math.round(n)), sep=lg==='en'?',':(lg==='fr'?' ':'.');s=s.replace(/\B(?=(\d{3})+(?!\d))/g,sep);return lg==='en'?'€'+s:s+' €';}
function esc(x){return String(x).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
var end=document.getElementById('presupuesto'); if(!end||document.getElementById('cath-cfg')) return;
var css=document.createElement('style');
css.textContent='#configurar{padding:56px 0}#configurar .cc-k{font-size:13px;letter-spacing:.08em;text-transform:uppercase;opacity:.7;margin:0}#configurar h2{margin:6px 0 8px}#configurar .cc-s{max-width:640px;margin:0 0 24px}.cc{display:grid;grid-template-columns:1fr 320px;gap:24px;align-items:start}.cc h3{font-size:17px;margin:0 0 10px}.cc-step{margin:0 0 22px}.cc-ch{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px}.cc-ch label,.cc-op{display:flex;gap:10px;align-items:flex-start;padding:12px 14px;border:1.5px solid #dfe5e8;border-radius:12px;background:#fff;cursor:pointer}.cc-ch label:has(input:checked),.cc-op:has(input:checked){border-color:#0E3042;box-shadow:0 0 0 1px #0E3042}.cc-ch b,.cc-op span{display:block;font-weight:600}.cc-ch small{display:block;opacity:.7;font-size:13px}.cc-ch em,.cc-op em{font-style:normal;margin-left:auto;white-space:nowrap;font-weight:600}.cc-ops{display:grid;gap:8px}.cc-op input,.cc-ch input{margin-top:3px}.cc-sum{position:sticky;top:90px;padding:20px;border-radius:16px;background:#0E3042;color:#fff}.cc-sum p{margin:0 0 6px;font-size:14px;opacity:.85}.cc-tot{font-size:30px;font-weight:700;margin:4px 0 2px}.cc-tot span{font-size:15px;font-weight:600;color:#ff8a80;margin-left:6px}.cc-sum ul{margin:10px 0 14px;padding-left:18px;font-size:14px;opacity:.9}.cc-sum .btn{display:block;width:100%;box-sizing:border-box;text-align:center}.cc-n{font-size:12px;opacity:.75;margin:12px 0 0}@media(max-width:860px){.cc{grid-template-columns:1fr}.cc-sum{position:static}}';
document.head.appendChild(css);
var sec=document.createElement('section'); sec.className='v2-sec'; sec.id='configurar';
var h='<div class="wrap"><p class="cc-k">'+T.k+'</p><h2>'+T.h+'</h2><p class="cc-s">'+T.s+'</p><div class="cc" id="cath-cfg"><div>';
h+='<div class="cc-step"><h3>'+T.e+'</h3><div class="cc-ch">';
ENG.forEach(function(e,i){h+='<label><input type="radio" name="cce" value="'+i+'"'+(i===0?' checked':'')+'><span><b>'+esc(e[lg][0])+'</b><small>'+esc(e[lg][1])+'</small></span><em>'+(e.p?'+'+eur(e.p):'')+'</em></label>';});
h+='</div></div><div class="cc-step"><h3>'+T.o+'</h3><div class="cc-ops">';
OPT.forEach(function(o,i){h+='<label class="cc-op"><input type="checkbox" name="cco" value="'+i+'"'+(o.g?' data-g="'+o.g+'"':'')+'><span>'+esc(o[lg])+'</span><em>+'+eur(o.p)+'</em></label>';});
h+='</div></div></div><aside class="cc-sum"><p>'+T.b+': '+eur(BASE)+'</p><p>'+T.t+'</p><div class="cc-tot" id="cc-tot"></div><ul id="cc-list"></ul><a class="btn btn-wa" id="cc-wa" target="_blank" rel="noopener" data-wa-context="configurador">'+T.cta+'</a><p class="cc-n">'+T.n+'</p></aside></div></div>';
sec.innerHTML=h; end.parentNode.insertBefore(sec,end);
var box=document.getElementById('cath-cfg');
function upd(ev){
 var t=ev&&ev.target;
 if(t&&t.checked&&t.dataset.g){[].forEach.call(box.querySelectorAll('input[data-g="'+t.dataset.g+'"]'),function(x){if(x!==t)x.checked=false;});}
 var e=ENG[+box.querySelector('input[name=cce]:checked').value], tot=BASE+e.p, sel=[];
 [].forEach.call(box.querySelectorAll('input[name=cco]:checked'),function(x){var o=OPT[+x.value];tot+=o.p;sel.push(o);});
 document.getElementById('cc-tot').innerHTML=eur(tot)+'<span>'+T.v+'</span>';
 var li='<li>'+esc(e[lg][0])+(e.p?' (+'+eur(e.p)+')':'')+'</li>'; sel.forEach(function(o){li+='<li>'+esc(o[lg])+'</li>';});
 document.getElementById('cc-list').innerHTML=li;
 var msg=T.wa+'\n- '+T.we+': '+e[lg][0]+'\n- '+T.wo+': '+(sel.length?sel.map(function(o){return o[lg];}).join(', '):T.wn)+'\n'+T.wt+': '+eur(tot)+' '+T.v+'\n'+location.origin+location.pathname;
 document.getElementById('cc-wa').href='https://wa.me/34633742973?text='+encodeURIComponent(msg);
}
box.addEventListener('change',upd); upd();
})();
