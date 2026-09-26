(function(){
"use strict";
var main = document.getElementById('main');
if(!main) return;
var L = {
  es: {dlg:'Foto ampliada', close:'Cerrar', prev:'Foto anterior', next:'Foto siguiente', zoom:'Ampliar foto'},
  ca: {dlg:'Foto ampliada', close:'Tancar', prev:'Foto anterior', next:'Foto següent', zoom:'Ampliar la foto'},
  en: {dlg:'Enlarged photo', close:'Close', prev:'Previous photo', next:'Next photo', zoom:'Enlarge photo'}
}[(document.documentElement.lang || 'es').slice(0,2)] || null;
if(!L) L = {dlg:'Foto ampliada', close:'Cerrar', prev:'Foto anterior', next:'Foto siguiente', zoom:'Ampliar foto'};

var thumbsWrap = document.querySelector('.thumbs');
var thumbs = thumbsWrap ? Array.prototype.slice.call(thumbsWrap.querySelectorAll('img')) : [];
var images = thumbs.length ? thumbs.map(function(t){ return { src: t.currentSrc || t.src, alt: t.alt || main.alt, note: t.getAttribute('data-note') || '' }; }) : [{ src: main.src, alt: main.alt, note: main.getAttribute('data-note') || '' }];
// Aviso visible cuando una imagen es ilustrativa (render), no una foto real
var galNote = null;
if(main.parentNode && images.some(function(im){ return im.note; })){
  galNote = document.createElement('span');
  galNote.className = 'img-note';
  main.parentNode.insertBefore(galNote, main.nextSibling);
}
function showNote(el, txt){ if(!el) return; el.textContent = txt; el.style.display = txt ? '' : 'none'; }
var current = 0;
if(galNote){ var i0 = thumbs.findIndex ? thumbs.findIndex(function(t){ return t.className === 'on'; }) : 0; showNote(galNote, images[i0 > 0 ? i0 : 0].note); }

function setMain(i){
  current = (i + images.length) % images.length;
  main.src = images[current].src;
  showNote(galNote, images[current].note);
  thumbs.forEach(function(t, idx){ t.className = idx === current ? 'on' : ''; });
}

var openFromThumb = null;
thumbs.forEach(function(t, idx){
  t.addEventListener('click', function(){ if(openFromThumb) openFromThumb(idx); else setMain(idx); });
});

if(images.length){
  var lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.setAttribute('role', 'dialog');
  lb.setAttribute('aria-modal', 'true');
  lb.setAttribute('aria-label', L.dlg);
  lb.innerHTML =
    '<button type="button" class="lb-close" aria-label="' + L.close + '">&times;</button>' +
    (images.length > 1 ? '<button type="button" class="lb-prev" aria-label="' + L.prev + '">&#8249;</button>' : '') +
    '<img class="lb-img" alt="">' +
    '<span class="img-note lb-note"></span>' +
    (images.length > 1 ? '<button type="button" class="lb-next" aria-label="' + L.next + '">&#8250;</button>' : '') +
    (images.length > 1 ? '<p class="lb-count"></p>' : '');
  document.body.appendChild(lb);

  var lbImg = lb.querySelector('.lb-img');
  var lbCount = lb.querySelector('.lb-count');
  var lbPrev = lb.querySelector('.lb-prev');
  var lbNext = lb.querySelector('.lb-next');
  var lbClose = lb.querySelector('.lb-close');
  var lbNote = lb.querySelector('.lb-note');

  function updateLb(){
    lbImg.src = images[current].src;
    lbImg.alt = images[current].alt;
    showNote(lbNote, images[current].note);
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

  openFromThumb = openLb;
  main.classList.add('zoomable');
  main.setAttribute('role', 'button');
  main.setAttribute('tabindex', '0');
  main.setAttribute('aria-label', L.zoom);
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
