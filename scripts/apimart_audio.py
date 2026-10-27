#!/usr/bin/env python3
"""Audio con Apimart: audiogen/*.json
 music:      {"type":"music","out":"…/x.mp3","body":{suno params}}
 transcribe: {"type":"transcribe","file":"…/x.mp4","out":"…/x.txt","language":"es"}
"""
import glob, json, os, sys, time, uuid, urllib.request, urllib.error
API="https://api.apimart.ai/v1"; KEY=os.environ.get("APIMART_API_KEY","")
def req(method,path,body=None,data=None,ctype="application/json"):
    r=urllib.request.Request(API+path,method=method,data=data if data is not None else (json.dumps(body).encode() if body is not None else None),
        headers={"Authorization":f"Bearer {KEY}","Content-Type":ctype})
    try:
        with urllib.request.urlopen(r,timeout=300) as x: return json.loads(x.read().decode())
    except urllib.error.HTTPError as e: raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:800]}")
def music(job):
    sub=req("POST","/music/generations",dict({"model":"suno"},**job["body"])); print("submit",json.dumps(sub)[:400],flush=True)
    tid=sub["data"][0]["task_id"]
    for _ in range(200):
        time.sleep(5); t=req("GET",f"/music/tasks/{tid}"); st=str(t.get("data",{}).get("status","")).lower()
        if st=="failed": raise RuntimeError(json.dumps(t)[:800])
        if st=="completed":
            job["task"]=t; ms=t["data"]["result"]["music"]
            base,ext=os.path.splitext(job["out"]); os.makedirs(os.path.dirname(job["out"]),exist_ok=True)
            for i,m in enumerate(ms):
                u=m["audio_url"]; o=f"{base}_{i+1}{ext}"
                with urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=300) as x: open(o,"wb").write(x.read())
                print("saved",o,flush=True)
            return
    raise RuntimeError("timeout")
def transcribe(job):
    b=uuid.uuid4().hex; fn=os.path.basename(job["file"]); parts=[]
    kv=[("model","whisper-1"),("language",job.get("language","es")),("response_format","verbose_json")]
    if job.get("words"): kv+=[("timestamp_granularities[]","word"),("timestamp_granularities[]","segment")]
    for k,v in kv:
        parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    parts.append(f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="{fn}"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode()+open(job["file"],"rb").read()+b"\r\n")
    parts.append(f"--{b}--\r\n".encode())
    t=req("POST","/audio/transcriptions",data=b"".join(parts),ctype=f"multipart/form-data; boundary={b}")
    lines=[f'{s.get("start",0):6.2f}-{s.get("end",0):6.2f}  {s.get("text","").strip()}' for s in t.get("segments",[])] or [t.get("text","")]
    os.makedirs(os.path.dirname(job["out"]),exist_ok=True); open(job["out"],"w").write("\n".join(lines)+"\n"); print("\n".join(lines))
    if job.get("words"): open(os.path.splitext(job["out"])[0]+".json","w").write(json.dumps(t,ensure_ascii=False))
def tts(job):
    errs=[]
    for model in job.get("models",["gpt-4o-mini-tts","tts-1"]):
        body=dict(job["body"]); body["model"]=model
        if model=="tts-1": body.pop("instructions",None)
        r=urllib.request.Request(API+"/audio/speech",method="POST",data=json.dumps(body).encode(),headers={"Authorization":f"Bearer {KEY}","Content-Type":"application/json"})
        try:
            with urllib.request.urlopen(r,timeout=300) as x: data=x.read(); ct=x.headers.get("Content-Type","")
        except urllib.error.HTTPError as e:
            errs.append(f"{model}: HTTP {e.code} {e.read().decode()[:300]}"); continue
        if "json" in ct: errs.append(f"{model}: {data[:300]}"); continue
        os.makedirs(os.path.dirname(job["out"]),exist_ok=True); open(job["out"],"wb").write(data); job["model_used"]=model; print("saved",job["out"],len(data)); return
    raise RuntimeError(" | ".join(errs))
def process(p):
    job=json.load(open(p)); dest="audiogen/done"
    try: {"music":music,"transcribe":transcribe,"tts":tts}[job["type"]](job)
    except Exception as e: print("ERROR",p,e); job["error"]=str(e)[:1500]; dest="audiogen/failed"
    os.makedirs(dest,exist_ok=True); json.dump(job,open(os.path.join(dest,os.path.basename(p)),"w"),ensure_ascii=False,indent=2); os.remove(p)
if __name__=="__main__":
    if not KEY: sys.exit("Falta APIMART_API_KEY")
    for p in sorted(glob.glob("audiogen/*.json")): process(p)
