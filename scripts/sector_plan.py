"""Bloque «Plan financiero 2027» al final de las páginas de sector (antes de las preguntas frecuentes),
enlazado a la landing del plan. Sin «gratis para siempre» (freemium aún no publicado).
Idempotente. Uso: python3 scripts/sector_plan.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LP = {'peluquerias': '/lp/plan-financiero-2027-peluquerias/'}
PAGES = ['peluquerias', 'barberias', 'centro-de-estetica-y-salones', 'salones-de-unas', 'spa-y-masajes', 'lashistas', 'maquilladoras']
CHECK = '<svg class="check" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>'
# plan y real (en miles de €) de enero a junio; el real va por delante desde marzo
MONTHS = [('Ene', 9.0, 9.4), ('Feb', 9.5, 9.2), ('Mar', 10.5, 11.0), ('Abr', 11.0, 11.6), ('May', 12.0, 12.9), ('Jun', 12.5, None)]


def block(key):
    lp = LP.get(key, '/lp/plan-financiero-2027/')
    top = 14.0
    bars = ''
    for m, plan, real in MONTHS:
        r = f'<span class="pf-real" data-h="{real / top * 100:.0f}"></span>' if real else '<span class="pf-real pf-empty"></span>'
        bars += f'<div class="pf-col"><div class="pf-pair"><span class="pf-plan" data-h="{plan / top * 100:.0f}"></span>{r}</div><i>{m}</i></div>'
    lis = ''.join(f'<li>{CHECK}{x}</li>' for x in [
        'Parte de tus citas y tus gastos; si empiezas, de unos números de partida',
        'Tú eliges cuánto quieres crecer y lo ajustas mes a mes cuando quieras',
        'Cada mes ves cómo vas, real contra plan, y la IA te avisa si te quedas por debajo'])
    return f'''
<!-- gd-blocks:plan (sector_plan.py) -->
<section class="gd-sec ex-sec pf-sec">
  <div class="gd-wrap ex-wrap">
    <div class="ex-text">
      <span class="cx-kicker">Plan financiero 2027</span>
      <h2>¿Cuánto quieres facturar en 2027? Hazte tu <span class="it">plan financiero</span> con tus números reales</h2>
      <p>Un plan financiero es saber, mes a mes, cuánto tienes que facturar para llegar a tu objetivo y cuánto puedes gastar. Godolphy te lo prepara con tus datos y luego te dice cada mes si vas bien.</p>
      <ul class="ex-list">{lis}</ul>
      <div class="gd-cta2"><a class="gd-btn2" href="{lp}" data-cta="sector-plan">Haz tu plan financiero 2027 gratis →</a><a class="gd-more" href="{lp}" data-cta="sector-plan-more">Qué es y cómo funciona →</a></div>
    </div>
    <div class="gd-card ex-card pf-card" aria-hidden="true">
      <div class="ex-head"><b>Plan 2027 · real vs plan</b><span>miles de €</span></div>
      <div class="pf-chart">{bars}</div>
      <div class="pf-leg"><span><i class="pf-plan"></i>Plan</span><span><i class="pf-real"></i>Real</span></div>
      <div class="pf-note"><b>Mayo: +7 % sobre el plan</b><small>Vas por delante de tu objetivo.</small></div>
      <p class="cx-ex">Ejemplo.</p>
    </div>
  </div>
</section>
'''


CSS = '''
/* Plan financiero (sector_plan.py) */
.pf-sec{background:#fff;}
.pf-chart{display:flex;align-items:flex-end;gap:12px;height:170px;margin-top:14px;}
.pf-col{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;height:100%;justify-content:flex-end;}
.pf-col i{font-style:normal;font-size:11.5px;color:rgba(2,2,30,.5);}
.pf-pair{display:flex;align-items:flex-end;gap:4px;height:100%;width:100%;justify-content:center;}
.pf-pair span{display:block;width:42%;max-width:18px;height:6%;border-radius:6px 6px 3px 3px;transition:height .9s cubic-bezier(.2,.8,.2,1);}
.pf-plan{background:#e6dcff;}.pf-real{background:linear-gradient(180deg,#9B4FE8,#631cff);}
.pf-pair .pf-empty{background:none;border:1.5px dashed #d6c9ff;height:20%!important;}
.pf-leg{display:flex;gap:16px;margin-top:12px;font-size:12.5px;color:rgba(2,2,30,.6);}
.pf-leg span{display:flex;align-items:center;gap:6px;}.pf-leg i{display:inline-block;width:12px;height:12px;border-radius:3px;}
.pf-note{margin-top:14px;background:#f3fbe9;border:1px solid #d7efbf;border-radius:14px;padding:12px 14px;}
.pf-note b{display:block;color:#1b7a3d;font-size:15px;}.pf-note small{font-size:13px;color:rgba(2,2,30,.6);}
'''
css = ROOT / 'assets/gx-motion.css'
if 'pf-sec' not in css.read_text():
    css.write_text(css.read_text() + CSS)

for key in PAGES:
    p = ROOT / f'sectores/software-para-{key}/index.html'
    s = p.read_text()
    if 'gd-blocks:plan' in s:
        continue
    i = s.find('Lo que te preguntas ')
    k = s.rfind('<section', 0, i)
    assert k > 0, key
    s = s[:k] + block(key) + '\n' + s[k:]
    p.write_text(s)
    print('ok', key)
