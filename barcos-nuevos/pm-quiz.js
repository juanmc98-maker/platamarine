/* Plata Marine · "¿Qué modelo me conviene?" (ES/CA/EN/FR), común a todas las marcas.
   Datos en window.PM_QUIZ = {brand, models:[{n:nombre, u:'/ruta/sin-idioma/', loa:eslora m, reg:eslora de registro m,
   pax:personas CE, cab:0 open|1 camarote|2 camarote con ducha|3 dos o más camarotes, eng:1|2|3 motores, p:precio desde sin IVA,
   pe:true si el precio incluye motores}]}. Orientativo: puntúa cada modelo con las respuestas y enseña los 3 que mejor encajan. */
(function(){
'use strict';
var Q=window.PM_QUIZ,box=document.getElementById('pm-quiz');if(!Q||!box||!Q.models||!Q.models.length)return;
var LG=(document.documentElement.lang||'es').slice(0,2);if(['es','ca','en','fr'].indexOf(LG)<0)LG='es';
var PRE=LG==='es'?'':'/'+LG;
var T={
es:{k:'Te ayudo a elegir',h:'¿Qué '+Q.brand+' me conviene?',s:'Contesta cinco preguntas y te enseño los modelos que mejor encajan contigo. Es orientativo: luego lo hablamos y lo afinamos juntos.',
 q1:'¿Para qué lo quieres sobre todo?',a1:['Salir a pasar el día','Dormir a bordo alguna noche','Hacer travesías de varios días'],
 q2:'¿Cuántas personas soléis ir?',a2:['Hasta 6','De 7 a 10','Más de 10'],
 q3:'¿Qué titulación tienes?',a3:['PNB','PER','Patrón de Yate o superior','Todavía ninguna'],
 q4:'¿Uno o dos motores?',a4:['Uno, más sencillo','Dos o más, más seguridad','Me da igual'],
 q5:'Presupuesto aproximado (sin IVA)',a5:['Hasta 100.000 €','100.000 – 200.000 €','200.000 – 400.000 €','Más de 400.000 €'],
 go:'Ver qué modelo me conviene',res:'Los que mejor encajan contigo',best:'El que más encaja',see:'Ver el modelo',again:'Cambiar respuestas',
 from:'desde',vat:'+ impuestos',eng_inc:'con motores',eng_exc:'sin motores',
 why:{day:'Es una open: todo el espacio para el día en el agua',cab:'Tiene camarote para dormir a bordo',cab2:'Camarote y ducha para pasar días a bordo',cab3:'Dos o más camarotes para travesías',
  pax:'Homologado para {p} personas',one:'Va con un solo motor',two:'Va con {e} motores',pnb:'Con {l} m de eslora de registro se lleva con el PNB',small:'Es de los más manejables de la gama ({l} m)',budget:'Entra en tu presupuesto'},
 warn:{open:'No tiene camarote para dormir',pnb:'Con tu PNB no podrías llevarlo: necesitas el PER',per:'Necesitas el PER o superior',none:'Te hará falta titulación: {t}',budget:'Se sale de tu presupuesto',pax:'Homologado solo para {p} personas',big:'Mide {l} m: más barco que mantener'},
 tn:{pnb:'el PNB',per:'el PER',py:'el Patrón de Yate'},
 note:'Orientativo y no vinculante. La titulación depende de la eslora que figure en los papeles: confírmalo con tu escuela o con Capitanía. Precios desde, según la tarifa del astillero.',
 wa:'Hola Juan, he hecho el test de '+Q.brand+' y me sale el {m}. ¿Lo hablamos?',ask:'Preguntarme por WhatsApp',err:'Contesta las preguntas para ver el resultado.'},
ca:{k:'T’ajudo a triar',h:'Quin '+Q.brand+' em convé?',s:'Contesta cinc preguntes i t’ensenyo els models que encaixen millor amb tu. És orientatiu: després en parlem i ho afinem junts.',
 q1:'Per a què el vols sobretot?',a1:['Sortir a passar el dia','Dormir a bord alguna nit','Fer travessies de diversos dies'],
 q2:'Quantes persones hi soleu anar?',a2:['Fins a 6','De 7 a 10','Més de 10'],
 q3:'Quina titulació tens?',a3:['PNB','PER','Patró de Iot o superior','Encara cap'],
 q4:'Un o dos motors?',a4:['Un, més senzill','Dos o més, més seguretat','M’és igual'],
 q5:'Pressupost aproximat (sense IVA)',a5:['Fins a 100.000 €','100.000 – 200.000 €','200.000 – 400.000 €','Més de 400.000 €'],
 go:'Veure quin model em convé',res:'Els que encaixen millor amb tu',best:'El que encaixa més',see:'Veure el model',again:'Canviar respostes',
 from:'des de',vat:'+ impostos',eng_inc:'amb motors',eng_exc:'sense motors',
 why:{day:'És una open: tot l’espai per al dia a l’aigua',cab:'Té cabina per dormir a bord',cab2:'Cabina i dutxa per passar dies a bord',cab3:'Dues o més cabines per a travessies',
  pax:'Homologat per a {p} persones',one:'Porta un sol motor',two:'Porta {e} motors',pnb:'Amb {l} m d’eslora de registre es porta amb el PNB',small:'És dels més manejables de la gamma ({l} m)',budget:'Entra al teu pressupost'},
 warn:{open:'No té cabina per dormir',pnb:'Amb el PNB no el podries portar: necessites el PER',per:'Necessites el PER o superior',none:'Et caldrà titulació: {t}',budget:'Se surt del teu pressupost',pax:'Homologat només per a {p} persones',big:'Fa {l} m: més vaixell per mantenir'},
 tn:{pnb:'el PNB',per:'el PER',py:'el Patró de Iot'},
 note:'Orientatiu i no vinculant. La titulació depèn de l’eslora que consti als papers: confirma-ho amb la teva escola o amb Capitania. Preus des de, segons la tarifa de la drassana.',
 wa:'Hola Juan, he fet el test de '+Q.brand+' i em surt el {m}. En parlem?',ask:'Pregunta’m per WhatsApp',err:'Contesta les preguntes per veure el resultat.'},
en:{k:'Let me help you choose',h:'Which '+Q.brand+' suits me?',s:'Answer five questions and I will show you the models that suit you best. It is only a guide: then we talk it through together.',
 q1:'What will you mainly use it for?',a1:['Day trips','Sleeping on board now and then','Cruising for several days'],
 q2:'How many of you usually go?',a2:['Up to 6','7 to 10','More than 10'],
 q3:'Which licence do you hold?',a3:['PNB (up to 8 m)','PER (up to 15 m)','Yachtmaster or higher','None yet'],
 q4:'One engine or two?',a4:['One, simpler','Two or more, extra safety','No preference'],
 q5:'Approximate budget (excl. VAT)',a5:['Up to €100,000','€100,000 – 200,000','€200,000 – 400,000','Over €400,000'],
 go:'See which model suits me',res:'The ones that suit you best',best:'Best match',see:'See the model',again:'Change answers',
 from:'from',vat:'+ taxes',eng_inc:'with engines',eng_exc:'without engines',
 why:{day:'An open boat: all the space for days on the water',cab:'It has a cabin to sleep on board',cab2:'Cabin and shower for days on board',cab3:'Two or more cabins for cruising',
  pax:'Rated for {p} people',one:'Single engine',two:'{e} engines',pnb:'With {l} m registered length it can be handled with the PNB',small:'One of the easiest to handle in the range ({l} m)',budget:'Within your budget'},
 warn:{open:'No cabin to sleep in',pnb:'With a PNB you could not skipper it: you need the PER',per:'You need the Spanish PER or higher',none:'You will need a licence: {t}',budget:'Above your budget',pax:'Rated for only {p} people',big:'It is {l} m: more boat to maintain'},
 tn:{pnb:'the PNB',per:'the PER',py:'the Yachtmaster (Patrón de Yate)'},
 note:'A guide only, not binding. The licence depends on the length on the registration papers: check with your school or the Harbour Master. From prices, per the builder’s price list.',
 wa:'Hi Juan, I did the '+Q.brand+' quiz and got the {m}. Shall we talk?',ask:'Ask me on WhatsApp',err:'Please answer the questions to see the result.'},
fr:{k:'Je vous aide à choisir',h:'Quel '+Q.brand+' me convient ?',s:'Répondez à cinq questions et je vous montre les modèles qui vous correspondent le mieux. C’est indicatif : ensuite, nous en parlons ensemble.',
 q1:'Pour quoi le voulez-vous surtout ?',a1:['Sorties à la journée','Dormir à bord de temps en temps','Croisières de plusieurs jours'],
 q2:'Combien êtes-vous en général ?',a2:['Jusqu’à 6','De 7 à 10','Plus de 10'],
 q3:'Quel permis avez-vous ?',a3:['PNB (jusqu’à 8 m)','PER (jusqu’à 15 m)','Patron de yacht ou supérieur','Aucun pour l’instant'],
 q4:'Un ou deux moteurs ?',a4:['Un, plus simple','Deux ou plus, plus de sécurité','Peu importe'],
 q5:'Budget approximatif (HT)',a5:['Jusqu’à 100 000 €','100 000 – 200 000 €','200 000 – 400 000 €','Plus de 400 000 €'],
 go:'Voir le modèle qui me convient',res:'Ceux qui vous correspondent le mieux',best:'Le plus adapté',see:'Voir le modèle',again:'Modifier les réponses',
 from:'à partir de',vat:'+ taxes',eng_inc:'avec moteurs',eng_exc:'sans moteurs',
 why:{day:'Un open : tout l’espace pour la journée en mer',cab:'Il a une cabine pour dormir à bord',cab2:'Cabine et douche pour passer des jours à bord',cab3:'Deux cabines ou plus pour la croisière',
  pax:'Homologué pour {p} personnes',one:'Un seul moteur',two:'{e} moteurs',pnb:'Avec {l} m de longueur d’immatriculation, il se pilote avec le PNB',small:'L’un des plus maniables de la gamme ({l} m)',budget:'Dans votre budget'},
 warn:{open:'Pas de cabine pour dormir',pnb:'Avec le PNB vous ne pourriez pas le piloter : il faut le PER',per:'Il faut le PER espagnol ou supérieur',none:'Il vous faudra un permis : {t}',budget:'Au-dessus de votre budget',pax:'Homologué pour seulement {p} personnes',big:'Il mesure {l} m : plus de bateau à entretenir'},
 tn:{pnb:'le PNB',per:'le PER',py:'le Patron de yacht'},
 note:'Indicatif et non contractuel. Le permis dépend de la longueur inscrite sur les papiers : vérifiez auprès de votre école ou de la Capitainerie. Prix à partir de, selon le tarif du chantier.',
 wa:'Bonjour Juan, j’ai fait le test '+Q.brand+' et il me propose le {m}. On en parle ?',ask:'Me demander sur WhatsApp',err:'Répondez aux questions pour voir le résultat.'}
}[LG];
function eur(n){var s=Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g,LG==='en'?',':(LG==='fr'?' ':'.'));return LG==='en'?'€'+s:s+' €';}
function f(s,o){return s.replace(/\{(\w)\}/g,function(_,k){return o[k];});}
function num(x){return (LG==='en'?String(x):String(x).replace('.',','));}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
var css='#pm-quiz .qz{display:grid;gap:18px}#pm-quiz fieldset{border:0;margin:0;padding:0}#pm-quiz legend{font-weight:700;margin:0 0 8px;font-size:1.02rem}'
+'#pm-quiz .qz-o{display:flex;flex-wrap:wrap;gap:8px}#pm-quiz .qz-o label{display:flex;align-items:center;gap:8px;border:1px solid rgba(14,48,66,.2);background:#fff;color:#0D1C27;border-radius:999px;padding:9px 14px;cursor:pointer;font-size:15px}'
+'#pm-quiz .qz-o label:has(input:checked){border-color:#0B766B;box-shadow:0 0 0 1px #0B766B;background:#EAF6F3}#pm-quiz .qz-o input{accent-color:#0B766B}'
+'#pm-quiz .qz-go{justify-self:start;background:#0B766B;color:#fff;border:0;border-radius:12px;padding:13px 20px;font:inherit;font-weight:700;cursor:pointer}'
+'#pm-quiz .qz-r{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:6px}#pm-quiz .qz-c{background:#fff;color:#0D1C27;border:1px solid rgba(14,48,66,.16);border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:8px}'
+'#pm-quiz .qz-c.top{border-color:#0B766B;box-shadow:0 0 0 2px #0B766B}#pm-quiz .qz-c small.b{color:#0B766B;font-weight:700;text-transform:uppercase;letter-spacing:.05em;font-size:12px}#pm-quiz .qz-c h3{margin:0;font-size:1.15rem}'
+'#pm-quiz .qz-c .pr{font-weight:700}#pm-quiz .qz-c .pr span{color:#d9534f;font-size:.85em;margin-left:4px}#pm-quiz .qz-c ul{margin:0;padding-left:18px;font-size:14px;line-height:1.45}#pm-quiz .qz-c li.w{color:#8a5a00}'
+'#pm-quiz .qz-c a{margin-top:auto;display:inline-block;background:#0E3042;color:#fff;border-radius:10px;padding:10px 14px;text-decoration:none;font-weight:600;text-align:center}'
+'#pm-quiz .qz-n{font-size:12.5px;opacity:.8;margin:6px 0 0}#pm-quiz .qz-act{display:flex;gap:10px;flex-wrap:wrap;margin-top:10px}#pm-quiz .qz-act button,#pm-quiz .qz-act a{background:transparent;border:1px solid currentColor;color:inherit;border-radius:10px;padding:9px 14px;font:inherit;font-size:14px;cursor:pointer;text-decoration:none}';
var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
function grp(n,q,a){return '<fieldset><legend>'+q+'</legend><div class="qz-o">'+a.map(function(t,i){return '<label><input type="radio" name="'+n+'" value="'+i+'">'+esc(t)+'</label>';}).join('')+'</div></fieldset>';}
function form(){
  box.innerHTML='<p class="v2-k" style="margin:0">'+T.k+'</p><h2 style="margin:4px 0 6px">'+T.h+'</h2><p style="margin:0 0 16px;max-width:680px">'+T.s+'</p>'
   +'<div class="qz">'+grp('q1',T.q1,T.a1)+grp('q2',T.q2,T.a2)+grp('q3',T.q3,T.a3)+grp('q4',T.q4,T.a4)+grp('q5',T.q5,T.a5)
   +'<button type="button" class="qz-go">'+T.go+'</button><p class="qz-e" role="status" hidden></p><div class="qz-out" aria-live="polite"></div></div>';
  box.querySelector('.qz-go').onclick=run;
}
function v(n){var x=box.querySelector('input[name='+n+']:checked');return x?+x.value:-1;}
function need(m){var r=m.reg||m.loa;return r<=8?'pnb':(r<=24?'per':'py');}
function run(){
  var a=[v('q1'),v('q2'),v('q3'),v('q4'),v('q5')],e=box.querySelector('.qz-e');
  if(a.indexOf(-1)>-1){e.hidden=false;e.textContent=T.err;return;}e.hidden=true;
  var cap=[100000,200000,400000,1e12][a[4]],floor=[0,100000,200000,400000][a[4]];
  var res=Q.models.map(function(m){
    var s=0,w=[],y=[],lic=need(m),reg=m.reg||m.loa;
    if(a[0]===0){if(m.cab===0){s+=3;y.push(T.why.day);}else if(m.cab===1)s+=1;else s-=1;}
    if(a[0]===1){if(m.cab>=1){s+=3;y.push(m.cab>=2?T.why.cab2:T.why.cab);}else{s-=4;w.push(T.warn.open);}}
    if(a[0]===2){if(m.cab>=2){s+=4;y.push(m.cab>=3?T.why.cab3:T.why.cab2);}else if(m.cab===1){s+=1;y.push(T.why.cab);}else{s-=6;w.push(T.warn.open);}}
    var px=[6,10,12][a[1]];
    if(m.pax){if(m.pax<px){s-=3;w.push(f(T.warn.pax,{p:m.pax}));}else{s+=1;if(a[1]===2)y.push(f(T.why.pax,{p:m.pax}));}}
    if(a[1]===0&&m.loa<=9){s+=1;y.push(f(T.why.small,{l:num(m.loa)}));}
    if(a[1]===0&&m.loa>11){s-=1;w.push(f(T.warn.big,{l:num(m.loa)}));}
    if(a[2]===0){if(lic==='pnb'){s+=3;y.push(f(T.why.pnb,{l:num(reg)}));}else{s-=5;w.push(T.warn.pnb);}}
    if(a[2]===3){if(lic==='pnb')s+=1;w.push(f(T.warn.none,{t:T.tn[lic]}));}
    if(a[2]===1&&lic==='py'){s-=5;w.push(f(T.warn.none,{t:T.tn.py}));}
    if(a[3]===0){if(m.eng===1){s+=2;y.push(T.why.one);}else s-=1;}
    if(a[3]===1){if(m.eng>=2){s+=2;y.push(f(T.why.two,{e:m.eng}));}else s-=2;}
    if(m.p){if(m.p>cap){s-=(m.p>cap*1.5?6:3);w.push(T.warn.budget);}else{s+=2;if(m.p>=floor*0.8)s+=1;y.push(T.why.budget);}}
    return {m:m,s:s,y:y.slice(0,4),w:w.slice(0,3)};
  }).sort(function(x,z){return z.s-x.s||((x.m.p||0)-(z.m.p||0));}).slice(0,Math.min(3,Q.models.length));
  var h='<h3 style="margin:8px 0 0">'+T.res+'</h3><div class="qz-r">';
  res.forEach(function(r,i){var m=r.m,u=PRE+m.u;
    h+='<div class="qz-c'+(i?'':' top')+'">'+(i?'':'<small class="b">'+T.best+'</small>')+'<h3>'+esc(m.n)+'</h3>'
     +(m.p?'<div class="pr">'+T.from+' '+eur(m.p)+'<span>'+T.vat+'</span> <small style="font-weight:400">('+(m.pe?T.eng_inc:T.eng_exc)+')</small></div>':'')
     +'<ul>'+r.y.map(function(t){return '<li>'+esc(t)+'</li>';}).join('')+r.w.map(function(t){return '<li class="w">'+esc(t)+'</li>';}).join('')+'</ul>'
     +'<a href="'+u+'">'+T.see+'</a></div>';});
  var wa='https://wa.me/34633742973?text='+encodeURIComponent(f(T.wa,{m:res[0].m.n}));
  h+='</div><div class="qz-act"><a href="'+wa+'" target="_blank" rel="noopener" data-contact-intent="quiz_'+esc(Q.brand.toLowerCase())+'">'+T.ask+'</a><button type="button" class="qz-ag">'+T.again+'</button></div><p class="qz-n">'+T.note+'</p>';
  var o=box.querySelector('.qz-out');o.innerHTML=h;o.querySelector('.qz-ag').onclick=function(){box.scrollIntoView({behavior:'smooth'});};
  o.scrollIntoView({behavior:'smooth',block:'start'});
  if(window.pmTrack)window.pmTrack('tool_use',{tool:'quiz_'+Q.brand.toLowerCase(),result_type:res[0].m.n});
}
form();
})();
