/* Godolphy · activa subrayados, círculos, contadores y gráficos al entrar en pantalla */
(function(){
  var d=document;
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function countUp(el){
    var to=parseFloat(el.getAttribute('data-count'))||0,suf=el.getAttribute('data-suf')||'',t0=null,dur=1100;
    if(reduce){el.textContent=to+suf;return;}
    function step(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/dur),v=Math.round(to*(1-Math.pow(1-p,3)));el.textContent=v+suf;if(p<1)requestAnimationFrame(step);}
    requestAnimationFrame(step);
  }
  function fire(el){
    if(el.classList.contains('mk')||el.classList.contains('ci')) el.classList.add('on');
    if(el.classList.contains('gd-card')) el.classList.add('gd-on');
    el.querySelectorAll('.gd-bars span[data-h]').forEach(function(s){s.style.height=s.getAttribute('data-h')+'%';});
    el.querySelectorAll('.gd-meter i[data-w]').forEach(function(s){s.style.width=s.getAttribute('data-w')+'%';});
    el.querySelectorAll('[data-count]').forEach(countUp);
  }
  var els=[].slice.call(d.querySelectorAll('.mk,.ci,.gd-card'));
  if(!('IntersectionObserver' in window)){els.forEach(fire);return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){fire(e.target);io.unobserve(e.target);}});},{threshold:.35});
  els.forEach(function(el){io.observe(el);});
})();
