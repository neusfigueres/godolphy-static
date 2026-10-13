#!/usr/bin/env python3
"""Pone una imagen de cabecera a un artículo del blog.

Uso: python3 scripts/set_article_image.py <ruta-articulo.html> <imagen-origen> <alt>

- Convierte la imagen a JPG (1600 px de ancho, calidad 82) en images/blog/<slug>.jpg
- La inserta antes de <div class="post-content">
- Añade og:image, twitter:image y "image" en el schema Article
"""
import json, os, re, sys
from PIL import Image

art, src, alt = sys.argv[1], sys.argv[2], sys.argv[3]
slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', os.path.basename(art)[:-5])
if slug == 'index':
    slug = os.path.basename(os.path.dirname(art))
out = f'images/blog/{slug}.jpg'
im = Image.open(src).convert('RGB')
if im.width > 1600:
    im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
os.makedirs('images/blog', exist_ok=True)
im.save(out, 'JPEG', quality=82, optimize=True, progressive=True)
url = f'https://www.godolphy.com/{out}'

s = open(art, encoding='utf-8').read()
s = re.sub(r'\s*<img class="post-hero"[^>]*>', '', s)
tag = (f'  <img class="post-hero" src="/{out}" alt="{alt}" width="{im.width}" height="{im.height}" '
       f'style="width:100%;height:auto;border-radius:16px;margin:0 0 40px;" />\n\n')
s = s.replace('  <div class="post-content">', tag + '  <div class="post-content">', 1)

s = re.sub(r'\s*<meta (property="og:image"|name="twitter:image")[^>]*>', '', s)
meta = f'\n  <meta property="og:image" content="{url}" />\n  <meta name="twitter:image" content="{url}" />'
s = s.replace('</title>', '</title>' + meta, 1)

def fix(m):
    try:
        d = json.loads(m.group(2))
    except Exception:
        return m.group(0)
    if d.get('@type') in ('Article', 'BlogPosting'):
        d['image'] = url
        return m.group(1) + json.dumps(d, ensure_ascii=False, indent=2) + m.group(3)
    return m.group(0)
s = re.sub(r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)', fix, s, flags=re.S)
open(art, 'w', encoding='utf-8').write(s)
print(out, im.size, os.path.getsize(out) // 1024, 'KB')
