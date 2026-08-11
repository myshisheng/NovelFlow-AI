from __future__ import annotations
import re
from pathlib import Path
from .canon import set_summary
from .storage import manifest, save_manifest
from .util import read_text, write_text

def chapter_path(root:Path,number:int)->Path: return root/"chapters"/f"{int(number):04d}-chapter.md"
def summary_path(root:Path,number:int)->Path: return root/"summaries"/f"{int(number):04d}-summary.md"
def set_chapter(root:Path,number:int,text:str)->Path:
    p=chapter_path(root,number); write_text(p,text); return p
def set_chapter_summary(root:Path,number:int,text:str)->Path:
    p=summary_path(root,number); write_text(p,text); set_summary(root,number,text); return p
def approve(root:Path,number:int)->dict:
    cp,sp=chapter_path(root,number),summary_path(root,number)
    if not cp.exists(): raise ValueError(f"Chapter text missing: {cp.name}")
    if not sp.exists() or not read_text(sp).strip(): raise ValueError(f"Chapter summary missing: {sp.name}")
    m=manifest(root); approved=set(m.get("approved_chapter_numbers",[])); approved.add(int(number)); m["approved_chapter_numbers"]=sorted(approved); m["approved_chapters"]=len(approved); m["stage"]="final_audit" if len(approved)>=int(m.get("target_chapters") or 10**9) else "serializing"; save_manifest(root,m); return m
def list_chapters(root:Path)->list[tuple[int,Path]]:
    out=[]
    for p in sorted((root/"chapters").glob("*-chapter.md")):
        m=re.match(r"(\d+)-chapter$",p.stem)
        if m: out.append((int(m.group(1)),p))
    return out
