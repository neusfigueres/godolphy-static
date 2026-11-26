#!/usr/bin/env python3
"""Actualiza las páginas de sector (nov. 2026) para las campañas de Google Ads.

- Títulos que explican lo que hay debajo, con acentos en cursiva serif (.it), subrayado (.mk)
  y círculo a mano alzada (.ci) — estilos y animaciones en /assets/gx-motion.css y .js.
- Bloque nuevo «Más que una agenda» con las funciones que faltaban (precio por día y hora,
  gestor diario, calculadora de precios, clientes que no vuelven), con gráficos animados.
- Bajas y ausencias en la tarjeta de horarios; recepcionista en el bloque de equipo.
- Rejilla de funcionalidades ampliada y FAQ con migración.
- CTA principal: «Prueba Godolphy gratis 30 días». CTA secundario solo en el bloque del
  plan financiero, hacia la landing del plan del sector.

Cada sector tiene su configuración en SECTORS. El script parte del HTML actual y falla
(assert) si algún texto esperado ya no está, para no pisar cambios de otros.
Uso: python3 scripts/sector_refresh.py peluquerias
"""
import re
import sys

CI_SVG = ('<svg viewBox="0 0 300 100" preserveAspectRatio="none" aria-hidden="true">'
          '<path d="M52 16C128 2 262 4 291 38c22 34-78 60-170 58C46 94 4 76 10 48 16 22 78 10 168 8"/></svg>')


def it(t, y=False):
    return f'<span class="it{" it--y" if y else ""}">{t}</span>'


def mk(t):
    return f'<span class="mk">{t}</span>'


def ci(t, v=False):
    return f'<span class="ci{" ci--v" if v else ""}">{t}{CI_SVG}</span>'


HEAD_ADD = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@1&display=swap" rel="stylesheet">'
            '<link rel="stylesheet" href="/assets/gx-motion.css?v=12">'
            '<script src="/assets/gx-motion.js?v=12" defer></script>')

FEAT_ICON = ('<div style="width:36px;height:36px;background:#f0ebff;border-radius:10px;display:flex;align-items:center;'
             'justify-content:center;margin-bottom:12px;"><svg width="18" height="18" fill="none" stroke="#631cff" '
             'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">{p}</svg></div>')
P = {
    'tag': '<path d="M20 12l-8 8-9-9V3h8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    'cal': '<rect x="3.5" y="5" width="17" height="15" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    'user': '<circle cx="12" cy="8" r="3.5"/><path d="M5 20a7 7 0 0 1 14 0"/>',
    'up': '<path d="M12 19V5M6 11l6-6 6 6"/>',
    'chart': '<path d="M5 19V11M10 19V6M15 19v-5M20 19V9"/><path d="M3 19h18"/>',
    'calc': '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 12h2M14 12h2M8 16h2M14 16h2"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2"/>',
    'ticket': '<path d="M4 7h16v3a2 2 0 0 0 0 4v3H4v-3a2 2 0 0 0 0-4z"/><path d="M12 7v10" stroke-dasharray="2 2"/>',
}


def feat_card(icon, title, text, href):
    return (f'      <div class="feat-card">{FEAT_ICON.format(p=P[icon])}<h4 style="color:#02021e;font-size:15px;font-weight:600;margin:0 0 8px;">'
            f'<a href="{href}" style="color:inherit;text-decoration:none;">{title}</a></h4>'
            f'<p style="color:rgba(2,2,30,.55);font-size:13px;line-height:1.55;margin:0;">{text}</p></div>\n')


def faq_item(q, a):
    return ('    <div class="faq-item"><button class="faq-btn" onclick="toggleFaq(this)"><span style="color:#02021e;font-size:17px;font-weight:600;">'
            f'{q}</span><svg class="faq-icon" width="20" height="20" fill="none" stroke="#631cff" stroke-width="2.5" viewBox="0 0 24 24">'
            '<path d="M12 5v14M5 12h14"/></svg></button><div class="faq-body"><p style="color:rgba(2,2,30,.65);font-size:16px;line-height:1.65;margin:0;">'
            f'{a}</p></div></div>\n')


