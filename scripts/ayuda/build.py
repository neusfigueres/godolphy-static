#!/usr/bin/env python3
"""Genera el centro de ayuda (/ayuda/) a partir de scripts/ayuda/.

Uso (desde la raíz del repo):  python3 scripts/ayuda/build.py

- indice.json            -> secciones y artículos en orden de configuración
- articulos/<slug>.html  -> contenido de cada artículo (con metadatos en <!--meta ... -->)
- La cabecera, el menú móvil y el pie se copian de una página existente de la web,
  para que el centro de ayuda siempre tenga el mismo menú que el resto del sitio.

Mientras INDEXABLE = False, todas las páginas llevan noindex (borrador).
"""
import html
import json
import re
from pathlib import Path

INDEXABLE = True

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(__file__).resolve().parent
OUT = ROOT / "ayuda"
TEMPLATE = ROOT / "funcionalidades" / "servicios-a-domicilio" / "index.html"
BASE_URL = "https://www.godolphy.com"


def chrome():
    t = TEMPLATE.read_text(encoding="utf-8")
    tracking = t[t.index("<!-- PostHog Analytics -->"): t.index('<script src="/assets/tracking.js"></script>') + len('<script src="/assets/tracking.js"></script>')]
    site_css = re.search(r"<style>(.*?)</style>", t, re.S).group(1)
    body_start = t.index("<body")
    body_start = t.index(">", body_start) + 1
    nav = t[body_start: t.index("<main>")]
    footer = t[t.index("<footer"): t.index("</footer>") + len("</footer>")]
    return tracking, site_css, nav, footer


