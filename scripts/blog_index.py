#!/usr/bin/env python3
"""Añade al listado del blog (blog/index.html) los artículos publicados en la raíz
(slug.html) que todavía no aparecen, y ordena las tarjetas por fecha (más reciente primero).
Lo ejecuta el workflow de publicación programada después de publicar."""
import re, glob, os, html, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'blog', 'index.html')
MESES = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
GRAD = 'linear-gradient(160deg,#9B4FE8 0%,#7835C3 30%,#631cff 65%,#3a0aaa 100%)'
SKIP = {'index.html'}

def parse_date(txt):
    m = re.search(r'(\d{1,2}) de ([a-záéíóú]+) de (\d{4})', txt)
    if not m or m.group(2) not in MESES: return (0, 0, 0)
    return (int(m.group(3)), MESES.index(m.group(2)) + 1, int(m.group(1)))

def card_for(path):
    s = open(path, encoding='utf-8').read()
    if '<div class="post-content">' not in s: return None
    slug = os.path.basename(path)[:-5]
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    if not h1: return None
    title = re.sub(r'<[^>]+>', '', h1.group(1)).strip()
    cat = re.search(r'<span style="font-size:13px;color:rgba\(2,2,30,\.4\);">([^<]+)</span>\s*</div>', s)
    cat = cat.group(1).strip() if cat else 'Consejos de negocio'
    date = re.search(r'<span style="font-size:14px;color:rgba\(2,2,30,\.45\);">([^<]*\d{4})</span>', s)
    date = date.group(1).strip() if date else ''
    return f'''    <a href="/{slug}/" class="post-card">
      <div style="aspect-ratio:16/9;background:{GRAD};display:flex;align-items:center;justify-content:center;"><img src="/wp-images/logo-blanco.png" alt="" style="width:auto;height:36px;aspect-ratio:auto;object-fit:contain;" loading="lazy" /></div>
      <div style="padding:24px;">
        <span style="font-size:12px;font-weight:600;color:#631cff;text-transform:uppercase;letter-spacing:.06em;">{cat}</span>
        <h2 class="font-gabarito" style="font-size:19px;font-weight:700;color:#02021e;margin:8px 0 10px;line-height:1.25;">{title}</h2>
        <p style="font-size:14px;color:rgba(2,2,30,.45);margin:0;">{date}</p>
      </div>
    </a>'''

def main():
    s = open(INDEX, encoding='utf-8').read()
    start_tag = '<div class="blog-grid"'
    gs = s.index(start_tag); gs = s.index('>', gs) + 1
    cards = re.findall(r'[ \t]*<a href="[^"]+" class="post-card">.*?</a>', s[gs:], re.S)
    ge = s.index(cards[-1], gs) + len(cards[-1])
    present = set(re.findall(r'<a href="(/[^"]+/)" class="post-card">', s))
    added = []
    for path in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        name = os.path.basename(path)
        if name in SKIP or name.startswith('godolphy-'): continue
        if f'/{name[:-5]}/' in present: continue
        c = card_for(path)
        if c: cards.append(c); added.append(name)
    def key(c):
        p = re.search(r'<p style="font-size:14px;color:rgba\(2,2,30,\.45\);margin:0;">([^<]*)</p>', c)
        return parse_date(p.group(1) if p else '')
    cards.sort(key=key, reverse=True)
    s = s[:gs] + '\n\n' + '\n\n'.join(c.rstrip() for c in cards) + '\n\n' + s[ge:]
    open(INDEX, 'w', encoding='utf-8').write(s)
    print('added:', added)

if __name__ == '__main__':
    main()