def more_than_agenda(c):
    """Bloque nuevo con las funciones diferenciales y gráficos animados (datos de ejemplo)."""
    days = ''.join(f'<i>{d}</i>' for d in 'LMXJVSD')
    bars = ''.join(
        f'<span data-h="{h}"' + (f' class="{k}"' if k else '') + '>' + (f'<b>{lab}</b>' if lab else '') + '</span>'
        for h, k, lab in [(55, '', ''), (30, 'low', '−15 %'), (58, '', ''), (66, '', ''), (88, 'hot', ''), (100, 'hot', '+10 %'), (0, '', '')])
    tasks = ''.join(f'<li><b>{i}</b><span>{t}</span></li>' for i, t in enumerate(c['gestor'], 1))
    return f'''
<!-- Más que una agenda (sector_refresh.py) -->
<section class="gd-sec">
  <div class="gd-wrap">
    <div class="gd-head">
      <h2>Más que una agenda: Godolphy {it('te dice qué hacer')} para ganar más</h2>
      <p>{c['mas_lead']}</p>
    </div>
    <div class="gd-grid">
      <article class="gd-card">
        <div class="gd-ui" aria-hidden="true"><div class="gd-bars">{bars}</div><div class="gd-days">{days}</div></div>
        <h3>Precio según el día y la hora</h3>
        <p>{c['precio_txt']}</p>
        <a href="/funcionalidades/precio-por-dia-y-hora/">Ver cómo funciona →</a>
      </article>
      <article class="gd-card">
        <div class="gd-ui" aria-hidden="true"><p style="margin:0 0 10px;font-weight:700;">Hoy te recomendamos</p><ul class="gd-list">{tasks}</ul></div>
        <h3>Un gestor que cada mañana te dice qué hacer</h3>
        <p>Cada día Godolphy revisa tu {c['negocio']} y te propone hasta tres cosas: citas sin cobrar, huecos en la agenda, clientes que no vuelven, precios o gastos.</p>
        <a href="/funcionalidades/gestor-diario/">Ver cómo funciona →</a>
      </article>
      <article class="gd-card">
        <div class="gd-ui" aria-hidden="true">
          <div class="gd-row"><span>{c['calc'][0][0]}</span><b>margen {c['calc'][0][1]} %</b></div><div class="gd-meter"><i data-w="{c['calc'][0][1]}"></i></div>
          <div class="gd-row"><span>{c['calc'][1][0]}</span><b style="color:#d63b3b;">margen {c['calc'][1][1]} %</b></div><div class="gd-meter"><i class="bad" data-w="{c['calc'][1][1]}"></i></div>
        </div>
        <h3>Qué servicios te hacen perder dinero</h3>
        <p>La calculadora de precios usa tus horarios, tus citas y tus gastos para decirte cuánto te cuesta de verdad cada servicio y qué precio cobrar para ganar el margen que quieres.</p>
        <a href="/funcionalidades/calculadora-de-precios/">Ver cómo funciona →</a>
      </article>
      <article class="gd-card">
        <div class="gd-ui" aria-hidden="true" style="display:flex;flex-direction:column;justify-content:center;gap:6px;">
          <span class="gd-big" data-count="{c['riesgo']}">0</span><span>clientes llevan más de 90 días sin venir</span>
        </div>
        <h3>Los clientes que están a punto de no volver</h3>
        <p>La IA detecta a quién estás perdiendo antes de que sea tarde. Con los planes Pro y Max, recupéralos con una campaña por email o WhatsApp.</p>
        <a href="/funcionalidades/fidelizacion-ai/">Ver cómo funciona →</a>
      </article>
    </div>
    <p style="text-align:center;font-size:12.5px;color:rgba(2,2,30,.45);margin:18px 0 0;">Cifras de ejemplo.</p>
  </div>
</section>
'''


