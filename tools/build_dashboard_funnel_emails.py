"""Genera el HTML y el texto de los 9 correos del Dashboard Funnel (AC #16) en formato anuncio.
Salida: emails-out/<id>.html, <id>.txt y meta.json (asunto, preheader, message_id)."""
import json, os, html

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'emails-out')
IMG = 'https://godolphy.com/img/email/dashboard-funnel/'
LOGO = 'https://godolphy.activehosted.com/content/EKKdk4/2026/05/15/fe290f7c-ae69-4e68-a1c7-a868dfc6068c.png'
LOGO_FOOT = 'https://godolphy.activehosted.com/content/EKKdk4/2026/05/15/2a290431-3185-4799-bcd1-ab5541721a79.png'
LINK = 'https://godolphy.com/dashboard-ia/?utm_source=email&utm_medium=automation&utm_campaign=dashboard-funnel&utm_content='

E = [
 dict(id='a1', msg=102, subject='Tu análisis te espera', pre='Sube tu Excel y en 30 segundos lo ves.',
      claim=('Tus números ya saben', 'dónde pierdes dinero.'), one='Sube el Excel de reservas y la IA te lo enseña en 30 segundos.',
      img='resumen', alt='Análisis de Godolphy: facturación, ocupación e ingresos mensuales', cta='Analizar mi negocio gratis',
      more_t='Lo que verás', more=['Qué servicios no te compensan.', 'Qué clientas habituales no han vuelto.', 'Dónde tienes oportunidades de negocio.'],
      extra='Mejor desde el ordenador. ¿Dudas? Responde a este email, lo leo yo.'),
 dict(id='b1', msg=103, subject='Ya tienes tu análisis. ¿Sabes leerlo?', pre='3 emails cortos, un bloque en cada uno.',
      claim=('Ver los números', 'no es entenderlos.'), one='Estos días te explico, en 3 emails cortos, qué te dice cada bloque.',
      img='resumen', alt='Análisis de Godolphy', cta='Volver a mi análisis',
      more_t='Lo que viene', more=['Mañana: qué servicios te dan dinero de verdad.', 'Después: las clientas que aún no han vuelto.', 'Y al final: cuánto rinde tu equipo y tu beneficio estimado.'],
      extra='<b>Un truco:</b> añade el coste mensual de tu equipo en el dashboard. El análisis sale mucho más exacto.'),
 dict(id='b2', msg=104, subject='El servicio que más vendes puede ser el que menos te deja', pre='Mira el margen por hora, no la facturación.',
      claim=('Facturar mucho', 'no es ganar mucho.'), one='Mira la columna «€/hora»: te dice qué servicio te paga mejor tu tiempo.',
      img='servicios', alt='Bloque Rendimiento por servicio', cta='Ver mis servicios',
      more_t='Un ejemplo', more=['Servicio A: 2.000 € en 80 h = 25 €/h.', 'Servicio B: 1.200 € en 20 h = 60 €/h.', 'El B factura menos y te paga más del doble por hora.'],
      extra='<b>Esta semana:</b> promociona el servicio con más €/h. Al de menos, súbele el precio, acorta el tiempo o quítalo.'),
 dict(id='b3', msg=105, subject='Hay clientas que ya deberían haber vuelto', pre='Tu análisis te dice quiénes son.',
      claim=('Las clientas no avisan', 'cuando dejan de venir.'), one='Tu análisis te dice qué clientas habituales suelen volver por estas fechas y aún no han reservado.',
      img='prevision', alt='Bloque Previsión: clientas habituales que aún no han reservado', cta='Ver quién falta por volver',
      more_t='Qué mirar', more=['Previsión: las clientas habituales que aún no han reservado.', 'Clientes más valiosos: quién gasta más.', 'Alertas: citas canceladas sin reagendar.'],
      extra='<b>Esta semana:</b> elige las que más gastan y aún no han reservado, y mándales un WhatsApp personal: «Hola Marta, hace tiempo que no nos vemos. ¿Te guardo hueco esta semana?»'),
 dict(id='b4', msg=106, subject='Cuánto rinde de verdad cada hora de tu equipo', pre='Y tu beneficio, en cuanto añades costes.',
      claim=('Lo que facturas', 'no es lo que ganas.'), one='Mira cuánto factura cada profesional por hora y añade tus costes para ver tu beneficio estimado.',
      img='profesional', alt='Bloque Rendimiento por profesional', cta='Ver mi equipo',
      more_t='Un ejemplo', more=['Profesional A: factura 450 € en 15 h = 30 €/h.', 'Profesional B: factura 450 € en 10 h = 45 €/h.', 'Misma facturación. Si una rinde menos por hora, suele ser por el tipo de servicio que hace, no por cómo trabaja.'],
      extra='<b>Un paso más:</b> pulsa «Añadir costes» y el dashboard te calcula el beneficio estimado del mes. Desde el 26 de octubre, Godolphy hace este análisis solo, cada mes, con tus reservas.'),
 dict(id='a3', msg=107, subject='Te falta un paso', pre='Sube tu Excel y listo.',
      claim=('Estás a 30 segundos', 'de ver tu análisis.'), one='Entraste, pero no llegaste a subir el Excel. Cuando tengas un minuto en el ordenador, lo arrastras y listo.',
      img='resumen', alt='Análisis de Godolphy', cta='Subir mi Excel',
      more_t='¿No sabes dónde está tu Excel?', more=[],
      extra='En tu programa de reservas, busca «Informes» o «Exportar». ¿Te atascas? Responde a este email.'),
 dict(id='a4', msg=109, subject='¿Sabes qué clientas no han vuelto?', pre='Tus reservas lo saben.',
      claim=('Tus reservas saben', 'quién ha dejado de venir.'), one='Sube tu Excel y verás qué clientas habituales aún no han reservado y cuáles gastan más.',
      img='valiosas', alt='Bloque Clientes más valiosos', cta='Ver mis clientas',
      more_t='Lo que verás', more=['Qué clientas suelen volver por estas fechas y aún no han reservado.', 'Tus clientas más valiosas por gasto.', 'Las citas canceladas sin reagendar.'], extra=''),
 dict(id='a5', msg=110, subject='¿Cuánto te deja de verdad tu servicio estrella?', pre='Quizás menos de lo que crees.',
      claim=('Tu servicio más vendido puede ser', 'el que menos te deja.'), one='Sube tu Excel y mira el margen por hora de cada servicio.',
      img='servicios', alt='Bloque Rendimiento por servicio', cta='Calcular mi margen',
      more_t='A mano o con Godolphy', more=['A mano: sacar servicios, cruzar tiempos y precios, montar fórmulas. Horas.', 'Con Godolphy: subes el archivo y lo ves.'],
      extra='Luego decides: subir precio, ajustar duración o quitarlo de la carta.'),
 dict(id='a6', msg=111, subject='3 cambios para ganar más sin trabajar más horas', pre='Tu Excel te dice cuáles.',
      claim=('Más ingresos', 'sin más clientas.'), one='Recuperar clientas, ajustar un precio y quitar un servicio que no rinde. El dashboard te dice cuáles.',
      img='oportunidades', alt='Bloque Oportunidades', cta='Subir mi Excel',
      more_t='Los 3 cambios', more=['Recupera a las que más gastan y llevan más de 45 días sin venir.', 'Revisa el precio del servicio con muchas reservas y poco margen.', 'Quita el servicio que casi nadie pide.'],
      extra='Es el último email de esta serie.'),
]

