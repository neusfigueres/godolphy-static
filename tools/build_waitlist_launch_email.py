"""Correo 1 a la lista de espera (lanzamiento 26/10/2026). Estilo godolphy.com: degradado violeta, Gabarito + Plus Jakarta Sans, botones píldora blancos."""
import os
OUT = '/home/claude/emails-out/waitlist'
IMG = 'https://godolphy.com/img/email/dashboard-funnel/'
LOGO = 'https://godolphy.com/wp-images/logo-blanco.png'
U = 'utm_source=email&utm_medium=campaign&utm_campaign=lista-espera-lanzamiento&utm_content=e1'
H = "font-family:'Gabarito','Plus Jakarta Sans','Segoe UI',Helvetica,Arial,sans-serif;"
B = "font-family:'Plus Jakarta Sans','Segoe UI',Helvetica,Arial,sans-serif;"
SUBJECT = 'Godolphy abre el 26 de octubre'
PRE = 'Agenda, cobros y números de tu salón, en un solo sitio.'
FEATS = ['Tus clientas reservan online, a cualquier hora.', 'Recordatorio por WhatsApp el día antes de la cita.',
         'Citas en el salón o a domicilio, con desplazamientos.', 'Cobros y tarjetas regalo.', 'Análisis de tu negocio con IA.']

def li(t):
    return (f'<tr><td width="28" valign="top" style="padding:0 0 10px 0;{B}font-size:16px;line-height:24px;color:#631cff;font-weight:700;">&#10003;</td>'
            f'<td valign="top" style="padding:0 0 10px 0;{B}font-size:16px;line-height:24px;color:#02021e;">{t}</td></tr>')

html = f'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es"><head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="x-apple-disable-message-reformatting" /><meta name="color-scheme" content="light only" /><meta name="supported-color-schemes" content="light only" />
<title>{SUBJECT}</title>
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@600;800&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet" />
<style type="text/css">
body,table,td,a{{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;}} table,td{{border-collapse:collapse;mso-table-lspace:0;mso-table-rspace:0;}}
img{{border:0;outline:none;text-decoration:none;display:block;-ms-interpolation-mode:bicubic;}} body{{margin:0!important;padding:0!important;width:100%!important;}}
@media screen and (max-width:620px){{.container{{width:100%!important;}} .px{{padding-left:22px!important;padding-right:22px!important;}} .claim{{font-size:34px!important;line-height:38px!important;}} .h2{{font-size:24px!important;line-height:28px!important;}}}}
</style>
<!--[if mso]><style type="text/css">table,td,p,a{{font-family:'Segoe UI',Arial,sans-serif!important;}}</style><![endif]-->
</head>
<body style="margin:0;padding:0;background:#f8f7ff;">
<!-- Godolphy · Lista de espera · lanzamiento · E1 (19/10/2026) -->
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:#f8f7ff;opacity:0;">{PRE}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f8f7ff;"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#FFFFFF;border-radius:24px;overflow:hidden;">

<tr><td class="px" align="center" bgcolor="#631cff" style="background:#631cff;background-image:linear-gradient(160deg,#9B4FE8 0%,#631cff 70%);padding:36px 40px 0 40px;">
<img src="{LOGO}" width="150" alt="Godolphy" style="width:150px;height:auto;margin:0 auto 30px auto;" />
<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center"><tr><td style="background:rgba(255,255,255,0.16);border-radius:999px;padding:7px 16px;{B}font-size:12px;letter-spacing:1.4px;font-weight:700;color:#FFFFFF;text-transform:uppercase;">Abrimos el 26 de octubre</td></tr></table>
<p class="claim" style="margin:22px 0 0 0;{H}font-size:42px;line-height:46px;font-weight:800;letter-spacing:-0.8px;color:#FFFFFF;">Tu agenda, tus cobros y tus números, con IA.</p>
<p style="margin:18px auto 0 auto;max-width:470px;{B}font-size:17px;line-height:26px;color:#EFE9FF;">Godolphy es el programa de reservas para profesionales de la belleza, en salón o a domicilio. Abrimos el 26 y eres de las primeras en saberlo.</p>
<img src="{IMG}calendario.jpg" width="520" alt="Calendario de Godolphy con las citas del día por profesional" style="width:100%;max-width:520px;height:auto;margin:32px auto 0 auto;border-radius:14px 14px 0 0;" />
</td></tr>

<tr><td class="px" style="padding:34px 40px 8px 40px;">
<p class="h2" style="margin:0 0 18px 0;{H}font-size:26px;line-height:30px;font-weight:800;color:#02021e;">Qué hace Godolphy</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{''.join(li(f) for f in FEATS)}</table>
<p style="margin:8px 0 0 0;{B}font-size:15px;line-height:22px;color:#5b5675;">Todo en <a href="https://godolphy.com/?{U}" style="color:#631cff;font-weight:700;text-decoration:underline;">godolphy.com</a></p>
</td></tr>

