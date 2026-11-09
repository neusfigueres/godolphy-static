#!/usr/bin/env python3
"""Landings de anuncios (Meta) para centros de estética: una por problema.

Genera /lp/<slug>/index.html. Mobile-first, sin menú, un solo objetivo.
Estructura: gancho por sector + problema → visual real → «¿te suena?» → cómo lo resuelve
(3 pasos) → además → quién hay detrás (Neus) → preguntas que frenan → CTA final + alternativa suave.
No indexables (noindex): la página de sector sigue siendo la de SEO.

Uso: python3 scripts/build_lp.py
"""
import html, json, os

SIGNUP = 'https://app.godolphy.com/auth/sign-up'
DASH = 'https://dashboard.godolphy.com/'

PHONE_IMG = lambda src, alt: f'<div class="phone"><img src="{src}" alt="{html.escape(alt)}" width="780" height="1688" fetchpriority="high"></div>'

WA_MOCK = '''<div class="phone phone--wa" aria-hidden="true"><div class="wa">
  <div class="wa__top"><span class="wa__av">G</span><div><b>Centro Lumen</b><small>en línea</small></div></div>
  <div class="wa__body">
    <div class="wa__day">AYER</div>
    <div class="wa__msg">Hola Marta 👋 Te recordamos tu cita de <b>limpieza facial</b> mañana a las <b>16:00</b>. Tienes una señal pagada de 10 €. ¿Nos confirmas?<small>10:02</small></div>
    <div class="wa__btns"><span>Confirmo</span><span>Cambiar cita</span></div>
    <div class="wa__msg wa__me">¡Confirmo! Hasta mañana 😊<small>10:05 ✓✓</small></div>
  </div></div></div>'''

