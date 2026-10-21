#!/usr/bin/env python3
"""Genera /verifactu/index.html (landing SEO) a partir del chrome de facturacion-y-reporte."""
import json, re, html

SRC = 'funcionalidades/facturacion-y-reporte/index.html'
OUT = 'verifactu/index.html'
URL = 'https://www.godolphy.com/verifactu/'
TITLE = 'Verifactu para peluquerías y centros de estética: qué es, fechas y cómo cumplir | Godolphy'
DESC = ('Qué es Verifactu, cuándo es obligatorio y qué cambia para tu salón. Con Godolphy, cobras la cita '
        'y el tique con QR ya está en Hacienda, sin programas aparte.')
UPDATED = '21 de octubre de 2026'

FAQ = [
    ('¿Qué es Verifactu?',
     'Es el sistema de la Agencia Tributaria que regula los programas de facturación (Reglamento aprobado por el Real Decreto 1007/2023). '
     'Obliga a que cada factura o tique genere un registro que no se puede modificar, encadenado con el anterior y con un código QR. '
     'En la modalidad VERI*FACTU, ese registro se envía a Hacienda en el momento.'),
    ('¿Cuándo es obligatorio Verifactu?',
     'Según el Real Decreto-ley 15/2025, el 1 de enero de 2027 para las sociedades y el 1 de julio de 2027 para el resto, incluidos los autónomos. '
     'El 5 de octubre de 2026 Hacienda anunció que lo aplazará a octubre de 2028, pero ese cambio todavía no se ha publicado en el BOE. '
     'Hasta que se publique, las fechas vigentes son las de 2027.'),
    ('¿Afecta a peluquerías, barberías y centros de estética?',
     'Sí, si emites tus tiques o facturas con un programa informático. Da igual que sean tiques (facturas simplificadas) a clientas particulares: también cuentan.'),
    ('¿Tengo que hacer algo para cumplir Verifactu con Godolphy?',
     'No. Cuando cobras una cita en el panel, Godolphy genera el tique con su QR VERI*FACTU y lo envía a Hacienda automáticamente. No tienes que configurar nada.'),
    ('¿Verifactu está activo durante la prueba gratuita?',
     'No. Verifactu se activa con tu suscripción de pago, desde el primer mes. Durante los 30 días de prueba gratuita no está activo.'),
    ('¿Qué pasa si hago una devolución?',
     'Godolphy genera automáticamente la factura rectificativa y también la envía a Hacienda.'),
    ('¿Puedo enviar el tique a la clienta?',
     'Sí. Puedes enviárselo por email con un botón o hacer que se envíe automáticamente al cobrar. También puedes imprimirlo.'),
    ('¿Qué multa hay por no cumplir Verifactu?',
     'La Ley General Tributaria (artículo 201 bis) prevé multas de hasta 50.000 euros por cada ejercicio para quien use un programa de facturación que no cumpla la normativa.'),
]

def faq_html():
    out = []
    for q, a in FAQ:
        out.append('<div class="faq-item"><button class="faq-btn" onclick="toggleFaq(this)"><span style="color:#02021e;font-size:17px;font-weight:600;">'
                   + html.escape(q) + '</span><svg class="faq-icon" width="20" height="20" fill="none" stroke="#631cff" stroke-width="2.5" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg></button>'
                   '<div class="faq-body"><p style="color:rgba(2,2,30,.65);font-size:16px;line-height:1.65;margin:0;">' + html.escape(a) + '</p></div></div>')
    return '\n'.join(out)

LD = [
    {"@context": "https://schema.org", "@type": "FAQPage",
     "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://www.godolphy.com/"},
        {"@type": "ListItem", "position": 2, "name": "Verifactu", "item": URL}]},
    {"@context": "https://schema.org", "@type": "WebPage", "name": TITLE, "description": DESC, "url": URL,
     "dateModified": "2026-10-21", "inLanguage": "es-ES"},
]

CHECK = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#631cff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex:0 0 20px;margin-top:2px;"><path d="M20 6 9 17l-5-5"/></svg>'

