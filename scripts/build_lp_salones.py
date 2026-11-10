#!/usr/bin/env python3
"""Landing larga de venta para anuncios: /lp/salones/ (genérica para salones).

Estructura tipo «long-form sales page»: hero → ¿te suena? → quién hay detrás (Neus) →
todo en un software → funcionalidad a funcionalidad → así se ve por dentro → comparativa →
3 pasos → precios → lo que NO es → sin riesgo → FAQ → cierre.
No indexable (noindex). Uso: python3 scripts/build_lp_salones.py
"""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_lp import CSS, SIGNUP, DASH, WA_MOCK, head_common

SLUG = 'salones'
IMG = f'/lp/{SLUG}/'
e = html.escape

PAINS = [
    ('Cada año, igual que el anterior', 'Trabajas mucho, facturas parecido y no sabes qué tocar para avanzar.'),
    ('Clientes que no se presentan', 'Una hora vacía que pagas igual y que ya no recuperas.'),
    ('Clientes fijos que dejan de venir', 'Y te enteras cuando ya hace dos meses que no aparecen.'),
    ('Precios puestos a ojo', 'Copiados de la competencia, sin saber cuánto te deja cada servicio.'),
    ('WhatsApp a las once de la noche', 'Contestando para dar una cita en lugar de descansar.'),
    ('Facturas, pero ¿cuánto te queda?', 'Después de alquiler, producto, equipo y gastos, nadie te lo dice.'),
]

OVERVIEW = [
    ('📅', 'Reservas y agenda', 'Tu enlace de reservas 24 h, calendario por profesional y citas que se mueven arrastrando.'),
    ('💳', 'Cobros sin plantones', 'Señal al reservar, recordatorio por WhatsApp y política de cancelación.'),
    ('✦', 'Análisis con IA', 'Cada mes, qué servicios te hacen ganar dinero y qué clientes estás perdiendo.'),
    ('📈', 'Plan financiero', 'Objetivos mes a mes comparados con lo real, como en las grandes empresas.'),
    ('👥', 'Equipo y comisiones', 'Horarios, ausencias, recepción con su acceso y comisiones calculadas solas.'),
    ('🎁', 'Vende más', 'Tarjetas regalo, bonos de sesiones, precio según día y hora y domicilios.'),
]

# (eyebrow, título, texto, bullets, imagen, alt)
FEATURES = [
    ('Tu reserva, no la suya', 'Tus clientes reservan solos, a cualquier hora',
     'Tu propia página de reservas, con tu nombre y tus servicios. Pon el enlace en Instagram y en Google y deja de dar citas por WhatsApp.',
     ['Sin comisiones por reserva: el cliente es tuyo, no de un marketplace.',
      'Varias personas, servicios y profesionales en una sola reserva y un solo pago.',
      'El cliente cambia su cita solo, sin llamarte.'],
     'z-cal', 'Agenda de Godolphy en el móvil'),
    ('Adiós a los plantones', 'Si no viene, la señal se queda en tu cuenta',
     'Cobras una señal al reservar y el día antes le llega un WhatsApp para confirmar o cambiar la cita. Tú no llamas a nadie.',
     ['Señal o pago completo al reservar, con Stripe y directo a tu cuenta.',
      'Política de cancelación: tú decides hasta cuándo se puede cancelar.',
      'Recordatorio automático por WhatsApp 24 h antes.'],
     'WA', ''),
    ('Tu negocio entendido cada mes', 'La IA te dice qué servicio te hace ganar dinero',
     'Cuánto te deja de verdad cada servicio después de producto y tiempo. Qué clientes están dejando de venir. Y qué hacer este mes, con el impacto en euros.',
     ['Rentabilidad por servicio y por profesional.',
      'Clientes en riesgo antes de perderlos.',
      'Cada mañana, hasta tres cosas que hacer hoy para ganar más.'],
     'd1', 'Rendimiento por servicio en Godolphy'),
    ('Como una gran empresa', 'Tu plan financiero, hecho con tus datos',
     'Eliges cuánto quieres crecer y cada mes ves si vas por delante o por detrás, y qué tocar para llegar. Citas, ticket medio, gastos, clientes nuevos, CAC y LTV.',
     ['Plan contra real, mes a mes.',
      'Tus gastos sin teclear: foto a la factura o extracto del banco.',
      'La calculadora de precios te dice cuánto cobrar para ganar lo que quieres.'],
     'd2', 'Plan financiero mes a mes en Godolphy'),
    ('Gana más con las mismas horas', 'Precio según el día y la hora',
     'Un recargo en las horas que todo el mundo quiere y un descuento para llenar las horas flojas. Tus clientes ven siempre el precio final al reservar.',
     ['Por día de la semana y franja horaria.',
      'Aplicable a servicios y extras.',
      'Las citas ya reservadas no cambian de precio.'],
     'd3', 'Precio según día y hora en Godolphy'),
    ('Domicilio sin líos', 'Domicilios con el desplazamiento calculado',
     'Si tienes horas libres en el equipo, ábrelas a domicilios cerca de tu salón. Tú defines las zonas y el precio por kilómetro; Godolphy calcula el desplazamiento y solo ofrece las horas a las que se llega a tiempo.',
     ['Precio por km y recargo por hotel, hospital o casa.',
      'El tiempo entre citas, calculado solo en la agenda.',
      'Local y domicilio en el mismo calendario.'],
     'd4', 'Domicilios con desplazamiento en Godolphy'),
]

