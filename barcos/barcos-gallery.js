(function(){
"use strict";
var main = document.getElementById('main');
if(!main) return;

var thumbsWrap = document.querySelector('.thumbs');
var thumbs = thumbsWrap ? Array.prototype.slice.call(thumbsWrap.querySelectorAll('img')) : [];
var images = thumbs.length ? thumbs.map(function(t){ return { src: t.currentSrc || t.src, alt: t.alt || main.alt }; }) : [{ src: main.src, alt: main.alt }];
var current = 0;

function setMain(i){
  current = (i + images.length) % images.length;
  main.src = images[current].src;
  thumbs.forEach(function(t, idx){ t.className = idx === current ? 'on' : ''; });
}

thumbs.forEach(function(t, idx){
  t.addEventListener('click', function(){ setMain(idx); });
});

if(images.length){
  var lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.setAttribute('role', 'dialog');
  lb.setAttribute('aria-modal', 'true');
  lb.setAttribute('aria-label', 'Foto ampliada');
  lb.innerHTML =
    '<button type="button" class="lb-close" aria-label="Cerrar">&times;</button>' +
    (images.length > 1 ? '<button type="button" class="lb-prev" aria-label="Foto anterior">&#8249;</button>' : '') +
    '<img class="lb-img" alt="">' +
    (images.length > 1 ? '<button type="button" class="lb-next" aria-label="Foto siguiente">&#8250;</button>' : '') +
    (images.length > 1 ? '<p class="lb-count"></p>' : '');
  document.body.appendChild(lb);

  var lbImg = lb.querySelector('.lb-img');
  var lbCount = lb.querySelector('.lb-count');
  var lbPrev = lb.querySelector('.lb-prev');
  var lbNext = lb.querySelector('.lb-next');
  var lbClose = lb.querySelector('.lb-close');

  function updateLb(){
    lbImg.src = images[current].src;
    lbImg.alt = images[current].alt;
    if(lbCount) lbCount.textContent = (current + 1) + ' / ' + images.length;
  }

  function openLb(i){
    setMain(i);
    updateLb();
    lb.classList.add('open');
    document.documentElement.style.overflow = 'hidden';
    document.body.style.overflow = 'hidden';
  }

  function closeLb(){
    lb.classList.remove('open');
    document.documentElement.style.overflow = '';
    document.body.style.overflow = '';
  }

  function step(d){
    setMain(current + d);
    updateLb();
  }

  main.classList.add('zoomable');
  main.setAttribute('role', 'button');
  main.setAttribute('tabindex', '0');
  main.setAttribute('aria-label', 'Ampliar foto');
  main.addEventListener('click', function(){ openLb(current); });
  main.addEventListener('keydown', function(e){
    if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); openLb(current); }
  });

  lbClose.addEventListener('click', closeLb);
  if(lbPrev) lbPrev.addEventListener('click', function(){ step(-1); });
  if(lbNext) lbNext.addEventListener('click', function(){ step(1); });
  lb.addEventListener('click', function(e){ if(e.target === lb) closeLb(); });

  document.addEventListener('keydown', function(e){
    if(!lb.classList.contains('open')) return;
    if(e.key === 'Escape') closeLb();
    else if(e.key === 'ArrowLeft') step(-1);
    else if(e.key === 'ArrowRight') step(1);
  });

  var touchX = null;
  lb.addEventListener('touchstart', function(e){ touchX = e.changedTouches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', function(e){
    if(touchX === null) return;
    var dx = e.changedTouches[0].clientX - touchX;
    if(Math.abs(dx) > 40) step(dx > 0 ? -1 : 1);
    touchX = null;
  }, { passive: true });
}
})();