def hero_photo(s, c):
    """Cabecera: foto real del sector a todo el ancho + notificaciones de la app (HTML animado)."""
    a = '<section class="hero-bg" style="position:relative;'
    assert a in s
    s = s.replace(a, f'<section class="hero-bg hero-photo" style="--hero:url(\'{c["hero_img"]}\');--hero-pos:{c.get("hero_pos", "70% center")};position:relative;', 1)
    i = s.find('<section class="hero-bg hero-photo"')
    k = s.find('<div style="flex:1;display:flex;justify-content:flex-end;">', i)
    assert k > 0
    e = s.find('</div>', k) + len('</div>')
    cards = ''.join(f'<div class="hn"><img src="/favicon-32.png" alt="" width="32" height="32"><div><b>{t}</b><span>{x}</span></div><small>{w}</small></div>'
                    for t, x, w in c['notifs'])
    s = s[:k] + f'<div class="hero-notifs" aria-hidden="true">{cards}</div>' + s[e:]
    if c.get('hero_video'):  # vídeo de fondo (sin sonido, en bucle) con la foto como póster
        j = s.find('>', s.find('<section class="hero-bg hero-photo"')) + 1
        v = c['hero_video']
        s = s[:j] + (f'<video class="hero-vid" autoplay muted loop playsinline preload="auto" poster="{c["hero_img"]}" aria-hidden="true">'
                     f'<source src="{v}.webm" type="video/webm"><source src="{v}.mp4" type="video/mp4"></video>') + s[j:]
    return s