SCREENS = [('s-cal', 'Calendario', 'La agenda de todo el equipo, por profesional y local.'),
           ('s-ana', 'Análisis con IA', 'Facturación, clientes nuevos y la conclusión del mes.'),
           ('s-book', 'Página de reservas', 'Lo que ve tu cliente: elige servicio, profesional, día y hora.'),
           ('s-cli', 'Clientes', 'Quién vale más, quién está en riesgo y qué oportunidades tienes.')]

COMPARE = [('Reservas online y recordatorios', True, True),
           ('Señal al reservar', True, True),
           ('Cuánto te deja cada servicio', False, True),
           ('Clientes en riesgo antes de perderlos', False, True),
           ('Plan financiero con tus datos', False, True),
           ('Precio según día y hora', False, True),
           ('Domicilio con desplazamiento calculado', False, True),
           ('Sin comisiones por cliente nuevo', False, True)]

NOT = [('No es un marketplace', 'Tus clientes no ven a tu competencia al reservar ni te cobramos comisión por ellos.'),
       ('No es solo una agenda', 'Además de dar citas, te dice dónde ganas y dónde pierdes dinero.'),
       ('No es un lío técnico', 'Si sabes usar WhatsApp, sabes usar Godolphy.'),
       ('No es una permanencia', 'Te vas cuando quieras, sin letra pequeña.')]

PLANS = [('Solo', '33', 'Para quien trabaja sola o solo', ['1 profesional', 'Reservas online y agenda', 'Pagos y señal del 20 %', 'Recordatorios WhatsApp', 'Análisis IA mensual'], False),
         ('Pro', '45', 'Para equipos que quieren crecer', ['Desde 2 profesionales', 'Todo lo de Solo', 'Gastos, precios y plan financiero', 'Precio según día y hora', 'Tarjetas regalo, bonos y comisiones', 'Análisis IA semanal'], True),
         ('Max', '360', 'Para cadenas y franquicias', ['Incluye 20 profesionales', 'Todo lo de Pro', 'Onboarding 1:1 y migración', 'Account manager', 'Análisis IA diario'], False)]

FAQ = [('¿Cuánto cuesta?', 'Desde 33 €/mes, y un 25 % menos con pago anual. Los 30 primeros días son gratis, con el plan Pro completo y sin tarjeta.'),
       ('¿Hay permanencia?', 'No. Te vas cuando quieras.'),
       ('¿Sirve para mi tipo de salón?', 'Sí: peluquerías, centros de estética, salones de uñas, barberías, masajes y profesionales a domicilio.'),
       ('¿Mis clientes tienen que descargarse una app?', 'No. Reservan desde un enlace, en el móvil o en el ordenador.'),
       ('¿Es un lío cambiar de programa?', 'No. Importas tus servicios y tu equipo desde Excel o una captura de pantalla, y los servicios también desde tu enlace de Treatwell, Booksy o Fresha.'),
       ('¿Qué hace exactamente la IA?', 'Lee tus reservas, cobros y gastos y te dice, en lenguaje normal, qué servicios te dejan margen, qué clientes están dejando de venir y qué hacer para ganar más.'),
       ('¿Los cobros pasan por Godolphy?', 'No. Conectas tu cuenta de Stripe y el dinero va directo a tu cuenta. Godolphy no se queda comisión de tus cobros.'),
       ('¿Cumple con Verifactu?', 'Sí. Cada cobro se envía solo a Hacienda con su tique y código QR. Se activa con la suscripción de pago; durante la prueba gratuita no está activo.')]

