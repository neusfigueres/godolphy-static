#!/usr/bin/env python3
"""Landing larga de venta para anuncios: /lp/salones/ (genérica para salones).

Long-form sales page: hero → ¿te suena? → quién hay detrás → todo en un software →
bloques por funcionalidad (con los reels publicados) → plan financiero 2027 → domicilios →
equipo (se va / de baja) → sectores → tour → beneficios → comparativa → 3 pasos → precios →
lo que no es → sin riesgo → FAQ → cierre. No indexable (noindex).
Uso: python3 scripts/build_lp_salones.py
"""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_lp import CSS, SIGNUP, DASH, head_common

SLUG = 'salones'
IMG = f'/lp/{SLUG}/'
e = html.escape

PAINS = [
    ('Cada año, igual que el anterior', 'Trabajas mucho, facturas parecido y no sabes qué tocar para avanzar.'),
    ('Clientes que no se presentan', 'Una hora vacía que pagas igual y que ya no recuperas.'),
    ('Clientes fijos que dejan de venir', 'Y te enteras cuando ya hace dos meses que no aparecen.'),
    ('Una profesional se va a la competencia', 'Y con ella, los clientes que solo tenía en su móvil.'),
    ('Una baja de un día para otro', 'La agenda patas arriba y tú llamando a todo el mundo.'),
    ('Horas muertas en el equipo', 'Sueldos que pagas igual, con la cabina vacía.'),
]

OVERVIEW = [
    ('📅', 'Reservas y agenda', 'Tu enlace de reservas 24 h, calendario por profesional y citas que se mueven arrastrando.'),
    ('💳', 'Cobros sin plantones', 'Señal al reservar, recordatorio por WhatsApp y política de cancelación.'),
    ('✦', 'Análisis con IA', 'Cada mes, qué servicios te hacen ganar dinero y qué clientes estás perdiendo.'),
    ('📈', 'Plan financiero 2027', 'Objetivos mes a mes comparados con lo real, como en las grandes empresas.'),
    ('🏡', 'Domicilios', 'Abre las horas libres de tu equipo a las casas de alrededor y factura más.'),
    ('👥', 'Equipo bajo control', 'Ausencias, bajas, recepción con su acceso y comisiones calculadas solas.'),
]

# (id, eyebrow, título, texto, bullets, visual)  visual: ('video', key) | ('img', file, alt)
FEATURES_A = [
    ('reservas', 'Tu reserva, no la suya', 'Tus clientes reservan solos, a cualquier hora',
     'Tu propia página de reservas, con tu nombre y tus servicios. Pon el enlace en Instagram y en Google y deja de dar citas por WhatsApp mientras trabajas.',
     ['Sin comisiones por reserva: el cliente es tuyo, no de un marketplace.',
      'Varias personas, servicios y profesionales en una sola reserva y un solo pago.',
      'El cliente cambia su cita solo, sin llamarte.'],
     ('video', 'telefono')),
    ('plantones', 'Adiós a los plantones', 'Si no viene, la señal se queda en tu cuenta',
     'Cobras una señal al reservar y el día antes le llega un WhatsApp para confirmar o cambiar la cita. Si cancela tarde, se aplica tu política. Tú no llamas a nadie.',
     ['Señal o pago completo al reservar, con Stripe y directo a tu cuenta.',
      'Política de cancelación: tú decides hasta cuándo se puede cancelar.',
      'Recordatorio automático por WhatsApp 24 h antes.'],
     ('video', 'cancelar')),
    ('ia', 'Tu negocio entendido cada mes', 'La IA te dice qué servicio te hace ganar dinero',
     'Facturar mucho no es ganar mucho. Godolphy junta tus cobros y tus gastos y te dice cuánto te deja de verdad cada servicio, qué clientes están dejando de venir y qué hacer este mes, con el impacto en euros.',
     ['Rentabilidad por servicio y por profesional.',
      'Clientes en riesgo antes de perderlos.',
      'Cada mañana, hasta tres cosas que hacer hoy para ganar más.',
      'Y si dudas de tus precios, la calculadora te dice cuánto cobrar por cada servicio.'],
     ('video', 'rentabilidad')),
]

PLAN_WHY = [
    ('🎯', 'Sabes a dónde vas', 'Decides cuánto quieres facturar en 2027 y Godolphy lo reparte mes a mes: citas, ticket medio y clientes nuevos que necesitas.'),
    ('🚦', 'Te enteras a tiempo', 'Cada mes ves el plan contra lo real. Si en marzo vas por detrás, lo sabes en marzo, no en diciembre.'),
    ('💶', 'Sabes cuánto puedes gastar', 'Cuánto te cuesta conseguir un cliente nuevo (CAC) y cuánto te deja a lo largo del tiempo (LTV). Así sabes cuánto invertir en publicidad.'),
    ('🧑‍🤝‍🧑', 'Decides con números', 'Cuándo contratar, cuándo subir precios o cuándo abrir más horas, con datos de tu salón y no a ojo.'),
]

FEATURES_B = [
    ('precio', 'Gana más con las mismas horas', 'Precio según el día y la hora',
     'Un recargo en las horas que todo el mundo quiere y un descuento para llenar las horas flojas. Tus clientes ven siempre el precio final al reservar.',
     ['Por día de la semana y franja horaria.',
      'Aplicable a servicios y extras.',
      'Las citas ya reservadas no cambian de precio.'],
     ('img', 'precio-lista', 'Franjas de precio según día y hora en Godolphy')),
]

