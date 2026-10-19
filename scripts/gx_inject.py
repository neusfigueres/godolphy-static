#!/usr/bin/env python3
"""Aplica la capa de estilo 2026-10 (assets/gx-pages.css + gx-pages.js) a páginas HTML.

- Cambia Poppins por Plus Jakarta Sans en el enlace de Google Fonts y en estilos inline.
- Añade el CSS y el JS compartidos si la página aún no los tiene.

Uso:  python3 scripts/gx_inject.py            # todas las páginas del sitio
      python3 scripts/gx_inject.py a.html b.html
Es idempotente: se puede ejecutar varias veces sin duplicar nada.
"""
import glob, os, re, sys

SKIP_DIRS = ('.git/', 'node_modules/', 'scripts/', 'imagegen/', 'videogen/', 'social/', 'descargas/')
# Páginas con diseño propio ya renovado o que no deben tocarse
SKIP_FILES = {'index.html', 'dashboard-ia/index.html'}

CSS = '<link rel="stylesheet" href="/assets/gx-pages.css">'
JS = '<script src="/assets/gx-pages.js" defer></script>'


def inject(path):
    s = open(path, encoding='utf-8').read()
    o = s
    s = s.replace('family=Poppins:wght@300;400;500;600;700', 'family=Plus+Jakarta+Sans:wght@400;500;600;700')
    s = s.replace('family=Poppins:wght@300;400;500;600', 'family=Plus+Jakarta+Sans:wght@400;500;600;700')
    s = re.sub(r"family=Poppins:[^&\"']*", 'family=Plus+Jakarta+Sans:wght@400;500;600;700', s)
    s = re.sub(r"font-family:\s*['\"]?Poppins['\"]?\s*,", "font-family:'Plus Jakarta Sans',", s)
    if 'gx-pages.css' not in s and '</head>' in s:
        s = s.replace('</head>', CSS + '\n</head>', 1)
    if 'gx-pages.js' not in s and '</body>' in s:
        s = s.replace('</body>', JS + '\n</body>', 1)
    if s != o:
        open(path, 'w', encoding='utf-8').write(s)
        return True
    return False


def all_pages():
    for p in sorted(glob.glob('**/*.html', recursive=True)):
        p = p.replace(os.sep, '/')
        if p.startswith(SKIP_DIRS) or p in SKIP_FILES or '/img/' in p:
            continue
        yield p


if __name__ == '__main__':
    files = sys.argv[1:] or list(all_pages())
    n = sum(inject(f) for f in files)
    print(f'gx_inject: {n} de {len(files)} páginas actualizadas')
