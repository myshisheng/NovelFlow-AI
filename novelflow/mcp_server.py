from __future__ import annotations
import json,sys
from pathlib import Path
from typing import Any
from .canon import add_fact,add_foreshadow,report,resolve_foreshadow
from .chapters import approve,set_chapter,set_chapter_summary
from .context import build_context
from .exporters import export_book
from .storage import complete_task,ensure_project,get_task,init_project,manifest
from .workflow import bootstrap,chapter_start,next_task,task_prompt
PROTOCOL_VERSION="2025-11-25"
def S(props,req=None): return {"type":"object","properties":props,"required":req or [],"additionalProperties":False}
TOOLS=[
{"name":"project_init","description":"Create NovelFlow project","inputSchema":S({"path":{"type":"string"},"idea":{"type":"string"},"platform":{"type":"string"},"genre":{"type":"string"},"target_words":{"type":"integer"},"chapters":{"type":"integer"},"title":{"type":"string"}},["path","idea"])},
{"name":"project_status","description":"Read project and canon status","inputSchema":S({"path":{"type":"string"}},["path"])},
{"name":"bootstrap","description":"Create foundation tasks","inputSchema":S({"path":{"type":"string"}},["path"])},
{"name":"next_task","description":"Claim next task","inputSchema":S({"path":{"type":"string"}},["path"])},
{"name":"task_prompt","description":"Get task prompt with bounded context","inputSchema":S({"path":{"type":"string"},"task_id":{"type":"string"},"last":{"type":"integer"}},["path"])},
{"name":"complete_task","description":"Complete task with final text","inputSchema":S({"path":{"type":"string"},"task_id":{"type":"string"},"result":{"type":"string"}},["path","task_id","result"])},
{"name":"context_bundle","description":"Build chapter context","inputSchema":S({"path":{"type":"string"},"chapter":{"type":"integer"},"last":{"type":"integer"}},["path"])},
{"name":"chapter_start","description":"Create chapter plan task","inputSchema":S({"path":{"type":"string"},"number":{"type":"integer"},"title":{"type":"string"}},["path","number"])},
{"name":"chapter_set","description":"Save chapter text","inputSchema":S({"path":{"type":"string"},"number":{"type":"integer"},"text":{"type":"string"}},["path","number","text"])},
{"name":"summary_set","description":"Save summary and memory","inputSchema":S({"path":{"type":"string"},"number":{"type":"integer"},"text":{"type":"string"}},["path","number","text"])},
{"name":"chapter_approve","description":"Approve chapter","inputSchema":S({"path":{"type":"string"},"number":{"type":"integer"}},["path","number"])},
{"name":"canon_add_fact","description":"Add hard continuity fact","inputSchema":S({"path":{"type":"string"},"text":{"type":"string"},"source":{"type":"string"}},["path","text"])},
{"name":"foreshadow_add","description":"Add foreshadowing","inputSchema":S({"path":{"type":"string"},"text":{"type":"string"},"chapter":{"type":"integer"},"target":{"type":"integer"}},["path","text","chapter"])},
{"name":"foreshadow_resolve","description":"Resolve foreshadowing","inputSchema":S({"path":{"type":"string"},"id":{"type":"string"},"chapter":{"type":"integer"},"note":{"type":"string"}},["path","id","chapter"])},
{"name":"canon_report","description":"Continuity report","inputSchema":S({"path":{"type":"string"}},["path"])},
{"name":"export_book","description":"Export complete book","inputSchema":S({"path":{"type":"string"},"format":{"type":"string","enum":["txt","md","html","docx","epub","pdf"]}},["path","format"])}]
def R(path): return ensure_project(path)
def call(n,a):
    if n=="project_init": return {"path":str(init_project(a["path"],idea=a["idea"],platform=a.get("platform","番茄"),genre=a.get("genre","网文"),target_words=a.get("target_words",1000000),chapters=a.get("chapters",500),title=a.get("title","")))}
    r=R(a["path"])
    if n=="project_status": return {"project":manifest(r),"canon":report(r)}
    if n=="bootstrap": return bootstrap(r)
    if n=="next_task": return next_task(r)
    if n=="task_prompt":
        t=get_task(r,a["task_id"]) if a.get("task_id") else next_task(r); return {"task":t,"prompt":task_prompt(r,t,build_context(r,(t or {}).get("metadata",{}).get("chapter"),a.get("last",5))) if t else "NO_TASK"}
    if n=="complete_task": return complete_task(r,a["task_id"],a["result"])
    if n=="context_bundle": return {"context":build_context(r,a.get("chapter"),a.get("last",5))}
    if n=="chapter_start": return chapter_start(r,a["number"],a.get("title",""))
    if n=="chapter_set": return {"path":str(set_chapter(r,a["number"],a["text"]))}
    if n=="summary_set": return {"path":str(set_chapter_summary(r,a["number"],a["text"]))}
    if n=="chapter_approve": return approve(r,a["number"])
    if n=="canon_add_fact": return add_fact(r,a["text"],a.get("source","mcp"))
    if n=="foreshadow_add": return add_foreshadow(r,a["text"],a["chapter"],a.get("target"))
    if n=="foreshadow_resolve": return resolve_foreshadow(r,a["id"],a["chapter"],a.get("note",""))
    if n=="canon_report": return report(r)
    if n=="export_book": return {"path":str(export_book(r,a["format"]))}
    raise KeyError(n)
def response(q):
    m=q.get("method"); rid=q.get("id")
    if m=="notifications/initialized": return None
    if m=="initialize": return {"jsonrpc":"2.0","id":rid,"result":{"protocolVersion":q.get("params",{}).get("protocolVersion") or PROTOCOL_VERSION,"capabilities":{"tools":{"listChanged":False}},"serverInfo":{"name":"novelflow-ai","version":"0.1.0"}}}
    if m=="ping": return {"jsonrpc":"2.0","id":rid,"result":{}}
    if m=="tools/list": return {"jsonrpc":"2.0","id":rid,"result":{"tools":TOOLS}}
    if m=="tools/call":
        try:
            p=q.get("params",{}); x=call(p.get("name"),p.get("arguments",{})); return {"jsonrpc":"2.0","id":rid,"result":{"content":[{"type":"text","text":json.dumps(x,ensure_ascii=False,indent=2)}],"structuredContent":x if isinstance(x,dict) else {"result":x},"isError":False}}
        except Exception as e: return {"jsonrpc":"2.0","id":rid,"result":{"content":[{"type":"text","text":f"ERROR: {e}"}],"isError":True}}
    return None if rid is None else {"jsonrpc":"2.0","id":rid,"error":{"code":-32601,"message":f"Method not found: {m}"}}
def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try: q=json.loads(line); x=response(q); 
        except Exception as e: x={"jsonrpc":"2.0","id":None,"error":{"code":-32700,"message":str(e)}}
        if x is not None: sys.stdout.write(json.dumps(x,ensure_ascii=False,separators=(",",":"))+"\n"); sys.stdout.flush()
if __name__=="__main__": main()
