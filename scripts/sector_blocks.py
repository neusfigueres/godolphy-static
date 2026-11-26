"""Bloques nuevos de las páginas de sector (nov. 2026), sobre las páginas ya transformadas por sector_refresh.py.

1. Reserva desde el móvil: la imagen de «Reservas online 24 h» pasa a ser tres móviles con capturas reales del booking.
2. Calculadora de precios: bloque propio con un ejemplo por sector (cifras de ejemplo, mismo cálculo que el producto).
3. «¿Por qué Godolphy…?»: lo que nos diferencia de la gestión actual del salón, antes de las preguntas frecuentes.

Idempotente: cada bloque lleva una marca y no se vuelve a insertar.
Uso: python3 scripts/sector_blocks.py
"""
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_lp_plan import icon  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SIGNUP = 'https://app.godolphy.com/auth/sign-up'
IVA = 1.21
MARGEN = 0.35


def it(t):
    return f'<span class="it">{t}</span>'


def eur(x):
    return f'{x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.') + ' €'


def recomendado(coste):
    """Igual que el producto: coste / (1 − margen), con IVA, redondeado hacia arriba a 0,50 €."""
    return math.ceil(coste / (1 - MARGEN) * IVA * 2) / 2


SECTORES = {
    'peluquerias': dict(tipo='Peluquería',
        file='sectores/software-para-peluquerias/index.html', negocio='peluquería', pro='peluquero/a',
        corto='un lavar y peinar o un flequillo',
        servicios=[('Lavar y peinar', '30 min', 14, 13.20), ('Corte caballero', '30 min', 15, 9.40), ('Mechas balayage', '2 h 30 min', 95, 48)]),
    'barberias': dict(tipo='Barbería',
        file='sectores/software-para-barberias/index.html', negocio='barbería', pro='barbero',
        corto='un arreglo de barba',
        servicios=[('Arreglo de barba', '15 min', 8, 7.10), ('Corte + barba', '45 min', 22, 14.10), ('Corte degradado', '40 min', 20, 10.20)]),
    'estetica': dict(tipo='Centro de estética',
        file='sectores/software-para-centro-de-estetica-y-salones/index.html', negocio='centro', pro='esteticista',
        corto='una depilación pequeña',
        servicios=[('Depilación labio', '10 min', 6, 5.30), ('Presoterapia', '45 min', 30, 18.60), ('Higiene facial', '60 min', 55, 26)]),
    'unas': dict(tipo='Salón de uñas',
        file='sectores/software-para-salones-de-unas/index.html', negocio='salón', pro='nail artist',
        corto='una decoración o una retirada',
        servicios=[('Decoración por uña', '10 min', 3, 2.79), ('Retirada de semipermanente', '20 min', 10, 6.90), ('Semipermanente', '45 min', 25, 12.40)]),
    'spa': dict(tipo='Spa y masajes',
        file='sectores/software-para-spa-y-masajes/index.html', negocio='spa', pro='terapeuta',
        corto='un ritual corto',
        servicios=[('Ritual de pies', '20 min', 18, 16.20), ('Masaje 30 min', '30 min', 35, 21), ('Masaje relajante 60 min', '60 min', 60, 30)]),
}

PHONES = [('portada', 'Eliges en el local o a domicilio'), ('servicios', 'Ves cada servicio con su foto, precio y duración'),
          ('resumen', 'Confirmas día, hora y profesional')]


# ---------- 0. Cabecera: «Ver demo» y «Pide una demo con Neus» (assets/gx-demo.js) ----------
def hero_demo(s, c):
    if 'data-gd-demo' in s:
        return s
    i = s.find('<section class="hero-bg hero-photo"')
    a = s.find('>Prueba Godolphy gratis 30 días</a>', i) + len('>Prueba Godolphy gratis 30 días</a>')
    assert a > i
    t = c['tipo']
    s = s[:a] + (f'<a href="#demo" class="gd-demo-btn" data-gd-demo="video" data-sector="{t}">'
                 '<span class="gd-play" aria-hidden="true"></span>Ver demo (1:30)</a>') + s[a:]
    p = s.find('30 días gratis · Sin tarjeta de crédito</p>', a) + len('30 días gratis · Sin tarjeta de crédito</p>')
    s = s[:p] + (f'<p class="gd-demo-neus">¿Prefieres que te lo enseñe en directo? '
                 f'<a href="#demo-neus" data-gd-demo="neus" data-sector="{t}">Pide una demo con Neus →</a></p>') + s[p:]
    if '/assets/gx-demo.js' not in s:
        s = s.replace('<script src="/assets/gx-pages.js"', '<script src="/assets/gx-demo.js?v=2" defer></script>\n<script src="/assets/gx-pages.js"', 1)
    return s


