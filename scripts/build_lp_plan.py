#!/usr/bin/env python3
"""Landing /lp/plan-financiero-2027/ (anuncios Meta, tráfico frío).

Vende solo el plan financiero del SaaS. Una sola acción: crear el plan →
https://app.godolphy.com/auth/sign-up?entrada=plan (con las UTMs de la visita,
que añade /assets/tracking.js). Los CTA llevan data-gd-direct para que el modal
rápido de alta NO los intercepte (deben llegar a la app con ?entrada=plan).

Capturas: si falta un archivo, se ve un recuadro con su nombre y tamaño; en cuanto
se sube a /lp/plan-financiero-2027/ con ese nombre, aparece solo.

Uso: python3 scripts/build_lp_plan.py
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build_lp import CSS, head_common  # noqa: E402

SLUG = 'plan-financiero-2027'
OUT = f'lp/{SLUG}/index.html'
IMG = f'/lp/{SLUG}/'
CTA_URL = 'https://app.godolphy.com/auth/sign-up?entrada=plan'
CTA_TXT = 'Crear mi plan 2027 gratis →'

e = html.escape


def cta(pos, cls='btn btn--v'):
    return f'<a class="{cls}" href="{CTA_URL}" data-cta="{pos}" data-gd-direct>{e(CTA_TXT)}</a>'


def shot(file, w, h, alt, label, cls=''):
    """Captura real; si el archivo aún no existe, recuadro con nombre y medida."""
    return (f'<div class="ph-wrap {cls}" data-ph="{e(file)} · {w}×{h} px · {e(label)}">'
            f'<img src="{IMG}{file}" alt="{e(alt)}" width="{w}" height="{h}" '
            f'loading="eager" onerror="this.parentNode.classList.add(\'ph\');this.remove();"></div>')


PAINS = [
    ('Cada año, igual que el anterior.', 'Facturas parecido y no sabes qué tocar para crecer.'),
    ('¿Estoy ganando de verdad?', 'El dinero de casa y el del salón van juntos, y a final de mes no sabes cuánto es tuyo.'),
    ('Diciembre a tope, agosto cerrado.', 'La facturación sube y baja, pero el alquiler y los sueldos llegan los doce meses.'),
    ('Sin colchón.', 'Un mes flojo o un imprevisto y ya vas tarde.'),
    ('Agenda llena no es dinero.', 'Pensar que si la agenda está llena, el salón va bien.'),
]

STEPS = [
    ('Te das de alta con tu email.', None),
    ('Pones tus números de partida.', 'Si ya usas Godolphy, partimos de tus citas y gastos reales.'),
    ('Eliges cuánto quieres crecer', 'y tienes tu plan mes a mes, editable cuando quieras.'),
]

AFTER = [
    ('📊', 'Cada mes ves lo real frente a lo planificado.'),
    ('🔔', 'Si un mes vas por debajo, la IA te avisa a tiempo.'),
    ('🔄', 'Un Excel lo descargas y te olvidas. Aquí el plan se actualiza solo con tu día a día.'),
]

FAQ = [
    ('¿Necesito saber de finanzas?', 'No. Pones tus números y Godolphy hace los cálculos.'),
    ('¿Sirve si no tengo historial?', 'Sí, empiezas con tus números de partida.'),
    ('¿Lo puedo cambiar?', 'Sí, cada mes es editable.'),
    ('¿Cuánto cuesta después?', 'Los primeros 30 días son gratis. Después, el plan financiero está incluido en el plan Pro, desde 45 €/mes. Si no eliges plan, no pagas nada.'),
]

VIDEO = ('<div class="vid"><video controls playsinline preload="none" data-vid="tutorial-plan" '
         'poster="/lp/plan-financiero-2027/tutorial-poster.webp" width="1280" height="720">'
         '<source src="/lp/plan-financiero-2027/tutorial-plan-financiero.mp4" type="video/mp4"></video>'
         '<p>Así se crea el plan, paso a paso (2 min).</p></div>')

VIDEO_JS = ("document.querySelectorAll('video[data-vid]').forEach(function(v){v.addEventListener('play',function(){"
            "try{if(window.posthog)posthog.capture('lp_video_play',{lp:document.body.getAttribute('data-lp'),video:v.getAttribute('data-vid')});}catch(_){}"
            "},{once:true});});")

EXTRA_CSS = r'''
.top{position:absolute;}
.hero2{background:var(--soft);padding:84px 0 56px;overflow:hidden;}
.hero2 .grid{display:grid;grid-template-columns:1.05fr .95fr;gap:40px;align-items:center;}
.hero2 .y{font-family:'Gabarito',sans-serif;font-size:clamp(84px,13vw,168px);line-height:.9;font-weight:800;letter-spacing:-.04em;margin:0 0 10px;}
.hero2 h1{font-family:'Gabarito',sans-serif;font-size:clamp(30px,4.2vw,48px);line-height:1.08;letter-spacing:-.02em;margin:0 0 14px;color:var(--ink);}
.hero2 .sub{font-size:clamp(16.5px,2vw,19px);line-height:1.55;color:var(--muted);margin:0 0 24px;max-width:540px;}
.hero2 .sub b{color:var(--v);}
.micro{font-size:13.5px;color:var(--muted);margin:10px 0 0;}
.devices{position:relative;padding:0 0 30px 0;}
.lap{background:#0d0627;border-radius:16px 16px 0 0;padding:10px 10px 0;box-shadow:0 30px 70px rgba(40,10,120,.22);}
.lap .ph-wrap{border-radius:8px 8px 0 0;overflow:hidden;aspect-ratio:16/10;background:#fff;}
.lap .ph{justify-content:flex-start;padding-right:36%;}
.lap .ph-wrap img{width:100%;height:100%;object-fit:cover;object-position:top;}
.lap-base{height:14px;background:linear-gradient(#cfcbe0,#a9a3c4);border-radius:0 0 14px 14px;margin:0 -4%;}
.mob2{position:absolute;right:-6px;bottom:0;width:34%;max-width:190px;border:7px solid #0d0627;border-radius:26px;overflow:hidden;background:#fff;box-shadow:0 24px 50px rgba(20,5,60,.35);aspect-ratio:9/17;}
.mob2 .ph-wrap{width:100%;height:100%;}.mob2 img{width:100%;height:auto;}
.ph{position:relative;display:flex!important;align-items:center;justify-content:center;background:repeating-linear-gradient(45deg,#f3efff,#f3efff 10px,#ebe4ff 10px,#ebe4ff 20px)!important;border:2px dashed #b9a6ff;color:#4b2bb8;min-height:140px;}
.ph::after{content:attr(data-ph);font:700 12.5px/1.4 'Plus Jakarta Sans',sans-serif;text-align:center;padding:10px;}
.pains2{list-style:none;padding:0;margin:0 0 22px;display:grid;grid-template-columns:1fr 1fr;gap:14px;}
.pains2 li{background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px 20px;font-size:16px;line-height:1.5;color:var(--muted);}
.pains2 b{display:block;color:var(--ink);font-size:17px;margin-bottom:4px;}
.close{font-family:'Gabarito',sans-serif;font-size:clamp(22px,2.8vw,30px);line-height:1.2;margin:8px 0 0;}
.big-co{max-width:760px;text-align:center;}
.pains2 li:last-child:nth-child(odd){grid-column:1/-1;}
.why{display:grid;grid-template-columns:1fr 1fr 1.2fr;gap:16px;margin-top:34px;max-width:1000px;}
.stat,.quote{background:#fff;border:1px solid var(--line);border-radius:20px;padding:22px;margin:0;}
.stat b{display:block;font-family:'Gabarito',sans-serif;font-size:44px;line-height:1;margin-bottom:8px;}
.stat p{margin:0 0 10px;font-size:16px;line-height:1.45;color:var(--ink);}
.stat small,.quote cite{font-size:12.5px;color:var(--muted);font-style:normal;}
.quote{font-family:'Gabarito',sans-serif;font-size:21px;line-height:1.3;color:var(--ink);display:flex;flex-direction:column;justify-content:center;gap:10px;}
@media(max-width:860px){.why{grid-template-columns:1fr 1fr;}.quote{grid-column:1/-1;font-size:19px;}.stat{padding:16px;}.stat b{font-size:34px;}.stat p{font-size:14.5px;}}
.big-co p{font-size:18px;line-height:1.6;color:var(--muted);margin:0;}
.reel{width:min(280px,72vw);margin:0 auto;border-radius:24px;overflow:hidden;box-shadow:0 24px 60px rgba(40,10,120,.2);background:#0c0628;aspect-ratio:9/16;}
.reel video{width:100%;height:100%;display:block;object-fit:cover;}
.steps2{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-bottom:28px;}
.step2{background:var(--soft);border:1px solid var(--line);border-radius:22px;padding:22px;display:flex;flex-direction:column;gap:14px;}
.step2 .n{font-family:'Gabarito',sans-serif;font-size:40px;line-height:1;}
.step2 h3{font-family:'Gabarito',sans-serif;font-size:20px;line-height:1.25;margin:0;}
.step2 p{margin:0;color:var(--muted);font-size:15.5px;line-height:1.5;}
.step2 .ph-wrap{border-radius:14px;overflow:hidden;margin-top:auto;}
.step2 .ph-wrap img{width:100%;}
.after{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center;}
.after ul{list-style:none;padding:0;margin:0;display:grid;gap:12px;}
.after li{display:flex;gap:12px;align-items:flex-start;background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px 18px;font-size:16.5px;line-height:1.5;}
.after li i{font-style:normal;font-size:22px;line-height:1.2;}
.after .shots{display:grid;grid-template-columns:1fr;gap:14px;align-items:start;}
.vid{max-width:920px;margin:0 0 30px;}
.vid video{width:100%;aspect-ratio:16/9;display:block;border-radius:18px;background:#0c0628;box-shadow:0 24px 60px rgba(40,10,120,.2);}
.vid p{margin:10px 0 0;font-size:14px;color:var(--muted);}
.after .ph-wrap{border-radius:16px;overflow:hidden;box-shadow:0 18px 40px rgba(40,10,120,.14);background:#fff;}
.neus2{display:grid;grid-template-columns:.7fr 1.3fr;gap:40px;align-items:center;}
.neus2 img{border-radius:24px;width:100%;max-width:360px;}
.neus2 p{font-size:18px;line-height:1.65;color:rgba(2,2,30,.8);margin:0 0 12px;}
.neus2 .sig{font-family:'Gabarito',sans-serif;font-weight:700;color:var(--v);margin:6px 0 0;}
.final .btn{background:var(--y);color:var(--ink);}
.foot{padding:24px 0 110px;}
@media(max-width:860px){
  .hero2{padding:66px 0 40px;}
  .hero2 .grid{grid-template-columns:1fr;gap:26px;}
  .hero2 .y{font-size:84px;margin:0 0 6px;}
  .hero2 h1{font-size:27px;margin:0 0 10px;}
  .hero2 .sub{font-size:15.5px;line-height:1.45;margin:0 0 16px;}
  .hero2 .btn{width:100%;padding:15px 20px;font-size:16.5px;}
  .micro{text-align:center;}
  .pains2,.steps2,.after,.after .shots,.big-co,.neus2{grid-template-columns:1fr;}
  .neus2 img{max-width:260px;}
  .after .shots{grid-template-columns:1fr;}
}
'''


def page():
    hc = head_common()
    pains = ''.join(f'<li><b>{e(t)}</b>{e(x)}</li>' for t, x in PAINS)
    step_shots = [
        '',
        shot('paso-numeros.webp', 1270, 650, 'Paso 1 del plan: ¿tienes la facturación del año pasado?', 'pantalla «números de partida»'),
        shot('paso-crecer.webp', 1360, 760, 'Paso 3 del plan: cuánto quieres crecer en 2027', 'pantalla del % de crecimiento'),
    ]
    steps = ''.join(
        f'<div class="step2"><span class="n grad">0{i}</span><h3>{e(t)}</h3>'
        + (f'<p>{e(x)}</p>' if x else '') + step_shots[i - 1] + '</div>'
        for i, (t, x) in enumerate(STEPS, 1))
    after = ''.join(f'<li><i>{ic}</i><span>{e(t)}</span></li>' for ic, t in AFTER)
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    title = 'Crea el plan financiero de tu salón para 2027 | Godolphy'
    desc = 'Mete tus números y Godolphy te monta el plan financiero de tu salón para 2027, mes a mes, con tus datos reales. Gratis 30 días.'
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
{hc.split('<head>', 1)[1].strip()}
<meta charset="UTF-8">
<title>{e(title)}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://www.godolphy.com/lp/{SLUG}/">
<meta property="og:title" content="Crea el plan financiero de tu salón para 2027">
<meta property="og:description" content="{e(desc)}">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}{EXTRA_CSS}</style>
</head>
<body data-lp="{SLUG}">
<header class="top"><div class="w"><img src="/wp-images/logo-gradient.png" alt="Godolphy" style="height:30px;width:auto;"></div></header>

<main>
<section class="hero2" id="hero">
  <div class="w grid">
    <div>
      <div class="y grad" aria-hidden="true">2027</div>
      <h1>Mueve el culo y crea el plan financiero de tu salón para 2027</h1>
      <p class="sub"><span id="cd" hidden>Quedan <b id="cd-n"></b> para enero. </span>Mete tus números y Godolphy te monta el plan mes a mes, con tus datos reales.</p>
      {cta('hero')}
      <p class="micro">Gratis 30 días.</p>
    </div>
    <div class="devices">
      <div class="lap">{shot('plan-portatil.webp', 1600, 1000, 'Plan financiero 2027 en el panel de Godolphy (ordenador)', 'captura del plan en el ordenador')}</div>
      <div class="lap-base"></div>
      <div class="mob2"><div class="ph-wrap" data-ph="plan-movil.webp · 780×1688 px"><img src="/lp/salones/plan-mes.webp" alt="Plan financiero del mes en el móvil: plan, real y diferencia" width="744" height="1164" loading="eager"></div></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="w">
    <h2 class="h2">Trabajas mucho. <span class="grad">Pero no sabes si avanzas.</span></h2>
    <ul class="pains2">{pains}</ul>
    <p class="close">No es que trabajes poco. <span class="grad">Es que trabajas sin plan.</span></p>
  </div>
</section>

<section class="sec sec--soft">
  <div class="w big-co">
    <h2 class="h2">No es cosa de <span class="grad">grandes empresas</span></h2>
    <p>Las grandes marcas no improvisan: se marcan un objetivo y lo miran cada mes. Que tu salón sea pequeño no es excusa. Es justo por eso que lo necesitas.</p>
  </div>
  <div class="w why">
    <div class="stat"><b class="grad">16 %</b><p>más probabilidades de que el negocio salga adelante si escribes un plan.</p><small>Harvard Business Review, 2017</small></div>
    <div class="stat"><b class="grad">4 de cada 10</b><p>pymes en España no planifican sus finanzas.</p><small>Fundación IE, 2025</small></div>
    <blockquote class="quote">«Los planes no sirven de nada, pero planificar lo es todo.»<cite>Dwight D. Eisenhower</cite></blockquote>
  </div>
</section>

<section class="sec">
  <div class="w">
    <h2 class="h2">Cómo funciona</h2>
    {VIDEO}
    <div class="steps2">{steps}</div>
    {cta('steps')}
  </div>
</section>

<section class="sec sec--soft">
  <div class="w after">
    <div>
      <h2 class="h2">Y después, <span class="grad">no se queda en un cajón</span></h2>
      <ul>{after}</ul>
    </div>
    <div class="shots">
      {shot('real-vs-plan.webp', 1420, 540, 'Gráfico del plan 2027: beneficio previsto y real de cada mes', 'gráfico real vs plan')}
      {shot('objetivos-mes.webp', 720, 680, 'Objetivos de un mes del plan, editables', 'objetivos del mes')}
    </div>
  </div>
</section>

<section class="sec" id="neus">
  <div class="w neus2">
    <img src="/lp/salones/neus.webp" alt="Neus, fundadora de Godolphy" width="798" height="997" loading="lazy">
    <div>
      <h2 class="h2">Quién está detrás</h2>
      <p>Soy Neus. He trabajado unos 15 años en multinacionales y monté mi propio salón con una socia, donde yo llevaba la parte de negocio.</p>
      <p>Godolphy es el consultor financiero que mi salón nunca tuvo.</p>
      <p class="sig">Neus, fundadora de Godolphy</p>
    </div>
  </div>
</section>

<section class="sec sec--soft">
  <div class="w">
    <h2 class="h2">Preguntas</h2>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="sec">
  <div class="w">
    <div class="final">
      <h2 style="margin-bottom:22px;">Enero llega igual. Que te pille con un plan.</h2>
      {cta('final', 'btn')}
    </div>
  </div>
</section>
</main>

<footer class="foot"><div class="w">© 2026 Godolphy · <a href="/politica-de-privacidad/">Privacidad</a><a href="/politica-de-cookies/">Cookies</a><a href="/aviso-legal/">Aviso legal</a></div></footer>

<div class="sticky" id="sticky">{cta('sticky', 'btn btn--v')}</div>

<script>
(function(){{
  // Cuenta atrás hasta el 1/1/2027 (hora local). Desde enero, la frase desaparece.
  var d=Math.ceil((new Date(2027,0,1)-new Date())/864e5);
  if(d>0){{document.getElementById('cd-n').textContent=d===1?'1 día':d+' días';
    var c=document.getElementById('cd');c.hidden=false;if(d===1)c.firstChild.textContent='Queda ';}}
  // Botón fijo en móvil cuando el botón del hero ya no se ve
  var st=document.getElementById('sticky'),hero=document.getElementById('hero'),lp=document.body.getAttribute('data-lp');
  function upd(){{var past=hero.getBoundingClientRect().bottom<0,cookie=document.getElementById('gd-cookies');st.classList.toggle('on',past&&!cookie);}}
  window.addEventListener('scroll',upd,{{passive:true}});setInterval(upd,1500);upd();
  {VIDEO_JS}
  document.addEventListener('click',function(e){{var a=e.target.closest&&e.target.closest('[data-cta]');if(!a)return;
    /* lp_cta_click lo envía /assets/signup-modal.js */
    try{{if(window.fbq)fbq('track','InitiateCheckout',{{content_name:lp}});}}catch(_){{}}
  }});
}})();
</script>
</body>
</html>
'''


if __name__ == '__main__':
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(page())
    print('ok', OUT)
