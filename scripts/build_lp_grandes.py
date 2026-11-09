#!/usr/bin/env python3
"""Landing /lp/grandes-empresas/: versión web del email «Lo que hacen las grandes empresas, ahora en tu salón»."""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_lp import CSS, FAQ, SIGNUP, DASH, head_common

SLUG = 'grandes-empresas'
IMG = f'/lp/{SLUG}/'
FEATS = [
    ('f-servicios', 'La IA te dice qué servicio te hace ganar dinero', 'Cuánto te deja de verdad cada servicio, por hora, después de producto y tiempo. Para que sepas qué promocionar y qué precio subir.'),
    ('f-plan', 'Tu plan financiero, hecho con tus datos', 'Eliges cuánto quieres crecer y cada mes ves si vas por delante o por detrás… y qué tocar para llegar.'),
    ('f-precio-hora', 'Precio según el día y la hora', 'Más caro en horas punta, más barato para llenar las horas flojas. Tus clientes ven siempre el precio final.'),
    ('f-domicilio', 'Domicilios con el desplazamiento calculado', 'Tus zonas, tu precio por desplazamiento y el tiempo entre citas, calculado solo en tu agenda.'),
]
EXTRA_CSS = r'''
.ge-top{background:#fff;padding:18px 0;text-align:center;}
.ge-top img{height:30px;width:auto;margin:0 auto;}
.ge-hero{background:#fff;padding:4px 0 8px;}
.ge-hero .w{max-width:1240px;}
.ge-hero img{width:100%;border-radius:28px;}
.ge-zz__img{position:relative;overflow:hidden;display:flex;justify-content:center;padding:34px 10px 10px;}
.ge-sun{position:absolute;width:62%;aspect-ratio:1;top:0;right:4%;border-radius:50%;background:radial-gradient(circle,#EEFE3A 0 64%,transparent 65%);}
.ge-sun::before{content:"";position:absolute;inset:-14%;background:repeating-conic-gradient(from 8deg,#EEFE3A 0 3deg,transparent 3deg 30deg);-webkit-mask:radial-gradient(circle,transparent 0 58%,#000 59% 70%,transparent 71%);mask:radial-gradient(circle,transparent 0 58%,#000 59% 70%,transparent 71%);}
.ge-card{position:relative;background:#fff;border-radius:16px;padding:10px;box-shadow:0 24px 60px rgba(40,20,90,.18);transform:rotate(-3deg);max-width:380px;width:92%;}
.ge-zz:nth-child(even) .ge-card{transform:rotate(3deg);}
.ge-card img{width:100%;border-radius:10px;border:1px solid rgba(2,2,30,.06);}
.ge-lap{max-width:900px;margin:26px auto 0;padding:0 4%;}
.ge-lap__scr{background:#0d0627;border-radius:18px 18px 0 0;padding:12px 12px 14px;box-shadow:0 30px 70px rgba(60,20,160,.2);}
.ge-lap__scr img{width:100%;border-radius:6px;}
.ge-lap__base{height:16px;margin:0 -4%;background:linear-gradient(#e6e3ef,#c9c5d6);border-radius:0 0 18px 18px;}
.ge-intro{max-width:620px;}
.ge-intro p{font-size:18px;line-height:1.65;color:rgba(2,2,30,.8);margin:0 0 14px;}
.ge-intro b{color:var(--ink);}
.ge-eyebrow{font-size:12.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--v);text-align:center;margin:0 0 8px;}
.ge-center{text-align:center;}
.ge-laptop{max-width:860px;margin:26px auto 0;}
.ge-laptop img{width:100%;}
.ge-cap{font-size:12.5px;color:var(--muted);text-align:center;margin-top:6px;}
.ge-zz{display:grid;grid-template-columns:1fr 1fr;gap:36px;align-items:center;max-width:860px;margin:0 auto 48px;}
.ge-zz:nth-child(even) .ge-zz__img{order:2;}
.ge-zz h3{font-family:'Gabarito',sans-serif;font-size:clamp(23px,2.6vw,28px);line-height:1.15;color:var(--v);margin:0 0 10px;}
.ge-zz p{margin:0;font-size:16.5px;line-height:1.6;color:rgba(2,2,30,.75);}
.ge-more{max-width:640px;margin:0 auto;text-align:center;color:var(--muted);line-height:1.6;}
.sec--cream{background:#faf6ef;}
.ge-final{background:linear-gradient(160deg,#5a16f0,#631cff 60%,#3a0aaa);color:#fff;text-align:center;padding:64px 0 70px;}
.ge-final h2{font-family:'Gabarito',sans-serif;font-size:clamp(30px,4.4vw,46px);line-height:1.08;margin:0 0 10px;}
.ge-final p{margin:0 0 26px;color:rgba(255,255,255,.88);font-size:17px;}
.ge-final .sm{margin:14px 0 0;font-size:12.5px;letter-spacing:.12em;text-transform:uppercase;opacity:.85;}
.ge-sig{font-family:'Brush Script MT','Segoe Script',cursive;font-size:34px;color:var(--y);margin:26px 0 0;}
.ge-sig small{display:block;font-family:'Plus Jakarta Sans',sans-serif;font-size:13px;color:rgba(255,255,255,.8);margin-top:2px;}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;}
@media(max-width:760px){.ge-zz{grid-template-columns:1fr;gap:18px;margin-bottom:40px;}.ge-zz:nth-child(even) .ge-zz__img{order:0;}.ge-intro .btn,.ge-final .btn{width:100%;}}
'''

