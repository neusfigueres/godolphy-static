"""Separa «Extras» y «Tiempos de exposición» en las páginas de sector (nov. 2026).
- La sección de extras pasa a hablar solo de extras (quita la línea de tiempos de exposición).
- Donde aplica (peluquerías, estética, lashistas), añade un bloque propio de tiempos de exposición con un ejemplo animado.
Idempotente. Uso: python3 scripts/sector_exposicion.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXTRAS_H2 = 'Extras opcionales u obligatorios: <span class="it">la agenda suma el tiempo y el precio</span> sola'


def it(t):
    return f'<span class="it">{t}</span>'


SECT = {
    'peluquerias': dict(
        h2=f'Tiempos de exposición: mientras actúa el tinte, {it("otra cita")}',
        p='Divides cada servicio en tramos: trabajo, exposición y trabajo. Mientras sube el color, la agenda te deja dar otra cita a la misma profesional, en el booking, en el panel y en el calendario.',
        main=('Tinte', 20, 35, 30), extra=('Corte', 30), servicios='tintes, mechas o permanentes'),
    'centro-de-estetica-y-salones': dict(
        h2=f'Tiempos de exposición: mientras actúa el lifting, {it("otra cita")}',
        p='Divides cada tratamiento en tramos: trabajo, exposición y trabajo. Mientras actúa el lifting o el laminado, la agenda te deja dar otra cita a la misma esteticista, en el booking, en el panel y en el calendario.',
        main=('Laminado de cejas', 15, 25, 15), extra=('Diseño de cejas', 20), servicios='lifting de pestañas o laminado de cejas'),
    'lashistas': dict(
        h2=f'Tiempos de exposición: mientras actúa el lifting, {it("otra cita")}',
        p='Divides cada servicio en tramos: trabajo, exposición y trabajo. Mientras actúa el lifting o el tinte de pestañas, la agenda te deja dar otra cita a la misma lashista, en el booking, en el panel y en el calendario.',
        main=('Lifting de pestañas', 15, 30, 15), extra=('Diseño de cejas', 20), servicios='lifting o tinte de pestañas'),
}

CHECK = '<svg class="check" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>'


def block(c):
    n, t1, ex, t2 = c['main']
    en, emin = c['extra']
    tot = t1 + ex + t2
    pct = lambda m: f'{m / tot * 100:.2f}%'
    lis = ''.join(f'<li>{CHECK}{x}</li>' for x in [
        'La IA propone los tiempos de tus servicios y tú los confirmas',
        'Nunca se pone una cita encima de un tramo de trabajo, solo dentro de la exposición',
        'Funciona en las citas en el local; los domicilios no se parten'])
    return f'''
<!-- gd-blocks:exposicion (sector_exposicion.py) -->
<section class="gd-sec ex-sec">
  <div class="gd-wrap ex-wrap">
    <div class="ex-text">
      <span class="cx-kicker">Tiempos de exposición</span>
      <h2>{c['h2']}</h2>
      <p>{c['p']}</p>
      <ul class="ex-list">{lis}</ul>
      <a class="gd-more" href="/funcionalidades/tiempos-de-exposicion/" data-cta="sector-feature">Cómo funcionan los tiempos de exposición →</a>
    </div>
    <div class="gd-card ex-card" aria-hidden="true">
      <div class="ex-head"><b>Agenda · Marta</b><span>{tot} min</span></div>
      <div class="ex-track">
        <i class="ex-seg ex-work" style="width:{pct(t1)}"><b>{n}</b><small>{t1} min</small></i>
        <i class="ex-seg ex-wait" style="width:{pct(ex)}"><b>Exposición</b><small>{ex} min</small></i>
        <i class="ex-seg ex-work" style="width:{pct(t2)}"><b>{n}</b><small>{t2} min</small></i>
      </div>
      <div class="ex-track ex-track2">
        <i class="ex-fit" style="margin-left:{pct(t1)};width:{pct(min(emin, ex))}"><b>{en}</b><small>{emin} min</small></i>
      </div>
      <p class="ex-note">Mientras actúa: <b>{en}</b> en el mismo hueco, con la misma profesional.</p>
      <p class="cx-ex">Ejemplo.</p>
    </div>
  </div>
</section>
'''


CSS = '''
/* Tiempos de exposición (sector_exposicion.py) */
.ex-sec{background:#fff;}
.ex-wrap{display:grid;grid-template-columns:1fr 1.05fr;gap:56px;align-items:center;}
.ex-text h2{font-family:'Gabarito',sans-serif;font-size:40px;line-height:1.12;font-weight:700;color:#02021e;margin:0 0 18px;}
.ex-text>p{font-size:17px;line-height:1.65;color:rgba(2,2,30,.68);margin:0 0 22px;}
.ex-list{list-style:none;margin:0;padding:0;display:grid;gap:12px;}
.ex-list li{display:flex;gap:12px;align-items:flex-start;font-size:16px;color:rgba(2,2,30,.82);}
.ex-list .check{width:20px;height:20px;flex:0 0 auto;fill:#631cff;margin-top:2px;}
.ex-card{background:#f8f7ff;padding:24px;box-shadow:0 24px 50px rgba(40,10,110,.10);}
.ex-head{display:flex;justify-content:space-between;align-items:baseline;font-size:14px;color:rgba(2,2,30,.55);margin-bottom:6px;}
.ex-head b{font-family:'Gabarito',sans-serif;font-size:20px;color:#02021e;}
.ex-track{display:flex;gap:4px;height:74px;}
.ex-seg,.ex-fit{display:flex;flex-direction:column;justify-content:center;border-radius:12px;padding:0 10px;font-style:normal;overflow:hidden;white-space:nowrap;min-width:0;}
.ex-seg b,.ex-fit b{font-size:13px;}.ex-seg small,.ex-fit small{font-size:11.5px;opacity:.8;}
.ex-work{background:linear-gradient(160deg,#9B4FE8,#631cff);color:#fff;}
.ex-wait{background:repeating-linear-gradient(135deg,#ece6ff 0 8px,#f8f7ff 8px 16px);border:1.5px dashed #b9a6ff;color:#631cff;}
.ex-track2{margin-top:10px;height:64px;}
.ex-fit{background:#EEFE3A;color:#02021e;box-shadow:0 10px 24px rgba(99,28,255,.18);opacity:0;transform:translateY(-26px);transition:opacity .5s ease .5s,transform .7s cubic-bezier(.2,.8,.2,1) .5s;}
.gd-on .ex-fit{opacity:1;transform:none;}
.ex-note{margin:16px 0 0;font-size:14.5px;color:rgba(2,2,30,.7);}
@media(max-width:860px){.ex-wrap{grid-template-columns:1fr;gap:32px;}.ex-text h2{font-size:30px;}.ex-card{padding:16px;}.ex-seg,.ex-fit{padding:0 6px;}.ex-seg b,.ex-fit b{font-size:11.5px;}}
@media(prefers-reduced-motion:reduce){.ex-fit{transition:none!important;opacity:1;transform:none;}}
'''

css = ROOT / 'assets/gx-motion.css'
if 'ex-sec' not in css.read_text():
    css.write_text(css.read_text() + CSS)

for p in sorted((ROOT / 'sectores').glob('software-para-*/index.html')):
    key = p.parent.name.replace('software-para-', '')
    s = p.read_text()
    # extras: solo extras
    m = re.search(r'(<h2[^>]*>)Extras (?:y tiempos de exposición|al reservar|opcionales u obligatorios):.*?(</h2>)', s, re.S)
    if not m:
        print(key, 'sin extras'); continue
    s = s[:m.start()] + m.group(1) + EXTRAS_H2 + m.group(2) + s[m.end():]
    s = re.sub(r'\s*<li[^>]*>(?:(?!</li>).)*?<strong>Tiempos de exposición</strong>.*?</li>', '', s, count=1, flags=re.S)
    if key in SECT and 'gd-blocks:exposicion' not in s:
        i = s.find(EXTRAS_H2)
        e = s.find('</section>', i) + len('</section>')
        assert i > 0
        s = s[:e] + block(SECT[key]) + s[e:]
    p.write_text(s)
    print(key, s.count(EXTRAS_H2), 'gd-blocks:exposicion' in s)
