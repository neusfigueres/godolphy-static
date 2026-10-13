#!/usr/bin/env python3
"""Genera imágenes con la API de Apimart a partir de trabajos en imagegen/*.json.

Cada trabajo es un JSON:
{
  "out": "images/blog/mi-articulo.png",        # dónde guardar (relativo al repo)
  "model": "gpt-image-2-ext",                   # modelo de Apimart
  "prompt": "…",
  "size": "16:9",                               # opcional
  "ref_files": ["images/mockups/agenda.png"],   # opcional: referencias del repo (se envían en base64)
  "image_urls": ["https://…"],                  # opcional: referencias por URL
  "extra": {"resolution": "1K"}                 # opcional: parámetros adicionales tal cual
}

Si "out" ya existe, el trabajo se salta. Al terminar, el JSON se mueve a imagegen/done/
(o a imagegen/failed/ con el error). La clave va en la variable de entorno APIMART_API_KEY.
"""
import base64, glob, json, mimetypes, os, shutil, sys, time, urllib.request, urllib.error

API = "https://api.apimart.ai/v1"
KEY = os.environ.get("APIMART_API_KEY", "")


def call(method, path, body=None):
    req = urllib.request.Request(API + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:800]}")


def find(obj, pred):
    """Busca recursivamente valores que cumplan pred."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if pred(k, v):
                out.append(v)
            out += find(v, pred)
    elif isinstance(obj, list):
        for v in obj:
            out += find(v, pred)
    return out


def data_url(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


def run(job):
    body = {"model": job["model"], "prompt": job["prompt"], "n": 1}
    if job.get("size"):
        body["size"] = job["size"]
    refs = list(job.get("image_urls", [])) + [data_url(p) for p in job.get("ref_files", [])]
    if refs:
        body["image_urls"] = refs
    body.update(job.get("extra", {}))

    sub = call("POST", "/images/generations", body)
    print("submit:", json.dumps(sub)[:600])
    ids = find(sub, lambda k, v: k == "task_id" and isinstance(v, str))
    urls = find(sub, lambda k, v: isinstance(v, str) and v.startswith("http") and k in ("url", "image_url"))
    if not urls:
        if not ids:
            raise RuntimeError("sin task_id ni url en la respuesta")
        for _ in range(100):  # ~8 min
            time.sleep(5)
            t = call("GET", f"/tasks/{ids[0]}")
            status = (find(t, lambda k, v: k == "status" and isinstance(v, str)) or ["?"])[0]
            if status.lower() in ("failed", "error", "cancelled"):
                raise RuntimeError("tarea fallida: " + json.dumps(t)[:800])
            urls = find(t, lambda k, v: isinstance(v, str) and v.startswith("http") and k in ("url", "image_url", "urls"))
            urls += [u for l in find(t, lambda k, v: k in ("url", "urls", "images") and isinstance(v, list)) for u in l if isinstance(u, str) and u.startswith("http")]
            if urls:
                print("task:", json.dumps(t)[:600])
                break
        else:
            raise RuntimeError("timeout esperando la imagen")
    b64 = find(sub, lambda k, v: k == "b64_json" and isinstance(v, str))
    os.makedirs(os.path.dirname(job["out"]) or ".", exist_ok=True)
    if urls:
        req = urllib.request.Request(urls[0], headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            open(job["out"], "wb").write(r.read())
    elif b64:
        open(job["out"], "wb").write(base64.b64decode(b64[0]))
    print("saved:", job["out"], os.path.getsize(job["out"]), "bytes")


def main():
    if not KEY:
        sys.exit("Falta APIMART_API_KEY")
    changed = False
    for path in sorted(glob.glob("imagegen/*.json")):
        job = json.load(open(path))
        print("==>", path, job.get("model"))
        dest = "imagegen/done"
        if os.path.exists(job["out"]):
            print("ya existe, se salta")
        else:
            try:
                run(job)
            except Exception as e:
                print("ERROR:", e)
                job["error"] = str(e)[:1500]
                json.dump(job, open(path, "w"), ensure_ascii=False, indent=2)
                dest = "imagegen/failed"
        os.makedirs(dest, exist_ok=True)
        shutil.move(path, os.path.join(dest, os.path.basename(path)))
        changed = True
    print("CHANGED=" + ("1" if changed else "0"))


if __name__ == "__main__":
    main()
