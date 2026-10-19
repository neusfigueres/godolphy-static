/* Godolphy · capa 2026-10 para sectores y funcionalidades */
(function(){
  var d=document;
  d.documentElement.classList.add('gx-js');

  // 1) Enmarcar capturas de producto
  d.querySelectorAll('img[src*="/images/producto/"]').forEach(function(img){
    if(img.closest('.gx-shot,.gx-phone,.gx-slider,.pv-frame,.frame')) return;
    var phone=/\/movil-/.test(img.getAttribute('src'));
    var w=d.createElement('div');
    w.className=phone?'gx-phone':'gx-shot';
    if(!phone){var dots=d.createElement('div');dots.className='gx-dots';dots.innerHTML='<i></i><i></i><i></i>';w.appendChild(dots);}
    img.parentNode.insertBefore(w,img);w.appendChild(img);
    img.removeAttribute('width');img.removeAttribute('height');
  });

  // 1b) Distintivo VERI*FACTU en el pie de página
  (function(){
    var f=d.querySelector('footer'); if(!f||f.querySelector('.gx-vf')) return;
    var a=d.createElement('a'); a.href='/ayuda/verifactu/'; a.className='gx-vf'; a.title='Facturación con VERI*FACTU';
    a.innerHTML='<img src="/assets/verifactu-white-sm.png" alt="VERI*FACTU" width="123" height="30" loading="lazy">';
    var row=f.querySelector('div[style*="justify-content:space-between"]');
    if(row){ row.insertBefore(a,row.children[1]||null); } else { (f.firstElementChild||f).appendChild(a); }
  })();

  // 2) Pasadores automáticos
  d.querySelectorAll('.gx-slider').forEach(function(sl){
    var btns=sl.querySelectorAll('.gx-slider-tabs button'),track=sl.querySelector('.gx-track'),n=btns.length,i=0,t=null,paused=false;
    function go(k,user){
      i=k;track.style.transform='translateX(-'+(k*100)+'%)';
      btns.forEach(function(b,j){b.classList.toggle('on',j===k);b.classList.remove('run');});
      void btns[k].offsetWidth;btns[k].classList.add('run');
      if(user&&btns[k].parentNode.scrollTo){btns[k].parentNode.scrollTo({left:btns[k].offsetLeft-16,behavior:'smooth'});}
      clearTimeout(t);if(!paused){t=setTimeout(function(){go((i+1)%n);},5000);}
    }
    btns.forEach(function(b,j){b.addEventListener('click',function(){go(j,true);});});
    sl.addEventListener('mouseenter',function(){paused=true;clearTimeout(t);});
    sl.addEventListener('mouseleave',function(){paused=false;go(i);});
    var x0=null,view=sl.querySelector('.gx-view');
    view.addEventListener('touchstart',function(e){x0=e.touches[0].clientX;},{passive:true});
    view.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>40)go((i+(dx<0?1:n-1))%n,true);x0=null;});
    go(0);
  });

  // 3) Aparición suave (con red de seguridad: nunca deja nada oculto)
  var els=[].slice.call(d.querySelectorAll('main section:not(.hero-bg) > div'));
  els.forEach(function(el){ if(el.getBoundingClientRect().top>window.innerHeight) el.classList.add('gx-rv'); });
  function check(){
    var lim=window.innerHeight*0.95;
    els=els.filter(function(el){
      if(!el.classList.contains('gx-rv')||el.classList.contains('gx-in')) return false;
      if(el.getBoundingClientRect().top<lim){ el.classList.add('gx-in'); return false; }
      return true;
    });
    if(!els.length){ window.removeEventListener('scroll',onScroll); }
  }
  var tick=false;
  function onScroll(){ if(tick) return; tick=true; requestAnimationFrame(function(){ tick=false; check(); }); }
  window.addEventListener('scroll',onScroll,{passive:true});
  window.addEventListener('resize',onScroll);
  check();
})();