CSS = """
:root{--lila:#631cff;--lila-50:#f4f0ff;--lila-100:#e9e1ff;--ink:#02021e;--ink-2:rgba(2,2,30,.7);--ink-3:rgba(2,2,30,.5);--line:rgba(2,2,30,.1);--yellow:#EEFE3A}
.ay-hero{background:linear-gradient(160deg,#9B4FE8 0%,#7835C3 30%,#631cff 65%,#3a0aaa 100%);padding:120px 40px 56px;color:#fff}
.ay-hero-in{max-width:1120px;margin:0 auto}
.ay-crumbs{font-size:13px;color:rgba(255,255,255,.75);margin:0 0 16px}
.ay-crumbs a{color:rgba(255,255,255,.75);text-decoration:none}.ay-crumbs a:hover{color:#fff}
.ay-hero h1{font-family:'Gabarito',sans-serif;font-size:44px;line-height:1.1;font-weight:700;margin:0 0 12px}
.ay-hero p{font-size:17px;line-height:1.6;color:rgba(255,255,255,.85);margin:0;max-width:680px}
.ay-meta{margin-top:18px;font-size:13px;color:rgba(255,255,255,.7)}
.ay-search{margin-top:28px;max-width:560px;position:relative}
.ay-search input{width:100%;box-sizing:border-box;border:0;border-radius:14px;padding:16px 18px 16px 48px;font:inherit;font-size:16px;color:var(--ink);outline:none;box-shadow:0 10px 30px rgba(20,0,80,.25)}
.ay-search input:focus{box-shadow:0 0 0 3px var(--yellow),0 10px 30px rgba(20,0,80,.25)}
.ay-search svg{position:absolute;left:16px;top:50%;transform:translateY(-50%)}
.ay-wrap{max-width:1120px;margin:0 auto;padding:56px 40px 96px;display:grid;grid-template-columns:260px minmax(0,1fr);gap:56px;align-items:start}
.ay-side{position:sticky;top:24px;font-size:14px;max-height:calc(100vh - 48px);overflow:auto;padding-right:8px}
.ay-side h3{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3);font-weight:600;margin:22px 0 8px}
.ay-side h3:first-child{margin-top:0}
.ay-side ul{list-style:none;margin:0;padding:0}
.ay-side li a,.ay-side li span{display:block;padding:6px 10px;border-radius:8px;color:var(--ink-2);text-decoration:none;line-height:1.4}
.ay-side li a:hover{background:var(--lila-50);color:var(--lila)}
.ay-side li a.current{background:var(--lila-100);color:var(--lila);font-weight:600}
.ay-side li span{color:rgba(2,2,30,.35)}
.ay-art{color:var(--ink);font-size:16px;line-height:1.75;max-width:720px}
.ay-art h2{font-family:'Gabarito',sans-serif;font-size:28px;line-height:1.2;margin:48px 0 14px;scroll-margin-top:24px}
.ay-art h2:first-child{margin-top:0}
.ay-art h3{font-family:'Gabarito',sans-serif;font-size:20px;margin:32px 0 10px}
.ay-art p{margin:0 0 14px;color:var(--ink-2)}
.ay-art strong{color:var(--ink);font-weight:600}
.ay-art a{color:var(--lila);text-decoration:underline;text-underline-offset:3px}
.ay-art ul{margin:0 0 16px;padding-left:22px;color:var(--ink-2)}
.ay-art ul li{margin:6px 0}
.ay-art ol.steps{list-style:none;counter-reset:s;margin:0 0 20px;padding:0}
.ay-art ol.steps>li{counter-increment:s;position:relative;padding:2px 0 14px 46px;color:var(--ink-2)}
.ay-art ol.steps>li::before{content:counter(s);position:absolute;left:0;top:0;width:30px;height:30px;border-radius:50%;background:var(--lila);color:#fff;font-weight:600;font-size:14px;display:flex;align-items:center;justify-content:center}
.ay-art ol.steps>li ul{margin-top:10px}
.callout{background:var(--lila-50);border:1px solid var(--lila-100);border-radius:14px;padding:18px 20px;margin:24px 0}
.callout>strong{display:block;margin-bottom:4px}.callout p{margin:0}
.tip{background:var(--ink);color:#fff;border-radius:20px;padding:32px 32px 18px;margin:48px 0}
.tip-label{display:inline-block;background:var(--yellow);color:var(--ink);font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;border-radius:20px;padding:4px 12px;margin-bottom:12px}
.tip h2{color:#fff;margin-top:0!important}
.tip p{color:rgba(255,255,255,.78)}.tip strong{color:#fff}.tip a{color:var(--yellow)}
.shot{margin:20px 0 28px;border:1.5px dashed rgba(99,28,255,.35);border-radius:14px;background:var(--lila-50);min-height:140px;display:flex;align-items:flex-end;padding:14px 16px}
.shot img{display:block;width:100%;height:auto;border-radius:10px}
.shot figcaption{font-size:13px;color:var(--ink-3)}
.shot.has-img{border:1px solid var(--line);background:#fff;padding:0;display:block}
.shot.has-img figcaption{padding:10px 14px}
dl.faq{margin:0;border-top:1px solid var(--line)}
dl.faq dt{font-weight:600;color:var(--ink);padding:18px 0 4px}
dl.faq dd{margin:0;padding:0 0 18px;border-bottom:1px solid var(--line);color:var(--ink-2)}
.ay-related{margin-top:56px;padding-top:28px;border-top:1px solid var(--line)}
.ay-related h2{font-size:22px!important;margin:0 0 14px!important}
.ay-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}
.ay-card{display:block;border:1px solid var(--line);border-radius:14px;padding:16px 18px;text-decoration:none!important;color:var(--ink)!important;transition:border-color .15s,box-shadow .15s}
a.ay-card:hover{border-color:var(--lila);box-shadow:0 6px 20px rgba(99,28,255,.12)}
.ay-card small{display:block;color:var(--ink-3);font-size:12px;margin-top:4px}
.ay-card.soon{color:rgba(2,2,30,.4)!important;background:#fafafa}
.ay-help{margin-top:40px;background:var(--lila-50);border-radius:16px;padding:22px 24px;font-size:15px;color:var(--ink-2)}
.ay-help a{color:var(--lila);font-weight:600}
.ay-sections{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
.ay-sec{border:1px solid var(--line);border-radius:18px;padding:24px}
.ay-sec h2{font-family:'Gabarito',sans-serif;font-size:21px;margin:0 0 4px;color:var(--ink)}
.ay-sec>p{color:var(--ink-3);font-size:14px;margin:0 0 14px}
.ay-sec ol{margin:0;padding-left:20px;font-size:15px;line-height:1.5}
.ay-sec li{margin:7px 0;color:rgba(2,2,30,.38)}
.ay-sec li a{color:var(--ink);text-decoration:none;font-weight:500}.ay-sec li a:hover{color:var(--lila)}
.ay-sec .num{display:inline-flex;width:26px;height:26px;border-radius:50%;background:var(--lila-100);color:var(--lila);font-size:13px;font-weight:700;align-items:center;justify-content:center;margin-bottom:10px}
.soon-tag{font-size:11px;color:rgba(2,2,30,.38);margin-left:4px}
.ay-empty{display:none;color:var(--ink-3)}
.ay-index-wrap{max-width:1120px;margin:0 auto;padding:56px 40px 96px}
.ay-intro{font-size:15px;color:var(--ink-2);margin:0 0 28px;max-width:720px;line-height:1.7}
@media(max-width:960px){.ay-wrap{grid-template-columns:1fr;gap:32px}.ay-side{position:static;max-height:none;order:2;border-top:1px solid var(--line);padding-top:24px}}
@media(max-width:768px){.ay-hero{padding:104px 20px 40px}.ay-hero h1{font-size:30px}.ay-hero p{font-size:15px}.ay-wrap,.ay-index-wrap{padding:36px 20px 64px}.ay-art h2{font-size:24px}.tip{padding:24px 20px 10px}}
"""