TEAM = [
    ('se-va', 'Cuando una profesional se va', '¿Y si se va a la competencia?',
     'Pasa en todos los salones: una profesional se va y, con ella, los clientes que tenía en su WhatsApp. Con Godolphy los clientes son del salón: su ficha, su historial y su contacto se quedan contigo.',
     ['Resuelves sus citas pendientes en un momento: las pasas a otra profesional.',
      'Avisas a su clientela con tu enlace de reservas, para que siga viniendo a tu salón.',
      'El historial de cada cliente sigue ahí para quien la atienda a partir de ahora.'],
     ('video', 'laura')),
    ('baja', 'Cuando una profesional está de baja', 'Una baja no te tira la semana',
     'Te escribe a las 8:30: está enferma y tiene la agenda llena. Marcas la ausencia y Godolphy te ayuda a resolver sus citas sin pasarte la mañana al teléfono.',
     ['Reasignas sus citas a otra profesional disponible.',
      'O dejas que cada cliente elija: otra profesional u otro día.',
      'Vacaciones, festivos y horarios especiales, en la misma agenda.'],
     ('video', 'baja')),
    ('regalo', 'Vende más sin hacer más', 'Tarjetas regalo y bonos de sesiones',
     'En Navidad, en el Día de la Madre o en un cumpleaños, tus clientes compran tarjetas regalo desde tu enlace. Y con los bonos de 5 o 10 sesiones cobras por adelantado y te aseguras de que vuelvan.',
     ['Tarjetas regalo digitales, a la venta en tu página de reservas.',
      'Bonos que se descuentan solos con cada cita.',
      'Cupones y descuentos para tus campañas.'],
     ('video', 'regalo')),
]

BENEFITS = [
    ('Más dinero en cada hora', 'Precio según la hora, extras bien cobrados y servicios que sabes que te dejan margen.'),
    ('Menos horas perdidas', 'Señal al reservar, recordatorios y huecos que se llenan con domicilios.'),
    ('Clientes que vuelven', 'Sabes quién está dejando de venir y la recuperas antes de perderla.'),
    ('Un equipo rentable', 'Las horas libres trabajan y las comisiones se calculan solas.'),
    ('Tranquilidad', 'Una baja o una profesional que se va ya no te desmontan el salón.'),
    ('Rumbo', 'Un plan para 2027 y cada mes sabes si vas bien.'),
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
           ('Domicilios con el desplazamiento en la agenda', False, True),
           ('Sin comisiones por cliente nuevo', False, True)]

NOT = [('No es un marketplace', 'Tus clientes no ven a tu competencia al reservar ni te cobramos comisión por ellos.'),
       ('No es solo una agenda', 'Además de dar citas, te dice dónde ganas y dónde pierdes dinero.'),
       ('No es un lío técnico', 'Si sabes usar WhatsApp, sabes usar Godolphy.'),
       ('No es una permanencia', 'Te vas cuando quieras, sin letra pequeña.')]

PLANS = [('Solo', '33', 'Para quien trabaja sola o solo', ['1 profesional', 'Reservas online y agenda', 'Pagos y señal del 20 %', 'Recordatorios WhatsApp', 'Domicilios', 'Análisis IA mensual'], False),
         ('Pro', '45', 'Para equipos que quieren crecer', ['Desde 2 profesionales', 'Todo lo de Solo', 'Gastos, precios y plan financiero', 'Precio según día y hora', 'Tarjetas regalo, bonos y comisiones', 'Análisis IA semanal'], True),
         ('Max', '360', 'Para cadenas y franquicias', ['Incluye 20 profesionales', 'Todo lo de Pro', 'Onboarding 1:1 y migración', 'Account manager', 'Análisis IA diario'], False)]

FAQ = [('¿Cuánto cuesta?', 'Desde 33 €/mes, y un 25 % menos con pago anual. Los 30 primeros días son gratis, con el plan Pro completo y sin tarjeta.'),
       ('¿Hay permanencia?', 'No. Te vas cuando quieras.'),
       ('¿Sirve para mi tipo de salón?', 'Sí: peluquerías, centros de estética, salones de uñas, barberías, masajes y profesionales a domicilio.'),
       ('Nunca he hecho domicilios. ¿Lo necesito?', 'No es obligatorio. Pero si tu equipo tiene horas libres, puedes abrirlas solo a las calles de alrededor de tu salón y Godolphy calcula el desplazamiento y el tiempo entre citas.'),
       ('¿Mis clientes tienen que descargarse una app?', 'No. Reservan desde un enlace, en el móvil o en el ordenador.'),
       ('¿Es un lío cambiar de programa?', 'No. Importas tus servicios y tu equipo desde Excel o una captura de pantalla, y los servicios también desde tu enlace de Treatwell, Booksy o Fresha.'),
       ('¿Qué hace exactamente la IA?', 'Lee tus reservas, cobros y gastos y te dice, en lenguaje normal, qué servicios te dejan margen, qué clientes están dejando de venir y qué hacer para ganar más.'),
       ('Nunca he hecho un plan financiero. ¿Es difícil?', 'No. Pones cuánto quieres facturar y Godolphy lo reparte mes a mes con tus datos. Tú solo miras si vas por delante o por detrás.'),
       ('¿Los cobros pasan por Godolphy?', 'No. Conectas tu cuenta de Stripe y el dinero va directo a tu cuenta. Godolphy no se queda comisión de tus cobros.'),
       ('¿Cumple con Verifactu?', 'Sí. Cada cobro se envía solo a Hacienda con su tique y código QR. Se activa con la suscripción de pago; durante la prueba gratuita no está activo.')]

# Mapa animado: tu salón en el centro y las casas de alrededor que piden servicios a domicilio.
HOUSE = '<g transform="translate({x},{y})"><rect x="-17" y="-8" width="34" height="26" rx="4" fill="#fff" stroke="#d9cffc" stroke-width="2"/><path d="M-22 -6 L0 -24 L22 -6 Z" fill="#efe9ff" stroke="#d9cffc" stroke-width="2" stroke-linejoin="round"/><rect x="-5" y="4" width="10" height="14" rx="2" fill="#d9cffc"/></g>'
HOUSES = [(110, 92), (460, 80), (70, 300), (520, 290), (190, 395), (400, 405), (300, 50)]
PINS = [(110, 92, 'Manicura · 11:00'), (520, 290, 'Peinado · Hotel'), (190, 395, 'Masaje · 17:30')]


