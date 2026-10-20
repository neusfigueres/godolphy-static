"""Correos 2 (23/10) y 3 (26/10) a la lista de espera. Misma estética que E1 (godolphy.com)."""
import os, html as H_
OUT = '/home/claude/emails-out/waitlist'
IMG = 'https://godolphy.com/img/email/dashboard-funnel/'
LOGO = 'https://godolphy.com/wp-images/logo-blanco.png'
H = "font-family:'Gabarito','Plus Jakarta Sans','Segoe UI',Helvetica,Arial,sans-serif;"
B = "font-family:'Plus Jakarta Sans','Segoe UI',Helvetica,Arial,sans-serif;"
SIGNUP = os.environ.get('SIGNUP_URL', 'https://app.godolphy.com/')  # pendiente de confirmar por Neus

def utm(c): return f'utm_source=email&utm_medium=campaign&utm_campaign=lista-espera-lanzamiento&utm_content={c}'
def u(url, c): return url + ('&' if '?' in url else '?') + utm(c)

E = [
 dict(id='e2', subject='El lunes abrimos Godolphy', pre='30 días gratis, sin tarjeta.', pill='Faltan 3 días',
      claim='El lunes abrimos.', one='Desde el 26 de octubre podrás probar Godolphy 30 días gratis, con todo el plan Pro y sin tarjeta.',
      img='oportunidades', alt='Oportunidades detectadas por el análisis IA de Godolphy', cta='Ver planes y precios', url='https://godolphy.com/precio/',
      more=[('Sin permanencia:', ' al acabar la prueba eliges plan o lo dejas.'),
            ('Mientras tanto,', ' el dashboard IA ya es gratis: <a href="{dia}" style="color:#631cff;font-weight:700;text-decoration:underline;">analiza tu salón</a>.')],
      close='El lunes te escribo con el enlace para entrar.'),
 dict(id='e3', subject='Ya puedes entrar en Godolphy', pre='30 días gratis, sin tarjeta.', pill='Ya disponible',
      claim='Ya está abierto.', one='Crea tu cuenta y prueba Godolphy 30 días gratis. Sin tarjeta.',
      img='calendario', alt='Calendario de Godolphy con las citas del día por profesional', cta='Crear mi cuenta', url=SIGNUP,
      more=[('Plan Pro completo', ' durante la prueba.'), ('Al terminar,', ' eliges el plan que te encaje. Sin permanencia.')],
      close='¿Dudas? Responde a este email: lo leo yo.'),
]

def build(e):
    cta = u(e['url'], e['id']); dia = u('https://godolphy.com/dashboard-ia/', e['id']); home = u('https://godolphy.com/', e['id'])
    rows = ''.join(f'<tr><td width="28" valign="top" style="padding:0 0 10px 0;{B}font-size:16px;line-height:24px;color:#631cff;font-weight:700;">&#10003;</td>'
                   f'<td valign="top" style="padding:0 0 10px 0;{B}font-size:16px;line-height:24px;color:#02021e;"><b>{a}</b>{b.format(dia=dia)}</td></tr>' for a, b in e['more'])
    return f'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es"><head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="x-apple-disable-message-reformatting" /><meta name="color-scheme" content="light only" /><meta name="supported-color-schemes" content="light only" />
