# -*- coding: utf-8 -*-
"""덱 글꼴: 경기천년바탕(경기도 무료 서체)을 덱에 쓰인 글자만 추려 woff2로 HTML에 넣는다.
인터넷이 끊겨도, 글꼴이 깔리지 않은 노트북에서도 같은 글꼴로 보인다.
글꼴 파일이 없으면 빈 문자열을 돌려주고 설치된 글꼴·대체 글꼴에 맡긴다."""
import base64, io, os, sys
from fontTools import subset
from fontTools.ttLib import TTFont

DIRS = [os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts"), r"C:\Windows\Fonts"]
FILES = {400: "경기천년바탕OTF_Regular.otf", 700: "경기천년바탕OTF_Bold.otf"}
FAMILY = '"GG Batang","경기천년바탕","경기천년바탕 Regular",Pretendard,"Noto Serif KR",serif'
_cache = {}


def face(text):
    chars = "".join(sorted(c for c in set(text) if ord(c) > 32))
    if chars in _cache: return _cache[chars]
    css = []
    for w, fn in FILES.items():
        path = next((os.path.join(d, fn) for d in DIRS if os.path.exists(os.path.join(d, fn))), None)
        if not path:
            print("글꼴 파일 없음:", fn, "→ 내장하지 않음", file=sys.stderr); continue
        f = TTFont(path)
        if w == 400:
            miss = [c for c in chars if ord(c) not in f.getBestCmap()]
            if miss: print("경기천년바탕에 없는 글자(대체 글꼴로 표시):", " ".join(miss))
        opt = subset.Options(); opt.flavor = "woff2"
        s = subset.Subsetter(opt); s.populate(text=chars); s.subset(f)
        b = io.BytesIO(); f.flavor = "woff2"; f.save(b)
        css.append(f'@font-face{{font-family:"GG Batang";font-weight:{w};font-display:block;src:url(data:font/woff2;base64,{base64.b64encode(b.getvalue()).decode()}) format("woff2")}}')
    _cache[chars] = "".join(css)
    return _cache[chars]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    out = face("국가는 사회자본을 만들 수 있는가 Krishna 2007 → ① β −.26")
    assert out.count("@font-face") == 2, "두 굵기가 모두 내장돼야 한다"
    print("ok", len(out) // 1024, "KB")
