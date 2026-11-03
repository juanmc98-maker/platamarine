/* Plata Marine · /barcos-nuevos/ (ES/CA/EN/FR): buscador por tipo, eslora y presupuesto
   y formulario de presupuesto (hoja de leads, source 'barco_nuevo'). Datos en window.PM_HUB. */
(function(){
  'use strict';
  var D=window.PM_HUB; if(!D) return;
  var S=D.s, M=D.m, L=D.lang;
  var $=function(id){return document.getElementById(id);};
  var res=$('nh-res'), cnt=$('nh-count'), st=$('nh-t'), sl=$('nh-l'), sb=$('nh-b');
  var LEN=[[0,6],[6,8],[8,10],[10,12],[12,15],[15,999]];
  var BUD=[[0,50000],[50000,150000],[150000,300000],[300000,600000],[600000,1e12]];
  var loc={es:'es-ES',ca:'es-ES',en:'en-GB',fr:'fr-FR'}[L]||'es-ES';
  function fmt(n){ // separadores de miles fijos (Intl no agrupa 4 cifras en es-ES)
    var s=String(Math.round(n)), sep=L==='en'?',':L==='fr'?' ':'.';
    s=s.replace(/\B(?=(\d{3})+(?!\d))/g,sep);
    return L==='en'?'€'+s:s+' €';
  }
  function len(l){ return l==null?'':(L==='en'?l.toFixed(2):l.toFixed(2).replace('.',','))+' m'; }
  function esc(s){ return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  function inR(x,r,first){ return x!=null && (first? x<=r[1] : x>r[0] && x<=r[1]); }
  function match(m,t,li,bi){
    if(t){ if(t==='alu'){ if(!m.a) return false; } else if(m.t!==t) return false; }
    if(li!=='' && !inR(m.l,LEN[+li],+li===0)) return false;
    if(bi!=='' && !inR(m.p,BUD[+bi],+bi===0)) return false;
    return true;
  }
  function render(){
    if(!res) return;
    var t=st.value, li=sl.value, bi=sb.value;
    if(!t&&li===''&&bi===''){ res.innerHTML=''; cnt.textContent=''; cnt.hidden=true; return; }
    cnt.hidden=false;
    var list=M.filter(function(m){return match(m,t,li,bi);});
    list.sort(function(a,b){ var sa=/^SKIPPER/.test(a.n)?1:0, sb2=/^SKIPPER/.test(b.n)?1:0; if(sa!==sb2) return sb2-sa; return (b.p==null?-1:b.p)-(a.p==null?-1:a.p); });
    cnt.textContent=list.length+' '+(list.length===1?S.res1:S.resn);
    if(!list.length){ res.innerHTML='<p class="nh-none">'+esc(S.none)+'</p>'; return; }
    res.innerHTML=list.map(function(m){
      var pr=m.p==null?esc(S.consult):esc(S.frm)+' '+fmt(m.p)+' <span class="vat">'+esc(S.tax)+'</span>';
      var sub=[len(m.l),S.types[m.t]].filter(Boolean).join(' · ');
      return '<article class="nh-m"><a class="ph" href="'+m.u+'"><img src="'+m.i+'" alt="'+esc(m.n)+'" loading="lazy" decoding="async"></a><div>'+
        '<h3><a href="'+m.u+'">'+esc(m.n)+'</a></h3><p>'+esc(sub)+'</p><b>'+pr+'</b>'+
        '<span class="acts"><a href="'+m.u+'">'+esc(S.see)+' →</a><a href="#presupuesto" data-q="'+esc(m.n)+'" data-qt="'+m.t+'">'+esc(S.ask)+'</a></span></div></article>';
    }).join('');
  }
  function pressCards(){
    var t=st.value;
    Array.prototype.forEach.call(document.querySelectorAll('.nh-card'),function(c){ c.setAttribute('aria-pressed',c.getAttribute('data-t')===t?'true':'false'); });
  }
  if(res){
    [st,sl,sb].forEach(function(s){ s.addEventListener('change',function(){ pressCards(); render(); if(window.pmTrack) window.pmTrack('filter_used',{label:s.id+':'+s.value}); }); });
    Array.prototype.forEach.call(document.querySelectorAll('.nh-card'),function(c){
      c.addEventListener('click',function(){
        var t=c.getAttribute('data-t'); st.value=(st.value===t?'':t); pressCards(); render();
        cnt.scrollIntoView({behavior:'smooth',block:'start'});
        if(window.pmTrack) window.pmTrack('filter_used',{label:'card:'+t});
      });
    });
    $('nh-reset').addEventListener('click',function(){ st.value=sl.value=sb.value=''; pressCards(); render(); });
    var hm=/[#&]tipo=([a-z]+)/.exec(location.hash); if(hm && S.types[hm[1]]){ st.value=hm[1]; }
    pressCards(); render();
    res.addEventListener('click',function(ev){
      var a=ev.target.closest('a[data-q]'); if(!a) return;
      var mo=$('nh_model'), ty=$('nh_type');
      if(mo) mo.value=a.getAttribute('data-q');
      if(ty){ var lab=S.types[a.getAttribute('data-qt')]; Array.prototype.forEach.call(ty.options,function(o){ if(o.text===lab) ty.value=o.value||o.text; }); }
      if(window.pmTrack) window.pmTrack('quote_start',{boat:a.getAttribute('data-q'),placement:'nuevos_finder'});
    });
  }

  /* ---------- formulario ---------- */
  var f=$('nhForm'); if(!f) return;
  var LEADS_URL='https://script.google.com/macros/s/AKfycbwJtBkktakE0qgmu_b8oHOOopCDnG6BDpBjg2zBUsZKi8l3_OBEuez_OHWmE9j8qCBF/exec';
  var T={
    es:{consent:'Marca la casilla de privacidad para poder enviarlo.',req:'Completa este campo.',name:'Escribe tu nombre (solo letras).',email:'Revisa el email, por ejemplo nombre@email.com.',tel:'Revisa el teléfono: con prefijo internacional, por ejemplo 612 345 678 o +33 6 12 34 56 78.',sending:'Enviando…',ok:'Solicitud recibida. Te contesto en 24 horas laborables.',okBtn:'Enviado ✓',send:'Solicitar presupuesto',fail:'No he podido confirmar que el mensaje ha llegado. Tus datos siguen aquí: vuelve a intentarlo en unos minutos o escríbeme a juan@platamarine.com.'},
    ca:{consent:'Marca la casella de privacitat per poder enviar-ho.',req:'Completa aquest camp.',name:'Escriu el teu nom (només lletres).',email:'Revisa el correu, per exemple nom@correu.com.',tel:'Revisa el telèfon: amb prefix internacional, per exemple 612 345 678 o +33 6 12 34 56 78.',sending:'Enviant…',ok:'Sol·licitud rebuda. Et contesto en 24 hores laborables.',okBtn:'Enviat ✓',send:'Sol·licitar pressupost',fail:"No he pogut confirmar que el missatge ha arribat. Les teves dades segueixen aquí: torna-ho a provar d'aquí a uns minuts o escriu-me a juan@platamarine.com."},
    en:{consent:'Please tick the privacy box so I can receive it.',req:'Please fill in this field.',name:'Please enter your name (letters only).',email:'Please check the email, e.g. name@email.com.',tel:'Please check the phone number, with the international code, e.g. +44 7700 900123.',sending:'Sending…',ok:'Request received. I will reply within 24 working hours.',okBtn:'Sent ✓',send:'Request a quote',fail:'I could not confirm that your message arrived. Your details are still here: please try again in a few minutes or write to juan@platamarine.com.'},
    fr:{consent:'Cochez la case de confidentialité pour pouvoir l’envoyer.',req:'Veuillez remplir ce champ.',name:'Indiquez votre nom (lettres uniquement).',email:"Vérifiez l'e-mail, par exemple nom@email.fr.",tel:"Vérifiez le numéro, avec l'indicatif international, par exemple +33 6 12 34 56 78.",sending:'Envoi…',ok:'Demande reçue. Je vous réponds sous 24 heures ouvrées.',okBtn:'Envoyé ✓',send:'Demander un devis',fail:"Je n'ai pas pu confirmer que votre message est bien arrivé. Vos informations sont toujours là : réessayez dans quelques minutes ou écrivez à juan@platamarine.com."}
  }[L]||{};
  function v(id){var e=$(id);return e?e.value.trim():'';}
  var status=$('nh_status'), btn=$('nh_send'), sent=false, busy=false, started=false;
  function okName(s){ return s.length>=2 && /\p{L}/u.test(s) && !/[0-9@]|https?:|www\./i.test(s); }
  function okEmail(s){ return /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(s); }
  function okTel(s){ var d=s.replace(/[\s().-]/g,''); return /^[6-9]\d{8}$/.test(d) || /^(\+|00)\d{8,15}$/.test(d); }
  function check(){
    var rules=[['nh_name',okName,T.name],['nh_tel',okTel,T.tel],['nh_email',okEmail,T.email]], first=null;
    rules.forEach(function(r){ var e=$(r[0]); var bad=!r[1](e.value.trim()); e.setCustomValidity(bad?(e.value.trim()?r[2]:T.req):''); if(bad&&!first) first=e; });
    var c=$('nh_consent'); c.setCustomValidity(c.checked?'':T.consent); if(!c.checked&&!first) first=c;
    if(first){ first.reportValidity(); return false; }
    return true;
  }
  f.addEventListener('input',function(e){ if(e.target.setCustomValidity) e.target.setCustomValidity(''); if(!started){ started=true; if(window.pmTrack) window.pmTrack('quote_start',{placement:'nuevos_form'}); } });
  f.addEventListener('submit',function(e){
    e.preventDefault();
    if(sent||busy||!check()) return;
    if(!window.submitConfirmed){ status.hidden=false; status.textContent=T.fail; return; }
    var boat=(v('nh_model')||v('nh_type'));
    var detail='Barco nuevo | Tipo: '+v('nh_type')+(v('nh_model')?' | Modelo: '+v('nh_model'):'')+(v('nh_bud')?' | Presupuesto: '+v('nh_bud'):'')+(v('nh_zone')?' | Zona: '+v('nh_zone'):'')+' | Email: '+v('nh_email')+(v('nh_msg')?' | Mensaje: '+v('nh_msg'):'');
    var payload={source:'barco_nuevo',barco:'Nuevo: '+boat,nombre:v('nh_name'),telefono:v('nh_tel'),email:v('nh_email'),detail:detail,lang:L,page:location.pathname,ua:navigator.userAgent.slice(0,120),consent:true,consent_v:'2026-10',consent_at:new Date().toISOString()};
    busy=true; btn.disabled=true; btn.textContent=T.sending; status.hidden=false; status.textContent=T.sending;
    window.submitConfirmed(LEADS_URL,payload,'json',f).then(function(){
      sent=true; busy=false; status.textContent=T.ok; btn.textContent=T.okBtn;
      if(window.pmTrack) window.pmTrack('generate_lead',{form_id:'barco_nuevo',contact_purpose:'quote',placement:'barcos_nuevos',boat:'Nuevo: '+boat});
    }).catch(function(){
      busy=false; status.textContent=T.fail; btn.disabled=false; btn.textContent=T.send;
      if(window.pmTrack) window.pmTrack('contact_form_error',{form_id:'barco_nuevo'});
    });
  });
})();
