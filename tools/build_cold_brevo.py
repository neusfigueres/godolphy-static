"""Email frío (Brevo) con test A/B de claim. Mismo branding que los correos de lanzamiento.
Merge tags de Brevo: {{ unsubscribe }} (obligatorio) y {{ mirror }}."""
import os, importlib.util
here = os.path.dirname(__file__)
spec = importlib.util.spec_from_file_location('w', os.path.join(here, 'build_waitlist_e2_e3.py')); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
IMG, LOGO, H, B = w.IMG, w.LOGO, w.H, w.B
OUT = '/home/claude/emails-out/brevo'

V = {
 'a': dict(subject='Una nueva era para tu centro de estética', claim='Una nueva era para los centros de estética, con IA.'),
 'b': dict(subject='El consultor financiero que tu salón nunca tuvo', claim='El consultor financiero que tu salón nunca tuvo.'),
}
PRE = 'Gratis: sube tu agenda y la IA te dice dónde pierdes dinero.'
ONE = 'Sube la exportación de tu agenda y la IA te dice cuánto ganas de verdad, qué clientas no han vuelto y qué servicios no te salen a cuenta.'
FEATS = ['Reservas online con tu marca, sin comisiones.', 'Recordatorio por WhatsApp el día antes de la cita.', 'Cobros y tarjetas regalo.', 'Análisis de tu negocio con IA, cada mes.']

def U(v): return f'utm_source=brevo&utm_medium=email&utm_campaign=frio-lanzamiento&utm_content={v}'

def build(v):
    d = V[v]; u = U(v); dia = f'https://godolphy.com/dashboard-ia/?{u}'; home = f'https://godolphy.com/?{u}'
    rows = ''.join(f'<tr><td width="28" valign="top" style="padding:0 0 10px 0;{B}font-size:16px;line-height:24px;color:#631cff;font-weight:700;">&#10003;</td>'
                   f'<td valign="top" style="padding:0 0 10px 0;{B}font-size:16px;line-height:24px;color:#02021e;">{f}</td></tr>' for f in FEATS)
    html = f'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es"><head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="x-apple-disable-message-reformatting" /><meta name="color-scheme" content="light only" /><meta name="supported-color-schemes" content="light only" />
