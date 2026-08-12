from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from . import __version__
from .canon import add_fact,add_foreshadow,report,resolve_foreshadow
from .chapters import approve,set_chapter,set_chapter_summary
from .context import build_context
from .cover import placeholder as make_placeholder
from .dashboard import serve
from .exporters import export_book
from .storage import complete_task,ensure_project,get_task,init_project,list_tasks,manifest,set_cover
from .util import read_text
from .workflow import bootstrap,chapter_start,next_task,task_prompt

def R(p): return ensure_project(p)
def cmd_init(a): print(init_project(a.path,idea=a.idea,platform=a.platform,genre=a.genre,target_words=a.target_words,chapters=a.chapters,title=a.title))
def cmd_bootstrap(a): print(json.dumps(bootstrap(R(a.path)),ensure_ascii=False,indent=2))
def cmd_status(a):
    r=R(a.path); ts=list_tasks(r); print(json.dumps({"project":manifest(r),"tasks":{"pending":sum(t['status']=='pending' for t in ts),"in_progress":sum(t['status']=='in_progress' for t in ts),"done":sum(t['status']=='done' for t in ts)},"canon":report(r)},ensure_ascii=False,indent=2))
def cmd_next(a):
    t=next_task(R(a.path)); print(json.dumps(t,ensure_ascii=False,indent=2) if t else "NO_TASK")
def cmd_prompt(a):
    r=R(a.path); t=get_task(r,a.task_id) if a.task_id else next_task(r)
    if not t: print("NO_TASK"); return
    print(task_prompt(r,t,build_context(r,chapter=t.get('metadata',{}).get('chapter'),last=a.last)))
def cmd_complete(a): print(json.dumps(complete_task(R(a.path),a.task_id,read_text(Path(a.file))),ensure_ascii=False,indent=2))
def cmd_context(a): print(build_context(R(a.path),a.chapter,a.last))
def cmd_chstart(a): print(json.dumps(chapter_start(R(a.path),a.number,a.title),ensure_ascii=False,indent=2))
def cmd_chset(a): print(set_chapter(R(a.path),a.number,read_text(Path(a.file))))
def cmd_sumset(a): print(set_chapter_summary(R(a.path),a.number,read_text(Path(a.file))))
def cmd_approve(a): print(json.dumps(approve(R(a.path),a.number),ensure_ascii=False,indent=2))
def cmd_fact(a): print(json.dumps(add_fact(R(a.path),a.text,a.source),ensure_ascii=False,indent=2))
def cmd_fsadd(a): print(json.dumps(add_foreshadow(R(a.path),a.text,a.chapter,a.target),ensure_ascii=False,indent=2))
def cmd_fsres(a): print(json.dumps(resolve_foreshadow(R(a.path),a.id,a.chapter,a.note),ensure_ascii=False,indent=2))
def cmd_report(a): print(json.dumps(report(R(a.path)),ensure_ascii=False,indent=2))
def cmd_cp(a): print(make_placeholder(R(a.path)))
def cmd_cs(a): print(set_cover(R(a.path),a.file))
def cmd_export(a): print(export_book(R(a.path),a.format))
def cmd_serve(a): serve(R(a.path),a.host,a.port)

def parser():
    p=argparse.ArgumentParser(prog="novelflow"); p.add_argument("--version",action="version",version=f"%(prog)s {__version__}"); s=p.add_subparsers(dest="cmd",required=True)
    x=s.add_parser("init"); x.add_argument("path"); x.add_argument("--idea",required=True); x.add_argument("--platform",default="番茄"); x.add_argument("--genre",default="网文"); x.add_argument("--target-words",type=int,default=1000000); x.add_argument("--chapters",type=int,default=500); x.add_argument("--title",default=""); x.set_defaults(func=cmd_init)
    for name,func in [("bootstrap",cmd_bootstrap),("status",cmd_status),("next",cmd_next),("canon-report",cmd_report),("cover-placeholder",cmd_cp)]: x=s.add_parser(name); x.add_argument("path"); x.set_defaults(func=func)
    x=s.add_parser("prompt"); x.add_argument("path"); x.add_argument("task_id",nargs="?"); x.add_argument("--last",type=int,default=5); x.set_defaults(func=cmd_prompt)
    x=s.add_parser("complete"); x.add_argument("path"); x.add_argument("task_id"); x.add_argument("--file",required=True); x.set_defaults(func=cmd_complete)
    x=s.add_parser("context"); x.add_argument("path"); x.add_argument("--chapter",type=int); x.add_argument("--last",type=int,default=5); x.set_defaults(func=cmd_context)
    x=s.add_parser("chapter-start"); x.add_argument("path"); x.add_argument("number",type=int); x.add_argument("--title",default=""); x.set_defaults(func=cmd_chstart)
    x=s.add_parser("chapter-set"); x.add_argument("path"); x.add_argument("number",type=int); x.add_argument("--file",required=True); x.set_defaults(func=cmd_chset)
    x=s.add_parser("summary-set"); x.add_argument("path"); x.add_argument("number",type=int); x.add_argument("--file",required=True); x.set_defaults(func=cmd_sumset)
    x=s.add_parser("approve"); x.add_argument("path"); x.add_argument("number",type=int); x.set_defaults(func=cmd_approve)
    x=s.add_parser("canon-fact"); x.add_argument("path"); x.add_argument("text"); x.add_argument("--source",default="manual"); x.set_defaults(func=cmd_fact)
    x=s.add_parser("foreshadow-add"); x.add_argument("path"); x.add_argument("text"); x.add_argument("--chapter",type=int,required=True); x.add_argument("--target",type=int); x.set_defaults(func=cmd_fsadd)
    x=s.add_parser("foreshadow-resolve"); x.add_argument("path"); x.add_argument("id"); x.add_argument("--chapter",type=int,required=True); x.add_argument("--note",default=""); x.set_defaults(func=cmd_fsres)
    x=s.add_parser("cover-set"); x.add_argument("path"); x.add_argument("file"); x.set_defaults(func=cmd_cs)
    x=s.add_parser("export"); x.add_argument("path"); x.add_argument("format",choices=["txt","md","html","docx","epub","pdf"]); x.set_defaults(func=cmd_export)
    x=s.add_parser("serve"); x.add_argument("path"); x.add_argument("--host",default="127.0.0.1"); x.add_argument("--port",type=int,default=8765); x.set_defaults(func=cmd_serve)
    return p

def main(argv=None):
    a=parser().parse_args(argv)
    try: a.func(a)
    except Exception as e: print(f"ERROR: {e}",file=sys.stderr); raise SystemExit(2)
if __name__=="__main__": main()
