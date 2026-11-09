# -*- coding: utf-8 -*-
"""발표판 전용 밈 템플릿(imgflip 빈 템플릿) → deck/memes/*.jpg (git 제외). 공개판 덱에는 넣지 않는다."""
import os, sys, io, time, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "memes"); os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
T = {"pigeon": ["Is-This-A-Pigeon.jpg"], "brain": ["Expanding-Brain.jpg"], "buttons": ["Two-Buttons.jpg"], "drake": ["Drake-Hotline-Bling.jpg"],
     "fine": ["This-Is-Fine.jpg"], "gru": ["Grus-Plan.jpg"], "handshake": ["Epic-Handshake.jpg"], "boyfriend": ["Distracted-Boyfriend.jpg"],
     "whynotboth": ["Why-Not-Both.jpg"], "spiderman": ["Spider-Man-Pointing-At-Spider-Man.jpg", "Spiderman-Pointing-At-Spiderman.jpg", "Spider-Man-Double.jpg"]}
for k, names in T.items():
    ok = False
    for n in names:
        try:
            data = urllib.request.urlopen(urllib.request.Request("https://imgflip.com/s/meme/" + n, headers=UA), timeout=60).read()
            if len(data) > 5000: open(os.path.join(OUT, k + ".jpg"), "wb").write(data); print("ok", k, n, len(data) // 1024, "KB"); ok = True; break
        except Exception as e: print("  실패", k, n, str(e)[:60])
        time.sleep(1)
    if not ok: print("없음:", k)
