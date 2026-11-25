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
    ('Pones tus números.', 'Tu facturación del año pasado (subes un documento o la escribes) y tus gastos. Si ya usas Godolphy, partimos de tus citas y gastos reales.'),
    ('Eliges cuánto quieres crecer.', 'Mantenerte, +10 %, +25 % o el porcentaje que tú quieras. Godolphy te monta el plan mes a mes.'),
    ('Haces el seguimiento mes a mes.', 'Ves lo real frente a lo planificado y, si te desvías, la IA te avisa a tiempo.'),
]

# Iconos propios (trazo blanco sobre círculo con el degradado violeta de Godolphy), en lugar de emojis.
_ICON_PATHS = {
    'chart': '<path d="M5 19V11M10 19V6M15 19v-5M20 19V9"/><path d="M3 19h18"/>',
    'bell': '<path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15z"/><path d="M10 20.5a2 2 0 0 0 4 0"/>',
    'sync': '<path d="M20 11a8 8 0 0 0-14.5-4.5L4 8"/><path d="M4 4v4h4"/><path d="M4 13a8 8 0 0 0 14.5 4.5L20 16"/><path d="M20 20v-4h-4"/>',
    'trophy': '<path d="M8 4h8v5a4 4 0 0 1-8 0z"/><path d="M8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4"/><path d="M12 13v4M8.5 20h7M10 17h4"/>',
    'trend': '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    'cal': '<rect x="3.5" y="5" width="17" height="15" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    'team': '<circle cx="9" cy="8" r="3.2"/><path d="M3 19a6 6 0 0 1 12 0"/><path d="M16 5.5a3 3 0 0 1 0 5.5M18 19a5.5 5.5 0 0 0-3-4.8"/>',
    'card': '<rect x="3" y="6" width="18" height="13" rx="2.5"/><path d="M3 10.5h18M7 15h4"/>',
    'gift': '<rect x="4" y="9" width="16" height="11" rx="1.5"/><path d="M3 9h18M12 9v11M12 9c-2-4-6-4-6-1.5S10 9 12 9c2 0 6 1 6-1.5S14 5 12 9"/>',
    'spark': '<path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/><path d="M18.5 15.5l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8z"/>',
    'sound': '<path d="M4 10v4h4l5 4V6L8 10z"/><path d="M16.5 9a4 4 0 0 1 0 6M19 6.5a7.5 7.5 0 0 1 0 11"/>',
}


def icon(name, cls='ico'):
    return (f'<span class="{cls}" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{_ICON_PATHS[name]}</svg></span>')


ICON_CSS = r"""
.ico{flex:0 0 auto;display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;background:linear-gradient(160deg,#9B4FE8 0%,#631cff 70%);color:#fff;box-shadow:0 6px 16px rgba(99,28,255,.25);}
.ico svg{width:21px;height:21px;}
.ico--s{width:30px;height:30px;}.ico--s svg{width:16px;height:16px;}
.ico--i{display:inline-flex;vertical-align:-4px;color:currentColor;}.ico--i svg{width:18px;height:18px;}
"""


AFTER = [
    ('chart', 'Cada mes ves lo real frente a lo planificado.'),
    ('bell', 'Si un mes vas por debajo, la IA te avisa a tiempo.'),
    ('sync', 'Un Excel lo descargas y te olvidas. Aquí el plan se actualiza solo con tu día a día.'),
]

FAQ = [
    ('¿Necesito saber de finanzas?', 'No. Pones tus números y Godolphy hace los cálculos.'),
    ('¿Sirve si no tengo historial?', 'Sí, empiezas con tus números de partida.'),
    ('¿Lo puedo cambiar?', 'Sí, cada mes es editable.'),
    ('¿Cuánto cuesta después?', 'Los primeros 30 días son gratis. Después, el plan financiero está incluido en el plan Pro, desde 45 €/mes. Si no eliges plan, no pagas nada.'),
]

TESTIMONIALS = [
    ('natalia-kilova.webp', 'Natalia Kilova', 'Propietaria de peluquería · Barcelona', 'Ha sido muy fácil configurar el plan. Creo que este será mi año.'),
    ('silvia-moreno.webp', 'Sílvia Moreno', 'Propietaria de salón de uñas · Toledo', 'Sabía que necesitaba tener un plan financiero, pero no sabía por dónde empezar.'),
]


