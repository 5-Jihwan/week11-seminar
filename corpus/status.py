# -*- coding: utf-8 -*-
"""수집 진행 한 줄 보고. 사용: python corpus/status.py"""
import os, sys, time, glob, subprocess
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw", "harvest"); C = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: open(p, encoding="utf-8", errors="replace").read().strip() if os.path.exists(p) else "-"
last = lambda p: (rd(p).splitlines() or ["-"])[-1]
lines = lambda p: sum(1 for _ in open(p, encoding="utf-8")) if os.path.exists(p) else 0
print(time.strftime("%H:%M"), "| w0 cursor", rd(os.path.join(H, "kci_w0.cursor")), "|", last(os.path.join(H, "kci_w0.log")))
print("w2b cursor", rd(os.path.join(H, "kci_w2.cursor")), "|", last(os.path.join(H, "kci_w2b.log")))
print("kci rows", sum(lines(p) for p in glob.glob(os.path.join(C, "kci_w*.jsonl"))), "| oa rows", lines(os.path.join(C, "openalex_all.jsonl")), "| oa done flags", len(glob.glob(os.path.join(H, "openalex_*.done"))))
oa = [l for l in rd(os.path.join(H, "openalex.log")).splitlines() if "retry" not in l]; print("oa last year line:", oa[-1] if oa else "-", "| last:", last(os.path.join(H, "openalex.log"))[:70])
print("OPENALEX_API_KEY:", "set" if os.environ.get("OPENALEX_API_KEY") else "none", "| KCI_API_KEY:", "set" if os.environ.get("KCI_API_KEY") else "none")
out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq python.exe"], capture_output=True, text=True).stdout; print("python procs", max(0, len(out.strip().splitlines()) - 3))