SECTORS = {
    'peluquerias': {
        'file': 'sectores/software-para-peluquerias/index.html',
        'negocio': 'peluquería',
        'lp_plan': '/lp/plan-financiero-2027-peluquerias/',
        # Foto real (Unsplash, licencia gratuita para uso comercial)
        'hero_img': 'https://images.unsplash.com/photo-1634449571010-02389ed0f9b0?w=2000&q=75&auto=format&fit=crop',
        'hero_pos': '65% center',
        'notifs': [('Nueva reserva', 'Laura · Mechas + corte · sáb. 11:00', 'ahora'),
                   ('Recordatorio enviado', 'WhatsApp a Marta · mañana 16:00 ✓', '2 min'),
                   ('Señal cobrada', '10,00 € · reserva de Ana', '5 min')],
        'mas_lead': 'Además de reservas y agenda, Godolphy analiza tu peluquería y te avisa de lo que hace que ganes más o pierdas dinero.',
        'precio_txt': 'Un recargo los sábados por la mañana o un descuento para llenar las horas flojas del martes. El cliente ve el precio final al reservar.',
        'gestor': ['3 citas de ayer sin cobrar', 'Mañana tienes 2 huecos: 11:00 y 12:30', '8 clientes llevan 3 meses sin venir'],
        'calc': [('Corte y peinado', 48), ('Mechas', 9)],
        'riesgo': 23,
        'h2': [
            # (texto actual exacto del interior del <h2>/<h1>/<h3>, texto nuevo)
            ('Software para peluquerías — Reservas, agenda y gestión con IA',
             f'Software para peluquerías: {it("reservas, negocio y crecimiento", True)}'),
            ('Una agenda con IA que incrementa tus beneficios',
             f'Reservas, agenda, equipo y análisis IA: {it("así se ve Godolphy")} en tu peluquería'),
            ('Descubre dónde estás perdiendo dinero y cómo recuperarlo.',
             f'Descubre dónde estás {ci("perdiendo dinero")} y cómo recuperarlo'),
            ('Los clientes reservan sin interrumpir tu tiempo.',
             f'Reservas online 24 h: tus clientes reservan {it("sin llamarte")}'),
            ('¡Qué no te dejen colgado/a! Solicita depósito.',
             f'Cobra una señal al reservar y {it("adiós a los plantones")}'),
            ('Y todo lo que necesitas para el día a día, <span class="gx-grad">en el mismo sitio.</span>',
             f'Recordatorios, horarios y bajas, tarjetas regalo y varios centros: {it("todo en la misma cuenta")}'),
            ('Gestión de horarios y vacaciones.', 'Horarios, vacaciones y bajas del equipo.'),
            ('Envía recordatorios vía whatsapp e email.', 'Recordatorios por WhatsApp y email.'),
            ('Y si realizas servicios de <span class="gx-grad">peluquería domicilio</span>',
             f'Peluquería a domicilio: {it("el desplazamiento se calcula y se cobra solo")}'),
            ('Tus empleados siempre tendrán trabajo.',
             f'Cada profesional ve {it("su agenda")}; la recepción lleva el día sin tocar la configuración'),
            ('Funcionalidades específicas para tu centro de peluqueria.',
             f'Todo lo que incluye Godolphy para {it("tu peluquería")}'),
            ('Preguntas frecuentes', f'Lo que te preguntas {it("antes de cambiar de programa")}'),
            ('Da de alta tu peluquería y empieza a optimizar tu tiempo',
             f'Prueba Godolphy 30 días gratis {it("con tu equipo y tus servicios reales", True)}'),
            ('El software de gestión para peluquerías que necesitas en 2026',
             'El software de gestión para peluquerías que necesitas en 2027'),
        ],
        'extras_h2': (re.compile(r'Calcula bien los tiempos\.\s*(?:<br\s*/?>)?\s*Extras obligatorios en el momento\s*(?:<br\s*/?>)?\s*de la reserva\.'),
                      f'Extras y tiempos de exposición: {it("la agenda calcula los tiempos")} por ti'),
        'baja_li': '<li>Si alguien se pone de baja, pasas sus citas a otra persona o envías un enlace para que cada cliente elija</li>',
        'equipo_faq_after': 'Sí. Cada profesional tiene su propio acceso y solo ve su agenda y sus clientes asignados.',
        'equipo_faq_new': ('¿Puede la recepcionista gestionar la agenda?',
                           'Sí. La recepcionista tiene su propio acceso: gestiona la agenda, las citas, los clientes, los cobros y la caja, sin tocar la configuración.'),
        'feats': [
            ('cal', 'Calendario', 'Arrastra citas, vista diaria o semanal y estados de llegada.', '/funcionalidades/calendario/'),
            ('sun', 'Precio por día y hora', 'Recargos y descuentos según la franja.', '/funcionalidades/precio-por-dia-y-hora/'),
            ('ticket', 'Bonos de sesiones', 'Vende bonos de 5 o 10 sesiones que se descuentan solos.', '/funcionalidades/bonos-de-sesiones/'),
            ('user', 'Recepcionista y permisos', 'Cada persona, su acceso.', '/funcionalidades/recepcionista-y-permisos/'),
            ('chart', 'Plan financiero', 'Tu objetivo de 2027, mes a mes.', '/funcionalidades/plan-financiero/'),
            ('calc', 'Calculadora de precios', 'Cuánto te cuesta cada servicio.', '/funcionalidades/calculadora-de-precios/'),
            ('up', 'Gestor diario', 'Tres recomendaciones cada mañana.', '/funcionalidades/gestor-diario/'),
            ('tag', 'Importar datos', 'Trae tus servicios y tu equipo desde Booksy, Fresha o Treatwell.', '/funcionalidades/importar-datos/'),
        ],
        'faq_new': [
            ('¿Puedo pasar mis datos desde Booksy, Fresha o Treatwell?',
             'Sí. Importas tus servicios y tu equipo desde un Excel, una captura o el enlace de tu ficha, y la IA lo lee por ti. Y si te pasas a Godolphy, te hago yo el cambio gratis. — Neus'),
            ('¿Qué pasa con las citas si alguien del equipo se pone de baja?',
             'Marcas la baja y Godolphy te enseña las citas afectadas: las pasas a otra persona del equipo o envías un enlace para que cada cliente elija nueva hora.'),
        ],
    },
}


