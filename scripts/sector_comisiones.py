"""Páginas de sector (nov. 2026):
1. El bloque de domicilio (gx-steps-sec) va justo después del bento («Múltiples … y servicios a domicilio»).
2. Bloque nuevo de comisiones del equipo, después de la sección de equipo («Cada profesional ve su agenda…»).
Idempotente. Uso: python3 scripts/sector_comisiones.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ['peluquerias', 'barberias', 'centro-de-estetica-y-salones', 'salones-de-unas', 'spa-y-masajes', 'lashistas', 'maquilladoras']
NAMES = {'barberias': ('Carlos', 'Javi')}
CHECK = '<svg class="check" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>'


def eur(x):
    return f'{x:,.0f}'.replace(',', '.') + ' €'


def block(key):
    a, b = NAMES.get(key, ('Laura', 'Marta'))
    base_a, pct_a = 3875, 32
    base_b, t1, p1, p2 = 3200, 2000, 25, 35
    com_a = base_a * pct_a / 100
    com_b = t1 * p1 / 100 + (base_b - t1) * p2 / 100
    lis = ''.join(f'<li>{CHECK}{x}</li>' for x in [
        'Tú decides si los extras y el desplazamiento a domicilio generan comisión',
        'Cada profesional ve solo las suyas en «Mis comisiones»; la recepcionista no las ve',
        'Las citas canceladas o no presentadas no generan comisión'])
    rows = (f'<li class="cm-row"><div><b>{a}</b><small>Porcentaje fijo · {pct_a} %</small></div><span>Base {eur(base_a)}</span><strong data-count="{com_a:.0f}" data-suf=" €">0 €</strong></li>'
            f'<li class="cm-row"><div><b>{b}</b><small>Por tramos · {p1} % hasta {eur(t1)}, {p2} % el resto</small></div><span>Base {eur(base_b)}</span><strong data-count="{com_b:.0f}" data-suf=" €">0 €</strong></li>')
    return f'''
<!-- gd-blocks:comisiones (sector_comisiones.py) -->
<section class="gd-sec ex-sec cm-sec">
  <div class="gd-wrap ex-wrap">
    <div class="ex-text">
      <span class="cx-kicker">Comisiones</span>
      <h2>Las comisiones de tu equipo, <span class="it">calculadas solas</span> cada mes</h2>
      <p>Godolphy calcula lo que gana cada profesional según lo cobrado de sus citas completadas, sin IVA y descontando las devoluciones. Con un porcentaje fijo o por tramos, como trabajes tú.</p>
      <ul class="ex-list">{lis}</ul>
      <a class="gd-more" href="/funcionalidades/comisiones/" data-cta="sector-feature">Cómo funcionan las comisiones →</a>
      <p class="cx-foot">Incluidas en los planes Pro y Max, y en la prueba gratuita.</p>
    </div>
    <div class="gd-card ex-card" aria-hidden="true">
      <div class="ex-head"><b>Comisiones · noviembre</b><span>Ventas → Comisiones</span></div>
      <ul class="cm-rows">{rows}</ul>
      <p class="cx-ex">Ejemplo.</p>
    </div>
  </div>
</section>
'''


CSS = '''
/* Comisiones (sector_comisiones.py) */
.cm-sec{background:#f8f7ff;}.cm-sec .ex-card{background:#fff;}
.cm-rows{list-style:none;margin:8px 0 0;padding:0;display:grid;gap:10px;}
.cm-row{display:grid;grid-template-columns:1fr auto auto;gap:14px;align-items:center;border:1px solid #ece6ff;border-radius:16px;padding:14px 16px;}
.cm-row b{display:block;font-size:15.5px;color:#02021e;}.cm-row small{font-size:12.5px;color:rgba(2,2,30,.5);}
.cm-row span{font-size:13px;color:rgba(2,2,30,.55);white-space:nowrap;}
.cm-row strong{font-family:'Gabarito',sans-serif;font-size:24px;color:#631cff;white-space:nowrap;}
@media(max-width:860px){.cm-row{grid-template-columns:1fr auto;}.cm-row span{grid-column:1;grid-row:2;}.cm-row strong{grid-row:1 / span 2;grid-column:2;}}
'''
css = ROOT / 'assets/gx-motion.css'
if 'cm-sec' not in css.read_text():
    css.write_text(css.read_text() + CSS)


def section_at(s, i):
    a = s.rfind('<section', 0, i)
    return a, s.find('</section>', i) + len('</section>')


for key in PAGES:
    p = ROOT / f'sectores/software-para-{key}/index.html'
    s = p.read_text()
    # 1. domicilio después del bento
    ds = s.find('<section class="gx-steps-sec">')
    de = s.find('</section>', ds) + len('</section>')
    dom = s[ds:de]
    s = s[:ds] + s[de:]
    b = s.find('<section class="gx-bento-sec">')
    be = s.find('</section>', b) + len('</section>')
    s = s[:be] + '\n\n' + dom + s[be:]
    # 2. comisiones después de la sección de equipo
    if 'gd-blocks:comisiones' not in s:
        m = re.search(r'Cada (?:profesional|[a-záéíóúñ ]+) ve su agenda', s)
        assert m, key
        _, te = section_at(s, m.start())
        s = s[:te] + block(key) + s[te:]
    p.write_text(s)
    order = [x for x in ('gx-bento-sec', 'gx-steps-sec', 'gd-blocks:comisiones') if x in s]
    print(key, [s.find(x) for x in order])