F = "font-family:'Inter Tight','Segoe UI',Helvetica,Arial,sans-serif;"
S = "font-family:'Instrument Serif',Georgia,'Times New Roman',serif;font-style:italic;font-weight:400;"

def build(e):
    url = LINK + e['id']
    lis = ''.join(f'<li style="margin:0 0 6px 0;">{html.escape(x)}</li>' for x in e['more'])
    ul = f'<ul style="margin:8px 0 0 0;padding-left:20px;{F}font-size:15px;line-height:22px;color:#4A3F6B;">{lis}</ul>' if lis else ''
    extra = f'<p style="margin:12px 0 0 0;{F}font-size:15px;line-height:22px;color:#4A3F6B;">{e["extra"]}</p>' if e['extra'] else ''
    c1, c2 = (html.escape(x) for x in e['claim'])
    return f'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es"><head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="x-apple-disable-message-reformatting" /><meta name="color-scheme" content="light only" /><meta name="supported-color-schemes" content="light only" />
<title>{html.escape(e['subject'])}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;600;800&family=Instrument+Serif:ital@1&display=swap" rel="stylesheet" />
<style type="text/css">
body,table,td,a{{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;}} table,td{{border-collapse:collapse;mso-table-lspace:0;mso-table-rspace:0;}}
img{{border:0;outline:none;text-decoration:none;display:block;-ms-interpolation-mode:bicubic;}} body{{margin:0!important;padding:0!important;width:100%!important;}}
@media screen and (max-width:620px){{.container{{width:100%!important;}} .px{{padding-left:22px!important;padding-right:22px!important;}} .claim{{font-size:32px!important;line-height:36px!important;}}}}
</style>
<!--[if mso]><style type="text/css">table,td,p,a,li{{font-family:'Segoe UI',Arial,sans-serif!important;}}</style><![endif]-->
</head>
<body style="margin:0;padding:0;background:#F1ECFB;">
<!-- Godolphy · Dashboard Funnel v2 · {e['id'].upper()} · formato anuncio (19/10/2026) -->
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:#F1ECFB;opacity:0;">{html.escape(e['pre'])}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F1ECFB;"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#FFFFFF;border-radius:20px;overflow:hidden;">
<tr><td class="px" bgcolor="#4B1FE8" style="background:#4B1FE8;background-image:linear-gradient(150deg,#4B1FE8 0%,#7B3BFF 100%);padding:32px 40px 34px 40px;">
<img src="{LOGO}" width="112" alt="Godolphy" style="height:28px;width:auto;margin:0 0 26px 0;" />
<p class="claim" style="margin:0;{F}font-size:40px;line-height:44px;font-weight:800;letter-spacing:-1.2px;color:#FFFFFF;">{c1}<br /><span style="{S}color:#F5D6B8;">{c2}</span></p>
<p style="margin:16px 0 0 0;{F}font-size:17px;line-height:25px;color:#EAE3FF;">{html.escape(e['one'])}</p>
</td></tr>
<tr><td class="px" style="padding:28px 40px 0 40px;">
<a href="{url}" style="text-decoration:none;"><img src="{IMG}{e['img']}.jpg" width="520" alt="{html.escape(e['alt'])}" style="width:100%;max-width:520px;height:auto;border:1px solid #E4DCF7;border-radius:12px;" /></a>
</td></tr>
<tr><td align="center" style="padding:26px 40px 0 40px;">
<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{url}" style="height:54px;v-text-anchor:middle;width:300px;" arcsize="50%" stroke="f" fillcolor="#0A0420"><w:anchorlock/><center style="color:#FFFFFF;font-family:'Segoe UI',Arial,sans-serif;font-size:17px;font-weight:bold;">{html.escape(e['cta'])} &rarr;</center></v:roundrect><![endif]-->
<!--[if !mso]><!-- --><a href="{url}" style="display:inline-block;padding:17px 32px;background:#0A0420;color:#FFFFFF;{F}font-size:17px;line-height:20px;font-weight:700;text-decoration:none;border-radius:999px;">{html.escape(e['cta'])} &rarr;</a><!--<![endif]-->
</td></tr>
<tr><td class="px" style="padding:30px 40px 0 40px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-top:1px solid #ECE5FB;padding-top:22px;">
<p style="margin:0;{F}font-size:15px;line-height:22px;font-weight:700;color:#0A0420;">{html.escape(e['more_t'])}</p>{ul}{extra}
</td></tr></table></td></tr>
<tr><td class="px" style="padding:26px 40px 34px 40px;"><p style="margin:0;{F}font-size:15px;color:#4A3F6B;">Un abrazo,<br /><span style="{S}font-size:26px;line-height:34px;color:#4B1FE8;">Neus</span><br /><span style="font-size:12px;color:#8A7DAE;">Fundadora · Godolphy</span></p></td></tr>
<tr><td class="px" align="center" style="background:#F7F4FC;border-top:1px solid #ECE5FB;padding:22px 40px 26px 40px;">
<img src="{LOGO_FOOT}" alt="Godolphy" width="88" style="height:22px;width:auto;opacity:0.75;margin:0 auto;" />
<p style="margin:12px 0 0 0;{F}font-size:12px;color:#8A7DAE;"><a href="https://godolphy.com" style="color:#8A7DAE;text-decoration:none;">godolphy.com</a> &middot; <a href="https://instagram.com/godolphy" style="color:#8A7DAE;text-decoration:none;">@godolphy</a> &middot; <a href="mailto:hello@godolphy.com" style="color:#8A7DAE;text-decoration:none;">Ayuda</a></p>
<p style="margin:12px 0 0 0;{F}font-size:11px;line-height:17px;color:#B1A6CE;">Recibes este email porque te registraste en Godolphy.<br />¿No quieres recibir más? <a href="%UNSUBSCRIBELINK%" style="color:#8A7DAE;text-decoration:underline;">Date de baja aquí.</a></p>
<p style="margin:8px 0 0 0;{F}font-size:11px;color:#B1A6CE;">Godolphy &middot; %ACCOUNT_ADDRESS%</p>
</td></tr>
</table></td></tr></table>
</body></html>
'''

def text(e):
    import re
    strip = lambda s: re.sub('<[^>]+>', '', s)
    url = LINK + e['id']
    parts = [e['pre'], '', ' '.join(e['claim']), '', e['one'], '', f"{e['cta']} → {url}", '', e['more_t']]
    parts += [f'- {x}' for x in e['more']]
    if e['extra']: parts += ['', strip(e['extra'])]
    parts += ['', 'Un abrazo,', 'Neus', 'Fundadora · Godolphy', '', 'Recibes este email porque te registraste en Godolphy.', '¿No quieres recibir más? Date de baja aquí: %UNSUBSCRIBELINK%', '', 'Godolphy · %ACCOUNT_ADDRESS%']
    return '\n'.join(parts)

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    meta = {}
    for e in E:
        open(os.path.join(OUT, e['id'] + '.html'), 'w').write(build(e))
        open(os.path.join(OUT, e['id'] + '.txt'), 'w').write(text(e))
        meta[e['id']] = dict(message_id=e['msg'], subject=e['subject'], preheader=e['pre'])
    json.dump(meta, open(os.path.join(OUT, 'meta.json'), 'w'), ensure_ascii=False, indent=1)
    print('ok', len(E))