def testimonials_html(title='Ellas ya tienen <span class="grad">su plan 2027</span>'):
    cards = ''.join(
        f'<figure class="tst"><blockquote>«{html.escape(q)}»</blockquote>'
        f'<figcaption><img src="/lp/plan-financiero-2027/{f}" alt="{html.escape(n)}" width="320" height="320" loading="lazy">'
        f'<span><b>{html.escape(n)}</b>{html.escape(c)}</span></figcaption></figure>'
        for f, n, c, q in TESTIMONIALS)
    return f'<section class="sec sec--soft"><div class="w"><h2 class="h2">{title}</h2><div class="tsts">{cards}</div></div></section>'


TST_CSS = r"""
.tsts{display:grid;grid-template-columns:1fr 1fr;gap:18px;max-width:980px;}
.tst{margin:0;background:#fff;border:1px solid var(--line);border-radius:22px;padding:24px;display:flex;flex-direction:column;justify-content:space-between;gap:18px;}
.tst blockquote{margin:0;font-family:'Gabarito',sans-serif;font-size:clamp(19px,2.2vw,23px);line-height:1.3;color:var(--ink);}
.tst figcaption{display:flex;align-items:center;gap:12px;font-size:14.5px;color:var(--muted);}
.tst figcaption img{width:56px;height:56px;border-radius:50%;object-fit:cover;}
.tst figcaption b{display:block;color:var(--ink);font-size:15.5px;}
@media(max-width:860px){.tsts{grid-template-columns:1fr;}}
"""


SALONS = [
    ('salon-peluqueria.webp', 'Peluquería con el equipo trabajando', 'Peluquerías'),
    ('salon-estetica.webp', 'Cabinas de un centro de estética', 'Centros de estética'),
    ('salon-detalle.webp', 'Plan de Godolphy en el móvil, en el tocador de un salón', 'Tu plan, también en el móvil'),
]


def salons_html():
    figs = ''.join(
        f'<figure><img src="/lp/plan-financiero-2027/{f}" alt="{html.escape(a)}" width="900" height="600" loading="lazy">'
        f'<figcaption>{html.escape(c)}</figcaption></figure>' for f, a, c in SALONS)
    return ('<section class="sec"><div class="w"><h2 class="h2">Hecho para salones: <span class="grad">peluquerías, centros de estética y salones de uñas</span></h2>'
            f'<div class="salons">{figs}</div></div></section>')


SALON_CSS = r"""
.salons{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}
.salons figure{margin:0;position:relative;border-radius:22px;overflow:hidden;}
.salons img{width:100%;height:100%;aspect-ratio:3/2;object-fit:cover;display:block;}
.salons figcaption{position:absolute;left:14px;bottom:14px;background:rgba(2,2,30,.72);color:#fff;font-weight:700;font-size:14px;padding:7px 12px;border-radius:999px;}
@media(max-width:860px){.salons{grid-template-columns:1fr;}}
.tsts{max-width:none;}
"""


WHY = [
    ('16 %', 'más probabilidades de que el negocio salga adelante si escribes un plan.', 'Greene y Hopp, Strategic Entrepreneurship Journal, 2017 (recogido en Harvard Business Review)'),
    ('35 años', 'de estudios sobre objetivos llegan a la misma conclusión: una meta concreta y exigente rinde más que «hacerlo lo mejor posible».', 'Locke y Latham, American Psychologist, 2002'),
    ('4 de cada 10', 'pymes en España no planifican sus finanzas. Con un plan, ya vas por delante de casi la mitad.', 'Fundación IE, 2025'),
    ('+', 'Planificar mejora los resultados de las pequeñas empresas: lo confirma un análisis que reúne decenas de estudios.', 'Brinckmann, Grichnik y Kapsa, Journal of Business Venturing, 2010'),
]


def why_cards():
    cards = ''.join(f'<div class="stat"><b class="grad">{html.escape(n)}</b><p>{html.escape(t)}</p><small>{html.escape(src)}</small></div>'
                    for n, t, src in WHY)
    return (f'<div class="why4">{cards}</div>'
            '<blockquote class="quote quote--w">«Los planes no sirven de nada, pero planificar lo es todo.»<cite>Dwight D. Eisenhower</cite></blockquote>')