EXTRA_CSS = r'''
html{scroll-behavior:smooth;}
.nav{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);}
.nav .w{display:flex;align-items:center;justify-content:space-between;height:64px;}
.nav img{height:26px;width:auto;}
.nav .links{display:flex;gap:24px;align-items:center;font-size:14.5px;font-weight:600;}
.nav .links a{text-decoration:none;color:rgba(2,2,30,.7);}
.nav .nbtn{background:linear-gradient(90deg,var(--v2),var(--v));color:#fff!important;padding:10px 18px;border-radius:999px;}
.hero{padding-top:64px;}
.hero .grid{align-items:center;}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px;}
.chips span{font-size:13px;font-weight:700;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.22);padding:7px 12px;border-radius:999px;}
.hero .vis img{width:100%;max-width:560px;border-radius:22px;filter:drop-shadow(0 30px 60px rgba(10,0,40,.45));}
.hero .txt{padding-bottom:64px;}
.lead2{font-size:18px;line-height:1.6;color:var(--muted);max-width:680px;margin:0 0 34px;}
.ctr{text-align:center;}.ctr .lead2{margin-left:auto;margin-right:auto;}
.eb{display:inline-block;font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--v);background:#efe9ff;padding:6px 12px;border-radius:999px;margin-bottom:14px;}
.painsg{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
.pain{background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px;}
.pain b{display:flex;gap:10px;align-items:center;font-size:17px;margin-bottom:6px;}
.pain b::before{content:"✕";flex:0 0 24px;height:24px;border-radius:50%;background:#ffe4e6;color:#be123c;font-size:12px;display:flex;align-items:center;justify-content:center;}
.pain span{color:var(--muted);line-height:1.5;font-size:15px;}
.punch{font-family:'Gabarito',sans-serif;font-size:clamp(22px,2.6vw,28px);line-height:1.25;max-width:760px;margin:36px auto 0;text-align:center;}
.story{display:grid;grid-template-columns:.85fr 1.15fr;gap:48px;align-items:center;}
.story img{border-radius:28px;width:100%;}
.story p{font-size:17.5px;line-height:1.7;color:rgba(2,2,30,.8);margin:0 0 16px;}
.story b{color:var(--ink);}
.story blockquote{margin:22px 0 0;padding:18px 20px;border-left:4px solid var(--v);background:var(--soft);border-radius:0 16px 16px 0;font-style:italic;color:rgba(2,2,30,.8);line-height:1.6;}
.story blockquote small{display:block;font-style:normal;font-weight:700;margin-top:8px;color:var(--ink);}
.sig2{font-family:'Gabarito',sans-serif;font-weight:700;font-size:18px;color:var(--v);margin:14px 0 0;}
.ov{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}
.ovc{background:#fff;border:1px solid var(--line);border-radius:22px;padding:24px;}
.ovc i{font-style:normal;font-size:26px;display:block;margin-bottom:12px;color:var(--v);}
.ovc h3{font-family:'Gabarito',sans-serif;font-size:21px;margin:0 0 6px;}
.ovc p{margin:0;color:var(--muted);line-height:1.55;font-size:15px;}
.ft{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center;max-width:980px;margin:0 auto 84px;}
.ft:last-child{margin-bottom:0;}
.ft.rev .ft__img{order:2;}
.ft__img{display:flex;justify-content:center;}
.ft__img img{width:100%;max-width:380px;border-radius:22px;}
.ft__img .phone{max-height:470px;}
.ft h3{font-family:'Gabarito',sans-serif;font-size:clamp(26px,3vw,34px);line-height:1.1;margin:0 0 12px;}
.ft p{margin:0 0 16px;font-size:17px;line-height:1.6;color:rgba(2,2,30,.75);}
.ft ul{list-style:none;padding:0;margin:0;display:grid;gap:9px;}
.ft li{display:flex;gap:10px;line-height:1.45;font-size:15.5px;}
.ft li::before{content:"✓";flex:0 0 22px;height:22px;border-radius:50%;background:#efe9ff;color:var(--v);font-weight:800;font-size:12px;display:flex;align-items:center;justify-content:center;margin-top:1px;}
.sectors{display:grid;grid-template-columns:1.3fr 1fr .75fr .75fr;gap:12px;margin-top:8px;}
.sectors figure{margin:0;position:relative;border-radius:20px;overflow:hidden;height:260px;}
.sectors img{width:100%;height:100%;object-fit:cover;}
.sectors figcaption{position:absolute;left:12px;bottom:12px;background:rgba(255,255,255,.92);font-weight:700;font-size:13.5px;padding:6px 12px;border-radius:999px;}
.tabs{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-bottom:22px;}
.tabs button{font:inherit;font-weight:700;font-size:15px;border:1px solid var(--line);background:#fff;color:var(--ink);padding:10px 18px;border-radius:999px;cursor:pointer;}
.tabs button.on{background:var(--v);color:#fff;border-color:var(--v);}
.scr{max-width:980px;margin:0 auto;}
.scr figure{margin:0;display:none;}
.scr figure.on{display:block;}
.scr img{width:100%;border-radius:18px;border:1px solid var(--line);box-shadow:0 24px 60px rgba(40,10,120,.15);}
.scr figcaption{text-align:center;color:var(--muted);font-size:15px;margin-top:14px;}
.cmp{max-width:760px;margin:0 auto;border:1px solid var(--line);border-radius:22px;overflow:hidden;background:#fff;}
.cmp table{width:100%;border-collapse:collapse;font-size:15.5px;}
.cmp th,.cmp td{padding:14px 16px;border-bottom:1px solid var(--line);text-align:center;}
.cmp th:first-child,.cmp td:first-child{text-align:left;}
.cmp thead th{font-family:'Gabarito',sans-serif;font-size:17px;background:var(--soft);}
.cmp thead th:last-child{background:var(--v);color:#fff;}
.cmp tr:last-child td{border-bottom:0;}
.cmp .y{color:var(--v);font-weight:800;font-size:18px;}
.cmp .n{color:#c4c2d4;font-weight:800;font-size:18px;}
.cmp td:last-child{background:#faf8ff;}
.plans{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;align-items:stretch;max-width:1000px;margin:0 auto;}
.plan{background:#fff;border:1px solid var(--line);border-radius:24px;padding:28px;display:flex;flex-direction:column;}
.plan.pop{border:2px solid var(--v);box-shadow:0 24px 60px rgba(99,28,255,.18);position:relative;}
.plan.pop::before{content:"Más popular";position:absolute;top:-13px;left:24px;background:var(--y);font-size:12px;font-weight:800;padding:5px 12px;border-radius:999px;}
.plan h3{font-family:'Gabarito',sans-serif;font-size:24px;margin:0;}
.plan .for{color:var(--muted);font-size:14.5px;margin:4px 0 16px;}
.plan .pr{font-family:'Gabarito',sans-serif;font-size:46px;font-weight:800;line-height:1;}
.plan .pr small{font-size:16px;font-weight:600;color:var(--muted);}
.plan ul{list-style:none;padding:0;margin:20px 0 24px;display:grid;gap:9px;flex:1;}
.plan li{font-size:15px;display:flex;gap:9px;}
.plan li::before{content:"✓";color:var(--v);font-weight:800;}
.plan .btn{width:100%;font-size:16px;padding:15px 20px;}
.nots{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;max-width:880px;margin:0 auto;}
.notc{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:18px;padding:20px 22px;}
.notc b{display:block;font-size:17px;margin-bottom:5px;}
.notc b::before{content:"✕ ";color:#ff8fa3;}
.notc span{color:rgba(255,255,255,.78);line-height:1.5;font-size:15px;}
.dark{background:linear-gradient(160deg,#1b0b4d,#0c0628);color:#fff;}
.dark .h2{color:#fff;}
.steps3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;}
.risk{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;max-width:900px;margin:0 auto;}
.risk div{text-align:center;padding:22px;background:var(--soft);border-radius:20px;border:1px solid var(--line);}
.risk b{display:block;font-family:'Gabarito',sans-serif;font-size:28px;color:var(--v);}
.risk span{color:var(--muted);font-size:15px;}
.cap{font-size:12.5px;color:var(--muted);text-align:center;margin-top:8px;}
@media(max-width:860px){
  .nav .links a:not(.nbtn){display:none;}
  .painsg,.ov,.steps3,.plans,.nots,.risk{grid-template-columns:1fr;}
  .story{grid-template-columns:1fr;gap:26px;}
  .story img{max-width:420px;margin:0 auto;}
  .ft{grid-template-columns:1fr;gap:24px;margin-bottom:64px;}
  .ft.rev .ft__img{order:0;}
  .sectors{grid-template-columns:1fr 1fr;}
  .sectors figure{height:190px;}
  .cmp th,.cmp td{padding:12px 10px;font-size:14px;}
  .hero .txt{padding-bottom:0;}
  .hero .vis{padding-bottom:32px;}
}
'''