# ---------- 1. Reserva desde el móvil ----------
def booking_movil(s, c):
    if 'bm-phones' in s:
        return s
    h = s.find('Reservas online 24 h')
    sec_end = s.find('</section>', h)
    i = s.find('<img ', h)
    assert 0 < i < sec_end, 'imagen de reservas no encontrada'
    # la columna de la imagen: <div ...><img ...></div>
    k = s.rfind('<div', 0, i)
    e = s.find('</div>', i) + len('</div>')
    phones = ''.join(
        f'<figure class="bm-phone"><div class="bm-screen"><img src="/images/sectores/booking-movil/{f}.webp" alt="{alt}" loading="lazy" width="600" height="1133"></div>'
        f'<figcaption>{alt}</figcaption></figure>' for f, alt in PHONES)
    col = (f'<div class="bm-col"><div class="bm-phones">{phones}</div>'
           '<p class="bm-note">Capturas reales de la web de reservas de un salón de demostración, en el móvil.</p></div>')
    s = s[:k] + col + s[e:]
    # texto: lista + enlace a la funcionalidad
    ul_end = s.find('</ul>', h)
    li = s.rfind('<li', 0, ul_end)
    li_end = s.find('</li>', li) + len('</li>')
    tpl = s[li:li_end]
    new_li = re.sub(r'(</svg>).*(</li>)', r'\1Pensada para el móvil: tus clientes reservan en un minuto, con fotos de tus servicios\2', tpl, flags=re.S)
    s = s[:ul_end] + new_li + s[ul_end:]
    ul_end = s.find('</ul>', h) + len('</ul>')
    s = s[:ul_end] + '<a class="gd-more" href="/funcionalidades/reservas-online/" data-cta="sector-feature">Cómo funciona la web de reservas →</a>' + s[ul_end:]
    return s


# ---------- 2. Calculadora de precios ----------
def calc_rows(servicios):
    rows = []
    for nombre, dur, precio, coste in servicios:
        neto = precio / IVA
        ben = neto - coste
        m = ben / neto
        if ben < 0:
            tag, cls = 'Pierdes dinero', 'bad'
        elif m < MARGEN:
            tag, cls = 'Por debajo de tu margen', 'mid'
        else:
            tag, cls = 'Bien', 'ok'
        rec = '' if cls == 'ok' else (f'<div class="cx-rec">Precio recomendado <b>{eur(recomendado(coste))}</b>'
                                      f'<span class="cx-apply">Aplicar</span></div>')
        signo = '−' if ben < 0 else '+'
        rows.append(f'''<li class="cx-row cx-{cls}">
          <div class="cx-top"><div><b>{nombre}</b><small>{dur}</small></div><span class="cx-tag">{tag}</span></div>
          <div class="cx-nums"><span>Cobras<b>{eur(precio)}</b></span><span>Te cuesta<b>{eur(coste)}</b></span><span>Beneficio<b class="cx-ben">{signo}{eur(abs(ben))}</b></span></div>
          {rec}
        </li>''')
    return ''.join(rows)