LPS = {
  'citas-perdidas': {
    'title': 'Menos clientes que no se presentan | Godolphy para centros de estética',
    'desc': 'Cobra una señal al reservar y deja que tus clientes confirmen por WhatsApp el día antes. 30 días gratis, sin tarjeta.',
    'h1': '¿Tienes un centro de estética y hay clientes que no se presentan?',
    'sub': 'Cada plantón es una cabina vacía y un tratamiento que ya no cobras. Con Godolphy cobras una señal al reservar y tus clientes confirman por WhatsApp el día antes.',
    'visual': WA_MOCK,
    'pains': ['Reservan por WhatsApp y luego no aparecen.',
              'Pierdes tiempo llamando una a una para confirmar.',
              'Esa hora ya no la recuperas, y la pagas igual.'],
    'steps_title': 'Así dejas de perder citas',
    'steps': [('Señal al reservar', 'Tú decides el porcentaje o el importe. Si la cliente no viene, la señal se queda en tu cuenta.'),
              ('Recordatorio por WhatsApp', 'El día antes le llega un mensaje con un botón para confirmar o cambiar la cita. Tú no llamas a nadie.'),
              ('Política de cancelación', 'Decides hasta cuándo se puede cancelar sin perder la señal. Si cancela a tiempo, el hueco vuelve a tu agenda.')],
    'note': 'En el plan Solo la señal es del 20 %. Elegir el importe y la política de cancelación está en Pro y Max, y en la prueba gratuita.',
  },
  'agenda-llena': {
    'title': 'Reservas 24 horas sin coger el teléfono | Godolphy para centros de estética',
    'desc': 'Tus clientes reservan solos desde Instagram, Google o tu web mientras tú trabajas. 30 días gratis, sin tarjeta.',
    'h1': '¿Tienes un centro de estética y pierdes reservas porque no puedes coger el teléfono?',
    'sub': 'Mientras haces un tratamiento, tus clientes reservan solos desde Instagram, Google o tu web, a cualquier hora. Tú solo miras la agenda.',
    'visual': PHONE_IMG('/images/producto/movil-calendario.webp', 'Agenda de Godolphy en el móvil con las citas del día por esteticista'),
    'pains': ['Te escriben para reservar a las once de la noche.',
              'Contestas mensajes entre clienta y clienta.',
              'Tienes huecos libres que nadie sabe que existen.'],
    'steps_title': 'Así se llena tu agenda sola',
    'steps': [('Tu página de reservas', 'Con tu nombre y tus tratamientos. Pon el enlace en la bio de Instagram y en tu ficha de Google.'),
              ('Reservan sin llamarte', 'Eligen tratamiento, esteticista, día y hora. La cita aparece en tu agenda y en la de la esteticista.'),
              ('Cada mañana, tus huecos', 'Godolphy te avisa a las 8:00 de los huecos que tienes mañana para que los llenes a tiempo.')],
  },
  'cuanto-ganas': {
    'title': '¿Cuánto ganas de verdad con tu centro? | Godolphy para centros de estética',
    'desc': 'Cobros, gastos y precios en un solo sitio. La IA te dice cuánto te queda, qué tratamientos te dejan margen y qué clientes dejan de venir.',
    'h1': '¿Tienes un centro de estética y no sabes si este mes has ganado dinero?',
    'sub': 'Godolphy junta tus cobros y tus gastos y te dice cuánto te queda de verdad, qué tratamientos te dejan margen y qué clientes están dejando de venir.',
    'visual': PHONE_IMG('/images/producto/movil-analisis.webp', 'Análisis con IA de Godolphy en el móvil: facturación del mes y recomendación'),
    'pains': ['Facturas, pero no sabes cuánto te queda después de pagarlo todo.',
              'Pones los precios a ojo o copiando a la competencia.',
              'Te enteras tarde de que una clienta fija ya no viene.'],
    'steps_title': 'Así sabes cuánto ganas',
    'steps': [('Tus gastos, sin teclear', 'Haz una foto a la factura o sube el extracto del banco: la IA registra cada gasto con su IVA y su categoría.'),
              ('El precio justo de cada tratamiento', 'Calcula cuánto te cuesta de verdad cada servicio y qué precio cobrar para ganar lo que quieres.'),
              ('Tu gestor cada mañana', 'A las 8:00, hasta 3 recomendaciones: citas sin cobrar, huecos en la agenda o clientes que no vuelven.')],
    'note': 'Gastos y precios están en los planes Pro y Max, y en la prueba gratuita.',
  },
}

EXTRAS = [('🧾', 'Verifactu integrado', 'Cobras la cita y el tique ya está en Hacienda.'),
          ('🚗', 'También a domicilio', 'El desplazamiento se calcula solo y se suma al precio.'),
          ('🎁', 'Tarjetas regalo', 'Véndelas desde tu página de reservas, sin hacer nada más.')]

FAQ = [('¿Cuánto cuesta?', 'Desde 33 €/mes (24,75 €/mes con pago anual). Los 30 primeros días son gratis y no te pedimos tarjeta.'),
       ('¿Hay permanencia?', 'No. Te vas cuando quieras.'),
       ('¿Mis clientes tienen que descargarse una app?', 'No. Reservan desde un enlace, en el móvil o en el ordenador.'),
       ('¿Es un lío cambiar de programa?', 'No. Importas tus servicios y tu equipo desde Excel o una captura de pantalla, y los servicios también desde tu enlace de Treatwell, Booksy o Fresha.'),
       ('¿Cumple con Verifactu?', 'Sí. Cada cobro se envía solo a Hacienda con su tique y código QR. Se activa con la suscripción de pago; durante la prueba gratuita no está activo.')]