<tr><td class="px" style="padding:28px 40px 8px 40px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f3efff;border-radius:20px;"><tr><td style="padding:28px 26px 30px 26px;" align="center">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center"><tr><td style="background:#EEFE3A;border-radius:999px;padding:6px 14px;{B}font-size:11px;letter-spacing:1.3px;font-weight:700;color:#02021e;text-transform:uppercase;">Ya disponible · gratis</td></tr></table>
<p class="h2" style="margin:16px 0 0 0;{H}font-size:28px;line-height:32px;font-weight:800;color:#02021e;">Mientras tanto, descubre dónde pierde dinero tu salón.</p>
<p style="margin:12px auto 0 auto;max-width:440px;{B}font-size:16px;line-height:24px;color:#3d3858;">Sube la exportación de tu agenda al dashboard IA y te dice cuánto ganas de verdad, qué clientas no han vuelto y qué servicios no te salen a cuenta.</p>
<a href="https://godolphy.com/dashboard-ia/?{U}" style="text-decoration:none;"><img src="{IMG}resumen.jpg" width="500" alt="Dashboard IA de Godolphy" style="width:100%;max-width:500px;height:auto;margin:22px auto 0 auto;border-radius:12px;border:1px solid #e3dafc;" /></a>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" style="margin-top:24px;"><tr><td align="center">
<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://godolphy.com/dashboard-ia/?{U}" style="height:54px;v-text-anchor:middle;width:300px;" arcsize="30%" stroke="f" fillcolor="#631cff"><w:anchorlock/><center style="color:#FFFFFF;font-family:'Segoe UI',Arial,sans-serif;font-size:17px;font-weight:bold;">Analizar mi salón gratis &rarr;</center></v:roundrect><![endif]-->
<!--[if !mso]><!-- --><a href="https://godolphy.com/dashboard-ia/?{U}" style="display:inline-block;padding:17px 30px;background:#631cff;color:#FFFFFF;{B}font-size:17px;line-height:20px;font-weight:700;text-decoration:none;border-radius:16px;">Analizar mi salón gratis &rarr;</a><!--<![endif]-->
</td></tr></table>
<p style="margin:12px 0 0 0;{B}font-size:11px;letter-spacing:1.3px;font-weight:700;color:#7d77a0;text-transform:uppercase;">Gratis · sin tarjeta · 30 segundos</p>
</td></tr></table>
</td></tr>

<tr><td class="px" style="padding:30px 40px 34px 40px;"><p style="margin:0;{B}font-size:16px;line-height:24px;color:#3d3858;">El 26 te escribo con el enlace para entrar. Si tienes cualquier duda, responde a este email: lo leo yo.</p>
<p style="margin:16px 0 0 0;{B}font-size:16px;color:#3d3858;">Un abrazo,<br /><span style="{H}font-size:22px;font-weight:800;color:#631cff;">Neus</span><br /><span style="font-size:13px;color:#7d77a0;">Fundadora de Godolphy</span></p></td></tr>

<tr><td class="px" align="center" style="background:#02021e;padding:26px 40px 28px 40px;">
<img src="{LOGO}" width="110" alt="Godolphy" style="width:110px;height:auto;margin:0 auto;opacity:0.9;" />
<p style="margin:14px 0 0 0;{B}font-size:12px;color:#b9b4d6;"><a href="https://godolphy.com/?{U}" style="color:#b9b4d6;text-decoration:none;">godolphy.com</a> &middot; <a href="https://instagram.com/godolphy" style="color:#b9b4d6;text-decoration:none;">@godolphy</a> &middot; <a href="mailto:hello@godolphy.com" style="color:#b9b4d6;text-decoration:none;">hello@godolphy.com</a></p>
<p style="margin:12px 0 0 0;{B}font-size:11px;line-height:17px;color:#8e89ad;">Recibes este email porque te apuntaste a la lista de espera de Godolphy.<br />¿No quieres recibir más? <a href="%UNSUBSCRIBELINK%" style="color:#b9b4d6;text-decoration:underline;">Date de baja aquí.</a></p>
<p style="margin:8px 0 0 0;{B}font-size:11px;color:#8e89ad;">Godolphy &middot; %ACCOUNT_ADDRESS%</p>
</td></tr>
</table></td></tr></table>
</body></html>
'''

text = '\n'.join([PRE, '', 'ABRIMOS EL 26 DE OCTUBRE', '', 'Tu agenda, tus cobros y tus números, con IA.', '',
  'Godolphy es el programa de reservas para profesionales de la belleza, en salón o a domicilio. Abrimos el 26 y eres de las primeras en saberlo.', '',
  'Qué hace Godolphy:'] + [f'- {f}' for f in FEATS] + [f'Todo en https://godolphy.com/?{U}', '',
  'MIENTRAS TANTO, DESCUBRE DÓNDE PIERDE DINERO TU SALÓN', 'Sube la exportación de tu agenda al dashboard IA y te dice cuánto ganas de verdad, qué clientas no han vuelto y qué servicios no te salen a cuenta.',
  f'Analizar mi salón gratis → https://godolphy.com/dashboard-ia/?{U}', 'Gratis · sin tarjeta · 30 segundos', '',
  'El 26 te escribo con el enlace para entrar. Si tienes cualquier duda, responde a este email: lo leo yo.', '', 'Un abrazo,', 'Neus', 'Fundadora de Godolphy', '',
  'Recibes este email porque te apuntaste a la lista de espera de Godolphy.', '¿No quieres recibir más? Date de baja aquí: %UNSUBSCRIBELINK%', '', 'Godolphy · %ACCOUNT_ADDRESS%'])

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    open(f'{OUT}/e1.html', 'w').write(html); open(f'{OUT}/e1.txt', 'w').write(text)
    print(len(html), len(text))
