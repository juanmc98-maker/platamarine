/* Plata Marine · vídeos de SKIPPER con carga al pulsar.
   Hasta que se pulsa el botón solo se muestra una foto propia: no se hace ninguna petición a YouTube.
   Al pulsar se inserta el reproductor de youtube-nocookie.com con reproducción automática. */
(function(){
  'use strict';
  document.querySelectorAll('.sk-video[data-yt]').forEach(function(box){
    var b=box.querySelector('button'); if(!b) return;
    b.addEventListener('click',function(){
      var id=box.getAttribute('data-yt'); if(!/^[\w-]{6,20}$/.test(id)) return;
      var f=document.createElement('iframe');
      f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0&playsinline=1';
      f.title=box.getAttribute('data-title')||'SKIPPER';
      f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      f.allowFullscreen=true;
      f.referrerPolicy='strict-origin-when-cross-origin';
      box.replaceChild(f,b);
      if(window.pmTrack) window.pmTrack('video_start',{video_provider:'youtube',video_id:id,placement:'skipper'});
    });
  });
})();