<title>{d['subject']}</title>
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@600;800&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet" />
<style type="text/css">
body,table,td,a{{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;}} table,td{{border-collapse:collapse;mso-table-lspace:0;mso-table-rspace:0;}}
img{{border:0;outline:none;text-decoration:none;display:block;-ms-interpolation-mode:bicubic;}} body{{margin:0!important;padding:0!important;width:100%!important;}}
@media screen and (max-width:620px){{.container{{width:100%!important;}} .px{{padding-left:22px!important;padding-right:22px!important;}} .claim{{font-size:34px!important;line-height:38px!important;}}}}
</style>
<!--[if mso]><style type="text/css">table,td,p,a{{font-family:'Segoe UI',Arial,sans-serif!important;}}</style><![endif]-->
</head>
<body style="margin:0;padding:0;background:#f8f7ff;">
<!-- Godolphy · Brevo · frío lanzamiento · variante {v.upper()} -->
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:#f8f7ff;opacity:0;">{PRE}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f8f7ff;"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#FFFFFF;border-radius:24px;overflow:hidden;">
<tr><td class="px" align="center" bgcolor="#631cff" style="background:#631cff;background-image:linear-gradient(160deg,#9B4FE8 0%,#631cff 70%);padding:36px 40px 0 40px;">
<img src="{LOGO}" width="150" alt="Godolphy" style="width:150px;height:auto;margin:0 auto 30px auto;" />
<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center"><tr><td style="background:#EEFE3A;border-radius:999px;padding:7px 16px;{B}font-size:12px;letter-spacing:1.4px;font-weight:700;color:#02021e;text-transform:uppercase;">Dashboard IA · gratis</td></tr></table>
<p class="claim" style="margin:22px 0 0 0;{H}font-size:44px;line-height:48px;font-weight:800;letter-spacing:-0.9px;color:#FFFFFF;">{d['claim']}</p>
<p style="margin:16px auto 0 auto;max-width:470px;{B}font-size:17px;line-height:26px;color:#EFE9FF;">{ONE}</p>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" style="margin-top:26px;"><tr><td align="center">
<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{dia}" style="height:54px;v-text-anchor:middle;width:300px;" arcsize="30%" stroke="f" fillcolor="#FFFFFF"><w:anchorlock/><center style="color:#631cff;font-family:'Segoe UI',Arial,sans-serif;font-size:17px;font-weight:bold;">Analizar mi salón gratis &rarr;</center></v:roundrect><![endif]-->
<!--[if !mso]><!-- --><a href="{dia}" style="display:inline-block;padding:17px 30px;background:#FFFFFF;color:#631cff;{B}font-size:17px;line-height:20px;font-weight:700;text-decoration:none;border-radius:16px;">Analizar mi salón gratis &rarr;</a><!--<![endif]-->
</td></tr></table>
<p style="margin:12px 0 0 0;{B}font-size:11px;letter-spacing:1.3px;font-weight:700;color:#E3D9FF;text-transform:uppercase;">Gratis · sin tarjeta · 30 segundos</p>
<a href="{dia}" style="text-decoration:none;"><img src="{IMG}resumen.jpg" width="520" alt="Dashboard IA de Godolphy" style="width:100%;max-width:520px;height:auto;margin:30px auto 0 auto;border-radius:14px 14px 0 0;" /></a>
</td></tr>
<tr><td class="px" style="padding:30px 40px 8px 40px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f3efff;border-radius:20px;"><tr><td style="padding:26px 26px 18px 26px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td style="background:#631cff;border-radius:999px;padding:6px 14px;{B}font-size:11px;letter-spacing:1.3px;font-weight:700;color:#FFFFFF;text-transform:uppercase;">Desde el 26 de octubre</td></tr></table>
<p style="margin:14px 0 16px 0;{H}font-size:24px;line-height:28px;font-weight:800;color:#02021e;">Godolphy, el programa de reservas con IA para centros de estética.</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{rows}</table>
<p style="margin:6px 0 0 0;{B}font-size:15px;line-height:22px;color:#3d3858;"><b>30 días gratis, sin tarjeta.</b> Todo en <a href="{home}" style="color:#631cff;font-weight:700;text-decoration:underline;">godolphy.com</a></p>
</td></tr></table>
</td></tr>
<tr><td class="px" style="padding:26px 40px 34px 40px;"><p style="margin:0;{B}font-size:16px;line-height:24px;color:#3d3858;">Si te encaja, responde a este email y te lo enseño.</p>
<p style="margin:16px 0 0 0;{B}font-size:16px;color:#3d3858;">Un saludo,<br /><span style="{H}font-size:22px;font-weight:800;color:#631cff;">Neus</span><br /><span style="font-size:13px;color:#7d77a0;">Fundadora de Godolphy</span></p></td></tr>
<tr><td class="px" align="center" style="background:#02021e;padding:26px 40px 28px 40px;">
<img src="{LOGO}" width="110" alt="Godolphy" style="width:110px;height:auto;margin:0 auto;opacity:0.9;" />
<p style="margin:14px 0 0 0;{B}font-size:12px;color:#b9b4d6;"><a href="{home}" style="color:#b9b4d6;text-decoration:none;">godolphy.com</a> &middot; <a href="https://instagram.com/godolphy" style="color:#b9b4d6;text-decoration:none;">@godolphy</a></p>
<p style="margin:12px 0 0 0;{B}font-size:11px;line-height:17px;color:#8e89ad;">¿No te interesa? <a href="{{{{ unsubscribe }}}}" style="color:#b9b4d6;text-decoration:underline;">Date de baja aquí</a> y no te volveremos a escribir.</p>
<p style="margin:8px 0 0 0;{B}font-size:11px;color:#8e89ad;">Godolphy Software LLC</p>
</td></tr>
</table></td></tr></table>
</body></html>
'''
    return html

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for v in V:
        h = build(v); open(f'{OUT}/frio_{v}.html', 'w').write(h); print(v, len(h), '{{ unsubscribe }}' in h)
