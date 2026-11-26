"""Notificaciones de la cabecera de sector: a las 3 operativas se suman 3 de negocio (cliente que no vuelve,
precio a revisar, plan financiero), intercaladas. Idempotente. Uso: python3 scripts/sector_notifs.py"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from sector_blocks import recomendado, eur  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAGES = {  # cliente, recupéral(a/o), servicio que pierde dinero, su coste, semanas sin venir
    'peluquerias': ('Marta', 'a', 'Lavar y peinar', 13.20, 9),
    'barberias': ('Javi', 'o', 'Arreglo de barba', 7.10, 7),
    'centro-de-estetica-y-salones': ('Elena', 'a', 'Depilación labio', 5.30, 12),
    'salones-de-unas': ('Paula', 'a', 'Decoración por uña', 2.79, 6),
    'spa-y-masajes': ('Pablo', 'o', 'Ritual de pies', 16.20, 10),
    'lashistas': ('Sara', 'a', 'Retirada de extensiones', 9.20, 6),
    'maquilladoras': ('Clara', 'a', 'Retoque de maquillaje', 13.40, 14),
}
for k, (name, g, serv, coste, sem) in PAGES.items():
    p = ROOT / f'sectores/software-para-{k}/index.html'
    s = p.read_text()
    m = re.search(r'<div class="hero-notifs" aria-hidden="true">((?:<div class="hn">.*?</small></div>)+)</div>', s, re.S)
    cards = re.findall(r'<div class="hn">.*?</small></div>', m.group(1), re.S)
    if len(cards) > 3:
        continue
    tpl = cards[0]

    def mk(t, x):
        c = re.sub(r'<b>.*?</b>', f'<b>{t}</b>', tpl, count=1)
        return re.sub(r'<span>.*?</span>', f'<span>{x}</span>', c, count=1)
    biz = [mk('Cliente a punto de no volver', f'{name} lleva {sem} semanas sin venir · Recupéral{g}'),
           mk('Revisa este precio', f'{serv} te hace perder dinero · Aplicar {eur(recomendado(coste))}'),
           mk('Plan financiero', 'Noviembre va un 8 % por encima de tu objetivo')]
    out = [cards[0], biz[0], cards[1], biz[1], cards[2], biz[2]]
    p.write_text(s[:m.start(1)] + ''.join(out) + s[m.end(1):])
    print('ok', k)
