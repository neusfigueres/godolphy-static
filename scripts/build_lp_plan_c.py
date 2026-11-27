#!/usr/bin/env python3
"""Landing /lp/plan-financiero-2027-historia/ — versión C (storytelling) de la del plan financiero.

Estructura del vídeo «storytelling para landings» (Talia Wolf / Get Uplift), viaje del héroe con PAS y antes-después:
la protagonista es la propietaria del salón, todo en segunda persona («tú»), con momentos concretos del año.
  1. La escena (hero): su situación de ahora, con el plan como promesa.
  2. Momentos concretos: su año, de enero a diciembre (el «zoom» del vídeo).
  3. El problema y su agitación (PAS): no es que trabaje poco, es que no tiene mapa.
  4. La mentora: Neus, que estuvo ahí (corto: la historia es de la clienta, no de la empresa).
  5. El puente (antes → después): qué cambia con un plan.
  6. El camino: 3 pasos + vídeo.
  7. La transformación: diciembre de 2027 + testimonios (que hacen el trabajo pesado) + datos.
  8. FAQ, producto y cierre.
Mismo contenido y capturas que las versiones A y B. Sin «gratis para siempre» (freemium aún no publicado).
Uso: python3 scripts/build_lp_plan_c.py
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build_lp import CSS, head_common  # noqa: E402
from build_lp_plan import (EXTRA_CSS as A_CSS, CTA_URL, VIDEO, VIDEO_JS, TST_CSS, testimonials_html, WHY_CSS, why_cards,  # noqa: E402
                           ICON_CSS, icon, PRODUCT_CSS, product_html, HAND_CSS, circ, mark)
from build_lp_plan_b import B_CSS  # noqa: E402

SLUG = 'plan-financiero-2027-historia'
OUT = f'lp/{SLUG}/index.html'
IMG = '/lp/plan-financiero-2027/'
CTA_TXT = 'Crear mi plan 2027 gratis →'

e = html.escape


def cta(pos, cls='btn btn--v', txt=CTA_TXT):
    return f'<a class="{cls}" href="{CTA_URL}" data-cta="{pos}" data-gd-direct>{e(txt)}</a>'


def shot(file, w, h, alt, label, cls='', eager=False):
    return (f'<div class="ph-wrap {cls}" data-ph="{e(file)} · {w}×{h} px · {e(label)}">'
            f'<img src="{IMG}{file}" alt="{e(alt)}" width="{w}" height="{h}" '
            f'loading="{"eager" if eager else "lazy"}" onerror="this.parentNode.classList.add(\'ph\');this.remove();"></div>')


FUD = ['30 días gratis', 'Sin tarjeta', 'Sin saber de finanzas']

YEAR = [
    ('Enero', 'Te dices que este año será distinto: subir precios, llenar los martes, guardar un colchón.'),
    ('Marzo', 'La agenda va llena. Vas tan a tope que los números los dejas «para cuando tenga un rato».'),
    ('Agosto', 'Cierras dos semanas. El alquiler y los sueldos llegan igual.'),
    ('Octubre', 'Llega una factura que no esperabas y tiras de la cuenta de casa.'),
    ('Diciembre', 'Haces cuentas en una libreta y la conclusión es la de cada año: «más o menos como el anterior».'),
]

AGITATE = [
    ('Agenda llena no es dinero.', 'Puedes tener la semana completa y aun así no saber cuánto te queda a ti.'),
    ('El dinero de casa y el del salón van juntos.', 'A final de mes no sabes qué parte es tuya.'),
    ('Los meses flojos te pillan siempre por sorpresa.', 'Y sin colchón, un imprevisto ya te hace ir tarde.'),
    ('Creces «si sale».', 'Sin un objetivo, no sabes qué tocar para que el año que viene sea mejor.'),
]

CONTRAST = [
    ('Cada año, igual que el anterior.', 'Un objetivo claro para 2027, el que tú elijas.'),
    ('Te enteras en diciembre de que el año ha ido flojo.', 'Cada mes ves si vas por delante o por detrás.'),
    ('Creces «si sale».', 'Sabes cuánto tienes que facturar cada mes para llegar.'),
    ('Los números, en una libreta o en un Excel olvidado.', 'El plan se actualiza solo con tu día a día en Godolphy.'),
]

STEPS = [
    ('Pones tus números.', 'Tu facturación del año pasado (subes un documento o la escribes) y tus gastos. Si ya usas Godolphy, partimos de tus citas y gastos reales.'),
    ('Eliges cuánto quieres crecer.', 'Mantenerte, +10 %, +25 % o el porcentaje que tú quieras. Godolphy te monta el plan mes a mes.'),
    ('Haces el seguimiento mes a mes.', 'Ves lo real frente a lo planificado y, si te desvías, la IA te avisa a tiempo.'),
]

FAQ = [
    ('¿Necesito saber de finanzas?', 'No. Pones tus números y Godolphy hace los cálculos.'),
    ('¿Sirve si no tengo historial?', 'Sí, empiezas con tus números de partida.'),
    ('¿Lo puedo cambiar?', 'Sí, cada mes es editable.'),
    ('¿Necesito tarjeta?', 'No. Te das de alta solo con tu email.'),
    ('¿Cuánto cuesta después?', 'Los primeros 30 días son gratis. Después, el plan financiero está incluido en el plan Pro, desde 45 €/mes. Si no eliges plan, no pagas nada.'),
]

C_CSS = r'''
.story{font-size:19px;line-height:1.65;color:var(--ink);max-width:760px;}
.story p{margin:0 0 14px;}
.year{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-top:30px;position:relative;}
.year::before{content:"";position:absolute;left:0;right:0;top:21px;height:2px;background:linear-gradient(90deg,var(--line),var(--v));}
.ym{position:relative;opacity:0;transform:translateY(14px);transition:opacity .5s,transform .5s;}
.ym.on{opacity:1;transform:none;}
.ym b{position:relative;display:inline-block;background:#fff;border:2px solid var(--v);color:var(--v);font:800 13px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.04em;text-transform:uppercase;padding:12px 14px;border-radius:999px;}
.ym:last-child b{background:var(--v);color:#fff;}
.ym p{margin:14px 0 0;font-size:16px;line-height:1.5;color:var(--ink);}
.agit{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:26px;}
.agit div{background:#fff;border:1px solid var(--line);border-left:4px solid var(--v);border-radius:16px;padding:18px 20px;}
.agit b{display:block;font-family:'Gabarito',sans-serif;font-size:20px;margin-bottom:6px;}
.agit p{margin:0;font-size:16px;line-height:1.5;color:var(--muted);}
.turn{margin:30px 0 0;font-family:'Gabarito',sans-serif;font-size:clamp(24px,3vw,32px);line-height:1.25;color:var(--ink);max-width:820px;}
.bridge{display:grid;grid-template-columns:1fr auto 1fr;gap:18px;align-items:stretch;}
.bridge .vs{display:block;}
.bridge .arrow{align-self:center;display:flex;flex-direction:column;align-items:center;gap:8px;font-weight:800;color:var(--v);font-size:14px;text-align:center;max-width:150px;}
.bridge .arrow span{font-size:34px;line-height:1;}
.elix{background:linear-gradient(160deg,#9B4FE8 0%,#631cff 70%);color:#fff;border-radius:28px;padding:40px;display:grid;grid-template-columns:1.1fr .9fr;gap:36px;align-items:center;}
.elix h2{color:#fff;margin:0 0 14px;}
.elix p{font-size:18px;line-height:1.6;margin:0 0 12px;color:rgba(255,255,255,.92);}
.elix .ph-wrap{border-radius:18px;overflow:hidden;background:#fff;box-shadow:0 20px 50px rgba(0,0,0,.25);}
.elix .ph-wrap img{width:100%;height:auto;display:block;}
@media(max-width:900px){
  .year{grid-template-columns:1fr;gap:18px;}.year::before{left:21px;right:auto;top:0;bottom:0;width:2px;height:auto;background:linear-gradient(180deg,var(--line),var(--v));}
  .ym{padding-left:0;}.agit{grid-template-columns:1fr;}
  .bridge{grid-template-columns:1fr;}.bridge .arrow{max-width:none;flex-direction:row;}.bridge .arrow span{transform:rotate(90deg);}
  .elix{grid-template-columns:1fr;padding:26px;}
  .story{font-size:17px;}
}
@media(prefers-reduced-motion:reduce){.ym{opacity:1;transform:none;transition:none;}}
'''


def page():
    hc = head_common()
    fud = ''.join(f'<li>{e(x)}</li>' for x in FUD)
    year = ''.join(f'<div class="ym"><b>{e(m)}</b><p>{e(t)}</p></div>' for m, t in YEAR)
    agit = ''.join(f'<div><b>{e(t)}</b><p>{e(x)}</p></div>' for t, x in AGITATE)
    vs_no = ''.join(f'<li>{e(a)}</li>' for a, _ in CONTRAST)
    vs_si = ''.join(f'<li>{e(b)}</li>' for _, b in CONTRAST)
    step_shots = [
        shot('paso-numeros.webp', 1270, 650, 'Paso 1 del plan: tus números de partida', 'números de partida'),
        shot('paso-crecer.webp', 1360, 760, 'Paso 2 del plan: cuánto quieres crecer en 2027', '% de crecimiento'),
        shot('real-vs-plan.webp', 1420, 540, 'Seguimiento mes a mes: beneficio previsto y real', 'seguimiento mes a mes'),
    ]
    steps = ''.join(
        f'<div class="step2"><span class="n grad">0{i}</span><h3>{e(t)}</h3><p>{e(x)}</p>' + step_shots[i - 1] + '</div>'
        for i, (t, x) in enumerate(STEPS, 1))
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    title = 'Cada año trabajas más. ¿Por qué tu salón no crece? Crea tu plan financiero 2027 | Godolphy'
    desc = 'Te haces tu plan financiero 2027: eliges cuánto quieres crecer y cada mes sabes si vas bien. Sin Excel y sin saber de finanzas. Gratis 30 días, sin tarjeta.'
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
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}{A_CSS}{B_CSS}{TST_CSS}{WHY_CSS}{ICON_CSS}{PRODUCT_CSS}{HAND_CSS}{C_CSS}</style>
</head>
<body data-lp="{SLUG}">
<header class="top"><div class="w"><img src="/wp-images/logo-gradient.png" alt="Godolphy" style="height:30px;width:auto;"></div></header>

<main>
<!-- 1. La escena -->
<section class="hero2" id="hero">
  <div class="w grid">
    <div>
      <p class="tag"><i>●</i> Plan 2027</p>
      <h1>Cada año trabajas más. {circ('<span class="grad">¿Por qué tu salón no crece?</span>')}</h1>
      <p class="sub">Con Godolphy te haces tu <b>plan financiero 2027</b>: eliges cuánto quieres crecer y cada mes sabes si vas bien. Sin Excel y sin saber de finanzas.<span id="cd" hidden> Quedan <b id="cd-n"></b> para enero.</span></p>
      {cta('hero')}
      <ul class="fud">{fud}</ul>
      <div class="proof">
        <p>{icon('trophy', 'ico ico--s')}<span><b>Premio Emprendedores Tech 2026</b> a la mejor app del sector estética</span></p>
        <p>{icon('trend', 'ico ico--s')}<span>Con un plan escrito, un <b>16 % más</b> de probabilidades de que el negocio salga adelante <small>(Harvard Business Review, 2017)</small></span></p>
      </div>
    </div>
    <div class="devices">
      <div class="lap">{shot('plan-portatil.webp', 1600, 1000, 'Plan financiero 2027 en el panel de Godolphy (ordenador)', 'captura del plan en el ordenador', eager=True)}</div>
      <div class="lap-base"></div>
      <div class="mob2"><div class="ph-wrap"><img src="/lp/salones/plan-mes.webp" alt="Plan financiero del mes en el móvil: plan, real y diferencia" width="744" height="1164" loading="eager"></div></div>
    </div>
  </div>
</section>

<!-- 2. Momentos concretos -->
<section class="sec sec--soft">
  <div class="w">
    <h2 class="h2">¿Te suena <span class="grad">este año</span>?</h2>
    <div class="year" id="year">{year}</div>
  </div>
</section>

<!-- 3. Problema y agitación -->
<section class="sec">
  <div class="w">
    <h2 class="h2">No es que trabajes poco. Es que <span class="grad">nadie te ha dado un mapa</span>.</h2>
    <div class="story">
      <p>Sabes peinar, maquillar o hacer unas uñas perfectas. Lo que nadie te enseñó es a mirar tu salón como un negocio: cuánto tienes que facturar, cuánto puedes gastar y cuánto te queda a ti.</p>
    </div>
    <div class="agit">{agit}</div>
    <p class="turn">Tu salón es un negocio, no solo un trabajo. Y un negocio se lleva {mark('con un plan')}.</p>
  </div>
</section>

<!-- 4. La mentora -->
<section class="sec sec--soft" id="neus">
  <div class="w neus2">
    <img src="/lp/salones/neus.webp" alt="Neus, fundadora de Godolphy" width="798" height="997" loading="lazy">
    <div>
      <h2 class="h2">Sé lo que es llevar un salón: <span class="grad">yo también tuve el mío</span></h2>
      <p>Soy Neus. Trabajé unos 15 años en multinacionales, donde nadie empieza el año sin un objetivo. Después monté mi propio salón con una socia, y yo llevaba la parte de negocio.</p>
      <p>Por eso he creado Godolphy: el consultor financiero que mi salón nunca tuvo.</p>
      <p class="award">{icon('trophy', 'ico ico--s')} Premio Emprendedores Tech 2026 a la mejor app del sector estética</p>
      <p class="sig">Neus, fundadora de Godolphy</p>
    </div>
  </div>
</section>

<!-- 5. El puente: antes → después -->
<section class="sec">
  <div class="w">
    <h2 class="h2">De «a ver qué tal» a <span class="grad">saber cada mes dónde estás</span></h2>
    <div class="bridge">
      <div class="vs"><div class="no" style="height:100%"><h3>Tu año sin plan</h3><ul>{vs_no}</ul></div></div>
      <div class="arrow"><span>→</span>Tu plan financiero en Godolphy</div>
      <div class="vs"><div class="si" style="height:100%"><h3>Tu año con plan</h3><ul>{vs_si}</ul></div></div>
    </div>
    <div class="mcta">{cta('bridge')}</div>
  </div>
</section>

<!-- 6. El camino -->
<section class="sec sec--soft">
  <div class="w">
    <h2 class="h2">Tu plan 2027 en 3 pasos: <span class="grad">tú pones los números, Godolphy calcula</span></h2>
    {VIDEO}
    <div class="steps2">{steps}</div>
    {cta('steps')}
  </div>
</section>

<!-- 7. La transformación -->
<section class="sec">
  <div class="w">
    <div class="elix">
      <div>
        <h2 class="h2">Diciembre de 2027.</h2>
        <p>Abres Godolphy y lo ves claro: mes a mes, lo que planificaste y lo que has hecho. Sabes cuánto has facturado, cuánto has gastado y cuánto te ha quedado.</p>
        <p>Y cuando alguien te pregunta qué tal ha ido el año, no dices «más o menos». Dices la cifra.</p>
        {cta('elixir', 'btn')}
      </div>
      {shot('real-vs-plan.webp', 1420, 540, 'Gráfico del plan 2027: beneficio previsto y real de cada mes', 'gráfico real vs plan')}
    </div>
  </div>
</section>

{testimonials_html('Ellas ya han empezado <span class="grad">su 2027 con un plan</span>')}

<section class="sec">
  <div class="w">
    <h2 class="h2">Y no es solo una sensación: <span class="grad">quien se marca un objetivo llega más lejos</span></h2>
    {why_cards()}
    <div class="mcta">{cta('why')}</div>
  </div>
</section>

<section class="sec sec--soft">
  <div class="w">
    <h2 class="h2">¿Dudas? <span class="grad">30 días gratis y sin tarjeta</span></h2>
    <div class="faq">{faq}</div>
  </div>
</section>

{product_html('<div class="mcta">' + cta('product') + '</div>')}

<section class="sec">
  <div class="w">
    <div class="final">
      <h2 style="margin-bottom:12px;">Enero llega igual. Que te pille con un plan.</h2>
      <p>30 días gratis · Sin tarjeta</p>
      {cta('final', 'btn')}
    </div>
  </div>
</section>
</main>

<footer class="foot"><div class="w">© 2026 Godolphy · <a href="/politica-de-privacidad/">Privacidad</a><a href="/politica-de-cookies/">Cookies</a><a href="/aviso-legal/">Aviso legal</a></div></footer>

<div class="sticky" id="sticky">{cta('sticky', 'btn btn--v')}</div>

<script>
(function(){{
  var d=Math.ceil((new Date(2027,0,1)-new Date())/864e5);
  if(d>0){{document.getElementById('cd-n').textContent=d===1?'1 día':d+' días';
    var c=document.getElementById('cd');c.hidden=false;if(d===1)c.firstChild.textContent=' Queda ';}}
  var st=document.getElementById('sticky'),hero=document.getElementById('hero'),lp=document.body.getAttribute('data-lp');
  function upd(){{var past=hero.getBoundingClientRect().bottom<0,cookie=document.getElementById('gd-cookies');st.classList.toggle('on',past&&!cookie);}}
  window.addEventListener('scroll',upd,{{passive:true}});setInterval(upd,1500);upd();
  /* el año aparece mes a mes al entrar en pantalla */
  var ms=[].slice.call(document.querySelectorAll('.ym'));
  if('IntersectionObserver' in window){{var io=new IntersectionObserver(function(es){{es.forEach(function(x){{if(x.isIntersecting){{ms.forEach(function(m,i){{setTimeout(function(){{m.classList.add('on');}},i*260);}});io.disconnect();}}}});}},{{threshold:.25}});io.observe(document.getElementById('year'));}}
  else ms.forEach(function(m){{m.classList.add('on');}});
  {VIDEO_JS}
  document.addEventListener('click',function(e){{var a=e.target.closest&&e.target.closest('[data-cta]');if(!a)return;
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