def refresh(key):
    c = SECTORS[key]
    s = open(c['file'], encoding='utf-8').read()
    if 'gx-motion.css' in s:
        print('ya actualizada:', c['file'])
        return
    s = s.replace('</head>', HEAD_ADD + '\n</head>', 1)
    for old, new in c.get('fixes', []):
        assert old in s, ('arreglo no encontrado', old[:60])
        s = s.replace(old, new)
    for h in c.get('drop_sections', []):
        i = s.find('>' + h + '<'); assert i > 0, ('sección a quitar no encontrada', h)
        a0 = s.rfind('<section', 0, i); a1 = s.find('</section>', i) + len('</section>')
        s = s[:a0] + s[a1:]
    s = hero_photo(s, c)
    # Títulos
    for old, new in c['h2']:
        if old in c.get('drop_sections', []):
            continue
        n = s.count('>' + old + '<')
        assert n >= 1, ('título no encontrado', old)
        s = s.replace('>' + old + '<', '>' + new + '<')
    s, n = c['extras_h2'][0].subn(c['extras_h2'][1], s, count=1)
    assert n == 1, 'título de extras no encontrado'
    # Bajas en la tarjeta de horarios + enlace
    a = '<li>Días de descanso y vacaciones bloqueadas</li>'
    assert a in s
    s = s.replace(a, a + c['baja_li'], 1)
    s, n = re.subn(r'Configura el horario de cada ([^,<]+), sus días libres y vacaciones\. La agenda se actualiza sola\.',
                   r'Configura el horario de cada \1, sus días libres, vacaciones y bajas. Las citas afectadas se resuelven en un momento.', s, count=1)
    assert n == 1, 'texto de horarios no encontrado'
    # Recepcionista en el bloque de equipo (mini FAQ)
    m = re.search(r'Sí\. Cada [^<]+ tiene su propio acceso y solo ve su agenda y sus clientes asignados\.</p></div></div>', s)
    assert m, 'mini FAQ de equipo no encontrada'
    a = m.group(0)
    q, ans = c['equipo_faq_new']
    mini = ('\n        <div style="border-bottom:1px solid rgba(2,2,30,.1);padding:16px 0;"><button onclick="var b=this.nextElementSibling;b.classList.toggle(\'open\');'
            'this.querySelector(\'.mini-faq-icon\').classList.toggle(\'open\')" style="width:100%;background:none;border:none;text-align:left;cursor:pointer;display:flex;'
            'justify-content:space-between;align-items:center;padding:0;"><span style="color:#02021e;font-size:15px;font-weight:600;">' + q + '</span>'
            '<svg class="mini-faq-icon" width="18" height="18" fill="none" stroke="#631cff" stroke-width="2.5" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>'
            '</button><div class="mini-faq-body"><p style="color:rgba(2,2,30,.6);font-size:14px;line-height:1.6;margin:0;">' + ans + '</p></div></div>')
    s = s.replace(a, a + mini, 1)
    # Plan financiero: CTA secundario hacia la landing del plan del sector
    a = '<a class="gx-btn gx-btn--light" href="/dashboard-ia/">Conoce el dashboard IA</a>'
    assert a in s
    s = s.replace(a, '<div class="gd-cta2">' + a + f'<a class="gd-btn2" href="{c["lp_plan"]}" data-cta="sector-plan">Haz tu plan financiero 2027 gratis →</a></div>', 1)
    # Bloque nuevo antes del paso a paso de domicilio
    a = '<section class="gx-steps-sec">'
    assert a in s
    s = s.replace(a, more_than_agenda(c) + a, 1)
    # Rejilla de funcionalidades
    i = s.find('Tarjetas y cupones</h4>')
    assert i > 0
    j = s.find('</div>\n', s.find('</p></div>', i)) if False else s.find('</p></div>', i) + len('</p></div>')
    s = s[:j] + '\n' + ''.join(feat_card(*f) for f in c['feats']) + s[j:]
    # FAQ visibles (antes de «¿Hay periodo de prueba gratuito?») + JSON-LD
    a = '<div class="faq-item"><button class="faq-btn" onclick="toggleFaq(this)"><span style="color:#02021e;font-size:17px;font-weight:600;">¿Hay periodo de prueba gratuito?'
    assert a in s
    s = s.replace(a, ''.join(faq_item(q, x) for q, x in c['faq_new']) + a, 1)
    a = '    {\n      "@type": "Question",\n      "name": "¿Hay periodo de prueba gratuito?",'
    if a in s:
        ld = ''.join('    {\n      "@type": "Question",\n      "name": "%s",\n      "acceptedAnswer": {\n        "@type": "Answer",\n        "text": "%s"\n      }\n    },\n' % (q, x) for q, x in c['faq_new'])
        s = s.replace(a, ld + a, 1)
    # CTA principal (los dos primeros son los del menú: se quedan cortos)
    parts = s.split('>Prueba gratis 30 días</a>')
    last = len(parts) - 2  # el último es el enlace del pie de página
    s = parts[0] + ''.join(('>Prueba gratis 30 días</a>' if k < 2 or k == last else '>Prueba Godolphy gratis 30 días</a>') + p for k, p in enumerate(parts[1:]))
    open(c['file'], 'w', encoding='utf-8').write(s)
    print('ok', c['file'])