WHY_CSS = r"""
.why4{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:30px;}
.why4 .stat b{font-size:40px;}
.quote--w{margin-top:16px;text-align:center;align-items:center;}
@media(max-width:1000px){.why4{grid-template-columns:1fr 1fr;}}
@media(max-width:520px){.why4{grid-template-columns:1fr;}}
"""



PRODUCT = [
    ('cal', 'Reservas online 24 h', 'Tus clientes reservan solos desde tu enlace, sin llamadas ni mensajes.'),
    ('bell', 'Recordatorios automáticos', 'Avisos antes de cada cita para que no se olviden.'),
    ('card', 'Cobros y señal', 'Cobra la señal al reservar y despídete de los plantones.'),
    ('team', 'Agenda y equipo', 'Horarios, ausencias y comisiones de cada profesional.'),
    ('gift', 'Tarjetas regalo y bonos', 'Vende más con regalos y packs de sesiones.'),
    ('spark', 'Análisis con IA cada mes', 'Qué servicios te hacen ganar dinero y qué clientes no vuelven.'),
]


def product_html(cta_html=''):
    items = ''.join(f'<div class="pitem">{icon(ic)}<div><h3>{html.escape(t)}</h3><p>{html.escape(x)}</p></div></div>'
                    for ic, t, x in PRODUCT)
    return ('<section class="sec sec--soft"><div class="w">'
            '<h2 class="h2">Y no es solo un plan: <span class="grad">Godolphy es tu software de reservas y gestión con IA</span></h2>'
            '<p class="plead">El plan financiero es una parte. Con la misma cuenta gestionas todo el día a día del salón, y cada cita que entra alimenta tu plan sola.</p>'
            f'<div class="pgrid">{items}</div>'
            '<p class="pmore"><a href="/funcionalidades/">Ver todas las funcionalidades →</a></p>'
            f'{cta_html}</div></section>')


PRODUCT_CSS = r"""
.plead{font-size:18px;line-height:1.6;color:var(--muted);margin:0 0 26px;max-width:760px;}
.pgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}
.pitem{display:flex;gap:14px;align-items:flex-start;background:#fff;border:1px solid var(--line);border-radius:20px;padding:20px;}
.pitem h3{font-family:'Gabarito',sans-serif;font-size:19px;margin:2px 0 6px;}
.pitem p{margin:0;font-size:15.5px;line-height:1.5;color:var(--muted);}
.mcta{margin-top:26px;text-align:center;}
.pmore{margin:22px 0 0;font-weight:700;}.pmore a{color:var(--v);}
@media(max-width:860px){.pgrid{grid-template-columns:1fr;}}
"""



WHAT = [
    ('¿Qué es?', 'Tu hoja de ruta del año: cuánto quieres facturar, cuánto vas a gastar y cuánto te quedará, mes a mes.'),
    ('¿Para qué sirve?', 'Para saber si vas bien antes de que acabe el año, decidir con números (contratar, subir precios, invertir), preparar los meses flojos y tenerlo listo si un día vas al banco.'),
    ('¿Cuándo hacerlo?', 'Ahora, antes de que empiece 2027. Así enero arranca con un objetivo y no con un «a ver qué tal».'),
]


def what_html(cta_html=''):
    cols = ''.join(f'<div class="wcol"><h3>{html.escape(t)}</h3><p>{html.escape(x)}</p></div>' for t, x in WHAT)
    return ('<section class="sec"><div class="w">'
            '<h2 class="h2">Un plan financiero es tu objetivo del año, <span class="grad">convertido en números de cada mes</span></h2>'
            f'<div class="wgrid">{cols}</div><div class="mcta">{cta_html}</div></div></section>')


WHAT_CSS = r"""
.wgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}
.wcol{border-radius:20px;padding:22px 24px;background:var(--soft);border:1px solid var(--line);}
.wcol h3{font-family:'Gabarito',sans-serif;font-size:22px;margin:0 0 8px;color:var(--v);}
.wcol p{margin:0;font-size:16.5px;line-height:1.55;color:var(--ink);}
@media(max-width:860px){.wgrid{grid-template-columns:1fr;}}
"""



