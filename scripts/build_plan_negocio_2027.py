#!/usr/bin/env python3
"""Página de entrega del lead magnet «Plan de negocio 2027» (prompt para la IA).

URL: /plan-negocio-2027/ — noindex, nofollow; no se enlaza desde menú, footer ni sitemap.
Llega gente desde un DM de Instagram (ManyChat), casi siempre en el móvil.
El prompt está en scripts/data/prompt-plan-negocio-2027.txt (copiado tal cual).

Uso: python3 scripts/build_plan_negocio_2027.py
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build_lp import head_common  # noqa: E402

OUT = 'plan-negocio-2027/index.html'
PROMPT = open(os.path.join(os.path.dirname(__file__), 'data', 'prompt-plan-negocio-2027.txt'), encoding='utf-8').read().rstrip('\n')
SIGNUP = 'https://app.godolphy.com/auth/sign-up?entrada=plan&utm_source=landing_prompt&utm_medium=lead_magnet&utm_campaign=plan_negocio_2027'
PDF = '/descargas/plan-negocio-2027.pdf'
e = html.escape

STEPS = [
    ('Abre Claude (claude.ai)', 'Con la cuenta gratuita es suficiente. En ChatGPT funciona con la versión de pago; con la gratuita se corta a mitad.'),
    ('Copia el prompt y pégalo en un chat nuevo.', ''),
    ('Responde a sus preguntas.', 'Si no sabes un dato, dilo: te ayudará a estimarlo. Son 30-40 minutos.'),
    ('Descarga tu documento.', 'Al final te dará también tus números para seguirlo cada mes.'),
]

COPY_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2"/>'
            '<path d="M5 15V6a2 2 0 0 1 2-2h9"/></svg>')

CSS = r'''
:root{--v:#631cff;--v2:#9B4FE8;--y:#EEFE3A;--ink:#02021e;--muted:#55536b;--line:#e7e1ff;--soft:#f6f3ff;}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{margin:0;background:#fff;color:var(--ink);font-family:'Plus Jakarta Sans',system-ui,sans-serif;font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased;}
h1,h2,h3{font-family:'Gabarito',sans-serif;line-height:1.1;margin:0;}
a{color:inherit;}
.w{max-width:860px;margin:0 auto;padding:0 20px;}
.hero{background:linear-gradient(160deg,#9B4FE8 0%,#7835C3 30%,#631cff 65%,#3a0aaa 100%);color:#fff;padding:22px 0 56px;}
.logo{display:block;height:30px;width:auto;margin:0 0 40px;}
.pill{display:inline-block;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.35);border-radius:999px;padding:8px 14px;font-weight:800;font-size:12.5px;letter-spacing:.08em;margin:0 0 18px;}
.hero h1{font-size:clamp(42px,10vw,76px);font-weight:800;letter-spacing:-.01em;}
.hero h1 .serif{font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-weight:400;letter-spacing:0;}
.hero h1 .yr{color:var(--y);}
.hero .sub{font-size:clamp(17px,2.4vw,20px);line-height:1.55;margin:18px 0 28px;max-width:640px;opacity:.95;}
.btn{display:flex;align-items:center;justify-content:center;gap:10px;width:100%;max-width:420px;min-height:60px;padding:16px 24px;border:0;border-radius:16px;cursor:pointer;font:800 18px/1.2 'Plus Jakarta Sans',sans-serif;text-decoration:none;text-align:center;-webkit-tap-highlight-color:transparent;transition:transform .12s ease;}
.btn:active{transform:scale(.98);}
.btn svg{width:22px;height:22px;flex:0 0 auto;}
.btn--y{background:var(--y);color:var(--ink);box-shadow:0 12px 28px rgba(0,0,0,.25);}
.btn--v{background:var(--v);color:#fff;box-shadow:0 12px 28px rgba(99,28,255,.3);}
.btn--o{background:#fff;color:var(--v);border:2px solid var(--v);min-height:56px;}
.btn.ok{background:#1f9d55;color:#fff;}
.sec{padding:52px 0;}
.sec--soft{background:var(--soft);}
.h2{font-size:clamp(28px,6vw,40px);font-weight:800;margin:0 0 24px;}
.steps{list-style:none;padding:0;margin:0;display:grid;gap:12px;counter-reset:s;}
.steps li{position:relative;background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px 18px 18px 70px;counter-increment:s;}
.steps li::before{content:counter(s);position:absolute;left:18px;top:16px;width:36px;height:36px;border-radius:50%;background:linear-gradient(160deg,#9B4FE8,#631cff);color:#fff;font:800 18px/36px 'Gabarito',sans-serif;text-align:center;}
.steps b{display:block;font-size:17.5px;}
.steps span{display:block;color:var(--muted);font-size:15.5px;margin-top:4px;}
.steps a{color:var(--v);font-weight:700;}
.warn{display:flex;gap:12px;align-items:flex-start;margin:18px 0 0;background:var(--y);border-radius:18px;padding:16px 18px;font-weight:700;font-size:16px;line-height:1.45;}
.warn svg{width:24px;height:24px;flex:0 0 auto;margin-top:1px;}
.actions{display:grid;gap:12px;justify-items:center;margin:0 0 16px;}
.prompt{background:#0f0b2b;color:#ece8ff;border-radius:18px;padding:18px;margin:0 0 16px;max-height:420px;overflow:auto;-webkit-overflow-scrolling:touch;white-space:pre-wrap;word-wrap:break-word;font:13.5px/1.6 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;border:1px solid #2c2360;}
.pdf{display:block;text-align:center;margin:18px 0 0;font-weight:700;color:var(--v);}
.close p{color:var(--muted);font-size:17.5px;margin:0 0 24px;}
.sign{display:flex;gap:16px;align-items:center;margin:34px 0 0;padding:20px;background:#fff;border:1px solid var(--line);border-radius:20px;}
.sign img{width:72px;height:72px;border-radius:50%;object-fit:cover;object-position:top;flex:0 0 auto;}
.sign p{margin:0;font-size:15.5px;line-height:1.5;color:var(--ink);}
.foot{padding:28px 0 40px;text-align:center;font-size:13px;color:var(--muted);}
.foot a{margin:0 6px;color:var(--muted);}
@media(min-width:700px){.actions{grid-template-columns:1fr 1fr;justify-items:stretch;}.actions .btn{max-width:none;}}
'''


def page():
    hc = head_common()
    # El enlace al PDF solo aparece cuando el archivo ya está en /descargas/
    pdf_link = (f'<a class="pdf" href="{PDF}" target="_blank" rel="noopener" data-pdf>Descargar la guía en PDF</a>'
                if os.path.exists(PDF.lstrip('/')) else '')
    steps = ''.join(
        f'<li><b>{s}</b>' + (f'<span>{e(x)}</span>' if x else '') + '</li>'
        for s, x in [(('Abre <a href="https://claude.ai/new" target="_blank" rel="noopener">Claude (claude.ai)</a>'), STEPS[0][1])]
        + [(e(t), x) for t, x in STEPS[1:]])
    copy_btn = lambda pos, cls='btn btn--v': (f'<button type="button" class="{cls}" data-copy="{pos}">{COPY_SVG}'
                                                f'<span>Copiar prompt</span></button>')
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
{hc.split('<head>', 1)[1].strip()}
<meta charset="UTF-8">
<title>Tu plan de negocio 2027 | Godolphy</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="El prompt que convierte a la IA en tu consultora de negocio: mercado, competencia, estrategia y números mes a mes.">
<meta name="robots" content="noindex, nofollow">
<meta property="og:title" content="Tu plan de negocio 2027">
<meta property="og:description" content="El prompt que convierte a la IA en tu consultora de negocio: mercado, competencia, estrategia y números mes a mes.">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@600;700;800&family=Instrument+Serif:ital@1&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body data-lp="plan-negocio-2027">
<header class="hero" id="hero">
  <div class="w">
    <img class="logo" src="/wp-images/logo.png" alt="Godolphy" width="864" height="215">
    <p class="pill">GRATIS · PARA SALONES DE BELLEZA</p>
    <h1>Tu plan de <span class="serif">negocio</span> <span class="yr">2027</span></h1>
    <p class="sub">El prompt que convierte a la IA en tu consultora de negocio: mercado, competencia, estrategia y números mes a mes.</p>
    {copy_btn('hero', 'btn btn--y')}
  </div>
</header>

<main>
<section class="sec">
  <div class="w">
    <h2 class="h2">Cómo usarlo</h2>
    <ol class="steps">{steps}</ol>
    <p class="warn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/></svg>
      <span>Mejor desde el ordenador: tendrás que copiar el prompt, responder con calma y descargar tu documento.</span></p>
  </div>
</section>

<section class="sec sec--soft" id="prompt">
  <div class="w">
    <h2 class="h2">El prompt</h2>
    <div class="actions">{copy_btn('arriba')}<a class="btn btn--o" href="https://claude.ai/new" target="_blank" rel="noopener" data-open-claude>Abrir Claude</a></div>
    <pre class="prompt" id="prompt-text" tabindex="0">{e(PROMPT)}</pre>
    <div class="actions">{copy_btn('abajo')}<a class="btn btn--o" href="https://claude.ai/new" target="_blank" rel="noopener" data-open-claude>Abrir Claude</a></div>
    {pdf_link}
  </div>
</section>

<section class="sec close">
  <div class="w">
    <h2 class="h2">Un plan se sigue cada mes</h2>
    <p>Al final, la IA te dará tus números para Godolphy: pégalos y tendrás tu plan financiero 2027 con el seguimiento mes a mes, gratis.</p>
    <a class="btn btn--v" href="{SIGNUP}" data-gd-direct data-cta="final">Crea tu plan en Godolphy →</a>
    <div class="sign">
      <img src="/lp/salones/neus.webp" alt="Neus, fundadora de Godolphy" width="798" height="997" loading="lazy">
      <p>Soy Neus. He trabajado 15 años en multinacionales y monté mi propio salón con una socia, donde llevaba la parte de negocio. Ahora te ayudo a llevar tu salón como lo haría una gran empresa.</p>
    </div>
  </div>
</section>
</main>

<footer class="foot">© 2026 Godolphy · <a href="/politica-de-privacidad/">Privacidad</a><a href="/politica-de-cookies/">Cookies</a><a href="/aviso-legal/">Aviso legal</a></footer>

<script>
(function(){{
  var pre=document.getElementById('prompt-text');
  function track(n,p){{try{{if(window.posthog)posthog.capture(n,p||{{}});}}catch(_){{}}}}
  function fallback(t){{
    var ta=document.createElement('textarea');ta.value=t;ta.setAttribute('readonly','');
    ta.style.position='fixed';ta.style.top='0';ta.style.left='0';ta.style.opacity='0';ta.style.fontSize='16px';
    document.body.appendChild(ta);ta.focus();ta.select();ta.setSelectionRange(0,t.length);
    var ok=false;try{{ok=document.execCommand('copy');}}catch(_){{}}
    document.body.removeChild(ta);return ok;
  }}
  function copy(t){{
    if(navigator.clipboard&&window.isSecureContext){{
      return navigator.clipboard.writeText(t).then(function(){{return true;}},function(){{return fallback(t);}});
    }}
    return Promise.resolve(fallback(t));
  }}
  function selectPrompt(){{var r=document.createRange();r.selectNodeContents(pre);var s=window.getSelection();s.removeAllRanges();s.addRange(r);}}
  document.querySelectorAll('[data-copy]').forEach(function(b){{
    var label=b.querySelector('span');
    b.addEventListener('click',function(){{
      var pos=b.getAttribute('data-copy');
      if(pos==='hero')document.getElementById('prompt').scrollIntoView({{behavior:'smooth',block:'start'}});
      copy(pre.textContent).then(function(ok){{
        if(ok){{label.textContent='¡Copiado!';b.classList.add('ok');track('prompt_copied',{{position:pos}});}}
        else{{selectPrompt();label.textContent='Mantén pulsado y copia';track('prompt_copy_failed',{{position:pos}});}}
        setTimeout(function(){{label.textContent='Copiar prompt';b.classList.remove('ok');}},2500);
      }});
    }});
  }});
  document.querySelectorAll('[data-open-claude]').forEach(function(a){{a.addEventListener('click',function(){{track('prompt_open_claude');}});}});
  var p=document.querySelector('[data-pdf]');if(p)p.addEventListener('click',function(){{track('prompt_pdf_download');}});
}})();
</script>
</body>
</html>
'''


if __name__ == '__main__':
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(page())
    print('ok', OUT)
