from __future__ import annotations
import uuid
from pathlib import Path
from typing import Any
from .util import now_iso, read_json, read_text, write_json

def load_canon(root: Path)->dict[str,Any]: return read_json(root/"state"/"canon.json",{})
def save_canon(root: Path, canon: dict[str,Any])->None: write_json(root/"state"/"canon.json",canon)
def add_fact(root: Path,text:str,source:str="manual")->dict[str,Any]:
    c=load_canon(root); f={"id":"F-"+uuid.uuid4().hex[:8],"text":text,"source":source,"active":True,"created_at":now_iso()}; c.setdefault("facts",[]).append(f); save_canon(root,c); return f
def add_foreshadow(root: Path,text:str,chapter:int,target:int|None=None)->dict[str,Any]:
    c=load_canon(root); x={"id":"FS-"+uuid.uuid4().hex[:8],"text":text,"introduced_chapter":int(chapter),"target_chapter":int(target) if target else None,"status":"open","created_at":now_iso()}; c.setdefault("foreshadowing",[]).append(x); save_canon(root,c); return x
def resolve_foreshadow(root: Path,item_id:str,chapter:int,note:str="")->dict[str,Any]:
    c=load_canon(root)
    for x in c.setdefault("foreshadowing",[]):
        if x.get("id")==item_id:
            x.update({"status":"resolved","resolved_chapter":int(chapter),"resolution_note":note}); save_canon(root,c); return x
    raise KeyError(f"Foreshadowing not found: {item_id}")
def set_summary(root: Path,chapter:int,summary:str)->None:
    c=load_canon(root); c.setdefault("chapter_summaries",{})[str(int(chapter))]=summary.strip(); save_canon(root,c)
def report(root: Path)->dict[str,Any]:
    c=load_canon(root); sums=c.get("chapter_summaries",{}); latest=max([int(k) for k in sums if str(k).isdigit()] or [0])
    unresolved=[x for x in c.get("foreshadowing",[]) if x.get("status")!="resolved"]
    overdue=[x for x in unresolved if x.get("target_chapter") and int(x["target_chapter"])<latest]
    warnings=[]
    for name,data in c.get("characters",{}).items():
        if isinstance(data,dict) and data.get("status")=="dead" and data.get("death_chapter"):
            d=int(data["death_chapter"])
            for p in sorted((root/"chapters").glob("*.md")):
                try: n=int(p.stem.split("-")[0])
                except Exception: continue
                if n>d and name in read_text(p):
                    warnings.append(f"Possible continuity check: dead character '{name}' is mentioned in chapter {n}; verify mention/flashback vs resurrection."); break
    return {"facts":len(c.get("facts",[])),"characters":len(c.get("characters",{})),"unresolved_foreshadowing":len(unresolved),"overdue_foreshadowing":overdue,"latest_summary_chapter":latest,"warnings":warnings}