def domicilio_svg():
    routes = ''.join(f'<path class="rt" d="M300 230 Q {(300 + x) / 2 + (40 if x < 300 else -40)} {(230 + y) / 2} {x} {y}" />' for x, y, _ in PINS)
    dots = ''.join(f'<circle r="6" fill="#631cff"><animateMotion dur="{3 + i}s" repeatCount="indefinite" path="M300 230 Q {(300 + x) / 2 + (40 if x < 300 else -40)} {(230 + y) / 2} {x} {y}"/></circle>' for i, (x, y, _) in enumerate(PINS))
    houses = ''.join(HOUSE.format(x=x, y=y) for x, y in HOUSES)
    pins = ''
    for i, (x, y, t) in enumerate(PINS):
        w = 12 + len(t) * 7
        pins += f'<g transform="translate({x},{y - 44})"><circle r="9" fill="#EEFE3A" stroke="#02021e" stroke-width="2"><animate attributeName="r" values="7;11;7" dur="1.8s" begin="{i * .5}s" repeatCount="indefinite"/></circle><rect x="{-w / 2}" y="-40" width="{w}" height="24" rx="12" fill="#02021e"/><text y="-23" text-anchor="middle" font-size="12.5" font-weight="700" fill="#fff" font-family="Plus Jakarta Sans,sans-serif">{e(t)}</text></g>'
    return f'''<svg class="map" viewBox="0 0 600 460" role="img" aria-label="Tu salón en el centro y las casas de alrededor pidiendo servicios a domicilio">
  <defs><radialGradient id="rg" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#631cff" stop-opacity=".18"/><stop offset="1" stop-color="#631cff" stop-opacity="0"/></radialGradient></defs>
  <rect width="600" height="460" rx="28" fill="#f8f7ff"/>
  <path d="M0 160 H600 M0 340 H600 M150 0 V460 M440 0 V460" stroke="#ece7fb" stroke-width="18"/>
  <circle cx="300" cy="230" r="190" fill="url(#rg)"><animate attributeName="r" values="150;200;150" dur="4s" repeatCount="indefinite"/></circle>
  <circle cx="300" cy="230" r="150" fill="none" stroke="#631cff" stroke-opacity=".25" stroke-width="2" stroke-dasharray="6 8"/>
  {routes}{houses}
  <g transform="translate(300,230)"><rect x="-62" y="-40" width="124" height="80" rx="18" fill="#631cff"/><path d="M-62 -14 H62" stroke="#EEFE3A" stroke-width="5"/><text y="12" text-anchor="middle" font-size="17" font-weight="800" fill="#fff" font-family="Gabarito,sans-serif">Tu salón</text><text y="30" text-anchor="middle" font-size="11.5" fill="#e9e1ff" font-family="Plus Jakarta Sans,sans-serif">2 profesionales libres</text></g>
  {dots}{pins}
</svg>'''