# Trazos «a mano alzada»: círculo alrededor de una palabra y subrayado tipo rotulador.
CIRCLE_SVG = ('<svg class="circ-svg" viewBox="0 0 300 100" preserveAspectRatio="none" aria-hidden="true">'
              '<path d="M52 16C128 2 262 4 291 38c22 34-78 60-170 58C46 94 4 76 10 48 16 22 78 10 168 8"/></svg>')


def circ(text):
    return f'<span class="circ">{text}{CIRCLE_SVG}</span>'


def mark(text):
    return f'<span class="mark">{text}</span>'


HAND_CSS = r"""
.mark{position:relative;z-index:0;font-style:italic;white-space:nowrap;padding:0 .06em;}
.mark::before{content:"";position:absolute;z-index:-1;left:-.08em;right:-.12em;bottom:.06em;height:.46em;background:var(--y);border-radius:.25em .6em .35em .7em;transform:rotate(-1.6deg) skewX(-8deg);transform-origin:left;animation:mk .7s .25s ease-out both;}
@keyframes mk{from{transform:rotate(-1.6deg) skewX(-8deg) scaleX(0);}}
.circ{position:relative;display:inline-block;white-space:nowrap;margin:0 .12em;}
.circ-svg{position:absolute;left:-5%;top:-16%;width:110%;height:134%;overflow:visible;pointer-events:none;}
.circ-svg path{fill:none;stroke:var(--v);stroke-width:3.2;stroke-linecap:round;vector-effect:non-scaling-stroke;stroke-dasharray:900;stroke-dashoffset:900;animation:cdraw 1.1s .5s ease-out forwards;}
@keyframes cdraw{to{stroke-dashoffset:0;}}
.h2 .grad{font-style:italic;padding-right:.08em;}
@media(prefers-reduced-motion:reduce){.mark::before,.circ-svg path{animation:none;stroke-dashoffset:0;}}
"""


VIDEO = ('<div class="vid"><div class="vbox"><video muted playsinline loop preload="none" data-vid="tutorial-plan" '
         'poster="/lp/plan-financiero-2027/tutorial-poster.webp" width="1280" height="720">'
         '<source src="/lp/plan-financiero-2027/tutorial-plan-financiero.mp4" type="video/mp4"></video>'
         '<button type="button" class="vsound" aria-label="Activar el sonido del vídeo">' + icon('sound', 'ico--i') + ' Activa la voz</button></div>'
         '<p>Así se crea el plan, paso a paso (2 min).</p></div>')

# Se reproduce solo y sin sonido cuando se ve en pantalla (los navegadores solo dejan
# reproducir solos los vídeos silenciados). «Activa la voz» lo reinicia con sonido.
VIDEO_JS = ("document.querySelectorAll('.vbox').forEach(function(box){var v=box.querySelector('video'),b=box.querySelector('.vsound'),lp=document.body.getAttribute('data-lp');"
            "function ev(n){try{if(window.posthog)posthog.capture(n,{lp:lp,video:v.getAttribute('data-vid')});}catch(_){}}"
            "if('IntersectionObserver' in window){new IntersectionObserver(function(es){es.forEach(function(e){if(!v.muted)return;"
            "if(e.isIntersecting){var p=v.play();if(p&&p.catch)p.catch(function(){});}else v.pause();});},{threshold:.5}).observe(v);}"
            "b.addEventListener('click',function(){v.muted=false;v.currentTime=0;v.loop=false;v.controls=true;var p=v.play();if(p&&p.catch)p.catch(function(){});b.remove();ev('lp_video_unmute');});"
            "v.addEventListener('play',function(){ev('lp_video_play');},{once:true});});")

