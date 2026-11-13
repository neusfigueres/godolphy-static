# Transcribe cada transcribe/*.wav sin .json todavía; guarda palabras con tiempos.
import glob, json, os, wave
import numpy as np
def load(p):
    with wave.open(p) as f:
        a=np.frombuffer(f.readframes(f.getnframes()),np.int16).astype(np.float32)/32768
    return a  # ha de ser mono 16 kHz
from faster_whisper import WhisperModel
todo=[w for w in sorted(glob.glob("transcribe/*.wav")) if not os.path.exists(w[:-4]+".json")]
if todo:
    m=WhisperModel("medium",compute_type="int8")
    for w in todo:
        segs,_=m.transcribe(load(w),language="es",word_timestamps=True,vad_filter=False)
        out=[{"start":round(x.start,2),"end":round(x.end,2),"word":x.word} for s in segs for x in s.words]
        json.dump(out,open(w[:-4]+".json","w"),ensure_ascii=False,indent=1)
        print(w,len(out),"words")