EXTRA_CSS = r'''
html{scroll-behavior:smooth;}
.hero h1{font-size:clamp(36px,5.2vw,64px);line-height:1.04;font-weight:700;}
.nav{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);}
.nav .w{display:flex;align-items:center;justify-content:space-between;height:64px;}
.nav img{height:26px;width:auto;}
.nav .links{display:flex;gap:22px;align-items:center;font-size:14.5px;font-weight:600;}
.nav .links a{text-decoration:none;color:rgba(2,2,30,.7);}
.nav .nbtn{background:linear-gradient(90deg,var(--v2),var(--v));color:#fff!important;padding:10px 18px;border-radius:999px;}
.hero{padding-top:64px;}
.hero .grid{align-items:center;grid-template-columns:1fr 1fr;}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px;}
.chips span{font-size:13px;font-weight:700;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.22);padding:7px 12px;border-radius:999px;}
.hero .txt{padding-bottom:64px;}
.dev{position:relative;width:100%;max-width:580px;margin:0 auto 56px;padding-right:70px;}
.lap{background:#0d0627;border-radius:16px 16px 6px 6px;padding:22px 8px 8px;box-shadow:0 40px 80px rgba(10,0,40,.5);position:relative;}
.lap::before{content:"";position:absolute;top:8px;left:12px;width:36px;height:7px;background:radial-gradient(circle,#ff5f57 3px,transparent 3.5px) 0 0/12px 7px repeat-x;}
.lap img{border-radius:6px;width:100%;}
.lap-base{height:12px;margin:0 -24px;background:linear-gradient(#cfc8e8,#a59cc9);border-radius:0 0 14px 14px;}
.mob{position:absolute;right:0;bottom:-34px;width:34%;border:7px solid #0d0627;border-radius:26px;overflow:hidden;background:#fff;box-shadow:0 30px 60px rgba(10,0,40,.5);animation:fl 6s ease-in-out infinite;}
.mob img{width:100%;}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
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
.ovc{background:#fff;border:1px solid var(--line);border-radius:22px;padding:24px;transition:transform .2s,box-shadow .2s;}
.ovc:hover{transform:translateY(-4px);box-shadow:0 18px 40px rgba(99,28,255,.12);}
.ovc i{font-style:normal;font-size:26px;display:block;margin-bottom:12px;color:var(--v);}
.ovc h3{font-family:'Gabarito',sans-serif;font-size:21px;margin:0 0 6px;}
.ovc p{margin:0;color:var(--muted);line-height:1.55;font-size:15px;}
.ft{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center;max-width:980px;margin:0 auto 96px;}
.ft:last-child{margin-bottom:0;}
.ft.rev .ft__img{order:2;}
.ft__img{display:flex;justify-content:center;}
.ft__img img{width:100%;max-width:380px;border-radius:22px;}
.ft h3{font-family:'Gabarito',sans-serif;font-size:clamp(26px,3vw,36px);line-height:1.1;margin:0 0 12px;}
.ft p{margin:0 0 16px;font-size:17px;line-height:1.6;color:rgba(2,2,30,.75);}
.ft ul{list-style:none;padding:0;margin:0;display:grid;gap:9px;}
.ft li{display:flex;gap:10px;line-height:1.45;font-size:15.5px;}
.ft li::before{content:"✓";flex:0 0 22px;height:22px;border-radius:50%;background:#efe9ff;color:var(--v);font-weight:800;font-size:12px;display:flex;align-items:center;justify-content:center;margin-top:1px;}
.reel{position:relative;width:min(290px,78vw);aspect-ratio:9/16;border:8px solid #0d0627;border-radius:34px;overflow:hidden;background:#0d0627;box-shadow:0 30px 70px rgba(40,10,120,.28);}
.reel video{width:100%;height:100%;object-fit:cover;display:block;}
.reel .snd{position:absolute;right:10px;bottom:10px;border:0;border-radius:999px;background:rgba(2,2,30,.72);color:#fff;font:700 12.5px 'Plus Jakarta Sans',sans-serif;padding:8px 12px;cursor:pointer;}
.reel .tag{position:absolute;left:10px;top:10px;background:rgba(255,255,255,.92);font-size:11.5px;font-weight:800;padding:5px 10px;border-radius:999px;}
.why{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:8px;}
.why div{background:#fff;border:1px solid var(--line);border-radius:20px;padding:22px;}
.why i{font-style:normal;font-size:26px;}
.why b{display:block;font-family:'Gabarito',sans-serif;font-size:19px;margin:10px 0 6px;}
.why span{color:var(--muted);font-size:15px;line-height:1.5;}
.plan2{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center;max-width:980px;margin:56px auto 0;}
.plan2 img{border-radius:22px;max-width:400px;margin:0 auto;}
.plan2 h3{font-family:'Gabarito',sans-serif;font-size:clamp(24px,2.8vw,32px);line-height:1.15;margin:0 0 12px;}
.plan2 p{font-size:17px;line-height:1.6;color:rgba(2,2,30,.75);margin:0 0 14px;}
.shot{background:#fff;border:1px solid var(--line);border-radius:20px!important;box-shadow:0 24px 60px rgba(40,10,120,.16);padding:6px;}
.big{font-family:'Gabarito',sans-serif;font-size:clamp(60px,9vw,110px);line-height:1;font-weight:800;letter-spacing:-.03em;}
.dom{display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center;}
.map{width:100%;height:auto;display:block;}
.rt{fill:none;stroke:#631cff;stroke-width:3;stroke-dasharray:4 7;opacity:.55;}
.dom h2{margin-bottom:14px;}
.dom p{font-size:17px;line-height:1.6;color:rgba(2,2,30,.75);margin:0 0 14px;}
.stat{display:flex;gap:16px;margin:22px 0;}
.stat div{flex:1;background:var(--soft);border:1px solid var(--line);border-radius:18px;padding:16px 18px;}
.stat b{display:block;font-family:'Gabarito',sans-serif;font-size:30px;color:var(--v);line-height:1.1;}
.stat span{font-size:14px;color:var(--muted);}
.domv{display:grid;grid-template-columns:auto 1fr;gap:40px;align-items:center;max-width:860px;margin:64px auto 0;}
.domv ul{list-style:none;padding:0;margin:0;display:grid;gap:10px;}
.domv li{display:flex;gap:10px;font-size:16px;line-height:1.5;}
.domv li::before{content:"✓";flex:0 0 22px;height:22px;border-radius:50%;background:#efe9ff;color:var(--v);font-weight:800;font-size:12px;display:flex;align-items:center;justify-content:center;margin-top:1px;}
.sectors{display:grid;grid-template-columns:1.3fr 1fr .75fr .75fr;gap:12px;margin-top:8px;}
.sectors figure{margin:0;position:relative;border-radius:20px;overflow:hidden;height:260px;}
.sectors img{width:100%;height:100%;object-fit:cover;transition:transform .6s;}
.sectors figure:hover img{transform:scale(1.05);}
.sectors figcaption{position:absolute;left:12px;bottom:12px;background:rgba(255,255,255,.92);font-weight:700;font-size:13.5px;padding:6px 12px;border-radius:999px;}
.tour{max-width:900px;margin:0 auto 48px;border-radius:22px;overflow:hidden;box-shadow:0 30px 70px rgba(40,10,120,.2);background:#0d0627;}
.tour video{width:100%;display:block;}
.tabs{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-bottom:22px;}
.tabs button{font:inherit;font-weight:700;font-size:15px;border:1px solid var(--line);background:#fff;color:var(--ink);padding:10px 18px;border-radius:999px;cursor:pointer;}
.tabs button.on{background:var(--v);color:#fff;border-color:var(--v);}
.scr{max-width:980px;margin:0 auto;}
.scr figure{margin:0;display:none;}
.scr figure.on{display:block;animation:fi .4s ease;}
@keyframes fi{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.scr img{width:100%;border-radius:18px;border:1px solid var(--line);box-shadow:0 24px 60px rgba(40,10,120,.15);}
.scr figcaption{text-align:center;color:var(--muted);font-size:15px;margin-top:14px;}
.ben{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}
.ben div{padding:24px;border-radius:22px;background:linear-gradient(160deg,#fff,#f6f2ff);border:1px solid var(--line);}
.ben b{display:block;font-family:'Gabarito',sans-serif;font-size:22px;margin-bottom:6px;}
.ben span{color:var(--muted);line-height:1.55;font-size:15.5px;}
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
.rv{opacity:0;transform:translateY(26px);transition:opacity .7s ease,transform .7s ease;}
.rv.in{opacity:1;transform:none;}
@media (prefers-reduced-motion:reduce){.rv{opacity:1;transform:none;transition:none}.mob{animation:none}}
@media(max-width:860px){
  .nav .links a:not(.nbtn){display:none;}
  .hero .grid{grid-template-columns:1fr;}
  .dev{padding-right:46px;margin-bottom:60px;}
  .painsg,.ov,.steps3,.plans,.nots,.risk,.ben{grid-template-columns:1fr;}
  .why{grid-template-columns:1fr 1fr;}
  .story,.plan2,.dom{grid-template-columns:1fr;gap:26px;}
  .story img{max-width:420px;margin:0 auto;}
  .ft{grid-template-columns:1fr;gap:24px;margin-bottom:72px;}
  .ft.rev .ft__img{order:0;}
  .domv{grid-template-columns:1fr;justify-items:center;gap:26px;}
  .sectors{grid-template-columns:1fr 1fr;}
  .sectors figure{height:190px;}
  .cmp th,.cmp td{padding:12px 10px;font-size:14px;}
  .hero .txt{padding-bottom:0;}
}
@media(max-width:520px){.why{grid-template-columns:1fr;}}
'''