COMMON_FEATS = SECTORS['peluquerias']['feats']
COMMON_FAQ = SECTORS['peluquerias']['faq_new']


def sector(file, negocio, negocios, art, h1_old, h1_new, dom_old, dom_new, func_old, final_old, seo_old, seo_new,
           lp_plan, img, pos, notifs, gestor, calc, riesgo, extras_new, precio_txt, fixes=(), drop=(), extra_h2=()):
    """Configuración de un sector a partir de los textos de su página."""
    return {
        'file': file, 'negocio': negocio, 'lp_plan': lp_plan, 'hero_img': img, 'hero_pos': pos, 'notifs': notifs,
        'mas_lead': f'Además de reservas y agenda, Godolphy analiza tu {negocio} y te avisa de lo que hace que ganes más o pierdas dinero.',
        'precio_txt': precio_txt, 'gestor': gestor, 'calc': calc, 'riesgo': riesgo,
        'fixes': list(fixes), 'drop_sections': list(drop),
        'h2': [
            (h1_old, h1_new),
            ('Una agenda con IA que incrementa tus beneficios',
             f'Reservas, agenda, equipo y análisis IA: {it("así se ve Godolphy")} en tu {negocio}'),
            ('Descubre dónde estás perdiendo dinero y cómo recuperarlo.',
             f'Descubre dónde estás {ci("perdiendo dinero")} y cómo recuperarlo'),
            ('Los clientes reservan sin interrumpir tu tiempo.',
             f'Reservas online 24 h: tus clientes reservan {it("sin llamarte")}'),
            ('¡Qué no te dejen colgado/a! Solicita depósito.',
             f'Cobra una señal al reservar y {it("adiós a los plantones")}'),
            ('Y todo lo que necesitas para el día a día, <span class="gx-grad">en el mismo sitio.</span>',
             f'Recordatorios, horarios y bajas, tarjetas regalo y varios centros: {it("todo en la misma cuenta")}'),
            ('Gestión de horarios y vacaciones.', 'Horarios, vacaciones y bajas del equipo.'),
            ('Envía recordatorios vía whatsapp e email.', 'Recordatorios por WhatsApp y email.'),
            (dom_old, dom_new),
            ('Tus empleados siempre tendrán trabajo.',
             f'Cada profesional ve {it("su agenda")}; la recepción lleva el día sin tocar la configuración'),
            (func_old, f'Todo lo que incluye Godolphy para {it(art + " " + negocio)}'),
            ('Preguntas frecuentes', f'Lo que te preguntas {it("antes de cambiar de programa")}'),
            (final_old, f'Prueba Godolphy 30 días gratis {it("con tu equipo y tus servicios reales", True)}'),
            (seo_old, seo_new),
        ] + list(extra_h2),
        'extras_h2': (SECTORS['peluquerias']['extras_h2'][0], extras_new),
        'baja_li': SECTORS['peluquerias']['baja_li'],
        'equipo_faq_new': SECTORS['peluquerias']['equipo_faq_new'],
        'feats': COMMON_FEATS, 'faq_new': COMMON_FAQ,
    }


