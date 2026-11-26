"""Páginas de sector nuevas (nov. 2026): lashistas y maquilladoras.

Parten de la página de centros de estética ya renovada (sector_refresh.py + sector_blocks.py),
cambian los términos del sector y reescriben las partes propias: cabecera, notificaciones, FAQ (+ JSON-LD),
calculadora, gestor diario, texto SEO y metadatos.
Uso: python3 scripts/build_sector_new.py
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sector_blocks import calculadora  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / 'sectores/software-para-centro-de-estetica-y-salones/index.html'
BASE_URL = 'https://www.godolphy.com/sectores/software-para-centro-de-estetica-y-salones/'


def it(t, y=False):
    return f'<span class="it{" it--y" if y else ""}">{t}</span>'


COMMON_FAQ_KEEP = ['¿Funciona con Instagram y Google?', '¿Puedo pasar mis datos desde Booksy, Fresha o Treatwell?',
                   '¿Qué pasa con las citas si alguien del equipo se pone de baja?', '¿Hay periodo de prueba gratuito?',
                   '¿Godolphy cumple con Verifactu?']

SECTORS = {
    'lashistas': dict(
        slug='software-para-lashistas', tipo='Lashista', badge='LASHISTAS',
        title='Software para lashistas: reservas, rellenos y agenda | Godolphy',
        desc='Software para lashistas con reservas online, bonos de rellenos, tiempos de exposición para el lifting, señal al reservar y recordatorios por WhatsApp. Prueba gratis 30 días.',
        h1=f'Software para lashistas: {it("reservas, rellenos y clientes que vuelven", True)}',
        sub='Reservas online, bonos de rellenos, tiempos de exposición para el lifting, cobros y recordatorios. Todo desde una sola plataforma.',
        hero='https://images.unsplash.com/photo-1735151226446-1d364b4adc2f?w=2000&q=75&auto=format&fit=crop', pos='70% center',
        notifs=[('Nueva reserva', 'Lucía · Relleno pelo a pelo · jue. 17:00', 'ahora'),
                ('Bono vendido', '5 rellenos · 150 €', '3 min'),
                ('Recordatorio enviado', 'WhatsApp a Elena · mañana 12:00 ✓', '8 min')],
        terms=[('CENTROS DE ESTÉTICA', 'LASHISTAS'), ('centros de estética', 'estudios de pestañas'),
               ('centro de estética', 'estudio de pestañas'), ('Múltiples centros', 'Varios estudios'),
               ('Varios centros', 'Varios estudios'), ('varios centros', 'varios estudios'),
               ('todos tus centros', 'todos tus estudios'), ('tu centro', 'tu estudio'), ('en centro', 'en el estudio'),
               ('múltiples centros', 'varios estudios'), ('esteticistas', 'lashistas'), ('esteticista', 'lashista'),
               ('Tratamientos', 'Servicios'), ('tratamientos', 'servicios'), ('tratamiento', 'servicio'),
               ('cabinas vacías', 'huecos vacíos'), ('para estética', 'para lashistas')],
        gestor=['2 citas de ayer sin cobrar', 'Mañana tienes un hueco de 10 a 12', '18 clientes llevan 5 semanas sin relleno'],
        margins=[('Lifting de pestañas', 52), ('Retirada de extensiones', 8)],
        corto='una retirada',
        servicios=[('Retirada de extensiones', '15 min', 10, 9.20), ('Relleno pelo a pelo', '60 min', 35, 22),
                   ('Lifting + tinte de pestañas', '60 min', 45, 18)],
        faq=[('¿Puedo hacer servicios en el estudio y a domicilio?',
              'Sí. Configuras qué servicios haces en el estudio y cuáles a domicilio, con precios distintos. El cliente elige dónde los quiere al reservar.'),
             ('¿Puedo vender los rellenos en bonos?',
              'Sí. Vendes bonos de 5 o 10 sesiones y cada relleno se descuenta solo del bono del cliente.'),
             ('¿Qué pasa con la agenda mientras actúa el lifting?',
              'Con los tiempos de exposición divides el servicio en tramos: trabajo, exposición y trabajo. Mientras actúa el lifting o el tinte, la agenda te deja dar otra cita. Funciona en las citas del estudio, no en las de domicilio.'),
             ('¿Los clientes pueden elegir a su lashista?',
              'Sí. Pueden elegir a su lashista o dejar que el sistema asigne la primera disponible.')],
        seo_h2='El software para lashistas que ordena tu agenda en 2027',
        seo=['Llevar un estudio de pestañas es encadenar extensiones, rellenos cada pocas semanas, lifting y clientes que reservan por Instagram. El <strong>software para lashistas</strong> Godolphy lo junta todo en un solo panel.',
             'Con la <strong>agenda para lashistas</strong> de Godolphy, tus clientes reservan online 24/7 desde el móvil, reciben recordatorios automáticos por WhatsApp y pueden dejar una señal al reservar para que no falten.',
             'Con los tiempos de exposición, mientras actúa el lifting o el tinte de pestañas puedes atender a otro cliente y la agenda lo tiene en cuenta sola. Y la IA te dice qué servicios te dejan margen y qué clientes llevan tiempo sin venir.',
             'Las <strong>reservas online para lashistas</strong> se integran con tu bio de Instagram y tu ficha de Google, para captar nuevos clientes desde donde ya te buscan.'],
    ),
    'maquilladoras': dict(
        slug='software-para-maquilladoras', tipo='Maquilladora', badge='MAQUILLADORAS',
        title='Software para maquilladoras: reservas a domicilio y agenda | Godolphy',
        desc='Software para maquilladoras profesionales: reservas a domicilio con el desplazamiento calculado, señal para asegurar la fecha, extras y recordatorios por WhatsApp. Prueba gratis 30 días.',
        h1=f'Software para maquilladoras: {it("reservas a domicilio", True)} con el desplazamiento calculado',
        sub='Tus clientes reservan desde el móvil, ponen su dirección y ven el precio con el desplazamiento incluido. Con señal para asegurar la fecha y recordatorios automáticos.',
        hero='https://images.unsplash.com/photo-1613966802194-d46a163af70d?w=2000&q=75&auto=format&fit=crop', pos='70% center',
        notifs=[('Nueva reserva a domicilio', 'Novia · Maquillaje + prueba · sáb. 9:00', 'ahora'),
                ('Señal cobrada', '60,00 € · boda de Clara', '4 min'),
                ('Desplazamiento calculado', '12,4 km · +8,50 €', '9 min')],
        terms=[('CENTROS DE ESTÉTICA', 'MAQUILLADORAS'), ('Múltiples centros de estética y servicios a domicilio.', 'A domicilio y en tu estudio.'),
               ('centros de estética', 'maquilladoras'), ('tu centro de estética', 'tu negocio'),
               ('centro de estética', 'negocio de maquillaje'), ('Varios centros', 'Varios estudios'),
               ('varios centros', 'varios estudios'), ('todos tus centros', 'todos tus estudios'), ('tu centro', 'tu negocio'),
               ('en centro', 'en el estudio'), ('múltiples centros', 'varios estudios'), ('esteticistas', 'maquilladoras'),
               ('esteticista', 'maquilladora'), ('Tratamientos', 'Servicios'), ('tratamientos', 'servicios'),
               ('tratamiento', 'servicio'), ('cabinas vacías', 'huecos vacíos'), ('para estética', 'para maquilladoras')],
        gestor=['1 cita de ayer sin cobrar', 'Mañana tienes un hueco de 16 a 19', 'Los retoques te hacen perder dinero: revisa el precio'],
        margins=[('Maquillaje de novia', 48), ('Retoque de maquillaje', 6)],
        corto='un retoque',
        servicios=[('Retoque de maquillaje', '20 min', 15, 13.40), ('Maquillaje de invitada', '45 min', 45, 32),
                   ('Maquillaje de novia con prueba', '2 h 30 min', 220, 95)],
        extras_li='<strong>Ejemplo</strong>: maquillaje de novia + prueba + pestañas postizas en una sola reserva, con el tiempo y el precio sumados.',
        move_domicilio=True,
        post=[('Paso a paso</span>', 'Paso a paso</span>'), ('Servicios a domicilio: ', 'Maquillaje a domicilio: '),
              ('Gestiona varios estudios desde una sola cuenta. Y si también haces servicios a domicilio, Godolphy calcula el precio del desplazamiento automáticamente.',
               'Godolphy calcula solo el precio del desplazamiento de cada domicilio. Y si también tienes estudio, lo llevas desde la misma cuenta.'),
              ('Un recargo el viernes por la tarde o un descuento para llenar las mañanas de entre semana.',
               'Un recargo los sábados de bodas o un descuento para llenar las mañanas de entre semana.')],
        faq=[('¿Puedo hacer maquillajes a domicilio?',
              'Sí. El cliente pone su dirección al reservar y Godolphy calcula el desplazamiento según la distancia y lo suma al precio.'),
             ('¿Cómo aseguro la fecha de una boda?',
              'Pides una señal al reservar. Si la cita es dentro de más de 6 días, la señal se cobra en ese momento; si el cliente cancela a tiempo, se le devuelve según tu política de cancelación.'),
             ('¿Puedo añadir la prueba o las pestañas postizas como extra?',
              'Sí. Los extras se eligen al reservar y la agenda suma su tiempo y su precio a la cita.'),
             ('¿Trabajo con más maquilladoras: cada una ve su agenda?',
              'Sí. Cada maquilladora tiene su propio acceso y ve sus citas del día, con la dirección si es a domicilio.')],
        seo_h2='El software para maquilladoras que trabaja contigo a domicilio en 2027',
        seo=['Una maquilladora pasa el día entre casas, hoteles y bodas. El <strong>software para maquilladoras</strong> Godolphy junta tu agenda, tus reservas a domicilio y tus cobros en un solo panel.',
             'Con la <strong>agenda para maquilladoras</strong> de Godolphy, tus clientes reservan online desde el móvil, ponen su dirección y ven el precio con el desplazamiento incluido. Y una señal al reservar asegura la fecha.',
             'Los extras, como la prueba de maquillaje o las pestañas postizas, se añaden en la misma reserva y la agenda suma su tiempo y su precio.',
             'La IA te dice qué servicios te dejan margen y qué clientes llevan tiempo sin volver, y los recordatorios por WhatsApp evitan olvidos.'],
    ),
}


def sub1(s, old, new, count=1):
    assert old in s, f'no encontrado: {old[:80]}'
    return s.replace(old, new, count)


def faq_items(s):
    return re.findall(r'<div class="faq-item">.*?</p></div></div>', s, re.S)


def build(key):
    c = SECTORS[key]
    s = BASE.read_text()
    head_end = s.find('<body')
    head, body = s[:head_end], s[head_end:]

    # --- cabecera (antes del cambio de términos) ---
    body = re.sub(r'(<h1 class="font-gabarito"[^>]*>).*?(</h1>)', lambda m: m.group(1) + c['h1'] + m.group(2), body, 1, re.S)
    body = sub1(body, 'Reservas online, gestión de esteticistas, cobros y recordatorios. Todo desde una sola plataforma.', c['sub'])
    body = sub1(body, "--hero:url('/images/sectores/hero/estetica-cabina.webp');--hero-pos:80% center;", f"--hero:url('{c['hero']}');--hero-pos:{c['pos']};")
    cards = ''.join(f'<div class="hn"><img src="/favicon-32.png" alt="" width="32" height="32"><div><b>{t}</b><span>{x}</span></div><small>{w}</small></div>'
                    for t, x, w in c['notifs'])
    body = re.sub(r'<div class="hero-notifs" aria-hidden="true">(?:<div class="hn">.*?</small></div>)+</div>', '<div class="hero-notifs" aria-hidden="true">' + cards + '</div>', body, 1, re.S)
    assert c['notifs'][0][1] in body
    body = body.replace('data-sector="Centro de estética"', f'data-sector="{c["tipo"]}"')

    # --- gestor diario y márgenes ---
    for old, new in zip(['4 sesiones de bono caducan esta semana', 'Mañana tienes la cabina 2 libre de 10 a 13', '15 clientes llevan 3 meses sin venir'], c['gestor']):
        body = sub1(body, old, new)
    (a, ma), (b, mb) = c['margins']
    body = sub1(body, '<span>Higiene facial</span><b>margen 44 %</b></div><div class="gd-meter"><i data-w="44">',
                f'<span>{a}</span><b>margen {ma} %</b></div><div class="gd-meter"><i data-w="{ma}">')
    body = sub1(body, '<span>Radiofrecuencia</span><b style="color:#d63b3b;">margen 11 %</b></div><div class="gd-meter"><i class="bad" data-w="11">',
                f'<span>{b}</span><b style="color:#d63b3b;">margen {mb} %</b></div><div class="gd-meter"><i class="bad" data-w="{mb}">')

    # --- calculadora con ejemplos del sector ---
    i = body.find('<!-- gd-blocks:calculadora')
    e = body.find('</section>', i) + len('</section>')
    body = body[:i] + calculadora(c).strip() + body[e:]

    # --- extras (maquilladoras: sin tiempos de exposición) ---
    if c.get('extras_li'):
        body = re.sub(r'<strong>Tiempos de exposición</strong>: mientras actúa.*?Ver cómo funciona</a>', c['extras_li'], body, 1, re.S)
        body = body.replace('Extras y tiempos de exposición: ', 'Extras al reservar: ')

    # --- FAQ (visible + JSON-LD) ---
    items = faq_items(body)
    tpl = items[0]
    keep = {}
    for it_ in items:
        q = re.search(r'<span[^>]*>(.*?)</span>', it_).group(1)
        keep[q] = it_
    new_items = []
    for q, a in c['faq']:
        x = re.sub(r'(<span[^>]*>).*?(</span>)', lambda m: m.group(1) + q + m.group(2), tpl, 1)
        x = re.sub(r'(<div class="faq-body"><p[^>]*>).*?(</p>)', lambda m: m.group(1) + a + m.group(2), x, 1, re.S)
        new_items.append(x)
    new_items += [keep[q] for q in COMMON_FAQ_KEEP]
    fs, fe = body.find(items[0]), body.find(items[-1]) + len(items[-1])
    body = body[:fs] + '\n'.join(new_items) + body[fe:]

    # --- texto SEO final ---
    i = body.find('El software para centros de estética que digitaliza tu negocio en 2027')
    h2s = body.rfind('<h2', 0, i)
    sec_end = body.find('</div>', i)
    ps = ''.join(f'<p style="color:rgba(2,2,30,.7);font-size:16px;line-height:1.75;margin:0 0 20px;">{p}</p>' for p in c['seo'])
    ps += '<p style="color:rgba(2,2,30,.7);font-size:16px;line-height:1.75;margin:0;">Planes desde 33€/mes sin comisión por cliente nuevo. Prueba gratis 30 días y comprueba cuánto tiempo puedes recuperar cada semana.</p>'
    body = body[:h2s] + f'<h2 style="font-family:\'Gabarito\',sans-serif;font-size:32px;font-weight:700;color:#02021e;margin:0 0 28px;line-height:1.2;">{c["seo_h2"]}</h2>\n    {ps}\n  ' + body[sec_end:]

    # --- maquilladoras: el domicilio sube justo después de las reservas online ---
    if c.get('move_domicilio'):
        ds = body.find('<section class="gx-steps-sec">')
        de = body.find('</section>', ds) + len('</section>')
        dom = body[ds:de]
        body = body[:ds] + body[de:]
        r = body.find('Reservas online 24 h')
        re_end = body.find('</section>', r) + len('</section>')
        body = body[:re_end] + '\n\n' + dom + body[re_end:]

    # --- términos del sector (texto visible) ---
    body = body.replace('La cliente', 'El cliente').replace('la cliente', 'el cliente').replace('Ellas ven su agenda', 'Cada una ve su agenda')
    for old, new in c['terms']:
        body = body.replace(old, new)
    body = body.replace('los precios según centro o domicilio', 'los precios en el estudio o a domicilio')
    for old, new in c.get('post', []):
        body = sub1(body, old, new) if old != new else body

    # --- head ---
    url = f'https://www.godolphy.com/sectores/{c["slug"]}/'
    head = re.sub(r'<title>.*?</title>', f'<title>{c["title"]}</title>', head, 1, re.S)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + c['desc'], head, 1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + c['title'], head, 1)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + c['desc'], head)
    head = re.sub(r'(<meta name="twitter:title" content=")[^"]*', lambda m: m.group(1) + c['title'], head)
    head = re.sub(r'(<meta name="twitter:description" content=")[^"]*', lambda m: m.group(1) + c['desc'], head)
    head = head.replace(BASE_URL, url)
    head = re.sub(r'("@type": "SoftwareApplication".*?"description": ")[^"]*', lambda m: m.group(1) + c['desc'], head, 1, re.S)
    # FAQ JSON-LD desde la FAQ visible
    qa = []
    for it_ in faq_items(body):
        q = html.unescape(re.sub(r'<[^>]+>', '', re.search(r'<span[^>]*>(.*?)</span>', it_).group(1)))
        a = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', re.search(r'<div class="faq-body"><p[^>]*>(.*?)</p>', it_, re.S).group(1)))).strip()
        qa.append((q, a))
    import json
    faq_ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in qa]}, ensure_ascii=False, indent=2)
    head = re.sub(r'(<script type="application/ld\+json">)\s*\{\s*"@context": "https://schema.org",\s*"@type": "FAQPage".*?(</script>)',
                  lambda m: m.group(1) + '\n' + faq_ld + '\n' + m.group(2), head, 1, re.S)
    out = head + body
    left = [w for w in ('estética', 'esteticista', 'cabina', 'Higiene facial', 'presoterapia', 'Radiofrecuencia') if w.lower() in out.lower()]
    p = ROOT / 'sectores' / c['slug'] / 'index.html'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(out)
    print('ok', key, '· quedan:', left)


if __name__ == '__main__':
    for k in (sys.argv[1:] or SECTORS):
        build(k)
