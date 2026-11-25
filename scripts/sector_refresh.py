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
            '<link rel="stylesheet" href="/assets/gx-motion.css">'
            '<script src="/assets/gx-motion.js" defer></script>')

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


SECTORS = {
    'peluquerias': {
        'file': 'sectores/software-para-peluquerias/index.html',
        'negocio': 'peluquería',
        'lp_plan': '/lp/plan-financiero-2027-peluquerias/',
        'mas_lead': 'Además de reservas y agenda, Godolphy analiza tu peluquería y te avisa de lo que hace que ganes más o pierdas dinero.',
        'precio_txt': 'Un recargo los sábados por la mañana o un descuento para llenar las horas flojas del martes. El cliente ve el precio final al reservar.',
        'gestor': ['3 citas de ayer sin cobrar', 'Mañana tienes 2 huecos: 11:00 y 12:30', '8 clientes llevan 3 meses sin venir'],
        'calc': [('Corte y peinado', 48), ('Mechas', 9)],
        'riesgo': 23,
        'h2': [
            # (texto actual exacto del interior del <h2>/<h1>/<h3>, texto nuevo)
            ('Software para peluquerías — Reservas, agenda y gestión con IA',
             f'Software para peluquerías: {it("reservas, agenda y números", True)} en un solo sitio'),
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
    # Títulos
    for old, new in c['h2']:
        n = s.count('>' + old + '<')
        assert n >= 1, ('título no encontrado', old)
        s = s.replace('>' + old + '<', '>' + new + '<')
    s, n = c['extras_h2'][0].subn(c['extras_h2'][1], s, count=1)
    assert n == 1, 'título de extras no encontrado'
    # Bajas en la tarjeta de horarios + enlace
    a = '<li>Días de descanso y vacaciones bloqueadas</li>'
    assert a in s
    s = s.replace(a, a + c['baja_li'], 1)
    s = s.replace('Configura el horario de cada profesional, sus días libres y vacaciones. La agenda se actualiza sola.',
                  'Configura el horario de cada profesional, sus días libres, vacaciones y bajas. Las citas afectadas se resuelven en un momento.', 1)
    # Recepcionista en el bloque de equipo (mini FAQ)
    a = c['equipo_faq_after'] + '</p></div></div>'
    assert a in s
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
    a = '    <div class="faq-item"><button class="faq-btn" onclick="toggleFaq(this)"><span style="color:#02021e;font-size:17px;font-weight:600;">¿Hay periodo de prueba gratuito?'
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


if __name__ == '__main__':
    for k in sys.argv[1:] or SECTORS:
        refresh(k)