U = 'https://images.unsplash.com/{}?w=2000&q=75&auto=format&fit=crop'
EXTRAS_STD = f'Extras al reservar: {it("la agenda suma el tiempo y el precio")} sola'
LAS_CLIENTES = [('Las clientes reservan sin interrumpir tu tiempo.', 'Los clientes reservan sin interrumpir tu tiempo.'),
                ('Sí. Las clientes pueden seleccionar', 'Sí. Los clientes pueden seleccionar')]

SECTORS['barberias'] = sector(
    'sectores/software-para-barberias/index.html', 'barbería', 'barberías', 'tu',
    'Software para barberías — Reservas online y gestión de agenda',
    f'Software para barberías: {it("reservas, negocio y crecimiento", True)}',
    'Y si realizas servicios de barbería <span class="gx-grad">a domicilio</span>',
    f'Barbería a domicilio: {it("el desplazamiento se calcula y se cobra solo")}',
    'Funcionalidades específicas para tu barbería.',
    'Da de alta tu barbería y empieza a optimizar tu tiempo',
    'Software para barberías: lo que de verdad necesitas',
    'Software para barberías: lo que de verdad necesitas en 2027',
    '/lp/plan-financiero-2027/', '/images/sectores/hero/barberia-poster.webp', '62% center',
    [('Nueva reserva', 'Carlos · Corte + barba · vie. 19:30', 'ahora'),
     ('Recordatorio enviado', 'WhatsApp a Javi · mañana 10:00 ✓', '2 min'),
     ('Señal cobrada', '5,00 € · reserva de Adrián', '6 min')],
    ['2 citas de ayer sin cobrar', 'Sábado lleno: sube el precio de 10:00 a 14:00', '11 clientes llevan 6 semanas sin venir'],
    [('Corte degradado', 52), ('Arreglo de barba', 14)], 31, EXTRAS_STD,
    'Un recargo el sábado por la mañana, cuando todos quieren venir, o un descuento para llenar los martes. El cliente ve el precio final al reservar.')
SECTORS['barberias']['hero_video'] = '/images/sectores/hero/barberia'

SECTORS['estetica'] = sector(
    'sectores/software-para-centro-de-estetica-y-salones/index.html', 'centro de estética', 'centros de estética', 'tu',
    'Software para centros de estética — Reservas, pagos y fidelización con IA',
    f'Software para centros de estética: {it("reservas, negocio y crecimiento", True)}',
    'Y si realizas tratamientos <span class="gx-grad">a domicilio</span>',
    f'Tratamientos a domicilio: {it("el desplazamiento se calcula y se cobra solo")}',
    'Funcionalidades específicas para tu centro de estética.',
    'Da de alta tu centro de estética y empieza a optimizar tu tiempo',
    'El software para centros de estética que digitaliza tu negocio en 2026',
    'El software para centros de estética que digitaliza tu negocio en 2027',
    '/lp/plan-financiero-2027/', '/images/sectores/hero/estetica-cabina.webp', '80% center',
    [('Nueva reserva', 'Lucía · Higiene facial · jue. 17:00', 'ahora'),
     ('Bono vendido', '10 sesiones de presoterapia · 350 €', '3 min'),
     ('Recordatorio enviado', 'WhatsApp a Elena · mañana 12:00 ✓', '8 min')],
    ['4 sesiones de bono caducan esta semana', 'Mañana tienes la cabina 2 libre de 10 a 13', '15 clientes llevan 3 meses sin venir'],
    [('Higiene facial', 44), ('Radiofrecuencia', 11)], 27,
    f'Extras y tiempos de exposición: {it("la agenda calcula los tiempos")} por ti',
    'Un recargo el viernes por la tarde o un descuento para llenar las mañanas de entre semana. El cliente ve el precio final al reservar.',
    fixes=LAS_CLIENTES + [('¿Las clientes pueden elegir esteticista específica?', '¿Los clientes pueden elegir a su esteticista?')])

