"""Emails Brevo novedades (oct. 2026): ausencias, tarjetas regalo, plan financiero 2027, calculadora de precios.
Estilo anuncio: claim + mensaje + más info. Merge tag Brevo obligatorio: {{ unsubscribe }}. Remitente/pie: «Godolphy»."""
import os, importlib.util, json
here = os.path.dirname(__file__)
spec = importlib.util.spec_from_file_location('w', os.path.join(here, 'build_waitlist_e2_e3.py')); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
LOGO, H, B = w.LOGO, w.H, w.B
OUT = '/home/claude/emails-out/brevo'
SIGNUP = 'https://app.godolphy.com/auth/sign-up'

def U(c, k='c1'): return f'utm_source=brevo&utm_medium=email&utm_campaign={c}&utm_content={k}'
def url(base, c, k='c1'): return f'{base}{"&" if "?" in base else "?"}{U(c, k)}'

def btn(link, label, bg, fg):
    return (f'<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{link}" style="height:54px;v-text-anchor:middle;width:300px;" arcsize="30%" stroke="f" fillcolor="{bg}"><w:anchorlock/><center style="color:{fg};font-family:\'Segoe UI\',Arial,sans-serif;font-size:17px;font-weight:bold;">{label} &rarr;</center></v:roundrect><![endif]-->'
            f'<!--[if !mso]><!-- --><a href="{link}" style="display:inline-block;padding:17px 30px;background:{bg};color:{fg};{B}font-size:17px;line-height:20px;font-weight:700;text-decoration:none;border-radius:16px;">{label} &rarr;</a><!--<![endif]-->')

def checks(items):
    return ''.join(f'<tr><td width="28" valign="top" style="padding:0 0 10px 0;{B}font-size:16px;line-height:24px;color:#631cff;font-weight:700;">&#10003;</td>'
                   f'<td valign="top" style="padding:0 0 10px 0;{B}font-size:16px;line-height:24px;color:#02021e;">{i}</td></tr>' for i in items)

def build(e):
    c = e['camp']; home = url('https://godolphy.com/', c, 'pie')
    main = url(e['cta_url'], c, 'c1')
    img_link = main
    if e.get('options'):
        opts = ''
        for i, o in enumerate(e['options']):
            link = url(o['url'], c, f'op{i+1}') if o['url'].startswith('https://godolphy.com') else url(o['url'], c, f'op{i+1}')
            bg, fg = ('#631cff', '#FFFFFF') if i == 1 else ('#FFFFFF', '#631cff')
            border = '' if i == 1 else 'border:2px solid #631cff;'
            opts += (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f3efff;border-radius:20px;margin:0 0 14px 0;"><tr><td style="padding:22px 24px;">'
                     f'<p style="margin:0 0 6px 0;{H}font-size:21px;line-height:26px;font-weight:800;color:#02021e;">{o["title"]}</p>'
                     f'<p style="margin:0 0 16px 0;{B}font-size:15px;line-height:23px;color:#3d3858;">{o["text"]}</p>'
                     f'<a href="{link}" style="display:inline-block;padding:13px 22px;background:{bg};{border}color:{fg};{B}font-size:15px;font-weight:700;text-decoration:none;border-radius:14px;">{o["label"]} &rarr;</a>'
                     f'</td></tr></table>')
        body = f'<tr><td class="px" style="padding:30px 40px 8px 40px;">{opts}</td></tr>'
        hero_btn = ''
        img_link = url(e['options'][1]['url'], c, 'img')
    else:
        body = (f'<tr><td class="px" style="padding:30px 40px 8px 40px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f3efff;border-radius:20px;"><tr><td style="padding:26px 26px 18px 26px;">'
                f'<p style="margin:0 0 16px 0;{H}font-size:24px;line-height:28px;font-weight:800;color:#02021e;">{e["box_title"]}</p>'
                f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{checks(e["items"])}</table>'
                f'<p style="margin:6px 0 0 0;{B}font-size:15px;line-height:22px;color:#3d3858;"><b>Pruébalo 30 días gratis, sin tarjeta.</b> <a href="{url(SIGNUP, c, "pie")}" style="color:#631cff;font-weight:700;text-decoration:underline;">Empezar ahora</a></p>'
                f'</td></tr></table></td></tr>')
        hero_btn = f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" style="margin-top:22px;"><tr><td align="center">{btn(main, e["cta"], "#FFFFFF", "#631cff")}</td></tr></table>'
    html = f'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es"><head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="x-apple-disable-message-reformatting" /><meta name="color-scheme" content="light only" /><meta name="supported-color-schemes" content="light only" />