CSS = r'''
:root{--v:#631cff;--v2:#9B4FE8;--ink:#02021e;--soft:#f8f7ff;--line:rgba(99,28,255,.12);--muted:rgba(2,2,30,.66);--y:#EEFE3A;}
*{box-sizing:border-box;}
html,body{margin:0;background:#fff;color:var(--ink);font-family:'Plus Jakarta Sans',system-ui,sans-serif;-webkit-font-smoothing:antialiased;}
img{max-width:100%;height:auto;display:block;}
a{color:inherit;}
.w{max-width:1080px;margin:0 auto;padding:0 20px;}
.g{font-family:'Gabarito',sans-serif;}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:var(--y);color:var(--ink);font-weight:800;font-size:17px;padding:17px 28px;border-radius:999px;text-decoration:none;box-shadow:0 10px 30px rgba(20,5,60,.25);transition:transform .15s;}
.btn:active{transform:scale(.98);}
.btn--v{background:linear-gradient(90deg,var(--v2),var(--v));color:#fff;box-shadow:0 10px 30px rgba(99,28,255,.3);}
.note{font-size:13.5px;opacity:.8;margin-top:12px;}
/* top */
.top{position:absolute;top:0;left:0;right:0;z-index:5;padding:18px 0;}
.top img{height:30px;width:auto;}
/* hero */
.hero{background:linear-gradient(160deg,#9B4FE8 0%,#7835C3 30%,#631cff 65%,#3a0aaa 100%);color:#fff;padding:84px 0 0;overflow:hidden;position:relative;}
.hero .grid{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:end;}
.eyebrow{display:inline-block;font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;background:rgba(255,255,255,.14);padding:7px 12px;border-radius:999px;}
.hero h1{font-family:'Gabarito',sans-serif;font-size:clamp(31px,5vw,52px);line-height:1.06;letter-spacing:-.02em;margin:16px 0 14px;}
.hero .sub{font-size:clamp(16.5px,2vw,19px);line-height:1.55;color:rgba(255,255,255,.9);margin:0 0 24px;max-width:560px;}
.hero .txt{padding-bottom:56px;}
.vis{display:flex;justify-content:center;}
.phone{width:min(300px,78vw);border-radius:38px 38px 0 0;border:10px solid #0d0627;border-bottom:0;background:#fff;overflow:hidden;box-shadow:0 30px 70px rgba(10,0,40,.45);max-height:430px;}
.phone img{width:100%;}
/* whatsapp */
.wa{background:#efeae2;min-height:420px;font-size:14px;}
.wa__top{display:flex;gap:10px;align-items:center;background:#075e54;color:#fff;padding:14px 14px;}
.wa__top small{display:block;font-size:11.5px;opacity:.8;}
.wa__av{width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,var(--v2),var(--v));display:flex;align-items:center;justify-content:center;font-weight:800;}
.wa__body{padding:14px;display:flex;flex-direction:column;gap:9px;}
.wa__day{align-self:center;background:#fff;color:#667;font-size:11px;padding:4px 10px;border-radius:8px;}
.wa__msg{background:#fff;color:#111;border-radius:4px 14px 14px 14px;padding:10px 12px;max-width:90%;line-height:1.45;box-shadow:0 1px 1px rgba(0,0,0,.06);}
.wa__msg small{display:block;text-align:right;color:#8a8a8a;font-size:11px;margin-top:4px;}
.wa__me{align-self:flex-end;background:#d9fdd3;border-radius:14px 4px 14px 14px;}
.wa__btns{display:flex;gap:6px;max-width:90%;}
.wa__btns span{flex:1;text-align:center;background:#fff;border-radius:10px;padding:9px;color:#0a7cff;font-weight:700;font-size:13px;}
/* sections */
.sec{padding:64px 0;}
.sec--soft{background:var(--soft);}
.h2{font-family:'Gabarito',sans-serif;font-size:clamp(27px,3.6vw,40px);line-height:1.1;letter-spacing:-.01em;margin:0 0 22px;}
.grad{background:linear-gradient(90deg,var(--v2),var(--v));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;}
.pains{list-style:none;padding:0;margin:0;display:grid;gap:12px;max-width:680px;}
.pains li{display:flex;gap:12px;align-items:flex-start;font-size:17px;line-height:1.45;background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px 18px;}
.pains li::before{content:"✕";flex:0 0 26px;height:26px;border-radius:50%;background:#ffe4e6;color:#be123c;font-weight:800;font-size:13px;display:flex;align-items:center;justify-content:center;}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;}
.step{background:var(--soft);border:1px solid var(--line);border-radius:22px;padding:24px;}
.step b{font-family:'Gabarito',sans-serif;font-size:44px;line-height:1;display:block;margin-bottom:10px;}
.step h3{font-family:'Gabarito',sans-serif;font-size:21px;margin:0 0 8px;}
.step p{margin:0;color:var(--muted);line-height:1.55;font-size:15.5px;}
.small{font-size:13.5px;color:var(--muted);margin:16px 0 0;}
.extras{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
.ex{display:flex;gap:12px;align-items:flex-start;background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px;}
.ex i{font-style:normal;font-size:24px;line-height:1;}
.ex b{display:block;font-size:16px;margin-bottom:3px;}
.ex span{color:var(--muted);font-size:14.5px;line-height:1.45;}
.me{display:flex;gap:22px;align-items:flex-start;background:linear-gradient(160deg,#1b0b4d,#0c0628);color:#fff;border-radius:26px;padding:32px;}
.me__av{flex:0 0 72px;width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,var(--v2),var(--v));display:flex;align-items:center;justify-content:center;font-family:'Gabarito',sans-serif;font-size:32px;font-weight:800;border:3px solid rgba(255,255,255,.25);}
.me p{margin:0 0 10px;font-size:17px;line-height:1.6;color:rgba(255,255,255,.9);}
.me .sig{font-weight:700;color:var(--y);margin:0;}
.faq{max-width:760px;}
.faq details{border-bottom:1px solid var(--line);padding:16px 0;}
.faq summary{cursor:pointer;font-weight:700;font-size:17px;list-style:none;display:flex;justify-content:space-between;gap:12px;}
.faq summary::after{content:"+";color:var(--v);font-size:22px;line-height:1;}
.faq details[open] summary::after{content:"–";}
.faq p{margin:10px 0 0;color:var(--muted);line-height:1.6;}
.final{background:linear-gradient(160deg,#9B4FE8 0%,#631cff 65%,#3a0aaa 100%);color:#fff;text-align:center;border-radius:28px;padding:44px 24px;}
.final h2{font-family:'Gabarito',sans-serif;font-size:clamp(28px,4vw,42px);line-height:1.1;margin:0 0 12px;}
.final p{margin:0 auto 24px;max-width:520px;color:rgba(255,255,255,.88);line-height:1.55;}
.alt{display:block;margin-top:18px;color:#fff;font-weight:600;font-size:15px;}
.alt span{text-decoration:underline;}
.foot{padding:28px 0 100px;text-align:center;font-size:13px;color:var(--muted);}
.foot a{margin:0 8px;color:var(--muted);}
.sticky{position:fixed;left:12px;right:12px;bottom:12px;z-index:9000;display:none;}
.sticky .btn{width:100%;}
.sticky.on{display:block;}
@media(max-width:860px){
  .hero{padding-top:76px;}
  .hero .grid{grid-template-columns:1fr;gap:28px;}
  .hero .txt{padding-bottom:0;}
  .hero .btn{width:100%;}
  .steps,.extras{grid-template-columns:1fr;}
  .me{flex-direction:column;padding:26px 22px;}
  .sec{padding:52px 0;}
}
@media(min-width:861px){.sticky{display:none!important;}}
'''