<title>{H_.escape(e['subject'])}</title>
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@600;800&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet" />
<style type="text/css">
body,table,td,a{{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;}} table,td{{border-collapse:collapse;mso-table-lspace:0;mso-table-rspace:0;}}
img{{border:0;outline:none;text-decoration:none;display:block;-ms-interpolation-mode:bicubic;}} body{{margin:0!important;padding:0!important;width:100%!important;}}
@media screen and (max-width:620px){{.container{{width:100%!important;}} .px{{padding-left:22px!important;padding-right:22px!important;}} .claim{{font-size:40px!important;line-height:44px!important;}}}}
</style>
<!--[if mso]><style type="text/css">table,td,p,a{{font-family:'Segoe UI',Arial,sans-serif!important;}}</style><![endif]-->
</head>
<body style="margin:0;padding:0;background:#f8f7ff;">
<!-- Godolphy · Lista de espera · lanzamiento · {e['id'].upper()} -->
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:#f8f7ff;opacity:0;">{H_.escape(e['pre'])}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f8f7ff;"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#FFFFFF;border-radius:24px;overflow:hidden;">
<tr><td class="px" align="center" bgcolor="#631cff" style="background:#631cff;background-image:linear-gradient(160deg,#9B4FE8 0%,#631cff 70%);padding:36px 40px 0 40px;">
<img src="{LOGO}" width="150" alt="Godolphy" style="width:150px;height:auto;margin:0 auto 30px auto;" />
<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center"><tr><td style="background:#EEFE3A;border-radius:999px;padding:7px 16px;{B}font-size:12px;letter-spacing:1.4px;font-weight:700;color:#02021e;text-transform:uppercase;">{H_.escape(e['pill'])}</td></tr></table>
<p class="claim" style="margin:22px 0 0 0;{H}font-size:52px;line-height:56px;font-weight:800;letter-spacing:-1px;color:#FFFFFF;">{H_.escape(e['claim'])}</p>
<p style="margin:16px auto 0 auto;max-width:460px;{B}font-size:17px;line-height:26px;color:#EFE9FF;">{H_.escape(e['one'])}</p>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" style="margin-top:26px;"><tr><td align="center">
<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{cta}" style="height:54px;v-text-anchor:middle;width:280px;" arcsize="30%" stroke="f" fillcolor="#FFFFFF"><w:anchorlock/><center style="color:#631cff;font-family:'Segoe UI',Arial,sans-serif;font-size:17px;font-weight:bold;">{H_.escape(e['cta'])} &rarr;</center></v:roundrect><![endif]-->
<!--[if !mso]><!-- --><a href="{cta}" style="display:inline-block;padding:17px 30px;background:#FFFFFF;color:#631cff;{B}font-size:17px;line-height:20px;font-weight:700;text-decoration:none;border-radius:16px;">{H_.escape(e['cta'])} &rarr;</a><!--<![endif]-->
</td></tr></table>
<p style="margin:12px 0 0 0;{B}font-size:11px;letter-spacing:1.3px;font-weight:700;color:#E3D9FF;text-transform:uppercase;">30 días gratis · sin tarjeta · sin permanencia</p>
<a href="{cta}" style="text-decoration:none;"><img src="{IMG}{e['img']}.jpg" width="520" alt="{H_.escape(e['alt'])}" style="width:100%;max-width:520px;height:auto;margin:30px auto 0 auto;border-radius:14px 14px 0 0;" /></a>
</td></tr>
<tr><td class="px" style="padding:32px 40px 6px 40px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{rows}</table>
</td></tr>
<tr><td class="px" style="padding:20px 40px 34px 40px;"><p style="margin:0;{B}font-size:16px;line-height:24px;color:#3d3858;">{H_.escape(e['close'])}</p>
<p style="margin:16px 0 0 0;{B}font-size:16px;color:#3d3858;">Un abrazo,<br /><span style="{H}font-size:22px;font-weight:800;color:#631cff;">Neus</span><br /><span style="font-size:13px;color:#7d77a0;">Fundadora de Godolphy</span></p></td></tr>
<tr><td class="px" align="center" style="background:#02021e;padding:26px 40px 28px 40px;">
<img src="{LOGO}" width="110" alt="Godolphy" style="width:110px;height:auto;margin:0 auto;opacity:0.9;" />
<p style="margin:14px 0 0 0;{B}font-size:12px;color:#b9b4d6;"><a href="{home}" style="color:#b9b4d6;text-decoration:none;">godolphy.com</a> &middot; <a href="https://instagram.com/godolphy" style="color:#b9b4d6;text-decoration:none;">@godolphy</a> &middot; <a href="mailto:hello@godolphy.com" style="color:#b9b4d6;text-decoration:none;">hello@godolphy.com</a></p>
<p style="margin:12px 0 0 0;{B}font-size:11px;line-height:17px;color:#8e89ad;">Recibes este email porque te apuntaste a la lista de espera de Godolphy.<br />¿No quieres recibir más? <a href="%UNSUBSCRIBELINK%" style="color:#b9b4d6;text-decoration:underline;">Date de baja aquí.</a></p>
<p style="margin:8px 0 0 0;{B}font-size:11px;color:#8e89ad;">Godolphy &middot; %ACCOUNT_ADDRESS%</p>
</td></tr>
</table></td></tr></table>
</body></html>
'''

def text(e):
    import re
    cta = u(e['url'], e['id']); dia = u('https://godolphy.com/dashboard-ia/', e['id'])
    lines = [e['pre'], '', e['pill'].upper(), '', e['claim'], '', e['one'], '', f"{e['cta']} → {cta}", '30 días gratis · sin tarjeta · sin permanencia', '']
    lines += ['- ' + re.sub('<[^>]+>', '', a + b.format(dia=dia)) + (f' ({dia})' if 'dia' in b else '') for a, b in e['more']]
    lines += ['', e['close'], '', 'Un abrazo,', 'Neus', 'Fundadora de Godolphy', '', 'Recibes este email porque te apuntaste a la lista de espera de Godolphy.',
              '¿No quieres recibir más? Date de baja aquí: %UNSUBSCRIBELINK%', '', 'Godolphy · %ACCOUNT_ADDRESS%']
    return '\n'.join(lines)

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for e in E:
        open(f"{OUT}/{e['id']}.html", 'w').write(build(e)); open(f"{OUT}/{e['id']}.txt", 'w').write(text(e))
        print(e['id'], len(build(e)), len(text(e)))