<title>{e["subject"]}</title>
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@600;800&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet" />
<style type="text/css">
body,table,td,a{{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;}} table,td{{border-collapse:collapse;mso-table-lspace:0;mso-table-rspace:0;}}
img{{border:0;outline:none;text-decoration:none;display:block;-ms-interpolation-mode:bicubic;}} body{{margin:0!important;padding:0!important;width:100%!important;}}
@media screen and (max-width:620px){{.container{{width:100%!important;}} .px{{padding-left:22px!important;padding-right:22px!important;}} .claim{{font-size:30px!important;line-height:34px!important;}}}}
</style>
<!--[if mso]><style type="text/css">table,td,p,a{{font-family:'Segoe UI',Arial,sans-serif!important;}}</style><![endif]-->
</head>
<body style="margin:0;padding:0;background:#f8f7ff;">
<!-- Godolphy · Brevo · novedades oct. 2026 · {e["id"]} -->
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:#f8f7ff;opacity:0;">{e["pre"]}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f8f7ff;"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#FFFFFF;border-radius:24px;overflow:hidden;">
<tr><td class="px" align="center" bgcolor="#631cff" style="background:#631cff;background-image:linear-gradient(160deg,#9B4FE8 0%,#631cff 70%);padding:36px 40px 34px 40px;">
<img src="{LOGO}" width="150" alt="Godolphy" style="width:150px;height:auto;margin:0 auto 30px auto;" />
<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center"><tr><td style="background:#EEFE3A;border-radius:999px;padding:7px 16px;{B}font-size:12px;letter-spacing:1.4px;font-weight:700;color:#02021e;text-transform:uppercase;">{e["pill"]}</td></tr></table>
<p class="claim" style="margin:22px 0 0 0;{H}font-size:42px;line-height:46px;font-weight:800;letter-spacing:-0.8px;color:#FFFFFF;">{e["claim"]}</p>
<p style="margin:16px auto 0 auto;max-width:480px;{B}font-size:17px;line-height:26px;color:#EFE9FF;">{e["msg"]}</p>
<a href="{img_link}" style="text-decoration:none;"><img src="{e["img"]}" width="520" alt="{e["alt"]}" style="width:100%;max-width:520px;height:auto;margin:28px auto 4px auto;border-radius:16px;background:#ffffff;" /></a>
{hero_btn}
</td></tr>
{body}
<tr><td class="px" style="padding:26px 40px 34px 40px;"><p style="margin:0;{B}font-size:16px;line-height:24px;color:#3d3858;">¿Dudas? Responde a este email: lo leo yo.</p>
<p style="margin:16px 0 0 0;{B}font-size:16px;color:#3d3858;">Un saludo,<br /><span style="{H}font-size:22px;font-weight:800;color:#631cff;">Neus</span><br /><span style="font-size:13px;color:#7d77a0;">Fundadora de Godolphy</span></p></td></tr>
<tr><td class="px" align="center" style="background:#02021e;padding:26px 40px 28px 40px;">
<img src="{LOGO}" width="110" alt="Godolphy" style="width:110px;height:auto;margin:0 auto;opacity:0.9;" />
<p style="margin:14px 0 0 0;{B}font-size:12px;color:#b9b4d6;"><a href="{home}" style="color:#b9b4d6;text-decoration:none;">godolphy.com</a> &middot; <a href="https://instagram.com/godolphy" style="color:#b9b4d6;text-decoration:none;">@godolphy</a></p>
<p style="margin:12px 0 0 0;{B}font-size:11px;line-height:17px;color:#8e89ad;">¿No te interesa? <a href="{{{{ unsubscribe }}}}" style="color:#b9b4d6;text-decoration:underline;">Date de baja aquí</a> y no te volveremos a escribir.</p>
<p style="margin:8px 0 0 0;{B}font-size:11px;color:#8e89ad;">Godolphy</p>
</td></tr>
</table></td></tr></table>
</body></html>
'''
    return html

G = 'https://godolphy.com'
E = [
 dict(id='n1-ausencias', camp='novedades-ausencias', subject='Mañana no vendré a trabajar', pre='Lo que pasa en tu agenda cuando alguien del equipo se pone de baja.',
      pill='Ausencias del equipo', claim='Si tu empleada está de baja, no pierdas el tiempo contactando a los clientes.',
      msg='Marca la ausencia y Godolphy te enseña las citas afectadas. Tú eliges qué hacer con ellas.',
      img=f'{G}/img/email/novedades/email-ausencias.png', alt='Citas afectadas por una ausencia en Godolphy',
      cta='Ver cómo funciona', cta_url=f'{G}/funcionalidades/vacaciones-y-ausencias/', box_title='Sin llamar a nadie.',
      items=['Pásalas a otra persona del equipo, a la misma hora y al mismo precio.',
             'O envía un enlace para que cada cliente elija a otra persona, otro día o cancele sin coste.',
             'Si no responde, 24 h antes Godolphy pasa la cita a quien esté libre o la cancela y lo devuelve todo.']),
 dict(id='n2-tarjetas', camp='novedades-tarjetas-regalo', subject='Has vendido una tarjeta regalo 🎁', pre='Este es el aviso que recibirás con cada venta. Llegas a tiempo para Navidad.',
      pill='Tarjetas regalo', claim='Has vendido una tarjeta regalo. Mientras dormías.',
      msg='Este es el mensaje que te llegará con cada venta. Tus clientes compran la tarjeta desde tu web de reservas, a cualquier hora y aunque el salón esté cerrado.',
      img=f'{G}/funcionalidades/cupones-y-tarjetas-regalo/img/s1-tarjeta-regalo.png', alt='Tarjeta regalo de Godolphy',
      cta='Activar tarjetas regalo', cta_url=f'{G}/funcionalidades/cupones-y-tarjetas-regalo/', box_title='Llegas a tiempo para Navidad.',
      items=['Se venden solas desde tu web de reservas, 24 horas.', 'El dinero va directo a tu cuenta.', 'La persona que la recibe la tiene en su email, lista para regalar.']),
 dict(id='n3-plan2027', camp='novedades-plan-financiero-2027', subject='Empieza tu plan financiero 2027', pre='Gratis en Excel, o automático con Godolphy. Tú eliges.',
      pill='Plan financiero 2027', claim='Este año sí: crea tu plan financiero 2027.',
      msg='Citas, facturación y gastos, mes a mes. Hay dos maneras de hacer tu plan financiero:',
      img=f'{G}/img/email/novedades/email-plan-2027.png', alt='Plan financiero mes a mes en Godolphy', cta='', cta_url=f'{G}/funcionalidades/plan-financiero/',
      options=[dict(title='Plantilla gratis en Excel', text='La rellenas tú, mes a mes.', label='Descargar plantilla', url=f'{G}/plan-financiero-salon-estetica-excel-google-sheet/'),
               dict(title='Con Godolphy, automático', text='Objetivos mes a mes a partir de tus datos reales. Y cada mes, plan contra real: citas, facturación, gastos, CAC, LTV y caja.', label='Probar gratis 30 días', url=SIGNUP)]),
 dict(id='n4-precios', camp='novedades-calculadora-precios', subject='Calcula tus precios con esta plantilla', pre='Descubre qué servicios te hacen perder dinero.',
      pill='Calculadora de precios', claim='¿Sabes cuánto te cuesta de verdad cada servicio?',
      msg='Hora de la profesional, local, gastos y producto. Con eso sale el precio que necesitas para tener el margen que quieres. Dos maneras de calcularlo:',
      img=f'{G}/img/email/novedades/email-precios.png', alt='Calculadora de precios de Godolphy', cta='', cta_url=f'{G}/funcionalidades/calculadora-de-precios/',
      options=[dict(title='Calculadora gratis en Excel', text='Pon tus costes y te dice el precio de cada servicio.', label='Descargar calculadora', url=f'{G}/descargas/calculadora-precios-centros-estetica-2027.xlsx'),
               dict(title='Con Godolphy, automático', text='Calcula el coste real de cada servicio con tus datos, te avisa de los que pierden dinero y cambia el precio con un botón.', label='Probar gratis 30 días', url=SIGNUP)]),
]
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    meta = []
    for e in E:
        h = build(e); open(f'{OUT}/{e["id"]}.html', 'w').write(h); meta.append({'id': e['id'], 'subject': e['subject'], 'pre': e['pre']})
        print(e['id'], len(h), 'clienta' in h.lower())
    json.dump(meta, open(f'{OUT}/novedades_meta.json', 'w'), ensure_ascii=False, indent=1)