SEARCH_ICON = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#631cff" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'


def esc(s):
    return html.escape(s, quote=True)


def page(title, description, canonical, body, jsonld):
    tracking, site_css, nav, footer = chrome()
    robots = "index,follow" if INDEXABLE else "noindex,nofollow"
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
{tracking}
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}" />
  <meta name="robots" content="{robots}" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(description)}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:type" content="article" />
  <link rel="icon" type="image/png" href="/favicon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gabarito:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap">
  <link rel="stylesheet" href="/assets/gx-pages.css">
  <style>{site_css}
{CSS}</style>
{ld}
</head>
<body style="overflow-x:hidden">
{nav}
<main>
{body}
</main>
{footer}
<script src="/assets/gx-pages.js" defer></script>
</body>
</html>
"""


def load_index():
    data = json.loads((SRC / "indice.json").read_text(encoding="utf-8"))
    flat = {}
    for si, sec in enumerate(data["secciones"]):
        for a in sec["articulos"]:
            a.setdefault("publicado", False)
            a["seccion"] = sec
            flat[a["slug"]] = a
    return data, flat


def load_article(slug):
    raw = (SRC / "articulos" / f"{slug}.html").read_text(encoding="utf-8")
    m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->", raw, re.S)
    meta = json.loads(m.group(1))
    body = raw[m.end():]
    # Texto de funciones aún no desplegadas: se escribe ya, pero no se publica
    # hasta quitar las marcas <!--pendiente--> ... <!--/pendiente-->.
    body = re.sub(r"<!--pendiente-->.*?<!--/pendiente-->", "", body, flags=re.S)
    return meta, body.strip()


def link_or_span(a, current=None):
    if a["publicado"]:
        cls = ' class="current"' if a["slug"] == current else ""
        return f'<a href="/ayuda/{a["slug"]}/"{cls}>{esc(a["titulo"])}</a>'
    return f'<span title="Próximamente">{esc(a["titulo"])}</span>'


def sidebar(data, current):
    out = ['<nav class="ay-side" aria-label="Índice del centro de ayuda">']
    for sec in data["secciones"]:
        out.append(f'<h3>{esc(sec["titulo"])}</h3><ul>')
        for a in sec["articulos"]:
            out.append(f"<li>{link_or_span(a, current)}</li>")
        out.append("</ul>")
    out.append("</nav>")
    return "\n".join(out)


def shots(content):
    """Si existe la captura en ayuda/img/<data-shot>.png, la inserta; si no, deja el hueco."""
    def repl(m):
        name, cap = m.group(1), m.group(2)
        for ext in ("png", "jpg", "webp"):
            if (OUT / "img" / f"{name}.{ext}").exists():
                return f'<figure class="shot has-img"><img src="/ayuda/img/{name}.{ext}" alt="{esc(cap)}" loading="lazy"/><figcaption>{cap}</figcaption></figure>'
        return ""
    return re.sub(r'<figure class="shot" data-shot="([^"]+)"><figcaption>(.*?)</figcaption></figure>', repl, content)


def unlink_unpublished(content, flat):
    """Los enlaces a artículos aún no publicados se quedan como texto (sin 404)."""
    def repl(m):
        a = flat.get(m.group(1))
        return m.group(0) if a and a["publicado"] else m.group(2)
    return re.sub(r'<a href="/ayuda/([^/"]+)/">(.*?)</a>', repl, content)


def faq_items(content):
    """Preguntas de los bloques <dl class="faq"> (Errores habituales) para el FAQPage."""
    out = []
    for dl in re.findall(r'<dl class="faq">(.*?)</dl>', content, re.S):
        for q, a in re.findall(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", dl, re.S):
            clean = lambda t: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip()
            out.append((clean(q), clean(a)))
    return out


def build_article(data, flat, slug):
    meta, content = load_article(slug)
    content = unlink_unpublished(content, flat)
    a = flat[slug]
    sec = a["seccion"]
    url = f"{BASE_URL}/ayuda/{slug}/"
    cards = []
    for r in meta.get("relacionados", []):
        ra = flat.get(r)
        if not ra:
            continue
        if ra["publicado"]:
            cards.append(f'<a class="ay-card" href="/ayuda/{r}/">{esc(ra["titulo"])}<small>{esc(ra["seccion"]["titulo"])}</small></a>')
        else:
            cards.append(f'<div class="ay-card soon">{esc(ra["titulo"])}<small>Próximamente</small></div>')
    related = f'<section class="ay-related"><h2>Artículos relacionados</h2><div class="ay-cards">{"".join(cards)}</div></section>' if cards else ""
    body = f"""<section class="ay-hero"><div class="ay-hero-in">
