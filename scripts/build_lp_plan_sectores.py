#!/usr/bin/env python3
"""Copias por sector de las landings del plan financiero 2027.

Las landings «master» son /lp/plan-financiero-2027/ (A) y /lp/plan-financiero-2027-b/ (B),
generadas por build_lp_plan.py y build_lp_plan_b.py. Este script parte del HTML de
cada master y lo adapta a un sector cambiando solo textos (nunca rutas de imágenes):
  /lp/plan-financiero-2027-<sector>/     ← A
  /lp/plan-financiero-2027-b-<sector>/   ← B

La historia de Neus («mi propio salón», «el consultor que mi salón nunca tuvo») y el
negocio de cada testimonio NO se cambian: son hechos reales.

Uso: python3 scripts/build_lp_plan_sectores.py [sector ...]   (sin argumentos: todos)
Para añadir un sector, añade una entrada a SECTORES. El seguimiento de todas las
landings se lleva en el Excel «seguimiento-landings.xlsx» (fuera del repo: no debe ser público).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_lp_plan as A  # noqa: E402
import build_lp_plan_b as B  # noqa: E402

SALONS_MASTER = ('<h2 class="h2">Hecho para salones: <span class="grad">peluquerías, centros de estética y salones de uñas</span></h2>')

SECTORES = {
    'peluquerias': {
        'tag': 'Peluquerías · Mueve el culo',
        'textos': [
            # (texto del master, texto del sector). Se aplican en este orden.
            ('Que tu salón sea pequeño no es excusa', 'Que tu peluquería sea pequeña no es excusa'),
            ('tu salón', 'tu peluquería'),
            ('Tu salón también puede', 'Tu peluquería también puede'),
            ('el del salón van juntos', 'el de la peluquería van juntos'),
            ('el salón va bien', 'la peluquería va bien'),
            ('el día a día del salón', 'el día a día de la peluquería'),
            ('en el tocador de un salón', 'en el tocador de una peluquería'),
            ('Godolphy es tu software de reservas y gestión con IA', 'Godolphy es el software de reservas y gestión con IA para tu peluquería'),
        ],
        'salons_h2': '<h2 class="h2">Hecho para <span class="grad">peluquerías</span>: tu agenda, tu equipo y tus números</h2>',
        'fotos': [
            # (foto del master, foto del sector, pie del master, pie del sector, alt del master, alt del sector)
            ('salon-estetica.webp', 'salon-pelu-recepcion.webp', 'Centros de estética', 'Recepción y cobros',
             'Cabinas de un centro de estética', 'Recepción de una peluquería cobrando a una clienta'),
            ('salon-peluqueria.webp', 'salon-peluqueria.webp', 'Peluquerías', 'Tu peluquería',
             'Peluquería con el equipo trabajando', 'Peluquería con el equipo trabajando'),
            ('salon-detalle.webp', 'salon-pelu-equipo.webp', 'Tu plan, también en el móvil', 'Tu agenda y tu equipo',
             'Plan de Godolphy en el móvil, en el tocador de una peluquería', 'Equipo de una peluquería mirando la agenda de Godolphy'),
        ],
    },
}


def adapt(html_text, master_slug, slug, cfg):
    h = html_text
    for a, b in cfg['textos']:
        h = h.replace(a, b)
    assert SALONS_MASTER in h, 'cambió el titular de la franja de fotos del master'
    h = h.replace(SALONS_MASTER, cfg['salons_h2'])
    for f_m, f_s, cap_m, cap_s, alt_m, alt_s in cfg['fotos']:
        h = h.replace(f'/lp/plan-financiero-2027/{f_m}" alt="{alt_m}"', f'/lp/plan-financiero-2027/{f_s}" alt="{alt_s}"')
        h = h.replace(f'<figcaption>{cap_m}</figcaption>', f'<figcaption>{cap_s}</figcaption>')
    # Etiqueta superior (solo la B la tiene)
    h = h.replace('<p class="tag"><i>●</i> Mueve el culo · Plan 2027</p>', f'<p class="tag"><i>●</i> {cfg["tag"]}</p>')
    # Slug: solo canonical y data-lp (las imágenes siguen en la carpeta del master)
    h = h.replace(f'href="https://www.godolphy.com/lp/{master_slug}/"', f'href="https://www.godolphy.com/lp/{slug}/"')
    h = h.replace(f'data-lp="{master_slug}"', f'data-lp="{slug}"')
    return h


def build(sector):
    cfg = SECTORES[sector]
    for mod, master_slug in ((A, 'plan-financiero-2027'), (B, 'plan-financiero-2027-b')):
        slug = f'{master_slug}-{sector}'
        out = f'lp/{slug}/index.html'
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(adapt(mod.page(), master_slug, slug, cfg))
        print('ok', out)


if __name__ == '__main__':
    for s in (sys.argv[1:] or SECTORES):
        build(s)
