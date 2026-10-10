/* Calculadora "¿Cuánto vale mi barco?" — rangos de /modelos/ (precios pedidos en anuncios, revisados cada mes). Muestra la horquilla observada completa, sin estrecharla.
   Al actualizar /modelos/ y /precios/ (tarea mensual), actualizar también M. No envía datos personales. */
(function(){
var M=[
 {s:'quicksilver-activ-605-open',n:'Quicksilver Activ 605 Open',b:[[2016,2021,20000,27000],[2022,2023,24000,36000],[2024,2026,33000,48000]]},
 {s:'beneteau-flyer-6-6-spacedeck',n:'Beneteau Flyer 6.6 SPACEdeck',b:[[2015,2017,26000,36500],[2018,2020,29000,43000]]},
 {s:'jeanneau-cap-camarat-6-5-cc',n:'Jeanneau Cap Camarat 6.5 CC',b:[[2008,2013,26000,32000],[2014,2018,33000,42000],[2019,2026,40000,60000]]},
 {s:'quicksilver-activ-675-sundeck',n:'Quicksilver Activ 675 Sundeck',b:[[2011,2016,25000,32000],[2017,2020,36000,45000],[2021,2026,45000,55000]]},
 {s:'jeanneau-cap-camarat-7-5-wa',n:'Jeanneau Cap Camarat 7.5 WA',b:[[2010,2014,32000,45000],[2015,2019,47000,76000],[2020,2026,65000,100000]]},
 {s:'jeanneau-merry-fisher-795',n:'Jeanneau Merry Fisher 795',b:[[2016,2017,45000,72000],[2018,2021,64000,83000],[2022,2026,87000,105000]]},
 {s:'beneteau-flyer-7-7-sundeck',n:'Beneteau Flyer 7.7 SUNdeck',b:[[2015,2016,41000,59000],[2017,2018,54000,72500]]},
 {s:'beneteau-antares-8',n:'Beneteau Antares 8',b:[[2016,2018,45000,73000],[2019,2021,67000,100000],[2022,2026,80000,110000]]},
 {s:'beneteau-flyer-8-sundeck',n:'Beneteau Flyer 8 SUNdeck',b:[[2019,2020,60000,80000],[2021,2024,72500,92500]]},
 {s:'bavaria-27-sport',n:'Bavaria 27 Sport',b:[[2006,2008,35000,65000],[2009,2012,50000,67000]]},
 {s:'jeanneau-cap-camarat-8-5-wa',n:'Jeanneau Cap Camarat 8.5 WA',b:[[2011,2014,60000,75000],[2015,2019,84000,107000],[2020,2026,120000,0]]},
 {s:'jeanneau-merry-fisher-895',n:'Jeanneau Merry Fisher 895',b:[[2017,2018,95000,135000],[2019,2020,115000,150000],[2021,2024,125000,180000]]}
];
var T=[ /* tipo: [esloraMin, esloraMax, desde, hasta] de la tabla por tipo de /precios/ */
 ['open',6.46,6.86,20000,60000],['sundeck',7.16,8.17,25000,92500],['wa',7.19,8.4,32000,120000],['pilot',7.43,8.9,45000,180000],['cruiser',8.35,8.35,35000,67000]
];
var root=document.getElementById('pmCalc'); if(!root) return;
var L=root.getAttribute('data-lang')||'es', P=(L==='es'?'':'/'+L);
var S=JSON.parse(document.getElementById('pmCalcI18n').textContent);
function $(id){return document.getElementById(id)}
function fmt(n){var r=Math.round(n/500)*500;var s=String(r).replace(/\B(?=(\d{3})+(?!\d))/g,L==='en'?',':'.');return L==='en'?'€'+s:s+' €'}
var sel=$('cvModelo');
M.forEach(function(m,i){var o=document.createElement('option');o.value=i;o.textContent=m.n;sel.appendChild(o)});
var o=document.createElement('option');o.value='otro';o.textContent=S.otro;sel.appendChild(o);
sel.onchange=function(){$('cvOtro').hidden=sel.value!=='otro'};
function track(r){try{window.pmTrack&&window.pmTrack('tool_result',{tool:'cuanto-vale',result_type:r})}catch(e){}}
function wa(txt){return 'https://wa.me/34633742973?text='+encodeURIComponent(txt)}
$('cvBtn').onclick=function(){
  var out=$('cvRes'),y=parseInt($('cvAnio').value,10),est=($('cvForm').querySelector('input[name=cvEst]:checked')||{}).value,hr=$('cvHoras').value;
  $('cvErr').textContent='';
  if(sel.value===''){$('cvErr').textContent=S.errModelo;return}
  if(!y||y<1960||y>2026){$('cvErr').textContent=S.errAnio;return}
  if(!est){$('cvErr').textContent=S.errEstado;return}
  var h='',name,msg;
  if(sel.value==='otro'){
    var tipo=$('cvTipo').value,es=parseFloat(($('cvEslora').value||'').replace(',','.'));name=($('cvMarca').value||'').trim()||S.miBarco;
    var t=null;T.forEach(function(x){if(x[0]===tipo&&es>=x[1]-0.3&&es<=x[2]+0.3)t=x});
    h='<h2>'+S.sinDatosT.replace('{n}',name)+'</h2><p>'+S.sinDatos+'</p>';
    if(t)h+='<p>'+S.refTipo.replace('{a}',fmt(t[3])).replace('{b}',fmt(t[4]))+'</p>';
    msg=S.waOtro.replace('{n}',name).replace('{y}',y).replace('{e}',$('cvEslora').value||'?');
    track(t?'tipo':'sin_datos');
  }else{
    var m=M[sel.value],b=null;name=m.n;
    m.b.forEach(function(x){if(y>=x[0]&&y<=x[1])b=x});
    if(!b){
      h='<h2>'+S.sinAnioT.replace('{n}',name).replace('{y}',y)+'</h2><p>'+S.sinAnio+'</p>';track('sin_anio');
    }else{
      var lo=b[2],hi=b[3];
      if(!hi){h='<h2>'+name+' · '+y+'</h2><p class="cv-big">'+S.desde+' '+fmt(lo)+'</p><p>'+S.pocos+'</p>';}
      else{
        /* Se muestra la horquilla observada completa. No se estrecha con porcentajes por estado u horas:
           no hay datos suficientes para justificar esos ajustes; el estado y las horas solo añaden notas. */
        h='<h2>'+name+' · '+y+'</h2><p class="cv-big">'+fmt(lo)+' – '+fmt(hi)+'</p>';
        h+='<p>'+S.contexto.replace('{a}',fmt(lo)).replace('{b}',fmt(hi)).replace('{y0}',b[0]).replace('{y1}',b[1])+'</p>';
        if(est==='top'&&S.top)h+='<p>'+S.top+'</p>';
        if(est==='obra')h+='<p>'+S.obra+'</p>';
        if(hr==='altas')h+='<p>'+S.horas+'</p>';
      }
      h+='<p><a href="'+P+'/modelos/'+m.s+'.html">'+S.verModelo.replace('{n}',name)+'</a></p>';
      track('rango');
    }
    msg=S.waModelo.replace('{n}',name).replace('{y}',y);
  }
  h+='<p class="cv-nota">'+S.nota+'</p>';
  h+='<p><a class="btn btn-wa" target="_blank" rel="noopener" href="'+wa(msg)+'">'+S.cta+'</a></p>';
  out.innerHTML=h;out.hidden=false;out.scrollIntoView({behavior:'smooth',block:'start'});
};
})();