<p class="ay-crumbs"><a href="/ayuda/">Centro de ayuda</a> › {esc(sec["titulo"])}</p>
<h1>{esc(meta["titulo"])}</h1>
<p>{esc(meta["resumen"])}</p>
<p class="ay-meta">Lectura: {esc(meta.get("tiempo", ""))} · Actualizado el {fecha(meta["actualizado"])}</p>
</div></section>
<div class="ay-wrap">
{sidebar(data, slug)}
<article class="ay-art">
{shots(content)}
{related}
<div class="ay-help">¿Te has quedado con alguna duda? Escríbenos a <a href="mailto:hello@godolphy.com">hello@godolphy.com</a> y te ayudamos.</div>
</article>
</div>"""
    jsonld = [
        {"@context": "https://schema.org", "@type": "TechArticle", "headline": meta["titulo"], "description": meta["descripcion"],
         "dateModified": meta["actualizado"], "inLanguage": "es", "mainEntityOfPage": url,
         "publisher": {"@type": "Organization", "name": "Godolphy", "url": BASE_URL}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Centro de ayuda", "item": f"{BASE_URL}/ayuda/"},
            {"@type": "ListItem", "position": 2, "name": meta["titulo"], "item": url}]},
    ]
    faq = faq_items(content)
    if faq:
        jsonld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    d = OUT / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(page(meta["seo_title"], meta["descripcion"], url, body, jsonld), encoding="utf-8")


MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def fecha(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} de {MESES[int(m) - 1]} de {y}"


def search_text(a):
    """Texto en el que busca el buscador: título, resumen, descripción, palabras «buscar» y títulos de sección."""
    try:
        meta, body = load_article(a["slug"])[:2]
    except Exception:
        return a["titulo"].lower()
    heads = " ".join(re.sub(r"<[^>]+>", "", h) for h in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", body, re.S))
    parts = [a["titulo"], meta.get("resumen", ""), meta.get("descripcion", ""), meta.get("buscar", ""), heads]
    return " ".join(parts).lower()


def build_index(data):
    secs = []
    for i, sec in enumerate(data["secciones"], 1):
        items = []
        for a in sec["articulos"]:
            if a["publicado"]:
                items.append(f'<li data-q="{esc(search_text(a))}"><a href="/ayuda/{a["slug"]}/">{esc(a["titulo"])}</a></li>')
            else:
                items.append(f'<li data-q="{esc(a["titulo"].lower())}">{esc(a["titulo"])}<span class="soon-tag">· próximamente</span></li>')
        secs.append(f'<section class="ay-sec"><span class="num">{i}</span><h2>{esc(sec["titulo"])}</h2><p>{esc(sec["descripcion"])}</p><ol>{"".join(items)}</ol></section>')
    body = f"""<section class="ay-hero"><div class="ay-hero-in">
