from __future__ import annotations
import html
from pathlib import Path
from .storage import manifest, save_manifest
from .util import write_text

def placeholder(root:Path)->Path:
    m=manifest(root); title=html.escape(m.get("title") or "未定书名"); subtitle=html.escape(f"{m.get('genre','')} · {m.get('platform','')}")
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1600" viewBox="0 0 1200 1600">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#111827"/><stop offset="1" stop-color="#312e81"/></linearGradient></defs>
<rect width="1200" height="1600" fill="url(#g)"/><circle cx="900" cy="400" r="260" fill="#ffffff" opacity="0.08"/><path d="M0 1250 L1200 780 L1200 1600 L0 1600 Z" fill="#000" opacity="0.28"/>
<text x="90" y="260" fill="#fff" font-size="92" font-family="sans-serif" font-weight="700">{title}</text><text x="95" y="340" fill="#ddd" font-size="34" font-family="sans-serif">{subtitle}</text><text x="95" y="1480" fill="#bbb" font-size="26" font-family="sans-serif">NovelFlow placeholder - replace with generated cover art</text></svg>'''
    p=root/"covers"/"cover.svg"; write_text(p,svg); m["cover"]=str(p.relative_to(root)); save_manifest(root,m); return p
