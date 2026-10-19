#!/usr/bin/env python3
"""Reestructura las páginas de sector con los bloques de la home.

- "Descubre dónde estás perdiendo dinero" → sección oscura del copiloto IA.
- Recordatorios, horarios, tarjetas regalo, múltiples centros (y en limpieza,
  geolocalización y tipos de cliente) → un único bento con interfaces dibujadas.
- "Y si realizas … a domicilio" → tres pasos en tarjetas.
El resto (reservas, depósito, empleados, extras, FAQ, CTA) se mantiene.
Idempotente: si la página ya tiene .gx-bento-sec no se toca.
"""
import re, sys

PAGES = [
    'sectores/software-para-barberias/index.html',
    'sectores/software-para-centro-de-estetica-y-salones/index.html',
    'sectores/software-para-empresas-de-limpieza/index.html',
    'sectores/software-para-peluquerias/index.html',
    'sectores/software-para-salones-de-unas/index.html',
    'sectores/software-para-spa-y-masajes/index.html',
]

def txt(h):
    return re.sub(r'\s+', ' ', re.sub(r'<br\s*/?>', ' ', h)).strip()

def h2_of(sec):
    m = re.search(r'<h2[^>]*>(.*?)</h2>', sec, re.S)
    return txt(m.group(1)) if m else ''

def p_of(sec):
    m = re.search(r'</h2>\s*<p[^>]*>(.*?)</p>', sec, re.S)
    return m.group(1).strip() if m else ''

def lis(sec):
    return [txt(re.sub(r'<svg.*?</svg>', '', x, flags=re.S)) for x in re.findall(r'<li[^>]*>(.*?)</li>', sec, re.S)]

def grad_last(title, n=2):
    w = title.rstrip('.').split(' ')
    if len(w) <= n:
        return f'<span class="gx-grad">{title}</span>'
    return ' '.join(w[:-n]) + ' <span class="gx-grad">' + ' '.join(w[-n:]) + '</span>'

MAP_SVG = ('<svg viewBox="0 0 600 230" preserveAspectRatio="xMidYMid slice"><g stroke="#dfe2f5" stroke-width="14" fill="none" stroke-linecap="round">'
           '<path d="M-20 60 H620"/><path d="M-20 170 H620"/><path d="M120 -20 V250"/><path d="M330 -20 V250"/><path d="M500 -20 V250"/><path d="M-20 240 L260 -20"/></g>'
           '<path class="gx-route" d="M120 170 H330 V60 H470" stroke="#631cff" stroke-width="4" fill="none" stroke-linecap="round"/>'
           '<circle cx="120" cy="170" r="11" fill="#631cff"/><circle cx="120" cy="170" r="4" fill="#fff"/>'
           '<circle cx="470" cy="60" r="11" fill="#02021e"/><circle cx="470" cy="60" r="4" fill="#fff"/></svg>')

def mock(kind, title):
    if kind == 'recordatorios':
        return ('<div class="gx-wa" aria-hidden="true"><div class="gx-wa__msg">Hola Marta 👋 Te recordamos tu cita de <b>mañana a las 16:00</b>. ¿Nos confirmas?<small>10:02</small></div>'
                '<div class="gx-wa__btns"><span>Confirmar</span><span>Cambiar cita</span></div>'
                '<div class="gx-wa__msg gx-wa__me">¡Confirmado! Hasta mañana<small>10:05 ✓✓</small></div></div>')
    if kind == 'horarios':
        def row(n, cells):
            return f'<em>{n}</em>' + ''.join(f'<span class="{c}"></span>' for c in cells)
        return ('<div class="gx-ui" aria-hidden="true"><div class="gx-week"><i></i><b>L</b><b>M</b><b>X</b><b>J</b><b>V</b><b>S</b><b>D</b>'
                + row('Ana', ['on', 'on', 'on', 'on', 'on', '', 'off'])
                + row('Leo', ['', 'on', 'on', 'on', 'on', 'on', 'off'])
                + row('Marta', ['off', 'off', 'off', 'on', 'on', 'on', 'off'])
                + '</div><div class="gx-ui__row" style="margin-top:10px;background:var(--gx-soft);"><span>Marta · vacaciones</span><b>L–X bloqueados</b></div></div>')
    if kind == 'tarjetas':
        return ('<div class="gx-gift" aria-hidden="true"><span style="font-size:12px;letter-spacing:.14em;text-transform:uppercase;opacity:.8;">Tarjeta regalo</span>'
                '<b>50 €</b><div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;"><span style="opacity:.85;font-size:13px;">Para: Laura · envío el 24/12</span><code>REGALO-8F3K</code></div></div>')
    if kind == 'multiples':
        return ('<div class="gx-map" aria-hidden="true">' + MAP_SVG +
                '<div class="gx-map__badge" style="left:16px;top:16px;"><span class="gx-ui__muted">Centro</span><b>Sede Gràcia</b></div>'
                '<div class="gx-map__badge" style="right:16px;bottom:16px;"><span class="gx-ui__muted">Domicilio</span><b>6,2 km · +3,10 €</b></div></div>')
    if kind == 'geo':
        return ('<div class="gx-map" aria-hidden="true">' + MAP_SVG +
                '<div class="gx-map__badge" style="left:16px;top:16px;"><span class="gx-ui__muted">Equipo 2</span><b>En ruta</b></div>'
                '<div class="gx-map__badge" style="right:16px;bottom:16px;"><span class="gx-ui__muted">Siguiente servicio</span><b>Oficina · 10:30</b></div></div>')
    if kind == 'tipos':
        return ('<div class="gx-ui" aria-hidden="true"><div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:4px;">'
                '<span class="gx-chip gx-chip--on">✓ Hogar</span><span class="gx-chip">Oficina</span><span class="gx-chip">Empresa</span><span class="gx-chip">Comunidad</span></div>'
                '<div class="gx-total"><span>Limpieza semanal · 3 h</span><span>Cada martes</span></div></div>')
    return ''

