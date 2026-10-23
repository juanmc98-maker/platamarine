/* Plata Marine · configurador de /seastorm/ (ES/CA/EN/FR).
   Datos en <script id="ssCfgData"> (los genera _tools/seastorm_config.py).
   Precio: solo el del barco (tarifa oficial, versión Advantage). Motor, remolque, transporte y matriculación: se presupuestan.
   Titulación: sin título hasta 5 m de eslora y 15 CV; si no, Licencia de Navegación o superior (hasta 6 m). */
(function(){
  'use strict';
  var box=document.getElementById('ssCfg'), raw=document.getElementById('ssCfgData');
  if(!box||!raw) return;
  var D; try{D=JSON.parse(raw.textContent);}catch(e){return;}
  var T=D.t, L=D.lang;
  function $(id){return document.getElementById(id);}
  function eur(n){
    var s=Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g,L==='en'?',':(L==='fr'?' ':'.'));
    return L==='en'?'€'+s:s+' €';
  }
  function val(name){var i=box.querySelector('input[name="'+name+'"]:checked');return i?i.value:null;}
  function fmt(s,o){return s.replace(/\{(\w+)\}/g,function(_,k){return o[k];});}

  function motors(){
    var m=D.m[val('cfg_m')], cur=val('cfg_e')||'rec', opts=[['none',T.m_none,T.m_none_d]];
    if(m.loa<=5) opts.push(['15',T.m_15,T.m_15_d]);
    opts.push(['rec',fmt(T.m_rec,{cv:m.rec}),T.m_rec_d]);
    if(m.max>m.rec) opts.push(['max',fmt(T.m_max,{cv:m.max}),T.m_max_d]);
    if(!opts.some(function(o){return o[0]===cur;})) cur='rec';
    $('ssCfgMot').innerHTML=opts.map(function(o){
      return '<label><input type="radio" name="cfg_e" value="'+o[0]+'"'+(o[0]===cur?' checked':'')+'><span>'+o[1]+'<em>'+o[2]+'</em></span></label>';
    }).join('');
  }

  function state(){
    var s=val('cfg_m'), m=D.m[s], c=D.c[val('cfg_c')], e=val('cfg_e')||'rec';
    var cv=e==='none'?0:e==='15'?15:e==='max'?m.max:m.rec;
    var x=[].map.call(box.querySelectorAll('input[name="cfg_x"]:checked'),function(i){return i.value;});
    return {s:s,m:m,c:c,e:e,cv:cv,x:x};
  }

  function render(){
    var st=state(), m=st.m;
    $('ssCfgName').textContent=m.n;
    $('ssCfgPr').innerHTML=eur(m.p)+'<span class="vat">'+(D.vat||'+ impuestos')+'</span>';
    $('ssCfgVi').textContent='';
    $('ssCfgCol').textContent=st.c.n; $('ssCfgCn').textContent=st.c.n;
    $('ssCfgHull').setAttribute('fill',st.c.hex);
    $('ssCfgEng').style.display=st.cv?'':'none';
    var mo=st.cv?(st.e==='15'?T.m_15:fmt(T.m_rec,{cv:st.cv})):T.m_none;
    $('ssCfgMo').textContent=mo;
    var free=m.loa<=5&&st.cv<=15;
    $('ssCfgLic').textContent=free?T.lic_none:T.lic_ln;
    var q=[];
    if(st.cv) q.push(fmt(T.q_motor,{cv:st.cv}));
    if(st.x.indexOf('trailer')>-1) q.push(T.q_trailer);
    if(st.x.indexOf('reg')>-1) q.push(T.q_reg);
    q.push(T.q_ship);
    $('ssCfgQ').textContent=q.join(', ');
    var cfg=m.n+', '+st.c.n.toLowerCase()+', '+mo.toLowerCase()+(st.x.length?', '+q.slice(st.cv?1:0,-1).join(', '):'');
    $('ssCfgWa').href='https://wa.me/34633742973?text='+encodeURIComponent(fmt(T.wa,{cfg:cfg}));
    box._cfg={st:st,cfg:cfg};
  }

  box.addEventListener('change',function(ev){
    if(ev.target.name==='cfg_m') motors();
    render();
  });
  $('ssCfgGo').addEventListener('click',function(){
    var c=box._cfg; if(!c) return;
    var sel=$('ss_model'); if(sel){[].forEach.call(sel.options,function(o){if(o.text===c.st.m.n) sel.value=o.value||o.text;});}
    var need=$('ss_need'); if(need){need.value=(c.st.x.indexOf('trailer')>-1||c.st.x.indexOf('reg')>-1)?'llave':(c.st.cv?'motor':'barco');}
    var col=$('ss_color'); if(col){[].forEach.call(col.options,function(o){if(o.text===c.st.c.n) col.value=o.value||o.text;});}
    var msg=$('ss_msg'); if(msg&&!msg.value.trim()) msg.value=fmt(T.msg,{cfg:c.cfg});
    if(window.pmTrack) window.pmTrack('configurator_submit',{placement:'seastorm',boat:c.st.m.n});
  });
  $('ssCfgWa').addEventListener('click',function(){
    var c=box._cfg; if(c&&window.pmTrack) window.pmTrack('contact_intent',{method:'whatsapp',placement:'seastorm_config',boat:c.st.m.n});
  });
  motors(); render();
})();
