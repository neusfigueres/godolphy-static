/* Godolphy · activa subrayados, círculos, contadores y gráficos al entrar en pantalla */
(function(){
  var d=document;
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function countUp(el){
    var to=parseFloat(el.getAttribute('data-count'))||0,suf=el.getAttribute('data-suf')||'',t0=null,dur=1100;
    if(reduce){el.textContent=String(to).replace(/\B(?=(\d{3})+(?!\d))/g,'.')+suf;return;}
    function step(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/dur),v=Math.round(to*(1-Math.pow(1-p,3)));el.textContent=String(v).replace(/\B(?=(\d{3})+(?!\d))/g,'.')+suf;if(p<1)requestAnimationFrame(step);}
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
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){fire(e.target);io.unobserve(e.target);}});},{threshold:.2});
  els.forEach(function(el){io.observe(el);});
})();
(function(){
  var d=document,reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* Notificaciones de la cabecera en bucle: entra una arriba, bajan las demás y la última se va por detrás */
  [].forEach.call(d.querySelectorAll('.hero-notifs'),function(box){
    var orig=[].slice.call(box.querySelectorAll('.hn'));
    if(reduce||orig.length<2)return;
    var cards=orig.slice();
    if(orig.length<5)orig.forEach(function(c){var k=c.cloneNode(true);box.appendChild(k);cards.push(k);});
    var times=['ahora','2 min','5 min'],offs=[40,0,24],gap=14,q=cards.slice().reverse();
    box.classList.add('hn-loop');
    function vis(){return window.innerWidth<=860?2:3;}
    function wait(c){c.style.transform='translate(-30px,-26px) scale(.92)';c.style.opacity=0;c.style.zIndex=12;}
    q.forEach(function(c){c.classList.add('hn-noanim');wait(c);});
    function layout(){
      var v=vis(),m=v===2,h=0;
      cards.forEach(function(c){h=Math.max(h,c.offsetHeight);});
      var step=h+gap;box.style.height=(v*step-gap)+'px';
      q.forEach(function(c,i){
        if(i<v){
          c.style.transform='translate('+(m?0:-offs[i])+'px,'+(i*step)+'px)';c.style.opacity=1;c.style.zIndex=10-i;
          var t=c.querySelector('small');if(t)t.textContent=times[i];
        }else if(i===v){c.style.transform='translate(0,'+((v-1)*step+16)+'px) scale(.86)';c.style.opacity=0;c.style.zIndex=1;}
        else wait(c);
      });
    }
    var shown=0;
    function tick(){q.unshift(q.pop());layout();}
    layout();q.forEach(function(c){wait(c);});box.offsetHeight;
    q.forEach(function(c){c.classList.remove('hn-noanim');});
    /* al principio todas en espera: entran una a una */
    function fill(){if(shown<vis()){shown++;tick();setTimeout(fill,650);}else setInterval(function(){if(!d.hidden)tick();},2800);}
    setTimeout(fill,500);
    window.addEventListener('resize',function(){if(shown)layout();});
  });
})();
/* Vídeo de cabecera: sin movimiento si el sistema lo pide */
(function(){if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches){[].forEach.call(document.querySelectorAll('.hero-vid'),function(v){v.removeAttribute('autoplay');v.pause();});}})();
