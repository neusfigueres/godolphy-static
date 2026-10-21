"""Email frío 3 (Brevo): Verifactu (meme). Mismo branding que frio_a/b.
Merge tag de Brevo obligatorio: {{ unsubscribe }}."""
import os, importlib.util
here = os.path.dirname(__file__)
spec = importlib.util.spec_from_file_location('w', os.path.join(here, 'build_waitlist_e2_e3.py')); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
LOGO, H, B = w.LOGO, w.H, w.B
OUT = '/home/claude/emails-out/brevo'
IMG = 'https://godolphy.com/img/email/frio/verifactu-meme.jpg'
SUBJECT = 'Verifactu te vigila...'
PRE = 'Con Godolphy, cobras la cita y el tique ya está en Hacienda.'
CLAIM = 'Cobra la cita y el tique ya está en Hacienda.'
ONE = 'Cada cobro se envía solo a Hacienda, con su tique y el QR VERI*FACTU. Tú no tienes que hacer nada.'
FEATS = ['Rectificativa automática si devuelves un cobro.', 'Tique por email a tu clienta.', 'Reservas online y recordatorio por WhatsApp.']
U = 'utm_source=brevo&utm_medium=email&utm_campaign=frio-verifactu&utm_content=c1'
LINK = f'https://godolphy.com/ayuda/verifactu/?{U}'
HOME = f'https://godolphy.com/?{U}'

rows = ''.join(f'<tr><td width="28" valign="top" style="padding:0 0 10px 0;{B}font-size:16px;line-height:24px;color:#631cff;font-weight:700;">&#10003;</td>'
               f'<td valign="top" style="padding:0 0 10px 0;{B}font-size:16px;line-height:24px;color:#02021e;">{f}</td></tr>' for f in FEATS)
btn = lambda bg, fg: (f'<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{LINK}" style="height:54px;v-text-anchor:middle;width:280px;" arcsize="30%" stroke="f" fillcolor="{bg}"><w:anchorlock/><center style="color:{fg};font-family:\'Segoe UI\',Arial,sans-serif;font-size:17px;font-weight:bold;">Ver cómo funciona &rarr;</center></v:roundrect><![endif]-->'
                      f'<!--[if !mso]><!-- --><a href="{LINK}" style="display:inline-block;padding:17px 30px;background:{bg};color:{fg};{B}font-size:17px;line-height:20px;font-weight:700;text-decoration:none;border-radius:16px;">Ver cómo funciona &rarr;</a><!--<![endif]-->')

html = f'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es"><head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="x-apple-disable-message-reformatting" /><meta name="color-scheme" content="light only" /><meta name="supported-color-schemes" content="light only" />
<title>{SUBJECT}</title>
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@600;800&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet" />
<style type="text/css">
body,table,td,a{{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;}} table,td{{border-collapse:collapse;mso-table-lspace:0;mso-table-rspace:0;}}
img{{border:0;outline:none;text-decoration:none;display:block;-ms-interpolation-mode:bicubic;}} body{{margin:0!important;padding:0!important;width:100%!important;}}
@media screen and (max-width:620px){{.container{{width:100%!important;}} .px{{padding-left:22px!important;padding-right:22px!important;}} .claim{{font-size:30px!important;line-height:34px!important;}}}}
</style>
<!--[if mso]><style type="text/css">table,td,p,a{{font-family:'Segoe UI',Arial,sans-serif!important;}}</style><![endif]-->
</head>
<body style="margin:0;padding:0;background:#f8f7ff;">
<!-- Godolphy · Brevo · frío 3 · verifactu -->
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:#f8f7ff;opacity:0;">{PRE}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f8f7ff;"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#FFFFFF;border-radius:24px;overflow:hidden;">
<tr><td class="px" align="center" bgcolor="#631cff" style="background:#631cff;background-image:linear-gradient(160deg,#9B4FE8 0%,#631cff 70%);padding:36px 40px 34px 40px;">
<img src="{LOGO}" width="150" alt="Godolphy" style="width:150px;height:auto;margin:0 auto 30px auto;" />
<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center"><tr><td style="background:#EEFE3A;border-radius:999px;padding:7px 16px;{B}font-size:12px;letter-spacing:1.4px;font-weight:700;color:#02021e;text-transform:uppercase;">Verifactu</td></tr></table>
<p class="claim" style="margin:22px 0 0 0;{H}font-size:44px;line-height:48px;font-weight:800;letter-spacing:-0.8px;color:#FFFFFF;">{CLAIM}</p>
<p style="margin:16px auto 0 auto;max-width:470px;{B}font-size:17px;line-height:26px;color:#EFE9FF;">{ONE}</p>
<a href="{LINK}" style="text-decoration:none;"><img src="{IMG}" width="520" alt="Meme: cuando Verifactu entra en tu cabina… y tú ya lo tienes con Godolphy" style="width:100%;max-width:520px;height:auto;margin:28px auto 4px auto;border-radius:16px;" /></a>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" style="margin-top:22px;"><tr><td align="center">{btn('#FFFFFF', '#631cff')}</td></tr></table>
</td></tr>
<tr><td class="px" style="padding:30px 40px 8px 40px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f3efff;border-radius:20px;"><tr><td style="padding:26px 26px 18px 26px;">
<p style="margin:0 0 16px 0;{H}font-size:24px;line-height:28px;font-weight:800;color:#02021e;">Y además, todo lo de tu salón en un sitio.</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{rows}</table>
<p style="margin:6px 0 0 0;{B}font-size:15px;line-height:22px;color:#3d3858;"><b>30 días gratis, sin tarjeta.</b> Verifactu se activa con tu plan. Todo en <a href="{HOME}" style="color:#631cff;font-weight:700;text-decoration:underline;">godolphy.com</a></p>
</td></tr></table>
</td></tr>
<tr><td class="px" style="padding:26px 40px 34px 40px;"><p style="margin:0;{B}font-size:16px;line-height:24px;color:#3d3858;">Si te encaja, responde a este email y te lo enseño.</p>
<p style="margin:16px 0 0 0;{B}font-size:16px;color:#3d3858;">Un saludo,<br /><span style="{H}font-size:22px;font-weight:800;color:#631cff;">Neus</span><br /><span style="font-size:13px;color:#7d77a0;">Fundadora de Godolphy</span></p></td></tr>
<tr><td class="px" align="center" style="background:#02021e;padding:26px 40px 28px 40px;">
<img src="{LOGO}" width="110" alt="Godolphy" style="width:110px;height:auto;margin:0 auto;opacity:0.9;" />
<p style="margin:14px 0 0 0;{B}font-size:12px;color:#b9b4d6;"><a href="{HOME}" style="color:#b9b4d6;text-decoration:none;">godolphy.com</a> &middot; <a href="https://instagram.com/godolphy" style="color:#b9b4d6;text-decoration:none;">@godolphy</a></p>
<p style="margin:12px 0 0 0;{B}font-size:11px;line-height:17px;color:#8e89ad;">¿No te interesa? <a href="{{{{ unsubscribe }}}}" style="color:#b9b4d6;text-decoration:underline;">Date de baja aquí</a> y no te volveremos a escribir.</p>
<p style="margin:8px 0 0 0;{B}font-size:11px;color:#8e89ad;">Godolphy Software LLC</p>
</td></tr>
</table></td></tr></table>
</body></html>
'''

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    open(f'{OUT}/frio_verifactu.html', 'w').write(html); print(len(html), '{{ unsubscribe }}' in html)
