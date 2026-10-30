/* Plata Marine · configurador Catharsis 930 (ES/CA/EN/FR). Precios sin IVA, orientativos. Oferta en PDF con registro del lead (source 'catharsis'). */
(function(){
'use strict';
var lg=(document.documentElement.lang||'es').slice(0,2); if(['es','ca','en','fr'].indexOf(lg)<0) lg='es';
var BASE=103990;
var ENG=[
 {id:'none',p:0,es:['Sin motores','Los vemos juntos según el uso'],ca:['Sense motors','Els triem junts segons l’ús'],en:['No engines','We choose them together for your use'],fr:['Sans moteurs','Nous les choisissons ensemble selon l’usage']},
 {id:'2x250',p:49490,es:['2 × 250 CV','Mercury o Suzuki, montados'],ca:['2 × 250 CV','Mercury o Suzuki, muntats'],en:['2 × 250 hp','Mercury or Suzuki, fitted'],fr:['2 × 250 ch','Mercury ou Suzuki, installés']},
 {id:'1x400',p:45990,es:['1 × 400 CV','Mercury, montado'],ca:['1 × 400 CV','Mercury, muntat'],en:['1 × 400 hp','Mercury, fitted'],fr:['1 × 400 ch','Mercury, installé']}
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
var PT={
 es:{btn:'Descargar PDF',h:'Descarga tu oferta en PDF',i:'Déjame tus datos y te descargas la oferta con tu configuración y un número de oferta, para que lo hablemos cuando quieras.',n:'Nombre',t:'Teléfono',priv:'Responsable: Juan Morante (Plata Marine). Usaré estos datos solo para contestarte y preparar tu presupuesto. Si avanzamos, los compartiré con el astillero para emitir el pedido. Puedes ejercer tus derechos en juan@platamarine.com.',privl:'Política de privacidad',privurl:'/privacidad.html',ok:'He leído la información de privacidad y acepto que uses estos datos para contestarme.',wait:'Preparando tu oferta…',offer:'Oferta',kind:'Crucero fueraborda · 9,30 m',for:'Preparada para',date:'Fecha',cfg:'Tu configuración',specs:'Datos principales',tot:'Total sin impuestos',tax:'Precio sin impuestos. IVA, impuesto de matriculación (IEDMT), matriculación y transporte desde fábrica, aparte: te lo detallo en el presupuesto.',scan:'Escanea el código para ver o cambiar esta configuración en la web',valid:'Oferta orientativa. No es vinculante: el precio final es el del presupuesto por escrito. Plazo de entrega a consultar, confirmado siempre por escrito antes del pedido. Transporte desde fábrica, impuesto de matriculación y gastos de matriculación, aparte.',e:['Escribe tu nombre (solo letras).','Revisa el email, por ejemplo nombre@email.com.','Revisa el teléfono, por ejemplo 612 345 678 o +33 6 12 34 56 78.','Marca la casilla de privacidad.','No he podido guardar tus datos. Vuelve a intentarlo en unos minutos o escríbeme a juan@platamarine.com.']},
 ca:{btn:'Descarregar PDF',h:'Descarrega la teva oferta en PDF',i:'Deixa’m les teves dades i et descarregues l’oferta amb la teva configuració i un número d’oferta, perquè en parlem quan vulguis.',n:'Nom',t:'Telèfon',priv:'Responsable: Juan Morante (Plata Marine). Faré servir aquestes dades només per contestar-te i preparar el teu pressupost. Si avancem, les compartiré amb la drassana per emetre la comanda. Pots exercir els teus drets a juan@platamarine.com.',privl:'Política de privacitat',privurl:'/ca/privacidad.html',ok:'He llegit la informació de privacitat i accepto que facis servir aquestes dades per contestar-me.',wait:'Preparant la teva oferta…',offer:'Oferta',kind:'Creuer fora borda · 9,30 m',for:'Preparada per a',date:'Data',cfg:'La teva configuració',specs:'Dades principals',tot:'Total sense impostos',tax:'Preu sense impostos. IVA, impost de matriculació (IEDMT), matriculació i transport des de fàbrica, a part: t’ho detallo al pressupost.',scan:'Escaneja el codi per veure o canviar aquesta configuració al web',valid:'Oferta orientativa. No és vinculant: el preu final és el del pressupost per escrit. Termini d’entrega a consultar, confirmat sempre per escrit abans de la comanda. Transport des de fàbrica, impost de matriculació i despeses de matriculació, a part.',e:['Escriu el teu nom (només lletres).','Revisa el correu, per exemple nom@correu.com.','Revisa el telèfon, per exemple 612 345 678 o +33 6 12 34 56 78.','Marca la casella de privacitat.','No he pogut desar les teves dades. Torna-ho a provar d’aquí a uns minuts o escriu-me a juan@platamarine.com.']},
 en:{btn:'Download PDF',h:'Download your offer as a PDF',i:'Leave me your details and download the offer with your configuration and an offer number, so we can talk about it whenever you like.',n:'Name',t:'Phone',priv:'Data controller: Juan Morante (Plata Marine). I will only use these details to reply to you and prepare your quote. If we go ahead, I will share them with the shipyard to place the order. You can exercise your rights at juan@platamarine.com.',privl:'Privacy policy',privurl:'/en/privacidad.html',ok:'I have read the privacy information and agree to you using these details to reply to me.',wait:'Preparing your offer…',offer:'Offer',kind:'Outboard cruiser · 9.30 m',for:'Prepared for',date:'Date',cfg:'Your configuration',specs:'Main data',tot:'Total excluding taxes',tax:'Price excluding taxes. VAT, Spanish registration tax (IEDMT), registration and transport from the factory are extra: I will detail them in the quote.',scan:'Scan the code to view or change this configuration on the website',valid:'Indicative offer. Not binding: the final price is the one in the written quote. Delivery time on request, always confirmed in writing before the order. Transport from the factory, registration tax and registration costs are extra.',e:['Please enter your name (letters only).','Please check the email, e.g. name@email.com.','Please check the phone number, e.g. +44 7700 900123.','Please tick the privacy box.','I could not save your details. Please try again in a few minutes or write to juan@platamarine.com.']},
 fr:{btn:'Télécharger le PDF',h:'Téléchargez votre offre en PDF',i:'Laissez-moi vos coordonnées et téléchargez l’offre avec votre configuration et un numéro d’offre, pour en parler quand vous voulez.',n:'Nom',t:'Téléphone',priv:'Responsable : Juan Morante (Plata Marine). J’utiliserai ces données uniquement pour vous répondre et préparer votre devis. Si nous avançons, je les transmettrai au chantier pour passer la commande. Vous pouvez exercer vos droits à juan@platamarine.com.',privl:'Politique de confidentialité',privurl:'/fr/privacidad.html',ok:'J’ai lu les informations de confidentialité et j’accepte que vous utilisiez ces données pour me répondre.',wait:'Préparation de votre offre…',offer:'Offre',kind:'Croiseur hors-bord · 9,30 m',for:'Préparée pour',date:'Date',cfg:'Votre configuration',specs:'Données principales',tot:'Total hors taxes',tax:'Prix hors taxes. TVA, taxe d’immatriculation espagnole (IEDMT), immatriculation et transport depuis l’usine en sus : je les détaille dans le devis.',scan:'Scannez le code pour voir ou modifier cette configuration sur le site',valid:'Offre indicative, non contractuelle : le prix final est celui du devis écrit. Délai de livraison sur demande, toujours confirmé par écrit avant la commande. Transport depuis l’usine, taxe et frais d’immatriculation en sus.',e:['Indiquez votre nom (lettres uniquement).','Vérifiez l’e-mail, par exemple nom@email.fr.','Vérifiez le numéro, par exemple +33 6 12 34 56 78.','Cochez la case de confidentialité.','Je n’ai pas pu enregistrer vos coordonnées. Réessayez dans quelques minutes ou écrivez à juan@platamarine.com.']}
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
h+='</div></div></div><aside class="cc-sum"><p>'+T.b+': '+eur(BASE)+'</p><p>'+T.t+'</p><div class="cc-tot" id="cc-tot"></div><ul id="cc-list"></ul><a class="btn btn-wa" id="cc-wa" target="_blank" rel="noopener" data-wa-context="configurador">'+T.cta+'</a><button type="button" class="btn cc-pdf" id="cc-pdf">'+PT.btn+'</button><p class="cc-n">'+T.n+'</p></aside></div></div>';
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
 ST={e:e,sel:sel,tot:tot,ei:+box.querySelector('input[name=cce]:checked').value,oi:[].map.call(box.querySelectorAll('input[name=cco]:checked'),function(x){return +x.value;})};
 if(ev&&history.replaceState) history.replaceState(null,'',hashOf());
}
box.addEventListener('change',upd); upd();
/* Oferta en PDF (como Mar.Co): pide nombre, teléfono y email, guarda el lead con nº de oferta y configuración, y genera la ficha imprimible */
var ST;
function hashOf(){return '#cfg='+ST.ei+(ST.oi.length?'-'+ST.oi.join('.'):'');}
(function(){var hm=location.hash.match(/^#cfg=(\d)(?:-([\d.]+))?$/);if(!hm)return;
 var r0=box.querySelector('input[name=cce][value="'+hm[1]+'"]');if(r0)r0.checked=true;
 (hm[2]||'').split('.').forEach(function(i){var o=box.querySelector('input[name=cco][value="'+i+'"]');if(o)o.checked=true;});
 upd();setTimeout(function(){sec.scrollIntoView();},300);})();
var LEADS_URL='https://script.google.com/macros/s/AKfycbwJtBkktakE0qgmu_b8oHOOopCDnG6BDpBjg2zBUsZKi8l3_OBEuez_OHWmE9j8qCBF/exec';
var SPECS={
 es:[['Eslora total','9,30 m'],['Eslora de casco','9,10 m'],['Manga','3,00 m'],['Personas','8'],['Camarotes','2 · 4 plazas para dormir'],['Combustible','2 × 225 l'],['Potencia máxima','447 kW (≈ 600 cv)'],['Categoría de diseño CE','C'],['Titulación','PER o superior']],
 ca:[['Eslora total','9,30 m'],['Eslora de buc','9,10 m'],['Mànega','3,00 m'],['Persones','8'],['Cabines','2 · 4 places per dormir'],['Combustible','2 × 225 l'],['Potència màxima','447 kW (≈ 600 cv)'],['Categoria de disseny CE','C'],['Titulació','PER o superior']],
 en:[['Length overall','9.30 m'],['Hull length','9.10 m'],['Beam','3.00 m'],['People','8'],['Cabins','2 · 4 berths'],['Fuel','2 × 225 l'],['Maximum power','447 kW (≈ 600 hp)'],['CE design category','C'],['Licence (Spain)','PER or higher']],
 fr:[['Longueur hors tout','9,30 m'],['Longueur de coque','9,10 m'],['Largeur','3,00 m'],['Personnes','8'],['Cabines','2 · 4 couchages'],['Carburant','2 × 225 l'],['Puissance maximale','447 kW (≈ 600 ch)'],['Catégorie de conception CE','C'],['Permis (Espagne)','PER ou supérieur']]
}[lg];
var dlCss=document.createElement('style');
dlCss.textContent='.cc-pdf{margin-top:8px;font-size:15px!important;padding:12px 16px;background:transparent!important;color:#fff!important;border:1.5px solid rgba(255,255,255,.6)!important;cursor:pointer;font:inherit;font-weight:600}.cc-pdf:hover{border-color:#fff!important}'+
'.cc-dl{position:fixed;inset:0;z-index:2147483001;background:rgba(6,10,14,.6);display:flex;align-items:center;justify-content:center;padding:16px}.cc-dl[hidden]{display:none}.cc-dl>div{background:#fff;color:#0D1C27;border-radius:16px;max-width:460px;width:100%;padding:24px 22px;box-shadow:0 30px 80px rgba(0,0,0,.35);max-height:92vh;overflow:auto;position:relative}.cc-dl h3{font-size:1.3rem;margin:0 0 8px;padding-right:30px}.cc-dl p{font-size:.93rem;line-height:1.5;margin:0 0 12px}.cc-dl .x{position:absolute;top:10px;right:12px;border:0;background:none;font-size:26px;cursor:pointer}.cc-dl label{display:block;font-weight:600;font-size:14px;margin:0 0 4px}.cc-dl input[type=text],.cc-dl input[type=tel],.cc-dl input[type=email]{width:100%;box-sizing:border-box;padding:11px 12px;border:1.5px solid #dfe5e8;border-radius:10px;font:inherit;margin:0 0 12px}.cc-dl .help{font-size:12.5px;color:#5b6b75}.cc-dl .chk{display:flex;gap:10px;align-items:flex-start;font-weight:400;font-size:14px;line-height:1.45;cursor:pointer;margin:0 0 14px}.cc-dl .chk input{width:20px;height:20px;min-width:20px;margin:1px 0 0;accent-color:#0B766B}.cc-dl button[type=submit]{width:100%;padding:13px;border:0;border-radius:12px;background:#0B766B;color:#fff;font:inherit;font-weight:700;cursor:pointer}'+
'#cc-sheet{display:none}@media print{@page{size:A4;margin:0}html,body{background:#fff!important}body>*:not(#cc-sheet){display:none!important}'+
'#cc-sheet{display:block;color:#0D1C27;font:9.5pt/1.4 "Helvetica Neue",Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}#cc-sheet .pg{width:210mm;box-sizing:border-box;padding:10mm 13mm 8mm}#cc-sheet .hd{display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #B58A2C;padding-bottom:5mm}#cc-sheet .hd img{height:10mm;width:auto}#cc-sheet .hd img.b{height:9mm}#cc-sheet .meta{display:flex;justify-content:space-between;align-items:flex-end;margin:4mm 0 3mm}#cc-sheet .meta .k{font-size:7.5pt;letter-spacing:.14em;text-transform:uppercase;color:#17465F;font-weight:700}#cc-sheet .meta h1{font-size:23pt;line-height:1.05;margin:1.5mm 0 1mm;font-weight:800}#cc-sheet .meta .s{color:#44545F}#cc-sheet .ref{text-align:right;border:1px solid #0D1C27;border-radius:3mm;padding:2.5mm 4mm}#cc-sheet .ref b{display:block;font-size:12pt;letter-spacing:.04em}#cc-sheet .ref span{font-size:7.5pt;color:#44545F;display:block}#cc-sheet .hero{width:100%;height:62mm;object-fit:cover;border-radius:3mm;display:block}#cc-sheet .th{display:grid;grid-template-columns:repeat(3,1fr);gap:2.5mm;margin-top:2.5mm}#cc-sheet .th img{width:100%;height:21mm;object-fit:cover;border-radius:2mm;display:block}#cc-sheet .cols{display:grid;grid-template-columns:1.55fr 1fr;gap:7mm;margin-top:4.5mm;font-size:8.6pt}#cc-sheet h2{font-size:8pt;letter-spacing:.14em;text-transform:uppercase;color:#17465F;margin:0 0 2mm;font-weight:700}#cc-sheet table{width:100%;border-collapse:collapse}#cc-sheet td{padding:1.1mm 0;border-bottom:.3mm solid #dfe4e7;vertical-align:top}#cc-sheet td:last-child{text-align:right;white-space:nowrap;padding-left:3mm;font-weight:600}#cc-sheet dl{margin:0;display:grid;grid-template-columns:1fr auto;gap:1.4mm 3mm}#cc-sheet dt{color:#44545F}#cc-sheet dd{margin:0;text-align:right;font-weight:700}#cc-sheet .tot{margin-top:4mm;background:#0D1C27;color:#fff;border-radius:3mm;padding:4.5mm 5mm;display:flex;justify-content:space-between;align-items:center;page-break-inside:avoid}#cc-sheet .tot .l{font-size:8pt;letter-spacing:.12em;text-transform:uppercase;color:#B7C3CB}#cc-sheet .tot .v{font-size:20pt;font-weight:800}#cc-sheet .tot .vat{color:#ff8a80;font-size:10pt;font-weight:800;margin-left:2mm}#cc-sheet .tot .iva{font-size:7.5pt;color:#B7C3CB;text-align:right;max-width:75mm;line-height:1.5}#cc-sheet .ft{display:flex;gap:6mm;align-items:center;margin-top:4mm;page-break-inside:avoid}#cc-sheet .ft .qr{width:24mm;height:24mm;flex:none}#cc-sheet .ft .qr svg{width:100%;height:100%;display:block}#cc-sheet .ft .c b{font-size:11pt;display:block}#cc-sheet .ft .c{line-height:1.55}#cc-sheet .ft .c small{display:block;color:#44545F;font-size:7.5pt}#cc-sheet .sm{font-size:6.8pt;color:#6b7a84;margin-top:3mm;line-height:1.4}#cc-sheet.many .th{display:none}#cc-sheet.many .hero{height:52mm}}';
document.head.appendChild(dlCss);
if(!window.submitConfirmed){var sc0=document.createElement('script');sc0.src='/submit-confirmed.js';document.head.appendChild(sc0);}
var dl=document.createElement('div');dl.className='cc-dl';dl.id='cc-dl';dl.hidden=true;dl.setAttribute('role','dialog');dl.setAttribute('aria-modal','true');
dl.innerHTML='<div><button type="button" class="x" aria-label="×">×</button><h3>'+PT.h+'</h3><p>'+PT.i+'</p><form id="ccDl" novalidate data-contact-intent="catharsis_pdf">'+
 '<label for="cdl_name">'+PT.n+' *</label><input id="cdl_name" type="text" required autocomplete="name" maxlength="60">'+
 '<label for="cdl_tel">'+PT.t+' *</label><input id="cdl_tel" type="tel" required autocomplete="tel" inputmode="tel" maxlength="20" placeholder="+34 6xx xxx xxx">'+
 '<label for="cdl_email">Email *</label><input id="cdl_email" type="email" required autocomplete="email" maxlength="100">'+
 '<p class="help">'+PT.priv+' <a href="'+PT.privurl+'">'+PT.privl+'</a>.</p>'+
 '<label class="chk"><input id="cdl_consent" type="checkbox" required><span>'+PT.ok+' *</span></label>'+
 '<button type="submit" id="cdl_send">'+PT.btn+'</button><p id="cdl_status" class="help" role="status" aria-live="polite" hidden></p></form></div>';
document.body.appendChild(dl);
var dlf=document.getElementById('ccDl'),client=null,lastF=null;
function offerNo(){var d=new Date(),p=function(n){return (n<10?'0':'')+n;};var a='ABCDEFGHJKLMNPQRSTUVWXYZ23456789',r='';for(var i=0;i<4;i++)r+=a.charAt(Math.floor(Math.random()*a.length));return 'PM-CA-'+String(d.getFullYear()).slice(2)+p(d.getMonth()+1)+p(d.getDate())+'-'+r;}
function cfgUrl(){return location.origin+location.pathname+hashOf();}
function loadQr(){return new Promise(function(ok){if(window.qrcode)return ok();var s=document.createElement('script');s.src='/marco/qr.js';s.onload=ok;s.onerror=ok;document.head.appendChild(s);});}
function sheet(no){
 var rows='<tr><td>'+esc(T.b)+' <span style="color:#6b7a84">('+esc(ENG[0][lg][0].toLowerCase())+')</span></td><td>'+eur(BASE)+'</td></tr>';
 rows+='<tr><td>'+esc(T.we)+' · '+esc(ST.e[lg][0])+(ST.e.p?' ('+esc(ST.e[lg][1])+')':'')+'</td><td>'+(ST.e.p?'+'+eur(ST.e.p):'—')+'</td></tr>';
 ST.sel.forEach(function(o){rows+='<tr><td>'+esc(o[lg])+'</td><td>+'+eur(o.p)+'</td></tr>';});
 var specs=SPECS.map(function(x){return '<dt>'+esc(x[0])+'</dt><dd>'+esc(x[1])+'</dd>';}).join('');
 var qr='';try{if(window.qrcode){var q=qrcode(0,'M');q.addData(cfgUrl());q.make();qr=q.createSvgTag({cellSize:4,margin:0,scalable:true});}}catch(e){}
 var dt=new Date().toLocaleDateString(lg==='en'?'en-GB':lg+'-ES',{day:'2-digit',month:'2-digit',year:'numeric'});
 var th=['2','3','4'].map(function(n){return '<img src="/catharsis/fotos/catharsis-930-'+n+'.jpg" alt="">';}).join('');
 var h='<div class="pg"><div class="hd"><img src="/logo-plata-marine.png" alt="Plata Marine"><img class="b" src="/barcos-nuevos/logos/avila-marin.png" alt="Avila Marin"></div>'+
  '<div class="meta"><div><div class="k">'+esc(PT.offer)+' · '+esc(PT.kind)+'</div><h1>Catharsis 930</h1><div class="s">'+esc(PT.for)+': <b>'+esc(client.n)+'</b></div></div>'+
  '<div class="ref"><span>'+esc(PT.offer)+' nº</span><b>'+no+'</b><span>'+esc(PT.date)+': '+dt+'</span></div></div>'+
  '<img class="hero" src="/catharsis/fotos/catharsis-930-1.jpg" alt=""><div class="th">'+th+'</div>'+
  '<div class="cols"><div><h2>'+esc(PT.cfg)+'</h2><table>'+rows+'</table></div><div><h2>'+esc(PT.specs)+'</h2><dl>'+specs+'</dl></div></div>'+
  '<div class="tot"><div><div class="l">'+esc(PT.tot)+'</div><div class="v">'+eur(ST.tot)+'<span class="vat">'+esc(T.v)+'</span></div></div><div class="iva">'+esc(PT.tax)+'</div></div>'+
  '<div class="ft">'+(qr?'<div class="qr">'+qr+'</div>':'')+'<div class="c"><small>'+esc(PT.scan)+'</small><b>Juan Morante · Plata Marine</b>+34 633 742 973 · juan@platamarine.com · www.platamarine.com</div></div>'+
  '<p class="sm">'+esc(PT.valid)+'</p></div>';
 var sh=document.getElementById('cc-sheet');if(!sh){sh=document.createElement('div');sh.id='cc-sheet';document.body.appendChild(sh);}
 sh.innerHTML=h;sh.className=ST.sel.length>9?'many':'';
 var imgs=[].slice.call(sh.querySelectorAll('img'));
 return Promise.all(imgs.map(function(i){return i.complete?1:new Promise(function(r){i.onload=i.onerror=r;});}));
}
function txt(){return 'Catharsis 930: '+eur(BASE)+' · '+T.we+': '+ST.e[lg][0]+(ST.e.p?' '+eur(ST.e.p):'')+(ST.sel.length?' · '+ST.sel.map(function(o){return '+ '+o[lg]+' '+eur(o.p);}).join(' · '):'')+' · '+PT.tot+': '+eur(ST.tot)+' '+T.v;}
function makePdf(){
 upd();var no=offerNo(),st=document.getElementById('cdl_status'),bt=document.getElementById('cdl_send');
 var payload={source:'catharsis',barco:'Catharsis 930 · oferta '+no,nombre:client.n,telefono:client.t,email:client.e,detail:'Oferta PDF '+no+' · '+txt()+' | Email: '+client.e+' | Enlace: '+cfgUrl(),lang:lg,page:location.pathname,ua:navigator.userAgent.slice(0,120),consent:true,consent_v:'2026-10',consent_at:new Date().toISOString()};
 st.hidden=false;st.textContent=PT.wait;bt.disabled=true;
 return window.submitConfirmed(LEADS_URL,payload,'json',dlf).then(function(){
  if(window.pmTrack)window.pmTrack('generate_lead',{form_id:'catharsis_pdf',contact_purpose:'offer_pdf',placement:'catharsis',boat:'Catharsis 930'});
  return loadQr().then(function(){return sheet(no);}).then(function(){dl.hidden=true;bt.disabled=false;st.hidden=true;var t0=document.title;document.title='Catharsis 930 · '+no;window.print();setTimeout(function(){document.title=t0;},1500);});
 });
}
document.getElementById('cc-pdf').addEventListener('click',function(){
 if(client){makePdf().catch(function(){});return;}
 lastF=document.activeElement;dl.hidden=false;var n=document.getElementById('cdl_name');if(n)n.focus();
 if(window.pmTrack)window.pmTrack('contact_intent',{method:'pdf',placement:'catharsis'});
});
dl.querySelector('.x').addEventListener('click',function(){dl.hidden=true;if(lastF)lastF.focus();});
dl.addEventListener('click',function(e){if(e.target===dl)dl.hidden=true;});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!dl.hidden)dl.hidden=true;});
dlf.addEventListener('input',function(e){if(e.target.setCustomValidity)e.target.setCustomValidity('');});
dlf.addEventListener('submit',function(e){
 e.preventDefault();
 var n=document.getElementById('cdl_name'),t=document.getElementById('cdl_tel'),m=document.getElementById('cdl_email'),c=document.getElementById('cdl_consent'),first=null;
 var okN=n.value.trim().length>=2&&/\p{L}/u.test(n.value)&&!/[0-9@]|https?:|www\./i.test(n.value);
 var d=t.value.replace(/[\s().-]/g,''),okT=/^[6-9]\d{8}$/.test(d)||/^(\+|00)\d{8,15}$/.test(d);
 var okE=/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(m.value.trim());
 [[n,okN,PT.e[0]],[m,okE,PT.e[1]],[t,okT,PT.e[2]],[c,c.checked,PT.e[3]]].forEach(function(r){r[0].setCustomValidity(r[1]?'':r[2]);if(!r[1]&&!first)first=r[0];});
 if(first){first.reportValidity();return;}
 var st=document.getElementById('cdl_status');
 if(!window.submitConfirmed){st.hidden=false;st.textContent=PT.e[4];return;}
 client={n:n.value.trim(),t:t.value.trim(),e:m.value.trim()};
 makePdf().catch(function(){client=null;document.getElementById('cdl_send').disabled=false;st.hidden=false;st.textContent=PT.e[4];});
});

var LBL={es:'Configurar y pedir presupuesto',ca:'Configurar i demanar pressupost',en:'Configure and get a quote',fr:'Configurer et demander un devis'}[lg];
[].forEach.call(document.querySelectorAll('.price-box .btn-wa, #presupuesto .btn-wa'),function(a){a.href='#configurar';a.removeAttribute('target');a.removeAttribute('rel');a.removeAttribute('data-wa-context');a.textContent=LBL;});
})();