def calculadora(c):
    return f'''
<!-- gd-blocks:calculadora (sector_blocks.py) -->
<section class="gd-sec cx-sec">
  <div class="gd-wrap cx-wrap">
    <div class="cx-text">
      <span class="cx-kicker">Calculadora de precios</span>
      <h2>¿Cuánto te cuesta de verdad cada servicio? Godolphy te dice {it('a qué precio cobrarlo')}</h2>
      <p>Reparte tus costes reales (equipo, local y gastos) entre tus horas de servicio y te dice qué servicios te hacen perder dinero. Muchas veces son los cortos, como {c['corto']}.</p>
      <ul class="cx-list">
        <li>{icon('chart', 'ico ico--s')}Con tus horarios, tus citas y tus gastos, no con medias del sector</li>
        <li>{icon('spark', 'ico ico--s')}Cada servicio con su etiqueta: pierdes dinero, por debajo de tu margen o bien</li>
        <li>{icon('sync', 'ico ico--s')}Pulsas «Aplicar» y el precio nuevo llega a tu web de reservas</li>
      </ul>
      <div class="gd-cta2"><a class="gd-btn2" href="{SIGNUP}" data-cta="sector-calculadora">Prueba gratis 30 días →</a><a class="gd-more" href="/funcionalidades/calculadora-de-precios/" data-cta="sector-feature">Cómo funciona la calculadora →</a></div>
      <p class="cx-foot">Incluida en los planes Pro y Max, y en la prueba gratuita.</p>
    </div>
    <div class="gd-card cx-card">
      <div class="cx-head"><b>Precios</b><span>Margen que quieres: 35&nbsp;%</span></div>
      <ul class="cx-rows">{calc_rows(c['servicios'])}</ul>
      <p class="cx-ex">Cifras de ejemplo.</p>
    </div>
  </div>
</section>
'''


# ---------- 3. ¿Por qué Godolphy? ----------
def porque(c):
    n = c['negocio']
    cards = [
        ('cal', 'Tu web de reservas, con fotos',
         'Cada servicio con su foto, su precio y su duración. El cliente ve lo que reserva y se decide sin escribirte para preguntar.'),
        ('team', 'Solo tu negocio, sin competencia al lado',
         f'En los directorios de reservas, tu perfil aparece junto a otros negocios de tu zona. Tu web de Godolphy es solo de tu {n}: tu nombre, tu logo y tus servicios.'),
        ('trend', 'Te dice cómo ganar más, no solo quién viene',
         'El análisis con IA, la calculadora de precios y el plan financiero te dicen qué servicios te hacen perder dinero, qué clientes no vuelven y cómo va el mes.'),
        ('card', 'Si no viene, no lo pierdes',
         'El cliente deja su tarjeta al reservar. Si no se presenta, puedes cobrarle con esa tarjeta desde el panel.'),
        ('gift', 'La señal no te cuesta comisión',
         'En las citas de los próximos 6 días, la señal es una retención en la tarjeta, no un cobro: si el cliente viene, se libera y no pagas comisión por ella.'),
    ]
    items = ''.join(f'<div class="py-card">{icon(ic)}<h3>{t}</h3><p>{x}</p></div>' for ic, t, x in cards)
    return f'''
<!-- gd-blocks:porque (sector_blocks.py) -->
<section class="gd-sec py-sec">
  <div class="gd-wrap">
    <div class="gd-head">
      <h2>¿Por qué Godolphy y no {it('tu sistema de siempre')}?</h2>
      <p>Lo que cambia cuando tu agenda, tus cobros y tus números están en el mismo sitio.</p>
    </div>
    <div class="py-grid">{items}</div>
    <div class="py-cta"><a class="gx-btn" href="{SIGNUP}" data-cta="sector-porque">Prueba Godolphy gratis 30 días</a><small>30 días gratis · Sin tarjeta de crédito</small></div>
  </div>
</section>
'''


def apply(key):
    c = SECTORES[key]
    p = ROOT / c['file']
    s = p.read_text()
    s = hero_demo(s, c)
    s = booking_movil(s, c)
    if 'gd-blocks:calculadora' not in s:
        a = '<section class="gx-steps-sec">'
        assert s.count(a) == 1
        s = s.replace(a, calculadora(c) + a)
    if 'gd-blocks:porque' not in s:
        h = s.find('Lo que te preguntas ')
        k = s.rfind('<section', 0, h)
        assert k > 0
        s = s[:k] + porque(c) + '\n' + s[k:]
    p.write_text(s)
    print('ok', key)


if __name__ == '__main__':
    for k in (sys.argv[1:] or SECTORES):
        apply(k)