SECTORS['unas'] = sector(
    'sectores/software-para-salones-de-unas/index.html', 'salón de uñas', 'salones de uñas', 'tu',
    'Software para salones de uñas — Agenda online y gestión de clientes',
    f'Software para salones de uñas: {it("reservas, negocio y crecimiento", True)}',
    'Y si realizas manicuras <span class="gx-grad">a domicilio</span>',
    f'Manicura a domicilio: {it("el desplazamiento se calcula y se cobra solo")}',
    'Funcionalidades específicas para tu salón de uñas.',
    'Da de alta tu salón de uñas y empieza a optimizar tu tiempo',
    'Software para salones de uñas — Gestiona tu negocio sin caos en 2026',
    'Software para salones de uñas: gestiona tu negocio sin caos en 2027',
    '/lp/plan-financiero-2027/', '/images/sectores/hero/unas-manicurista-2.webp', '75% center'  # foto de stock propia (Envato); alternativa: U.format('photo-1588854337326-8afc3ad810b5'),
    [('Nueva reserva', 'Sara · Semipermanente + nail art · sáb. 12:00', 'ahora'),
     ('Recordatorio enviado', 'WhatsApp a Paula · relleno en 3 semanas ✓', '4 min'),
     ('Señal cobrada', '8,00 € · reserva de Irene', '7 min')],
    ['3 citas de ayer sin cobrar', 'Mañana tienes 2 huecos: 16:00 y 17:30', '19 clientes no han vuelto a por su relleno'],
    [('Semipermanente', 46), ('Uñas acrílicas', 12)], 19, EXTRAS_STD,
    'Un recargo el sábado o un descuento para llenar las mañanas de entre semana. El cliente ve el precio final al reservar.',
    fixes=LAS_CLIENTES + [('¿Las clientes pueden elegir nail artist específica?', '¿Los clientes pueden elegir a su nail artist?')],
    drop=['Tus empleados siempre tendrán trabajo.'],
    extra_h2=[('Tus nail artists siempre tendrán trabajo.',
               f'Cada nail artist ve {it("su agenda")}; la recepción lleva el día sin tocar la configuración')])

SECTORS['spa'] = sector(
    'sectores/software-para-spa-y-masajes/index.html', 'centro', 'spas y centros de masaje', 'tu',
    'Software para spas y centros de masajes — Reservas y gestión integral',
    f'Software para spas y centros de masaje: {it("reservas, negocio y crecimiento", True)}',
    'Y si ofreces masajes y tratamientos <span class="gx-grad">a domicilio</span>',
    f'Masajes a domicilio: {it("el desplazamiento se calcula y se cobra solo")}',
    'Funcionalidades específicas para tu centro de spa y masajes.',
    'Da de alta tu spa y empieza a optimizar tu tiempo',
    'Software para spas y centros de masajes — Gestión profesional en 2026',
    'Software para spas y centros de masaje: gestión profesional en 2027',
    '/lp/plan-financiero-2027/', '/images/sectores/hero/spa-3.webp', '65% center',
    [('Nueva reserva', 'Marta · Masaje relajante 60 min · dom. 11:00', 'ahora'),
     ('Tarjeta regalo vendida', 'Circuito spa para 2 · 120 €', '3 min'),
     ('Recordatorio enviado', 'WhatsApp a Pablo · mañana 18:00 ✓', '9 min')],
    ['2 sesiones de ayer sin cobrar', 'El domingo por la tarde tienes 3 huecos', '12 clientes llevan 2 meses sin venir'],
    [('Masaje relajante 60 min', 49), ('Ritual de 90 min', 13)], 12, EXTRAS_STD,
    'Un recargo el fin de semana o un descuento para llenar las mañanas de entre semana. El cliente ve el precio final al reservar.')


if __name__ == '__main__':
    for k in sys.argv[1:] or SECTORS:
        refresh(k)