MAIN = f'''<main>
<section class="hero-bg" style="position:relative;padding:130px 40px 110px;text-align:center;overflow:hidden;">
  <img src="/assets/verifactu-white.png" alt="VERI*FACTU" width="246" height="60" style="display:block;height:44px;width:auto;margin:0 auto 26px;opacity:.95;">
  <h1 class="font-gabarito" style="color:#fff;font-size:56px;font-weight:700;margin:0 auto 20px;line-height:1.05;max-width:900px;">Verifactu para peluquerías y centros de estética</h1>
  <p style="color:rgba(255,255,255,.85);font-size:20px;line-height:1.6;max-width:680px;margin:0 auto;">Qué es, cuándo es obligatorio y qué cambia en tu salón. Con Godolphy, cobras la cita y el tique ya está en Hacienda.</p>
  <div style="margin-top:36px;display:flex;gap:16px;justify-content:center;flex-wrap:wrap;">
    <a href="/lista-de-espera/" style="background:#EEFE3A;color:#02021e;font-size:16px;font-weight:700;padding:14px 36px;border-radius:20px;text-decoration:none;">Apúntate a la lista de espera</a>
  </div>
  <p style="color:rgba(255,255,255,.6);font-size:13px;margin:22px 0 0;">Actualizado el {UPDATED}</p>
  <div style="position:absolute;bottom:-1px;left:0;right:0;line-height:0;"><svg viewBox="0 0 1440 60" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" style="display:block;width:100%;height:60px;"><path d="M0,30 C360,60 1080,0 1440,30 L1440,60 L0,60 Z" fill="#fff"/></svg></div>
</section>

<section class="gx-bento-sec" style="padding-top:90px;"><div class="gx-wrap">
  <div style="text-align:center;">
    <span class="gx-eyebrow">Qué es</span>
    <h2 class="gx-h2">Qué es <span class="gx-grad">Verifactu</span>, sin letra pequeña</h2>
    <p class="gx-lead" style="margin:0 auto;">Es el sistema de la Agencia Tributaria que regula los programas con los que se emiten facturas y tiques (Reglamento aprobado por el Real Decreto 1007/2023). El objetivo: que ninguna venta se pueda borrar o modificar después.</p>
  </div>
  <div class="gx-bento">
    <article class="gx-card gx-c4"><div class="gx-step__n gx-grad" style="font-size:48px;margin-bottom:14px;">01</div><h3>Registro que no se puede tocar</h3><p>Cada tique genera un registro con una huella encadenada al anterior. Si alguien lo cambia, se nota.</p></article>
    <article class="gx-card gx-c4"><div class="gx-step__n gx-grad" style="font-size:48px;margin-bottom:14px;">02</div><h3>Un QR en cada tique</h3><p>Tus clientas pueden escanearlo y comprobar en la web de Hacienda que el tique se ha registrado.</p></article>
    <article class="gx-card gx-c4"><div class="gx-step__n gx-grad" style="font-size:48px;margin-bottom:14px;">03</div><h3>Envío a Hacienda al momento</h3><p>En la modalidad VERI*FACTU, cada registro se envía a la Agencia Tributaria en cuanto cobras.</p></article>
  </div>
</div></section>

<section class="gx-steps-sec"><div class="gx-wrap" style="max-width:980px;">
  <div style="text-align:center;">
    <span class="gx-eyebrow">Fechas</span>
    <h2 class="gx-h2">¿Cuándo es <span class="gx-grad">obligatorio</span>?</h2>
    <p class="gx-lead" style="margin:0 auto;">Las fechas ya se han aplazado varias veces. Esto es lo que hay a {UPDATED}.</p>
  </div>
  <div class="gx-steps3 gx-two">
    <div class="gx-step"><span class="gx-eyebrow" style="font-size:11px;">Vigente · Real Decreto-ley 15/2025</span><div class="gx-step__n gx-grad" style="font-size:40px;margin:18px 0 8px;">1 ene 2027</div><h3>Sociedades</h3><p>Contribuyentes del Impuesto sobre Sociedades (por ejemplo, si tu salón es una SL).</p></div>
    <div class="gx-step"><span class="gx-eyebrow" style="font-size:11px;">Vigente · Real Decreto-ley 15/2025</span><div class="gx-step__n gx-grad" style="font-size:40px;margin:18px 0 8px;">1 jul 2027</div><h3>Autónomos y resto</h3><p>Profesionales autónomos y el resto de obligados que emiten facturas o tiques con un programa.</p></div>
  </div>
  <div style="margin-top:24px;background:#fff;border:1px dashed rgba(99,28,255,.35);border-radius:20px;padding:22px 26px;display:flex;gap:14px;align-items:flex-start;">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#631cff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex:0 0 22px;margin-top:2px;"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>
    <p style="margin:0;font-size:15.5px;line-height:1.6;color:rgba(2,2,30,.75);"><b style="color:#02021e;">Aplazamiento anunciado a octubre de 2028.</b> El 5 de octubre de 2026 Hacienda anunció un nuevo aplazamiento para alinearlo con la factura electrónica obligatoria. Todavía no se ha publicado en el BOE, así que, hasta entonces, las fechas legales son las de 2027. Actualizaremos esta página en cuanto se publique.</p>
  </div>
</div></section>

<section class="gx-ai"><div class="gx-wrap gx-ai__grid">
  <div>
    <span class="gx-eyebrow">Con Godolphy</span>
    <h2 class="gx-h2">Cobra la cita y el tique ya está en Hacienda.</h2>
    <p class="gx-lead">No necesitas un programa de facturación aparte. Verifactu está integrado en el cobro de la cita, y tú no tienes que configurar nada.</p>
    <ul class="gx-ai__list">
      <li>Al cobrar, se genera el tique (factura simplificada) con su QR VERI*FACTU</li>
      <li>Se envía a Hacienda automáticamente y ves su estado en la propia cita</li>
      <li>Si haces una devolución, la factura rectificativa se hace sola</li>
      <li>La clienta recibe el tique por email, con un botón o de forma automática</li>
      <li>Activo desde el primer mes de tu suscripción de pago (no durante la prueba gratuita)</li>
    </ul>
    <a class="gx-btn gx-btn--light" href="/ayuda/verifactu/">Ver cómo funciona paso a paso</a>
  </div>
  <div style="display:flex;justify-content:center;">
    <img src="/ayuda/img/verifactu-tique.jpg" alt="Tique de un salón con el código QR VERI*FACTU" width="460" height="690" loading="lazy" style="width:100%;max-width:340px;height:auto;border-radius:22px;box-shadow:0 30px 80px rgba(0,0,0,.45);background:#fff;">
  </div>
</div></section>

<section style="background:#fff;padding:110px 40px;"><div class="gx-wrap">
  <div class="gx-split">
    <div>
      <span class="gx-eyebrow">En tu panel</span>
      <h2 class="gx-h2">Cada cobro, con su <span class="gx-grad">tique y su estado</span></h2>
      <p class="gx-lead">En el bloque «Cobros» de cada cita ves el número de tique y si Hacienda lo ha aceptado. Sin abrir otro programa.</p>
      <ul style="list-style:none;padding:0;margin:26px 0 0;display:flex;flex-direction:column;gap:12px;font-size:16px;color:rgba(2,2,30,.8);">
        <li style="display:flex;gap:12px;">{CHECK}Número de tique y estado del envío</li>
        <li style="display:flex;gap:12px;">{CHECK}Pagos divididos entre varios métodos</li>
        <li style="display:flex;gap:12px;">{CHECK}Todo queda guardado para el cierre de caja</li>
      </ul>
    </div>
    <div><img src="/ayuda/img/verifactu-cobros.jpg" alt="Bloque Cobros de una cita con el número de tique y su estado en Hacienda" width="1535" height="784" loading="lazy" style="width:100%;height:auto;border-radius:18px;box-shadow:0 20px 60px rgba(2,2,30,.12);border:1px solid rgba(99,28,255,.10);"></div>
  </div>
</div></section>

<section style="background:#f8f7ff;padding:100px 40px;"><div class="gx-wrap" style="max-width:900px;">
  <div style="text-align:center;margin-bottom:40px;">
    <span class="gx-eyebrow">Riesgos</span>
    <h2 class="gx-h2">¿Qué pasa si <span class="gx-grad">no cumples</span>?</h2>
  </div>
  <div class="gx-bento" style="margin-top:0;">
    <article class="gx-card gx-c6" style="background:#fff;"><h3>Hasta 50.000 € por ejercicio</h3><p>La Ley General Tributaria (artículo 201 bis) prevé esta multa para quien use un programa de facturación que no cumpla la normativa.</p></article>
    <article class="gx-card gx-c6" style="background:#fff;"><h3>Ojo con las hojas de cálculo</h3><p>Si emites tiques con un Excel o con un programa que permite borrar ventas, ese sistema no cumple. Lo más sencillo es que el tique salga del mismo sitio donde cobras la cita.</p></article>
  </div>
  <p style="text-align:center;font-size:13.5px;color:rgba(2,2,30,.5);margin:28px 0 0;">Esta página es informativa y no sustituye el asesoramiento de un gestor o asesor fiscal.</p>
</div></section>

<section style="background:#fff;padding:96px 40px;"><div style="max-width:780px;margin:0 auto;"><div style="text-align:center;margin-bottom:56px;"><h2 class="font-gabarito" style="background:linear-gradient(90deg,#9B4FE8,#631cff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-size:42px;font-weight:700;margin:0;">Preguntas frecuentes sobre Verifactu</h2></div>
{faq_html()}
</div></section>

<section style="background:#f8f7ff;padding:80px 40px;"><div style="max-width:900px;margin:0 auto;background:linear-gradient(160deg,#9B4FE8 0%,#7835C3 30%,#631cff 65%,#3a0aaa 100%);border-radius:32px;padding:80px 60px;text-align:center;"><h2 class="font-gabarito" style="color:#fff;font-size:46px;line-height:1.1;font-weight:700;margin:0 0 20px;">Olvídate de Verifactu. Cobra y listo.</h2><p style="color:rgba(255,255,255,.85);font-size:18px;line-height:1.6;max-width:560px;margin:0 auto 40px;">Reservas, agenda, cobros y tiques con Verifactu en un solo sitio. 30 días para probarlo todo.</p><div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;"><a href="/lista-de-espera/" style="background:#EEFE3A;color:#02021e;font-size:18px;font-weight:700;padding:16px 40px;border-radius:20px;text-decoration:none;">Apúntate a la lista de espera</a></div></div></section>

<section style="background:#fff;padding:70px 40px 90px;"><div class="gx-wrap" style="max-width:900px;">
  <h2 class="font-gabarito" style="font-size:26px;color:#02021e;margin:0 0 20px;">Sigue leyendo</h2>
  <div style="display:flex;flex-wrap:wrap;gap:10px;">
    <a class="gx-chip" href="/ayuda/verifactu/" style="text-decoration:none;">Verifactu en Godolphy, paso a paso</a>
    <a class="gx-chip" href="/funcionalidades/facturacion-y-reporte/" style="text-decoration:none;">Facturación y reportes</a>
    <a class="gx-chip" href="/obligaciones-fiscales-centro-estetica/" style="text-decoration:none;">Obligaciones fiscales de un centro de estética</a>
    <a class="gx-chip" href="/precio/" style="text-decoration:none;">Precio</a>
  </div>
</div></section>
</main>'''


def build():
    s = open(SRC, encoding='utf-8').read()
    s = re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', s, 1, re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + DESC, s, 1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', r'\g<1>' + URL, s, 1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>' + TITLE, s, 1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>' + DESC, s, 1)
    s = re.sub(r'<meta property="og:url" content="[^"]*"\s*/?>', '', s)
    s = s.replace('<meta property="og:description"', f'<meta property="og:url" content="{URL}" />\n  <meta property="og:description"', 1)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', s, flags=re.S)
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in LD)
    s = s.replace('</head>', ld + '</head>', 1)
    s = re.sub(r'<main>.*?</main>', lambda m: MAIN, s, 1, re.S)
    import os
    os.makedirs('verifactu', exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(s)
    print('ok', OUT)

if __name__ == '__main__':
    build()