def build():
    hc = head_common()
    cta = lambda pos: f'<a class="btn btn--v" href="{SIGNUP}" data-cta="{pos}">Pruébalo 30 días gratis →</a>'
    feats = ''.join(f'''<div class="ge-zz"><div class="ge-zz__img"><span class="ge-sun" aria-hidden="true"></span><div class="ge-card"><img src="{IMG}{f}.webp" alt="{html.escape(t)} en Godolphy" loading="lazy"></div></div><div><h3>{html.escape(t)}</h3><p>{html.escape(x)}</p></div></div>''' for f, t, x in FEATS)
    faq = ''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in FAQ)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    page = f'''<!DOCTYPE html>
<html lang="es">
<head>
{hc.split('<head>',1)[1].strip()}
<meta charset="UTF-8">
<title>Lo que hacen las grandes empresas, ahora en tu salón | Godolphy</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="El software de gestión con IA para salones: rentabilidad por servicio, plan financiero, precio según día y hora y domicilios. 30 días gratis, sin tarjeta.">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://www.godolphy.com/lp/{SLUG}/">
<meta property="og:title" content="Lo que hacen las grandes empresas, ahora en tu salón">
<meta property="og:image" content="https://www.godolphy.com/img/email/grandes-empresas/hero-ia-2.jpg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}{EXTRA_CSS}</style>
</head>
<body data-lp="{SLUG}">
<header class="ge-top"><img src="/wp-images/logo-gradient.png" alt="Godolphy" width="140" height="30"></header>
<main>
<section class="ge-hero">
  <div class="w">
    <h1 class="sr">Lo que hacen las grandes empresas, ahora en tu salón, con IA</h1>
    <picture>
      {'<source media="(min-width: 761px)" srcset="'+IMG+'hero-ancho.webp" width="2048" height="1152">' if os.path.exists('lp/'+SLUG+'/hero-ancho.webp') else ''}
      <img src="{IMG}hero-movil.webp" alt="Neus, fundadora de Godolphy. Lo que hacen las grandes empresas, ahora en tu salón, con IA" width="1080" height="1350" fetchpriority="high">
    </picture>
  </div>
</section>

<section class="sec" style="padding-top:36px;">
  <div class="w ge-intro">
    <p>Soy Neus. He trabajado siempre en multinacionales y, además, monté mi propio salón con una socia. De los dos mundos aprendí lo mismo: <b>quien conoce sus datos, gana.</b></p>
    <p>Por eso he creado Godolphy: un software de gestión como el que ya usas, pero con todo lo que al tuyo le falta.</p>
    <div style="margin-top:22px;">{cta('hero')}</div>
    <div class="note" style="color:var(--muted);">30 días gratis · Sin tarjeta · Sin permanencia</div>
  </div>
</section>

<section class="sec" style="padding-top:20px;">
  <div class="w">
    <p class="ge-eyebrow">Así se ve por dentro</p>
    <h2 class="h2 ge-center">Tu negocio, analizado con IA</h2>
    <div class="ge-lap"><div class="ge-lap__scr"><img src="{IMG}panel.webp" alt="Panel de Godolphy con el análisis del negocio con IA" width="1600" height="1000" loading="lazy"></div><div class="ge-lap__base"></div><p class="ge-cap">Datos de ejemplo.</p></div>
  </div>
</section>

<section class="sec sec--cream">
  <div class="w">
    <h2 class="h2 ge-center" style="color:var(--v);margin-bottom:8px;">Todo lo que al tuyo le falta</h2>
    <p class="ge-more" style="margin-bottom:44px;">Lo que hacen las grandes empresas y tu programa actual no te deja hacer.</p>
    {feats}
    <p class="ge-more">Y además: reservas online 24/7, recordatorios por WhatsApp, cobros, tarjetas regalo y todo lo que ya esperas de un software de gestión.</p>
  </div>
</section>

<section class="sec">
  <div class="w">
    <h2 class="h2">Preguntas antes de empezar</h2>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="ge-final">
  <div class="w">
    <h2>Quien conoce sus datos, gana.</h2>
    <p>Lo mejor del mundo corporativo, aplicado a tu salón.</p>
    <a class="btn" href="{SIGNUP}" data-cta="final">Pruébalo 30 días gratis →</a>
    <p class="sm">30 días gratis · sin tarjeta</p>
    <a class="alt" href="{DASH}" data-cta="dashboard">¿Aún no? <span>Analiza tu salón gratis en 2 minutos</span></a>
    <div class="ge-sig">Neus<small>Fundadora de Godolphy</small></div>
  </div>
</section>
</main>
<footer class="foot"><div class="w">© 2026 Godolphy · <a href="/politica-de-privacidad/">Privacidad</a><a href="/politica-de-cookies/">Cookies</a><a href="/aviso-legal/">Aviso legal</a></div></footer>
<div class="sticky" id="sticky"><a class="btn" href="{SIGNUP}" data-cta="sticky">Pruébalo 30 días gratis →</a></div>
<script>
(function(){{
  var lp=document.body.getAttribute('data-lp'),st=document.getElementById('sticky'),hero=document.querySelector('.ge-intro');
  function upd(){{var past=hero.getBoundingClientRect().bottom<0,cookie=document.getElementById('gd-cookies');st.classList.toggle('on',past&&!cookie);}}
  window.addEventListener('scroll',upd,{{passive:true}});upd();
  document.addEventListener('click',function(e){{var a=e.target.closest&&e.target.closest('[data-cta]');if(!a)return;
    try{{if(window.posthog)posthog.capture('lp_cta_click',{{lp:lp,position:a.getAttribute('data-cta')}});}}catch(_){{}}
    try{{if(window.fbq&&a.getAttribute('data-cta')!=='dashboard')fbq('track','InitiateCheckout',{{content_name:lp}});}}catch(_){{}}
  }});
}})();
</script>
</body>
</html>
'''
    os.makedirs(f'lp/{SLUG}', exist_ok=True)
    open(f'lp/{SLUG}/index.html', 'w', encoding='utf-8').write(page)
    print('ok', SLUG)

if __name__ == '__main__':
    build()
