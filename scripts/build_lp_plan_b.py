#!/usr/bin/env python3
"""Landing /lp/plan-financiero-2027-b/ — versión B (beneficio) de la del plan financiero.

Estructura según el método de landings de Hormozi / ThrillX:
- Arriba del todo (donde va el 80 % del esfuerzo): resultado (+20 % como OBJETIVO
  que se marca el salón, no promesa), etiqueta «Mueve el culo» para que case con
  el anuncio, subtítulo de cómo + sin esfuerzo, CTA único, quitar miedos debajo del
  botón y pruebas apiladas (premio + estudio).
- 4 bloques de beneficio en «tú» (problema → solución), cada uno con su CTA.
- Cómo funciona en 3 pasos, quién está detrás, FAQ (incluida «¿está garantizado?»).

Las capturas son las mismas que en la versión A (/lp/plan-financiero-2027/): al
subirlas allí aparecen en las dos.

Uso: python3 scripts/build_lp_plan_b.py
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build_lp import CSS, head_common  # noqa: E402
from build_lp_plan import EXTRA_CSS as A_CSS, CTA_URL  # noqa: E402

SLUG = 'plan-financiero-2027-b'
OUT = f'lp/{SLUG}/index.html'
IMG = '/lp/plan-financiero-2027/'
CTA_TXT = 'Crear mi plan +20 % gratis →'

e = html.escape


def cta(pos, cls='btn btn--v', txt=CTA_TXT):
    return f'<a class="{cls}" href="{CTA_URL}" data-cta="{pos}" data-gd-direct>{e(txt)}</a>'


def shot(file, w, h, alt, label, cls=''):
    return (f'<div class="ph-wrap {cls}" data-ph="{e(file)} · {w}×{h} px · {e(label)}">'
            f'<img src="{IMG}{file}" alt="{e(alt)}" width="{w}" height="{h}" '
            f'loading="lazy" onerror="this.parentNode.classList.add(\'ph\');this.remove();"></div>')


FUD = ['30 días gratis', 'Sin tarjeta', 'Si no eliges plan, no pagas nada']

CONTRAST = [
    ('Cada año, igual que el anterior.', 'Un objetivo claro: +20 % en 2027.'),
    ('Te enteras en diciembre de que el año ha ido flojo.', 'Cada mes ves si vas por delante o por detrás.'),
    ('Creces «si sale».', 'Sabes cuánto tienes que facturar cada mes para llegar.'),
]

BENEFITS = [
    {
        'h': 'Tu +20 % convertido en <span class="grad">una cifra para cada mes</span>',
        'p': '«Facturar más» no se puede perseguir. «Facturar X este mes» sí. Pones tus números de partida, eliges el +20 % y Godolphy te dice cuánto te toca facturar cada mes para llegar.',
        'img': ('paso-crecer.webp', 780, 1100, 'Elegir cuánto quieres crecer en 2027', 'pantalla del % de crecimiento'),
    },
    {
        'h': 'Con un objetivo concreto <span class="grad">rindes más que con un «a ver qué tal»</span>',
        'p': 'No lo decimos nosotros. Es una de las conclusiones más repetidas de la psicología del trabajo: quien se marca una meta concreta y exigente llega más lejos que quien «hace lo que puede».',
        'stat': ('35 años', 'de estudios sobre objetivos llegan a la misma conclusión: una meta concreta y exigente rinde más que «hacerlo lo mejor posible».', 'Locke y Latham, American Psychologist, 2002'),
    },
    {
        'h': '¿Vas por detrás? <span class="grad">Lo sabes este mes, no en diciembre</span>',
        'p': 'Cada mes ves lo real frente a lo planificado. Y si un mes vas por debajo, la IA te avisa a tiempo para reaccionar.',
        'imgs': [('real-vs-plan.webp', 780, 1100, 'Este mes: real frente al plan', 'tarjeta «real vs plan»'),
                 ('aviso-ia.webp', 780, 1100, 'Aviso de la IA cuando el mes va por debajo del plan', 'aviso de la IA')],
    },
    {
        'h': 'Sin Excel <span class="grad">y sin saber de finanzas</span>',
        'p': 'Un Excel lo descargas y te olvidas. Aquí el plan se actualiza solo con tu día a día: si ya usas Godolphy, partimos de tus citas y gastos reales. Tú pones los números, Godolphy hace los cálculos.',
        'img': ('paso-numeros.webp', 780, 1100, 'Números de partida del plan financiero', 'pantalla «números de partida»'),
    },
]

STEPS = [
    ('Te das de alta con tu email.', 'Sin tarjeta.'),
    ('Pones tus números de partida.', 'Si ya usas Godolphy, partimos de tus citas y gastos reales.'),
    ('Eliges +20 % (o lo que tú quieras)', 'y tienes tu plan mes a mes, editable cuando quieras.'),
]

FAQ = [
    ('¿El +20 % está garantizado?', 'No. El +20 % es el objetivo que te marcas tú. Godolphy lo convierte en una cifra para cada mes y te enseña si vas bien, para que puedas reaccionar a tiempo. Si prefieres otro porcentaje, eliges el que quieras.'),
    ('¿Necesito saber de finanzas?', 'No. Pones tus números y Godolphy hace los cálculos.'),
    ('¿Sirve si no tengo historial?', 'Sí, empiezas con tus números de partida.'),
    ('¿Necesito tarjeta?', 'No. Te das de alta solo con tu email.'),
    ('¿Cuánto cuesta después?', 'Los primeros 30 días son gratis. Después, el plan financiero está incluido en el plan Pro, desde 45 €/mes. Si no eliges plan, no pagas nada.'),
]

B_CSS = r'''
.tag{display:inline-flex;align-items:center;gap:8px;background:#02021e;color:#fff;font:800 13px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.06em;text-transform:uppercase;padding:9px 14px;border-radius:999px;margin:0 0 18px;}
.tag i{font-style:normal;color:var(--y);}
.hero2 h1 .big{display:block;}
.fud{list-style:none;padding:0;margin:14px 0 0;display:flex;flex-wrap:wrap;gap:8px 16px;font-size:14px;color:var(--ink);font-weight:600;}
.fud li::before{content:"✓ ";color:var(--v);font-weight:800;}
.proof{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0 0;}
.proof p{margin:0;background:#fff;border:1px solid var(--line);border-radius:14px;padding:10px 14px;font-size:14px;line-height:1.35;color:var(--ink);max-width:262px;}
.proof b{color:var(--v);}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:900px;}
.vs > div{border-radius:20px;padding:22px 24px;}
.vs .no{background:#fff;border:1px solid var(--line);}
.vs .si{background:linear-gradient(160deg,#9B4FE8 0%,#631cff 70%);color:#fff;}
.vs h3{font-family:'Gabarito',sans-serif;font-size:22px;margin:0 0 12px;}
.vs ul{list-style:none;padding:0;margin:0;display:grid;gap:10px;font-size:16px;line-height:1.45;}
.vs .no li::before{content:"✗ ";color:#c0392b;font-weight:800;}
.vs .si li::before{content:"✓ ";font-weight:800;}
.ben{display:grid;grid-template-columns:1.1fr .9fr;gap:44px;align-items:center;}
.ben.rev > :first-child{order:2;}
.ben p.t{font-size:18px;line-height:1.6;color:var(--muted);margin:0 0 22px;}
.ben .pics{display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start;}
.ben .ph-wrap{border-radius:18px;overflow:hidden;box-shadow:0 18px 40px rgba(40,10,120,.14);background:#fff;max-width:360px;margin:0 auto;}
.ben .ph-wrap img{width:100%;height:auto;display:block;}
.ben .stat{max-width:420px;margin:0 auto;}
.award{display:inline-block;background:#fff;border:1px solid var(--line);border-radius:14px;padding:10px 14px;font-size:15px;margin:0 0 16px;}
@media(max-width:860px){
  .vs,.ben{grid-template-columns:1fr;gap:22px;}
  .ben.rev > :first-child{order:0;}
  .ben p.t{font-size:16px;}
  .proof p{max-width:none;flex:1 1 100%;}
  .tag{margin:0 0 12px;}
}
'''


def page():
    hc = head_common()
    fud = ''.join(f'<li>{e(x)}</li>' for x in FUD)
    vs_no = ''.join(f'<li>{e(a)}</li>' for a, _ in CONTRAST)
    vs_si = ''.join(f'<li>{e(b)}</li>' for _, b in CONTRAST)
    bens = []
    for i, b in enumerate(BENEFITS):
        if 'img' in b:
            vis = shot(*b['img'])
        elif 'imgs' in b:
            vis = '<div class="pics">' + ''.join(shot(*x) for x in b['imgs']) + '</div>'
        else:
            n, t, src = b['stat']
            vis = f'<div class="stat"><b class="grad">{e(n)}</b><p>{e(t)}</p><small>{e(src)}</small></div>'
        soft = ' sec--soft' if i % 2 == 0 else ''
        rev = ' rev' if i % 2 else ''
        bens.append(f'''<section class="sec{soft}">
  <div class="w ben{rev}">
    <div>
      <h2 class="h2">{b['h']}</h2>
      <p class="t">{e(b['p'])}</p>
      {cta(f'ben{i + 1}')}
    </div>
    <div>{vis}</div>
  </div>
</section>''')
    bens = '\n'.join(bens)
    step_shot = shot('paso-alta.webp', 780, 1100, 'Alta en Godolphy con tu email', 'pantalla de alta')
    steps = ''.join(
        f'<div class="step2"><span class="n grad">0{i}</span><h3>{e(t)}</h3><p>{e(x)}</p>'
        + (step_shot if i == 1 else '') + '</div>'
        for i, (t, x) in enumerate(STEPS, 1))
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    title = 'Ponte un objetivo: +20 % de facturación en 2027 | Godolphy'
    desc = 'Marca tu objetivo para 2027 y Godolphy lo convierte en una cifra para cada mes, con tus datos reales. Gratis 30 días, sin tarjeta.'
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
<meta property="og:title" content="Ponte un objetivo: +20 % de facturación en 2027">
<meta property="og:description" content="{e(desc)}">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}{A_CSS}{B_CSS}</style>
</head>
<body data-lp="{SLUG}">
<header class="top"><div class="w"><img src="/wp-images/logo-gradient.png" alt="Godolphy" style="height:30px;width:auto;"></div></header>

<main>
<section class="hero2" id="hero">
  <div class="w grid">
    <div>
      <p class="tag"><i>●</i> Mueve el culo · Plan 2027</p>
      <h1>Ponte un objetivo: <span class="grad big">+20 % de facturación en 2027.</span> Y llega mes a mes.</h1>
      <p class="sub">Godolphy convierte tu +20 % en una cifra para cada mes y te avisa si te desvías. <b>Empiezas hoy</b>, sin saber de finanzas.<span id="cd" hidden> Quedan <b id="cd-n"></b> para enero.</span></p>
      {cta('hero')}
      <ul class="fud">{fud}</ul>
      <div class="proof">
        <p>🏆 <b>Premio Emprendedores Tech 2026</b> a la mejor app del sector estética</p>
        <p>📈 Con un plan escrito, un <b>16 % más</b> de probabilidades de que el negocio salga adelante <small>(Harvard Business Review, 2017)</small></p>
      </div>
    </div>
    <div class="devices">
      <div class="lap">{shot('plan-portatil.webp', 1600, 1000, 'Plan financiero 2027 en el panel de Godolphy (ordenador)', 'captura del plan en el ordenador').replace('loading="lazy"', 'loading="eager"')}</div>
      <div class="lap-base"></div>
      <div class="mob2"><div class="ph-wrap"><img src="/lp/salones/plan-mes.webp" alt="Plan financiero del mes en el móvil: plan, real y diferencia" width="744" height="1164" loading="eager"></div></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="w">
    <h2 class="h2">Sin plan, 2027 será <span class="grad">igual que 2026</span></h2>
    <div class="vs">
      <div class="no"><h3>Sin plan</h3><ul>{vs_no}</ul></div>
      <div class="si"><h3>Con tu plan en Godolphy</h3><ul>{vs_si}</ul></div>
    </div>
  </div>
</section>

{bens}

<section class="sec">
  <div class="w">
    <h2 class="h2">Tu plan 2027, <span class="grad">en 3 pasos</span></h2>
    <div class="steps2">{steps}</div>
    {cta('steps')}
  </div>
</section>

<section class="sec sec--soft" id="neus">
  <div class="w neus2">
    <img src="/lp/salones/neus.webp" alt="Neus, fundadora de Godolphy" width="798" height="997" loading="lazy">
    <div>
      <h2 class="h2">Las grandes empresas no improvisan. <span class="grad">Tu salón tampoco debería.</span></h2>
      <p>Soy Neus. He trabajado unos 15 años en multinacionales, donde nadie empieza el año sin un objetivo, y monté mi propio salón con una socia, donde yo llevaba la parte de negocio.</p>
      <p>Godolphy es el consultor financiero que mi salón nunca tuvo.</p>
      <p class="award">🏆 Premio Emprendedores Tech 2026 a la mejor app del sector estética</p>
      <p class="sig">Neus, fundadora de Godolphy</p>
    </div>
  </div>
</section>

<section class="sec">
  <div class="w">
    <h2 class="h2">Preguntas</h2>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="sec">
  <div class="w">
    <div class="final">
      <h2 style="margin-bottom:12px;">Enero llega igual. Que te pille con un objetivo.</h2>
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
