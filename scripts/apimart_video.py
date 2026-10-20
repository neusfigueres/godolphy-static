#!/usr/bin/env python3
"""Genera vídeos con la API de Apimart a partir de trabajos en videogen/*.json.

Cada trabajo:
{
  "out": "imagegen/video-calculo/videos/salto.mp4",
  "model": "kling-v3",
  "prompt": "…",
  "frames": ["imagegen/…/inicio.png", "imagegen/…/final.png"],  # rutas del repo (se pasan como URL pública de GitHub)
  "body": {"duration": 5, "mode": "std", "aspect_ratio": "9:16"}  # parámetros extra tal cual
}
Al terminar el JSON se mueve a videogen/done/ (con la respuesta de la tarea) o videogen/failed/.
"""
import glob, json, os, shutil, sys, time, urllib.request, urllib.error

API = "https://api.apimart.ai/v1"
KEY = os.environ.get("APIMART_API_KEY", "")
REPO = os.environ.get("GITHUB_REPOSITORY", "neusfigueres/godolphy-static")
SHA = os.environ.get("GITHUB_SHA", "main")


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


def run(job):
    body = {"model": job["model"], "prompt": job["prompt"]}
    frames = [f"https://raw.githubusercontent.com/{REPO}/{SHA}/{p}" for p in job.get("frames", [])]
    if frames and job.get("roles"):
        body["image_with_roles"] = [{"url": u, "role": r} for u, r in zip(frames, job["roles"])]
    elif frames:
        body["image_urls"] = frames
    body.update(job.get("body", {}))
    sub = call("POST", "/videos/generations", body)
    print("submit:", json.dumps(sub)[:600], flush=True)
    ids = find(sub, lambda k, v: k == "task_id" and isinstance(v, str))
    if not ids:
        raise RuntimeError("sin task_id: " + json.dumps(sub)[:500])
    for _ in range(int(job.get("poll", 240))):  # 240 = ~20 min
        time.sleep(5)
        t = call("GET", f"/tasks/{ids[0]}")
        status = (find(t, lambda k, v: k == "status" and isinstance(v, str)) or ["?"])[0].lower()
        if status in ("failed", "error", "cancelled"):
            raise RuntimeError("tarea fallida: " + json.dumps(t)[:800])
        urls = [v for v in find(t, lambda k, v: isinstance(v, str) and v.startswith("http") and ".mp4" in v)]
        urls += [u for l in find(t, lambda k, v: isinstance(v, list)) for u in l if isinstance(u, str) and u.startswith("http") and ".mp4" in u]
        if not urls and status in ("completed", "succeeded", "success"):
            urls = [v for v in find(t, lambda k, v: isinstance(v, str) and v.startswith("http"))]
        if urls:
            print("task:", json.dumps(t)[:1500], flush=True)
            job["task"] = t
            break
    else:
        raise RuntimeError("timeout esperando el vídeo")
    os.makedirs(os.path.dirname(job["out"]), exist_ok=True)
    req = urllib.request.Request(urls[0], headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        open(job["out"], "wb").write(r.read())
    print("saved:", job["out"], os.path.getsize(job["out"]), "bytes")


def process(path):
    job = json.load(open(path))
    print("==>", path, job.get("model"), flush=True)
    dest = "videogen/done"
    if os.path.exists(job["out"]):
        print("ya existe, se salta")
    else:
        try:
            run(job)
        except Exception as e:
            print("ERROR:", path, e)
            job["error"] = str(e)[:1500]
            dest = "videogen/failed"
    os.makedirs(dest, exist_ok=True)
    json.dump(job, open(os.path.join(dest, os.path.basename(path)), "w"), ensure_ascii=False, indent=2)
    os.remove(path)


def main():
    if not KEY:
        sys.exit("Falta APIMART_API_KEY")
    from concurrent.futures import ThreadPoolExecutor
    paths = sorted(glob.glob("videogen/*.json"))
    with ThreadPoolExecutor(max_workers=3) as ex:
        list(ex.map(process, paths))


if __name__ == "__main__":
    main()
