from __future__ import annotations
import shutil, uuid
from pathlib import Path
from typing import Any
from .util import now_iso, read_json, slugify, write_json, write_text

REQUIRED_DIRS = ["state","tasks","chapters","reviews","summaries","covers","exports","logs","artifacts"]

def project_root(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()

def ensure_project(path: str | Path) -> Path:
    root = project_root(path)
    if not (root/"novel.json").exists(): raise FileNotFoundError(f"Not a NovelFlow project: {root}")
    return root

def init_project(path: str | Path, *, idea: str, platform: str="番茄", genre: str="网文", target_words: int=1000000, chapters: int=500, title: str="") -> Path:
    root = project_root(path); root.mkdir(parents=True, exist_ok=True)
    if (root/"novel.json").exists(): raise FileExistsError(f"Project already exists: {root}")
    for d in REQUIRED_DIRS: (root/d).mkdir(parents=True, exist_ok=True)
    write_json(root/"novel.json", {"schema_version":1,"id":str(uuid.uuid4()),"slug":slugify(title or idea[:24]),"title":title,"idea":idea,"platform":platform,"genre":genre,"target_words":int(target_words),"target_chapters":int(chapters),"stage":"foundation","approved_chapters":0,"approved_chapter_numbers":[],"created_at":now_iso(),"updated_at":now_iso()})
    write_json(root/"state"/"canon.json", {"schema_version":1,"facts":[],"characters":{},"locations":{},"items":{},"foreshadowing":[],"timeline":[],"chapter_summaries":{}})
    write_text(root/"metadata.md", "# Book Metadata\n\n_TODO: metadata task._")
    write_text(root/"story_bible.md", "# Story Bible\n\n_TODO: story_bible task._")
    write_text(root/"master_outline.md", "# Master Outline\n\n_TODO: master_outline task._")
    return root

def manifest(root: Path) -> dict[str,Any]: return read_json(root/"novel.json", {})
def save_manifest(root: Path, data: dict[str,Any]) -> None:
    data["updated_at"] = now_iso(); write_json(root/"novel.json", data)
def task_path(root: Path, task_id: str) -> Path: return root/"tasks"/f"{task_id}.json"
def create_task(root: Path, kind: str, title: str, instructions: str, *, target: str="", priority: int=50, metadata: dict[str,Any]|None=None) -> dict[str,Any]:
    tid=f"{kind.replace(':','-')}-{uuid.uuid4().hex[:8]}"
    task={"id":tid,"kind":kind,"title":title,"status":"pending","priority":priority,"instructions":instructions,"target":target,"metadata":metadata or {},"created_at":now_iso(),"updated_at":now_iso()}
    write_json(task_path(root,tid),task); return task

def list_tasks(root: Path, status: str|None=None) -> list[dict[str,Any]]:
    out=[]
    for p in (root/"tasks").glob("*.json"):
        t=read_json(p,{})
        if not status or t.get("status")==status: out.append(t)
    out.sort(key=lambda t:(0 if t.get("status")=="in_progress" else 1,int(t.get("priority",50)),t.get("created_at","")))
    return out

def get_task(root: Path, task_id: str) -> dict[str,Any]:
    p=task_path(root,task_id)
    if not p.exists(): raise FileNotFoundError(f"Task not found: {task_id}")
    return read_json(p,{})
def save_task(root: Path, task: dict[str,Any]) -> None:
    task["updated_at"]=now_iso(); write_json(task_path(root,task["id"]),task)
def complete_task(root: Path, task_id: str, result_text: str) -> dict[str,Any]:
    task=get_task(root,task_id); target=task.get("target") or f"artifacts/{task_id}.md"
    write_text(root/target,result_text); task["status"]="done"; task["completed_at"]=now_iso(); save_task(root,task); return task

def set_cover(root: Path, source: str|Path) -> Path:
    src=Path(source).expanduser().resolve()
    if not src.exists(): raise FileNotFoundError(src)
    dst=root/"covers"/f"cover{src.suffix.lower() or '.img'}"; shutil.copy2(src,dst)
    m=manifest(root); m["cover"]=str(dst.relative_to(root)); save_manifest(root,m); return dst