ERA_HTML = '<!-- ===================== NUEVA ERA · MÁSCARA ===================== -->\n<section class="sec era ctr" id="nueva-era">\n  <div class="w">\n    <div class="rv">\n      <span class="eb">La nueva era</span>\n      <h2 class="h2">Una nueva era para los salones, con IA</h2>\n      <p class="lead2">Con la máscara de Godolphy ves tu salón con otros ojos: lo que ganas de verdad, quién se está yendo y dónde se escapa el dinero.</p>\n    </div>\n    <div class="mask rv" aria-hidden="true">\n      <svg viewBox="0 0 680 360" xmlns="http://www.w3.org/2000/svg">\n        <defs>\n          <linearGradient id="mG" x1="0" y1="0" x2="1" y2="1">\n            <stop offset="0" stop-color="#d9c8ff"/><stop offset=".3" stop-color="#9B4FE8"/><stop offset=".7" stop-color="#631cff"/><stop offset="1" stop-color="#3a0aaa"/>\n          </linearGradient>\n          <linearGradient id="mGloss" x1="0" y1="0" x2="0" y2="1">\n            <stop offset="0" stop-color="#fff" stop-opacity=".28"/><stop offset=".3" stop-color="#fff" stop-opacity="0"/>\n          </linearGradient>\n          <linearGradient id="mShine" x1="0" y1="0" x2="1" y2="0">\n            <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".32"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>\n          </linearGradient>\n          <path id="eL" d="M126 128 H246 C270 128 282 146 282 170 V184 C282 214 258 234 226 234 H150 C112 234 86 212 86 180 C86 150 100 128 126 128 Z"/>\n          <path id="eR" d="M554 128 H434 C410 128 398 146 398 170 V184 C398 214 422 234 454 234 H530 C568 234 594 212 594 180 C594 150 580 128 554 128 Z"/>\n          <clipPath id="cL"><use href="#eL"/></clipPath>\n          <clipPath id="cR"><use href="#eR"/></clipPath>\n          <path id="mS" fill-rule="evenodd" d="M44 8 H636 Q676 8 676 48 V262 C676 318 634 352 560 352 C486 352 440 326 404 288 Q376 258 340 258 Q304 258 276 288 C240 326 194 352 120 352 C46 352 4 318 4 262 V48 Q4 8 44 8 Z M126 128 H246 C270 128 282 146 282 170 V184 C282 214 258 234 226 234 H150 C112 234 86 212 86 180 C86 150 100 128 126 128 Z M554 128 H434 C410 128 398 146 398 170 V184 C398 214 422 234 454 234 H530 C568 234 594 212 594 180 C594 150 580 128 554 128 Z"/>\n          <clipPath id="cS"><use href="#mS"/></clipPath>\n        </defs>\n\n        <g clip-path="url(#cL)">\n          <rect x="80" y="120" width="210" height="120" fill="#0c0628"/>\n          <g class="tick2" font-family="Plus Jakarta Sans, sans-serif" text-anchor="middle">\n            <text x="184" y="168" fill="#9cf0c6" font-size="12" font-weight="700" letter-spacing="2">BENEFICIO ESTIMADO</text><text x="184" y="200" fill="#fff" font-size="30" font-weight="800">3.480 €</text>\n            <text x="184" y="288" fill="#ffd98a" font-size="12" font-weight="700" letter-spacing="2">€ POR HORA</text><text x="184" y="320" fill="#fff" font-size="30" font-weight="800">28 €/h</text>\n            <text x="184" y="408" fill="#ffb3c4" font-size="12" font-weight="700" letter-spacing="2">EN RIESGO</text><text x="184" y="440" fill="#fff" font-size="30" font-weight="800">4 clientes</text>\n            <text x="184" y="528" fill="#d9c8ff" font-size="12" font-weight="700" letter-spacing="2">OCUPACIÓN</text><text x="184" y="560" fill="#fff" font-size="30" font-weight="800">72 %</text>\n            <text x="184" y="648" fill="#9cf0c6" font-size="12" font-weight="700" letter-spacing="2">BENEFICIO ESTIMADO</text><text x="184" y="680" fill="#fff" font-size="30" font-weight="800">3.480 €</text>\n          </g>\n        </g>\n        <g clip-path="url(#cR)">\n          <rect x="390" y="120" width="210" height="120" fill="#0c0628"/>\n          <g transform="translate(422 150)"><g class="tick2">\n            <g><rect x="0" y="22" width="18" height="34" rx="3" fill="#631cff"/><rect x="26" y="10" width="18" height="46" rx="3" fill="#7B4DFF"/><rect x="52" y="-2" width="18" height="58" rx="3" fill="#9B4FE8"/><rect x="78" y="16" width="18" height="40" rx="3" fill="#631cff"/><rect x="104" y="2" width="18" height="54" rx="3" fill="#d9c8ff"/><rect x="130" y="26" width="18" height="30" rx="3" fill="#7B4DFF"/></g>\n            <g transform="translate(0 120)"><polyline points="0,48 30,36 60,40 90,16 120,22 148,2" fill="none" stroke="#9cf0c6" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="148" cy="2" r="5" fill="#9cf0c6"/></g>\n            <g transform="translate(0 240)"><circle cx="18" cy="28" r="15" fill="#f6c6d6"/><circle cx="55" cy="28" r="15" fill="#ffe1a8"/><circle cx="92" cy="28" r="15" fill="#c7f0dc"/><circle cx="129" cy="28" r="15" fill="#c7d7ff"/></g>\n            <g transform="translate(0 360)"><rect x="0" y="12" width="148" height="10" rx="5" fill="#2A1660"/><rect x="0" y="12" width="58" height="10" rx="5" fill="#ffd98a"/><rect x="0" y="36" width="148" height="10" rx="5" fill="#2A1660"/><rect x="0" y="36" width="112" height="10" rx="5" fill="#9B4FE8"/></g>\n            <g transform="translate(0 480)"><rect x="0" y="22" width="18" height="34" rx="3" fill="#631cff"/><rect x="26" y="10" width="18" height="46" rx="3" fill="#7B4DFF"/><rect x="52" y="-2" width="18" height="58" rx="3" fill="#9B4FE8"/><rect x="78" y="16" width="18" height="40" rx="3" fill="#631cff"/><rect x="104" y="2" width="18" height="54" rx="3" fill="#d9c8ff"/><rect x="130" y="26" width="18" height="30" rx="3" fill="#7B4DFF"/></g>\n          </g></g>\n        </g>\n\n        <use href="#mS" fill="url(#mG)"/>\n        <use href="#mS" fill="url(#mGloss)"/>\n        <g clip-path="url(#cS)"><rect class="shine" x="0" y="-20" width="130" height="400" fill="url(#mShine)"/></g>\n        <use href="#eL" fill="none" stroke="rgba(255,255,255,.5)" stroke-width="3"/>\n        <use href="#eR" fill="none" stroke="rgba(255,255,255,.5)" stroke-width="3"/>\n      </svg>\n    </div>\n    <div class="rv" style="margin-top:44px;">\n      {CTA_ERA}\n    </div>\n  </div>\n</section>'
ERA_CSS = '\n.era{background:radial-gradient(700px 380px at 50% 72%,rgba(123,77,255,.16),transparent 70%),#fff;}\n.era .h2{font-size:clamp(38px,5.6vw,74px);max-width:940px;margin-left:auto;margin-right:auto;background:linear-gradient(90deg,#02021e 0%,#631cff 55%,#9B4FE8 100%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;}\n.mask{max-width:760px;margin:60px auto 0;}\n.mask svg{width:100%;height:auto;display:block;overflow:visible;animation:mfloat 6s ease-in-out infinite;filter:drop-shadow(0 40px 60px rgba(99,28,255,.35));}\n@keyframes mfloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}\n.tick{animation:tick 12s cubic-bezier(.7,0,.3,1) infinite;}\n@keyframes tick{0%,20%{transform:translateY(0)}25%,45%{transform:translateY(-70px)}50%,70%{transform:translateY(-140px)}75%,95%{transform:translateY(-210px)}100%{transform:translateY(-280px)}}\n.tick2{animation:tick2 12s cubic-bezier(.7,0,.3,1) infinite;}\n@keyframes tick2{0%,20%{transform:translateY(0)}25%,45%{transform:translateY(-120px)}50%,70%{transform:translateY(-240px)}75%,95%{transform:translateY(-360px)}100%{transform:translateY(-480px)}}\n.shine{animation:shine 5s ease-in-out infinite;}\n@keyframes shine{0%,100%{transform:translateX(-300px) skewX(-18deg)}50%{transform:translateX(420px) skewX(-18deg)}}\n@media (prefers-reduced-motion:reduce){.mask svg,.tick,.tick2,.shine{animation:none}}\n'