HEAD_COMMON = None


def head_common():
    src = open('dashboard-ia/index.html', encoding='utf-8').read()
    return src.split('<meta charset="UTF-8">')[0]


def page(slug, d):
    hc = head_common()
    pains = ''.join(f'<li>{html.escape(p)}</li>' for p in d['pains'])
    steps = ''.join(f'<div class="step"><b class="grad">0{i}</b><h3>{html.escape(t)}</h3><p>{html.escape(x)}</p></div>' for i, (t, x) in enumerate(d['steps'], 1))
    extras = ''.join(f'<div class="ex"><i>{e}</i><div><b>{html.escape(t)}</b><span>{html.escape(x)}</span></div></div>' for e, t, x in EXTRAS)
    faq = ''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in FAQ)
    note = f'<p class="small">{html.escape(d["note"])}</p>' if d.get('note') else ''
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    cta = lambda pos, cls='btn': f'<a class="{cls}" href="{SIGNUP}" data-cta="{pos}">Prueba gratis 30 días</a>'
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
{hc.split('<head>',1)[1].strip()}
<meta charset="UTF-8">
<title>{html.escape(d['title'])}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{html.escape(d['desc'])}">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://www.godolphy.com/lp/{slug}/">
<meta property="og:title" content="{html.escape(d['h1'])}">
<meta property="og:description" content="{html.escape(d['desc'])}">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body data-lp="{slug}">
<header class="top"><div class="w"><img src="/dashboard-ia/img/godolphy-white.png" alt="Godolphy" width="140" height="30"></div></header>

