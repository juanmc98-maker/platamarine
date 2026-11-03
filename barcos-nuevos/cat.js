/* Plata Marine · páginas de categoría de /barcos-nuevos/: «Pedir presupuesto» de cada modelo rellena el formulario. */
(function(){
  'use strict';
  var r=document.getElementById('ct-res'); if(!r) return;
  r.addEventListener('click',function(ev){
    var a=ev.target.closest('a[data-q]'); if(!a) return;
    var mo=document.getElementById('nh_model'); if(mo) mo.value=a.getAttribute('data-q');
    if(window.pmTrack) window.pmTrack('quote_start',{boat:a.getAttribute('data-q'),placement:'nuevos_categoria'});
  });
})();