def kind_of(h):
    l = h.lower()
    if 'recordatorio' in l: return 'recordatorios'
    if 'horarios' in l: return 'horarios'
    if 'tarjetas regalo' in l: return 'tarjetas'
    if l.startswith('múltiples'): return 'multiples'
    if 'dónde está tu equipo' in l: return 'geo'
    if 'hogares, oficinas' in l: return 'tipos'
    return None

LINKS = {
    'recordatorios': '/funcionalidades/chat-y-notificaciones/',
    'horarios': '/funcionalidades/equipo-y-horarios/',
    'tarjetas': '/funcionalidades/cupones-y-tarjetas-regalo/',
    'multiples': '/funcionalidades/multiples-ubicaciones/',
    'geo': '/funcionalidades/geolocalizacion-equipo/',
}

def card(kind, sec, size):
    h, p, li = h2_of(sec), p_of(sec), lis(sec)
    v = ' gx-card--v' if kind == 'tarjetas' else ''
    out = f'<article class="gx-card gx-c{size}{v}">' + mock(kind, h) + f'<h3>{h}</h3>'
    if p: out += f'<p>{p}</p>'
    if li: out += '<ul>' + ''.join(f'<li>{x}</li>' for x in li) + '</ul>'
    if kind in LINKS and not v:
        out += f'<a class="gx-link" href="{LINKS[kind]}" style="margin-top:16px;">Ver cómo funciona</a>'
    return out + '</article>'

def ai_section(sec):
    h, p, li = h2_of(sec), p_of(sec), lis(sec)
    img = re.search(r'<img[^>]*>', sec).group(0)
    img = re.sub(r'\sstyle="[^"]*"', '', img).replace(' / loading', ' loading')
    return ('<section class="gx-ai"><div class="gx-wrap gx-ai__grid"><div>'
            '<span class="gx-eyebrow">Copiloto IA</span>'
            f'<h2 class="gx-h2">{h}</h2><p class="gx-lead">{p}</p>'
            '<ul class="gx-ai__list">' + ''.join(f'<li>{x}</li>' for x in li) + '</ul>'
            '<a class="gx-btn gx-btn--light" href="/dashboard-ia/">Conoce el dashboard IA</a>'
            f'</div><div>{img}</div></div></section>\n')

def steps_section(sec):
    h = h2_of(sec)
    m = re.search(r'</h2>\s*<p[^>]*>(.*?)</p>', sec, re.S)
    p = m.group(1).strip() if m else ''
    steps = re.findall(r'<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>', sec, re.S)
    out = ('<section class="gx-steps-sec"><div class="gx-wrap" style="text-align:center;">'
           '<span class="gx-eyebrow">Paso a paso</span>'
           f'<h2 class="gx-h2">{grad_last(h)}</h2>')
    if p: out += f'<p class="gx-lead" style="margin:0 auto;">{p}</p>'
    out += '<div class="gx-steps3">'
    for i, (t, d) in enumerate(steps, 1):
        out += f'<div class="gx-step"><div class="gx-step__n gx-grad">0{i}</div><h3>{txt(t)}</h3><p>{d.strip()}</p></div>'
    return out + '</div></div></section>\n'

SIZES = [7, 5, 5, 7, 6, 6]

def restructure(path):
    s = open(path, encoding='utf-8').read()
    if 'gx-bento-sec' in s:
        return False
    head, *secs = re.split(r'(?=<section[\s>])', s)
    new, bento, bento_at = [], [], None
    for sec in secs:
        # separar lo que va después del cierre de la sección (comentarios, etc.)
        h = h2_of(sec)
        k = kind_of(h)
        if 'perdiendo dinero' in h:
            body, _, tail = sec.partition('</section>')
            new.append(ai_section(body) + tail.lstrip('\n'))
        elif k:
            body, _, tail = sec.partition('</section>')
            if bento_at is None:
                bento_at = len(new); new.append(None)
            bento.append((k, body))
            if tail.strip(): new.append(tail)
        elif h.lower().startswith('y si ') and '<h3' in sec:
            body, _, tail = sec.partition('</section>')
            new.append(steps_section(body) + tail.lstrip('\n'))
        else:
            new.append(sec)
    if bento_at is None:
        return False
    cards = ''.join(card(k, b, SIZES[i] if i < len(SIZES) else 6) for i, (k, b) in enumerate(bento))
    if len(bento) % 2 == 1:  # la última ocupa todo el ancho
        cards = re.sub(r'gx-c\d+((?: gx-card--v)?)"([^>]*)>(?!.*<article)', r'gx-c12\1"\2>', cards, flags=re.S)
    new[bento_at] = ('<section class="gx-bento-sec"><div class="gx-wrap"><div style="text-align:center;">'
                     '<span class="gx-eyebrow">Todo en un sitio</span>'
                     '<h2 class="gx-h2">Y todo lo que necesitas para el día a día, <span class="gx-grad">en el mismo sitio.</span></h2>'
                     '</div><div class="gx-bento">' + cards + '</div></div></section>\n\n')
    open(path, 'w', encoding='utf-8').write(head + ''.join(new))
    return True

if __name__ == '__main__':
    for p in sys.argv[1:] or PAGES:
        print(p, 'reestructurada' if restructure(p) else 'sin cambios')