<main>
<section class="hero">
  <div class="w grid">
    <div class="txt">
      <span class="eyebrow">Para centros de estética</span>
      <h1>{html.escape(d['h1'])}</h1>
      <p class="sub">{html.escape(d['sub'])}</p>
      {cta('hero')}
      <div class="note">30 días gratis · Sin tarjeta · Sin permanencia</div>
    </div>
    <div class="vis">{d['visual']}</div>
  </div>
</section>

<section class="sec sec--soft">
  <div class="w">
    <h2 class="h2">¿Te suena?</h2>
    <ul class="pains">{pains}</ul>
  </div>
</section>

<section class="sec">
  <div class="w">
    <h2 class="h2">{html.escape(d['steps_title'])} <span class="grad">con Godolphy</span></h2>
    <div class="steps">{steps}</div>
    {note}
    <div style="margin-top:28px;">{cta('steps', 'btn btn--v')}</div>
  </div>
</section>

<section class="sec sec--soft">
  <div class="w">
    <h2 class="h2">Y además, en el mismo sitio</h2>
    <div class="extras">{extras}</div>
  </div>
</section>

<section class="sec">
  <div class="w">
    <div class="me">
      <div class="me__av" aria-hidden="true">N</div>
      <div>
        <p>Soy Neus. He trabajado en multinacionales y monté mi propio centro con una socia, donde yo llevaba la parte de negocio.</p>
        <p>Godolphy es la herramienta que me habría gustado tener: para que tu centro funcione como un negocio, no solo como una agenda.</p>
        <p class="sig">Neus, fundadora de Godolphy</p>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--soft">
  <div class="w">
    <h2 class="h2">Preguntas antes de empezar</h2>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="sec">
  <div class="w">
    <div class="final">
      <h2>Pruébalo 30 días en tu centro</h2>
      <p>Configúralo en una tarde y compruébalo con tus clientes. Si no te convence, no pagas nada.</p>
      {cta('final')}
      <a class="alt" href="{DASH}" data-cta="dashboard">¿Aún no? <span>Analiza tu centro gratis en 2 minutos</span></a>
    </div>
  </div>
</section>
</main>

<footer class="foot"><div class="w">© 2026 Godolphy · <a href="/politica-de-privacidad/">Privacidad</a><a href="/politica-de-cookies/">Cookies</a><a href="/aviso-legal/">Aviso legal</a></div></footer>

<div class="sticky" id="sticky">{cta('sticky')}</div>

<script>
(function(){{
  var lp=document.body.getAttribute('data-lp'),st=document.getElementById('sticky'),hero=document.querySelector('.hero');
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


if __name__ == '__main__':
    for slug, d in LPS.items():
        os.makedirs(f'lp/{slug}', exist_ok=True)
        open(f'lp/{slug}/index.html', 'w', encoding='utf-8').write(page(slug, d))
        print('ok', slug)
