(function(){
  var dds=document.querySelectorAll('.pmx-dd');
  function closeAll(except){for(var i=0;i<dds.length;i++){if(dds[i]!==except){dds[i].classList.remove('open');dds[i].firstElementChild.setAttribute('aria-expanded','false');}}}
  for(var i=0;i<dds.length;i++){(function(dd){
    var b=dd.firstElementChild;
    b.addEventListener('click',function(e){e.stopPropagation();var o=!dd.classList.contains('open');closeAll(dd);dd.classList.toggle('open',o);b.setAttribute('aria-expanded',o?'true':'false');});
  })(dds[i]);}
  document.addEventListener('click',function(e){if(!e.target.closest('.pmx-dd'))closeAll();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){closeAll();closeP();}});
  var btn=document.getElementById('pmxBtn'),p=document.getElementById('pmxPanel');
  function closeP(){if(!btn||!p)return;p.classList.remove('open');btn.setAttribute('aria-expanded','false');btn.setAttribute('aria-label',btn.getAttribute('data-open'));}
  if(btn&&p){
    btn.addEventListener('click',function(){var o=p.classList.toggle('open');btn.setAttribute('aria-expanded',o?'true':'false');btn.setAttribute('aria-label',btn.getAttribute(o?'data-close':'data-open'));});
    p.addEventListener('click',function(e){if(e.target.closest('a'))closeP();});
    window.addEventListener('resize',function(){if(window.innerWidth>=1120)closeP();});
  }
})();