def build():
    hc = head_common()
    cta = lambda pos, cls='btn': f'<a class="{cls}" href="{SIGNUP}" data-cta="{pos}">Prueba gratis 30 días →</a>'
    pains = ''.join(f'<div class="pain"><b>{e(t)}</b><span>{e(x)}</span></div>' for t, x in PAINS)
    ov = ''.join(f'<div class="ovc"><i>{i}</i><h3>{e(t)}</h3><p>{e(x)}</p></div>' for i, t, x in OVERVIEW)
    feats = ''
    for n, (eb, t, x, bl, img, alt) in enumerate(FEATURES):
        vis = WA_MOCK if img == 'WA' else f'<img src="{IMG}{img}.webp" alt="{e(alt)}" width="520" height="600" loading="lazy">'
        lis = ''.join(f'<li>{e(b)}</li>' for b in bl)
        feats += f'<div class="ft{" rev" if n % 2 else ""}"><div class="ft__img">{vis}</div><div><span class="eb">{e(eb)}</span><h3>{e(t)}</h3><p>{e(x)}</p><ul>{lis}</ul></div></div>'
    tabs = ''.join(f'<button type="button" data-t="{i}" class="{"on" if i == 0 else ""}">{e(t)}</button>' for i, (_, t, _x) in enumerate(SCREENS))
    scr = ''.join(f'<figure data-t="{i}" class="{"on" if i == 0 else ""}"><img src="{IMG}{f}.webp" alt="{e(t)} de Godolphy" width="1400" height="875" loading="lazy"><figcaption>{e(x)} <span style="opacity:.7">· Datos de ejemplo</span></figcaption></figure>' for i, (f, t, x) in enumerate(SCREENS))
    mark = lambda v: '<span class="y">✓</span>' if v else '<span class="n">—</span>'
    cmp = ''.join(f'<tr><td>{e(r)}</td><td>{mark(a)}</td><td>{mark(b)}</td></tr>' for r, a, b in COMPARE)
    plans = ''
    for name, price, for_, items, pop in PLANS:
        lis = ''.join(f'<li>{e(i)}</li>' for i in items)
        plans += f'<div class="plan{" pop" if pop else ""}"><h3>{name}</h3><p class="for">{e(for_)}</p><div class="pr">{price} €<small> /mes</small></div><ul>{lis}</ul>{cta("plan-" + name.lower(), "btn btn--v" if pop else "btn")}</div>'
    nots = ''.join(f'<div class="notc"><b>{e(t)}</b><span>{e(x)}</span></div>' for t, x in NOT)
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}

    page = f'''<!DOCTYPE html>
<html lang="es">
<head>
{hc.split('<head>', 1)[1].strip()}
<meta charset="UTF-8">
<title>Godolphy · El software de gestión con IA para tu salón</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Reservas, cobros sin plantones, equipo y, cada mes, la IA te dice dónde ganas y dónde pierdes dinero. 30 días gratis, sin tarjeta.">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://www.godolphy.com/lp/{SLUG}/">
<meta property="og:title" content="Gestiona tu salón como lo haría una gran empresa">
<meta property="og:description" content="El software de gestión con IA para salones. 30 días gratis, sin tarjeta.">
<meta property="og:image" content="https://www.godolphy.com/lp/{SLUG}/app.webp">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}{EXTRA_CSS}</style>
</head>
<body data-lp="{SLUG}">
<header class="nav"><div class="w">
  <img src="/wp-images/logo-gradient.png" alt="Godolphy" width="140" height="30">
  <nav class="links"><a href="#funciones">Qué hace</a><a href="#neus">Quién hay detrás</a><a href="#precios">Precios</a><a href="#faq">Preguntas</a><a class="nbtn" href="{SIGNUP}" data-cta="nav">Pruébalo gratis</a></nav>
</div></header>

<main>
<section class="hero">
  <div class="w grid">
    <div class="txt">
      <span class="eyebrow">Software de gestión con IA para salones</span>
      <h1>Gestiona tu salón como lo haría una gran empresa.</h1>
      <p class="sub">Reservas, cobros sin plantones y tu equipo en un solo sitio. Y cada mes, la IA te dice dónde ganas y dónde pierdes dinero.</p>
      {cta('hero')}
      <div class="chips"><span>30 días gratis</span><span>Sin tarjeta</span><span>Sin permanencia</span><span>Sin comisiones por reserva</span></div>
    </div>
    <div class="vis"><img src="{IMG}app.webp" alt="Panel de Godolphy en el ordenador y en el móvil" width="1040" height="760" fetchpriority="high"></div>
  </div>
</section>

<section class="sec sec--soft">
  <div class="w">
    <div class="ctr"><span class="eb">¿Te suena?</span>
    <h2 class="h2">Tu salón funciona. Pero no avanza.</h2></div>
    <div class="painsg">{pains}</div>
    <p class="punch">No es que trabajes poco. Es que tu programa de reservas solo te da una agenda, <span class="grad">y una agenda no te dice cómo ganar más.</span></p>
  </div>
</section>

<section class="sec" id="neus">
  <div class="w story">
    <img src="{IMG}neus.webp" alt="Neus, fundadora de Godolphy" width="798" height="997" loading="lazy">
    <div>
      <span class="eb">Quién hay detrás</span>
      <h2 class="h2">Hola, soy Neus.</h2>
      <p>Llevo unos 15 años trabajando en marketing en multinacionales, en campañas para empresas grandes. Allí aprendí cómo funciona un negocio que crece: <b>mira sus números cada mes, sabe qué le da dinero y trabaja para que el cliente vuelva.</b></p>
      <p>Después monté mi propio salón con una socia. Yo llevaba la parte de negocio y apliqué lo mismo que hacen las grandes empresas.</p>
      <p>Ahí vi el problema: <b>un salón pequeño no crece porque nadie le aplica esas estrategias.</b> Se trata como un oficio, no como una empresa. Y los programas de reservas que existen solo te dan una agenda.</p>
      <p>Por eso he creado Godolphy: el software de gestión que me habría gustado tener. Todo lo que aprendí en las grandes empresas, metido en un solo sitio y pensado para salones pequeños y medianos.</p>
      <blockquote>«Hemos mejorado muchísimo el tiempo de transporte entre servicios y aumentado el número de servicios diarios por profesional.»<small>Probado primero en mi propio salón</small></blockquote>
      <p class="sig2">Neus, fundadora de Godolphy</p>
    </div>
  </div>
</section>

<section class="sec sec--soft" id="funciones">
  <div class="w">
    <div class="ctr"><span class="eb">Todo en un solo software</span>
    <h2 class="h2">Lo que ya esperas de un programa de reservas. <span class="grad">Y todo lo que le falta.</span></h2></div>
    <div class="ov">{ov}</div>
  </div>
</section>

<section class="sec">
  <div class="w">{feats}
    <div class="ctr" style="margin-top:64px;">{cta('features', 'btn btn--v')}<p class="note" style="color:var(--muted);">30 días con el plan Pro completo · Sin tarjeta</p></div>
  </div>
</section>

<section class="sec sec--soft">
  <div class="w">
    <div class="ctr"><span class="eb">Para cualquier tipo de salón</span>
    <h2 class="h2">Peluquerías, estética, uñas, barberías y masajes</h2>
    <p class="lead2">Con local, a domicilio o las dos cosas. Tú sola o con un equipo de veinte.</p></div>
    <div class="sectors">
      <figure><img src="{IMG}f-pelu.webp" alt="Peluquería" loading="lazy"><figcaption>Peluquerías</figcaption></figure>
      <figure><img src="{IMG}f-unas.webp" alt="Salón de uñas" loading="lazy"><figcaption>Uñas y estética</figcaption></figure>
      <figure><img src="{IMG}f-barber.webp" alt="Barbería" loading="lazy"><figcaption>Barberías</figcaption></figure>
      <figure><img src="{IMG}f-movil.webp" alt="Reserva desde el móvil" loading="lazy"><figcaption>A domicilio</figcaption></figure>
    </div>
  </div>
</section>

<section class="sec">
  <div class="w">
    <div class="ctr"><span class="eb">Así se ve por dentro</span>
    <h2 class="h2">Godolphy, pantalla a pantalla</h2></div>
    <div class="tabs" id="tabs">{tabs}</div>
    <div class="scr" id="scr">{scr}</div>
  </div>
</section>

<section class="sec sec--soft">
  <div class="w">
    <div class="ctr"><span class="eb">La diferencia</span>
    <h2 class="h2">Una agenda te da citas. <span class="grad">Godolphy te da un negocio.</span></h2></div>
    <div class="cmp"><table><thead><tr><th></th><th>Una agenda de reservas</th><th>Godolphy</th></tr></thead><tbody>{cmp}</tbody></table></div>
  </div>
</section>

<section class="sec">
  <div class="w">
    <div class="ctr"><span class="eb">Más simple de lo que parece</span>
    <h2 class="h2">Empiezas en una tarde</h2></div>
    <div class="steps3">
      <div class="step"><b class="grad">01</b><h3>Crea tu cuenta</h3><p>Solo con tu email. Sin tarjeta y con el plan Pro completo durante 30 días.</p></div>
      <div class="step"><b class="grad">02</b><h3>Importa tus datos</h3><p>Tus servicios y tu equipo desde Excel, una captura de pantalla o tu enlace de Treatwell, Booksy o Fresha.</p></div>
      <div class="step"><b class="grad">03</b><h3>Comparte tu enlace</h3><p>Ponlo en Instagram y en Google. Tus clientes reservan solos y tú empiezas a ver tus números.</p></div>
    </div>
  </div>
</section>

<section class="sec sec--soft" id="precios">
  <div class="w">
    <div class="ctr"><span class="eb">Precios claros</span>
    <h2 class="h2">Sin comisiones. Sin sorpresas.</h2>
    <p class="lead2">Todos empiezan con 30 días gratis del plan Pro. Con pago anual, un 25 % menos.</p></div>
    <div class="plans">{plans}</div>
    <p class="cap" style="margin-top:18px;">Precio final: no se añade IVA. <a href="/precio/">Ver la comparativa completa de planes</a></p>
  </div>
</section>

<section class="sec dark">
  <div class="w">
    <div class="ctr"><h2 class="h2">Lo que Godolphy no es</h2></div>
    <div class="nots">{nots}</div>
  </div>
</section>

<section class="sec">
  <div class="w">
    <div class="ctr"><span class="eb">Sin riesgo</span>
    <h2 class="h2">Pruébalo con tus clientes de verdad</h2>
    <p class="lead2">Configúralo, compártelo y compruébalo en tu salón. Si no te convence, no pagas nada.</p></div>
    <div class="risk"><div><b>30 días</b><span>gratis, con todo el plan Pro</span></div><div><b>0 €</b><span>sin tarjeta para empezar</span></div><div><b>0</b><span>permanencia: te vas cuando quieras</span></div></div>
  </div>
</section>

<section class="sec sec--soft" id="faq">
  <div class="w">
    <h2 class="h2">Preguntas antes de empezar</h2>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="sec">
  <div class="w">
    <div class="final">
      <h2>Una nueva era para los salones, con IA</h2>
      <p>Lo que hacen las grandes empresas, ahora en tu salón. Empieza hoy y en 30 días sabrás más de tu negocio que en todo el año.</p>
      {cta('final')}
      <a class="alt" href="{DASH}" data-cta="dashboard">¿Aún no? <span>Analiza tu salón gratis en 2 minutos</span></a>
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
  var tabs=document.querySelectorAll('#tabs button'),figs=document.querySelectorAll('#scr figure');
  tabs.forEach(function(b){{b.addEventListener('click',function(){{var t=b.getAttribute('data-t');
    tabs.forEach(function(x){{x.classList.toggle('on',x===b);}});figs.forEach(function(f){{f.classList.toggle('on',f.getAttribute('data-t')===t);}});}});}});
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
