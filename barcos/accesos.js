(function(){
  var box=document.querySelector('.bquick'),f=document.querySelector('.bfilt');
  if(!box||!f)return;
  var chips=[].slice.call(box.querySelectorAll('button[data-k]'));
  function seg(k,v){return f.querySelector('.seg[data-f="'+k+'"] button[data-v="'+v+'"]');}
  function on(c){
    var k=c.dataset.k,v=c.dataset.v;
    if(k.charAt(0)==='#'){var s=f.querySelector(k);return !!s&&s.value===v;}
    var b=seg(k,v);return !!b&&b.getAttribute('aria-pressed')==='true';
  }
  function sync(){chips.forEach(function(c){c.setAttribute('aria-pressed',on(c)?'true':'false');});}
  chips.forEach(function(c){
    c.addEventListener('click',function(){
      var k=c.dataset.k,act=on(c),v=act?'all':c.dataset.v;
      if(k.charAt(0)==='#'){var s=f.querySelector(k);if(!s)return;s.value=v;s.dispatchEvent(new Event('change',{bubbles:true}));}
      else{var b=seg(k,v);if(b)b.click();}
      sync();
    });
  });
  f.addEventListener('change',sync);f.addEventListener('click',function(){setTimeout(sync,0);});
  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('.bclear'))setTimeout(sync,0);});
  window.addEventListener('popstate',function(){setTimeout(sync,0);});
  setTimeout(sync,0);
})();