def reel(key, tag=''):
    t = f'<span class="tag">{e(tag)}</span>' if tag else ''
    return (f'<div class="reel">{t}<video data-src="{IMG}v/{key}.mp4" poster="{IMG}v/{key}.jpg" muted loop playsinline preload="none"></video>'
            f'<button type="button" class="snd" aria-label="Activar sonido">🔇 Activar sonido</button></div>')


def feature_block(n, f):
    fid, eb, t, x, bl, vis = f
    v = reel(vis[1]) if vis[0] == 'video' else f'<img class="shot" src="{IMG}{vis[1]}.webp" alt="{e(vis[2])}" loading="lazy">'
    lis = ''.join(f'<li>{e(b)}</li>' for b in bl)
    return f'<div class="ft rv{" rev" if n % 2 else ""}" id="{fid}"><div class="ft__img">{v}</div><div><span class="eb">{e(eb)}</span><h3>{e(t)}</h3><p>{e(x)}</p><ul>{lis}</ul></div></div>'


def build():
    hc = head_common()
    cta = lambda pos, cls='btn': f'<a class="{cls}" href="{SIGNUP}" data-cta="{pos}">Prueba gratis 30 días →</a>'
    midcta = lambda pos: f'<div class="ctr rv" style="margin-top:56px;">{cta(pos, "btn btn--v")}<p class="note" style="color:var(--muted);">30 días con el plan Pro completo · Sin tarjeta</p></div>'
    pains = ''.join(f'<div class="pain rv"><b>{e(t)}</b><span>{e(x)}</span></div>' for t, x in PAINS)
    ov = ''.join(f'<div class="ovc rv"><i>{i}</i><h3>{e(t)}</h3><p>{e(x)}</p></div>' for i, t, x in OVERVIEW)
    feats_a = ''.join(feature_block(n, f) for n, f in enumerate(FEATURES_A))
    feats_b = ''.join(feature_block(n + 1, f) for n, f in enumerate(FEATURES_B))
    team = ''.join(feature_block(n, f) for n, f in enumerate(TEAM))
    why = ''.join(f'<div class="rv"><i>{i}</i><b>{e(t)}</b><span>{e(x)}</span></div>' for i, t, x in PLAN_WHY)
    ben = ''.join(f'<div class="rv"><b>{e(t)}</b><span>{e(x)}</span></div>' for t, x in BENEFITS)
    tabs = ''.join(f'<button type="button" data-t="{i}" class="{"on" if i == 0 else ""}">{e(t)}</button>' for i, (_, t, _x) in enumerate(SCREENS))
    scr = ''.join(f'<figure data-t="{i}" class="{"on" if i == 0 else ""}"><img src="{IMG}{f}.webp" alt="{e(t)} de Godolphy" width="1400" height="875" loading="lazy"><figcaption>{e(x)} <span style="opacity:.7">· Datos de ejemplo</span></figcaption></figure>' for i, (f, t, x) in enumerate(SCREENS))
    mark = lambda v: '<span class="y">✓</span>' if v else '<span class="n">—</span>'
    cmp = ''.join(f'<tr><td>{e(r)}</td><td>{mark(a)}</td><td>{mark(b)}</td></tr>' for r, a, b in COMPARE)
    plans = ''
    for name, price, for_, items, pop in PLANS:
        lis = ''.join(f'<li>{e(i)}</li>' for i in items)
        plans += f'<div class="plan rv{" pop" if pop else ""}"><h3>{name}</h3><p class="for">{e(for_)}</p><div class="pr">{price} €<small> /mes</small></div><ul>{lis}</ul>{cta("plan-" + name.lower(), "btn btn--v" if pop else "btn")}</div>'
    nots = ''.join(f'<div class="notc rv"><b>{e(t)}</b><span>{e(x)}</span></div>' for t, x in NOT)
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}

    page = f'''<!DOCTYPE html>
<html lang="es">
<head>
{hc.split('<head>', 1)[1].strip()}
<meta charset="UTF-8">
<title>Godolphy · El software de gestión con IA para tu salón</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Reservas, cobros sin plantones, domicilios, equipo y un plan financiero para 2027. Cada mes, la IA te dice dónde ganas y dónde pierdes dinero. 30 días gratis, sin tarjeta.">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://www.godolphy.com/lp/{SLUG}/">
<meta property="og:title" content="Gestiona tu salón como lo haría una gran empresa">
<meta property="og:description" content="El software de gestión con IA para salones. 30 días gratis, sin tarjeta.">
<meta property="og:image" content="https://www.godolphy.com/lp/{SLUG}/s-ana-hero.webp">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}{EXTRA_CSS}{ERA_CSS}</style>
</head>
<body data-lp="{SLUG}">
<header class="nav"><div class="w">
  <img src="/wp-images/logo-gradient.png" alt="Godolphy" width="140" height="30">
  <nav class="links"><a href="#funciones">Qué hace</a><a href="#plan">Plan 2027</a><a href="#domicilios">Domicilios</a><a href="#precios">Precios</a><a class="nbtn" href="{SIGNUP}" data-cta="nav">Pruébalo gratis</a></nav>
</div></header>

<main>
<section class="hero">
  <div class="w grid">
    <div class="txt">
      <span class="eyebrow">Software de gestión con IA para salones</span>
      <h1>Gestiona tu salón como lo haría una gran empresa.</h1>
      <p class="sub">Reservas, cobros sin plantones, domicilios y tu equipo en un solo sitio. Y cada mes, la IA te dice dónde ganas y dónde pierdes dinero.</p>
      {cta('hero')}
      <div class="chips"><span>30 días gratis</span><span>Sin tarjeta</span><span>Sin permanencia</span><span>Sin comisiones por reserva</span></div>
    </div>
    <div class="vis"><div class="dev">
      <div class="lap"><img src="{IMG}s-ana-hero.webp" alt="Análisis con IA de Godolphy en el ordenador" width="1200" height="750" fetchpriority="high"></div>
      <div class="lap-base"></div>
      <div class="mob"><img src="{IMG}m-cal.webp" alt="Agenda de Godolphy en el móvil" width="780" height="1688"></div>
    </div></div>
  </div>
</section>

<section class="sec sec--soft">
  <div class="w">
    <div class="ctr rv"><span class="eb">¿Te suena?</span>
    <h2 class="h2">Tu salón funciona. Pero no avanza.</h2></div>
    <div class="painsg">{pains}</div>
    <p class="punch rv">No es que trabajes poco. Es que tu programa de reservas solo te da una agenda, <span class="grad">y una agenda no te dice cómo ganar más.</span></p>
  </div>
</section>

{ERA_HTML.replace('{CTA_ERA}', cta('era', 'btn btn--v'))}

<section class="sec" id="neus">
  <div class="w story">
    <img class="rv" src="{IMG}neus.webp" alt="Neus, fundadora de Godolphy" width="798" height="997" loading="lazy">
    <div class="rv">
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
    <div class="ctr rv"><span class="eb">Todo en un solo software</span>
    <h2 class="h2">Lo que ya esperas de un programa de reservas. <span class="grad">Y todo lo que le falta.</span></h2></div>
    <div class="ov">{ov}</div>
  </div>
</section>

<section class="sec">
  <div class="w">{feats_a}{midcta('features')}</div>
</section>

<section class="sec sec--soft" id="plan">
  <div class="w">
    <div class="ctr rv"><span class="eb">Como una gran empresa</span>
    <div class="big grad">2027</div>
    <h2 class="h2">Tu plan financiero para 2027, hecho con tus datos</h2>
    <p class="lead2">Las grandes empresas no empiezan el año improvisando: saben cuánto quieren facturar, cuántos clientes necesitan y cuánto pueden gastar. Ahora tu salón también.</p></div>
    <div class="why">{why}</div>
    <div class="plan2">
      <div class="rv" style="display:flex;justify-content:center;">{reel('plan')}</div>
      <div class="rv">
        <h3>¿Cada año igual que el anterior?</h3>
        <p>Si no sabes a dónde vas, cualquier mes te parece normal. Con un plan, cada mes sabes si vas por delante o por detrás, y qué tocar para llegar.</p>
        <p>Pones tu objetivo para 2027 y Godolphy lo reparte mes a mes: citas, ticket medio, gastos y clientes nuevos. Después lo compara con lo real, solo, con tus reservas y tus cobros.</p>
        <img class="shot" src="{IMG}plan-mes.webp" alt="Plan financiero del mes en Godolphy: plan, real y diferencia" width="744" height="1164" loading="lazy" style="margin:18px 0 0;max-width:340px;">
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="w">{feats_b}</div>
</section>

<section class="sec sec--soft" id="domicilios">
  <div class="w">
    <div class="dom">
      <div class="rv">{domicilio_svg()}</div>
      <div class="rv">
        <span class="eb">Domicilio sin líos</span>
        <h2 class="h2">Saca partido a tu equipo: haz domicilios y factura más</h2>
        <p>En España casi ningún salón hace domicilios. Y alrededor del tuyo hay casas, hoteles y residencias que los necesitan: una novia, una persona mayor, una madre que no puede salir.</p>
        <p>Si tu equipo tiene horas libres, no las pagues vacías. Ábrelas solo a las calles de alrededor de tu salón y conviértelas en facturación.</p>
        <div class="stat"><div><b>+20–50 %</b><span>más por cita a domicilio, según el servicio y el sitio</span></div><div><b>0 h</b><span>muertas: el equipo trabaja cuando la cabina está vacía</span></div></div>
      </div>
    </div>
    <div class="domv">
      <div class="rv">{reel('domicilio')}</div>
      <div class="rv">
        <h3 class="h2" style="font-size:clamp(24px,2.8vw,32px);">Tú pones las reglas. Godolphy hace los cálculos.</h3>
        <ul>
          <li>Defines tus zonas y el precio por kilómetro.</li>
          <li>Recargo distinto para hotel, hospital o casa.</li>
          <li>Solo se ofrecen las horas a las que tu equipo llega a tiempo.</li>
          <li>Local y domicilio en el mismo calendario, con el desplazamiento ya reservado.</li>
          <li>Cada reserva le llega a la profesional con la dirección.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="equipo">
  <div class="w">
    <div class="ctr rv"><span class="eb">Tu equipo, bajo control</span>
    <h2 class="h2">Lo que pasa en todos los salones. <span class="grad">Y cómo te ayuda Godolphy.</span></h2></div>
    <div style="margin-top:48px;">{team}</div>
    {midcta('team')}
  </div>
</section>

<section class="sec sec--soft">
  <div class="w">
    <div class="ctr rv"><span class="eb">Para cualquier tipo de salón</span>
    <h2 class="h2">Peluquerías, estética, uñas, barberías y masajes</h2>
    <p class="lead2">Con local, a domicilio o las dos cosas. Tú sola o con un equipo de veinte.</p></div>
    <div class="sectors rv">
      <figure><img src="{IMG}f-pelu.webp" alt="Peluquería" loading="lazy"><figcaption>Peluquerías</figcaption></figure>
      <figure><img src="{IMG}f-unas.webp" alt="Salón de uñas" loading="lazy"><figcaption>Uñas y estética</figcaption></figure>
      <figure><img src="{IMG}f-barber.webp" alt="Barbería" loading="lazy"><figcaption>Barberías</figcaption></figure>
      <figure><img src="{IMG}f-movil.webp" alt="Reserva desde el móvil" loading="lazy"><figcaption>A domicilio</figcaption></figure>
    </div>
  </div>
</section>

<section class="sec" id="dentro">
  <div class="w">
    <div class="ctr rv"><span class="eb">Así se ve por dentro</span>
    <h2 class="h2">Godolphy en minuto y medio</h2></div>
    <div class="tour rv"><video controls preload="none" playsinline poster="/videos/godolphy-tour-poster.jpg" src="/videos/godolphy-tour-720.mp4"></video></div>
    <div class="tabs rv" id="tabs">{tabs}</div>
    <div class="scr rv" id="scr">{scr}</div>
  </div>
</section>

<section class="sec sec--soft">
  <div class="w">
    <div class="ctr rv"><span class="eb">Lo que cambia en tu salón</span>
    <h2 class="h2">Menos apagar fuegos. <span class="grad">Más negocio.</span></h2></div>
    <div class="ben">{ben}</div>
  </div>
</section>

<section class="sec">
  <div class="w">
    <div class="ctr rv"><span class="eb">La diferencia</span>
    <h2 class="h2">Una agenda te da citas. <span class="grad">Godolphy te da un negocio.</span></h2></div>
    <div class="cmp rv"><table><thead><tr><th></th><th>Una agenda de reservas</th><th>Godolphy</th></tr></thead><tbody>{cmp}</tbody></table></div>
  </div>
</section>

<section class="sec sec--soft">
  <div class="w">
    <div class="ctr rv"><span class="eb">Más simple de lo que parece</span>
    <h2 class="h2">Empiezas en una tarde</h2></div>
    <div class="steps3">
      <div class="step rv"><b class="grad">01</b><h3>Crea tu cuenta</h3><p>Solo con tu email. Sin tarjeta y con el plan Pro completo durante 30 días.</p></div>
      <div class="step rv"><b class="grad">02</b><h3>Importa tus datos</h3><p>Tus servicios y tu equipo desde Excel, una captura de pantalla o tu enlace de Treatwell, Booksy o Fresha.</p></div>
      <div class="step rv"><b class="grad">03</b><h3>Comparte tu enlace</h3><p>Ponlo en Instagram y en Google. Tus clientes reservan solos y tú empiezas a ver tus números.</p></div>
    </div>
  </div>
</section>

<section class="sec" id="precios">
  <div class="w">
    <div class="ctr rv"><span class="eb">Precios claros</span>
    <h2 class="h2">Sin comisiones. Sin sorpresas.</h2>
    <p class="lead2">Todos empiezan con 30 días gratis del plan Pro. Con pago anual, un 25 % menos.</p></div>
    <div class="plans">{plans}</div>
    <p class="cap" style="margin-top:18px;">Precio final: no se añade IVA. <a href="/precio/">Ver la comparativa completa de planes</a></p>
  </div>
</section>

<section class="sec dark">
  <div class="w">
    <div class="ctr rv"><h2 class="h2">Lo que Godolphy no es</h2></div>
    <div class="nots">{nots}</div>
  </div>
</section>

<section class="sec">
  <div class="w">
    <div class="ctr rv"><span class="eb">Sin riesgo</span>
    <h2 class="h2">Pruébalo con tus clientes de verdad</h2>
    <p class="lead2">Configúralo, compártelo y compruébalo en tu salón. Si no te convence, no pagas nada.</p></div>
    <div class="risk rv"><div><b>30 días</b><span>gratis, con todo el plan Pro</span></div><div><b>0 €</b><span>sin tarjeta para empezar</span></div><div><b>0</b><span>permanencia: te vas cuando quieras</span></div></div>
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
    <div class="final rv">
      <h2>Lo que hacen las grandes empresas, ahora en tu salón</h2>
      <p>Empieza hoy y llega a 2027 sabiendo a dónde vas.</p>
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
  // aparición al hacer scroll
  var rv=document.querySelectorAll('.rv');
  if('IntersectionObserver' in window){{
    var io=new IntersectionObserver(function(es){{es.forEach(function(x){{if(x.isIntersecting){{x.target.classList.add('in');io.unobserve(x.target);}}}});}},{{threshold:.12}});
    rv.forEach(function(el){{io.observe(el);}});
    // reels: se cargan y se reproducen en silencio al verlos
    var vo=new IntersectionObserver(function(es){{es.forEach(function(x){{var v=x.target;
      if(x.isIntersecting){{if(!v.src){{v.src=v.getAttribute('data-src');}}var p=v.play();if(p&&p.catch)p.catch(function(){{}});}}else{{v.pause();}}}});}},{{threshold:.45}});
    document.querySelectorAll('.reel video').forEach(function(v){{vo.observe(v);}});
  }}else{{rv.forEach(function(el){{el.classList.add('in');}});document.querySelectorAll('.reel video').forEach(function(v){{v.src=v.getAttribute('data-src');v.controls=true;}});}}
  document.querySelectorAll('.reel .snd').forEach(function(b){{b.addEventListener('click',function(){{
    var v=b.parentNode.querySelector('video');if(!v.src)v.src=v.getAttribute('data-src');
    var on=v.muted;document.querySelectorAll('.reel video').forEach(function(o){{if(o!==v)o.muted=true;}});
    document.querySelectorAll('.reel .snd').forEach(function(o){{o.textContent='🔇 Activar sonido';}});
    v.muted=!on;if(on){{v.currentTime=0;v.play();b.textContent='🔊 Sonido activado';}}
    try{{if(window.posthog)posthog.capture('lp_video_sound',{{lp:lp,video:v.getAttribute('data-src')}});}}catch(_){{}}
  }});}});
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
