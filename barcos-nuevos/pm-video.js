/* Plata Marine · vídeos de YouTube con carga al pulsar (páginas de barcos nuevos).
   Hasta que se pulsa solo se muestra una foto propia; al pulsar se inserta youtube-nocookie.com. */
(function(){
  'use strict';
  document.querySelectorAll('.pm-video[data-yt]').forEach(function(box){
    var b=box.querySelector('button'); if(!b) return;
    b.addEventListener('click',function(){
      var id=box.getAttribute('data-yt'); if(!/^[\w-]{6,20}$/.test(id)) return;
      var f=document.createElement('iframe');
      f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0&playsinline=1';
      f.title=box.getAttribute('data-title')||'Vídeo';
      f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      f.allowFullscreen=true;
      f.referrerPolicy='strict-origin-when-cross-origin';
      box.replaceChild(f,b);
      if(window.pmTrack) window.pmTrack('video_start',{video_provider:'youtube',video_id:id,placement:box.getAttribute('data-place')||''});
    });
  });
})();