EXTRA_CSS = r'''
.top{position:absolute;}
.w{max-width:1280px;padding:0 32px;}
@media(min-width:1600px){.w{max-width:1440px;}}
@media(max-width:860px){.w{padding:0 20px;}}
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
.after li{align-items:center;}
.after .shots{display:grid;grid-template-columns:1fr;gap:14px;align-items:start;}
.vid{max-width:1040px;margin:0 auto 34px;text-align:center;}
.vid video{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;display:block;border-radius:18px;background:#0c0628;box-shadow:0 24px 60px rgba(40,10,120,.2);}
.vid p{margin:10px 0 0;font-size:14px;color:var(--muted);}
.vbox{position:relative;}
.vsound{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);border:0;cursor:pointer;background:var(--y);color:var(--ink);font:800 16px/1 'Plus Jakarta Sans',sans-serif;padding:13px 20px;border-radius:999px;box-shadow:0 10px 30px rgba(0,0,0,.35);animation:vpulse 1.8s ease-in-out infinite;}
@keyframes vpulse{50%{transform:translateX(-50%) scale(1.06);}}
@media(prefers-reduced-motion:reduce){.vsound{animation:none;}}
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
        shot('paso-numeros.webp', 1270, 650, 'Paso 1 del plan: tus números de partida', 'números de partida'),
        shot('paso-crecer.webp', 1360, 760, 'Paso 2 del plan: cuánto quieres crecer en 2027', '% de crecimiento'),
        shot('real-vs-plan.webp', 1420, 540, 'Seguimiento mes a mes: beneficio previsto y real', 'seguimiento mes a mes'),
    ]
    steps = ''.join(
        f'<div class="step2"><span class="n grad">0{i}</span><h3>{e(t)}</h3>'
        + (f'<p>{e(x)}</p>' if x else '') + step_shots[i - 1] + '</div>'
        for i, (t, x) in enumerate(STEPS, 1))
    after = ''.join(f'<li>{icon(ic)}<span>{e(t)}</span></li>' for ic, t in AFTER)
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
<style>{CSS}{EXTRA_CSS}{TST_CSS}{SALON_CSS}{WHY_CSS}{ICON_CSS}{PRODUCT_CSS}{WHAT_CSS}{HAND_CSS}</style>
</head>
<body data-lp="{SLUG}">
<header class="top"><div class="w"><img src="/wp-images/logo-gradient.png" alt="Godolphy" style="height:30px;width:auto;"></div></header>

<main>
<section class="hero2" id="hero">
  <div class="w grid">
    <div>
      <div class="y grad" aria-hidden="true">2027</div>
      <h1>{mark('Mueve el culo')} y crea el {circ('plan financiero')} de tu salón para 2027</h1>
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

{testimonials_html()}

{salons_html()}

{what_html(cta('what'))}

<section class="sec">
  <div class="w">
    <h2 class="h2">Trabajas mucho. <span class="grad">Pero no sabes si avanzas.</span></h2>
    <ul class="pains2">{pains}</ul>
    <p class="close">No es que trabajes poco. <span class="grad">Es que trabajas sin plan.</span></p>
  </div>
</section>

<section class="sec sec--soft">
  <div class="w big-co">
    <h2 class="h2">Las grandes marcas se marcan un objetivo cada año. <span class="grad">Tu salón también puede.</span></h2>
    <p>Las grandes marcas no improvisan: se marcan un objetivo y lo miran cada mes. Que tu salón sea pequeño no es excusa. Es justo por eso que lo necesitas.</p>
  </div>
  <div class="w">{why_cards()}<div class="mcta">{cta('why')}</div></div>
</section>

<section class="sec">
  <div class="w">
    <h2 class="h2">Tu plan 2027 en 3 pasos, <span class="grad">sin saber de finanzas</span></h2>
    {VIDEO}
    <div class="steps2">{steps}</div>
    {cta('steps')}
  </div>
</section>

<section class="sec sec--soft">
  <div class="w after">
    <div>
      <h2 class="h2">Cada mes sabes si vas <span class="grad">por delante o por detrás</span></h2>
      <ul>{after}</ul>
      <div style="margin-top:22px;">{cta('after')}</div>
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
      <h2 class="h2">Detrás de Godolphy: <span class="grad">15 años en multinacionales y un salón propio</span></h2>
      <p>Soy Neus. He trabajado unos 15 años en multinacionales y monté mi propio salón con una socia, donde yo llevaba la parte de negocio.</p>
      <p>Godolphy es el consultor financiero que mi salón nunca tuvo.</p>
      <p class="sig">Neus, fundadora de Godolphy</p>
    </div>
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