<h1>Centro de ayuda</h1>
<p>Todo lo que necesitas para poner en marcha tu salón en Godolphy, paso a paso y en el mismo orden en que lo configurarás.</p>
<div class="ay-search">{SEARCH_ICON}<input id="ay-q" type="search" placeholder="Busca: servicios, horarios, depósito…" aria-label="Buscar en el centro de ayuda" autocomplete="off"/></div>
</div></section>
<div class="ay-index-wrap">
<p class="ay-intro">Si acabas de empezar, sigue las secciones en orden: cada paso deja preparado el siguiente. Además de explicar cómo se hace, cada artículo incluye consejos para sacarle más partido a tu negocio.</p>
<div class="ay-sections" id="ay-sections">{"".join(secs)}</div>
<p class="ay-empty" id="ay-empty">No hemos encontrado nada con esa búsqueda. Escríbenos a <a href="mailto:hello@godolphy.com">hello@godolphy.com</a>.</p>
</div>
<script>
(function(){{var q=document.getElementById('ay-q'),secs=document.querySelectorAll('.ay-sec'),empty=document.getElementById('ay-empty');
function norm(s){{return s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');}}
var stop=' de la el los las del al un una y o en con para por que como mi tu se lo '.split(' ');
q.addEventListener('input',function(){{var t=norm(q.value.trim()),w=t.split(/\\s+/).filter(function(x){{return x.length>1&&stop.indexOf(x)<0;}}),any=false;secs.forEach(function(s){{var hit=0,h=norm(s.querySelector('h2').textContent);s.querySelectorAll('li').forEach(function(li){{var d=norm(li.getAttribute('data-q'))+' '+h;var ok=!w.length||w.every(function(x){{return d.indexOf(x)>-1||(x.length>4&&d.indexOf(x.slice(0,-1))>-1);}});li.style.display=ok?'':'none';if(ok)hit++;}});s.style.display=hit?'':'none';if(hit)any=true;}});empty.style.display=any?'none':'block';}});}})();
</script>"""
    url = f"{BASE_URL}/ayuda/"
    jsonld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Centro de ayuda de Godolphy", "url": url, "inLanguage": "es"}]
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(page("Centro de ayuda | Godolphy", "Guías paso a paso para configurar tu salón en Godolphy: servicios, equipo, horarios, domicilio, cobros y reservas, con consejos para tu negocio.", url, body, jsonld), encoding="utf-8")


def sitemap(slugs):
    sm = ROOT / "sitemap.xml"
    x = sm.read_text(encoding="utf-8")
    x = re.sub(r"\s*<!-- Centro de ayuda -->.*?<!-- /Centro de ayuda -->", "", x, flags=re.S)
    x = re.sub(r"\s*</urlset>", "\n</urlset>", x)
    if not INDEXABLE:
        sm.write_text(x, encoding="utf-8"); return
    urls = ["/ayuda/"] + [f"/ayuda/{s}/" for s in slugs]
    block = "\n\n  <!-- Centro de ayuda -->\n" + "".join(
        f"  <url>\n    <loc>{BASE_URL}{u}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>{'0.7' if u == '/ayuda/' else '0.6'}</priority>\n  </url>\n" for u in urls) + "  <!-- /Centro de ayuda -->"
    x = x.replace("\n</urlset>", block + "\n</urlset>")
    sm.write_text(x, encoding="utf-8")


def main():
    data, flat = load_index()
    build_index(data)
    built = []
    for slug, a in flat.items():
        if a["publicado"]:
            build_article(data, flat, slug)
            built.append(slug)
    sitemap(built)
    print(f"Índice + {len(built)} artículo(s): {', '.join(built)}  (indexable={INDEXABLE})")


if __name__ == "__main__":
    main()
