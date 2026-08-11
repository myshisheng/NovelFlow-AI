from __future__ import annotations
import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from .canon import report
from .chapters import list_chapters
from .storage import list_tasks, manifest

def serve(root:Path,host:str="127.0.0.1",port:int=8765)->None:
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path not in ("/","/index.html"): self.send_error(404); return
            m=manifest(root); tasks=list_tasks(root); rep=report(root); chapters=list_chapters(root); pending=sum(t.get("status") in ("pending","in_progress") for t in tasks)
            rows="".join(f"<tr><td>{html.escape(t.get('kind',''))}</td><td>{html.escape(t.get('status',''))}</td><td>{html.escape(t.get('title',''))}</td></tr>" for t in tasks[-20:]); ch="".join(f"<li>第 {n} 章 - {html.escape(p.name)}</li>" for n,p in chapters[-30:]) or "<li>暂无正文</li>"
            body=f'''<!doctype html><meta charset="utf-8"><title>NovelFlow</title><style>body{{font-family:system-ui;max-width:1100px;margin:30px auto;background:#fafafa}}.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}.card{{background:#fff;border:1px solid #ddd;border-radius:12px;padding:16px}}table{{width:100%;border-collapse:collapse;background:#fff}}td,th{{padding:8px;border-bottom:1px solid #eee;text-align:left}}</style><h1>{html.escape(m.get('title') or '未定书名')}</h1><p>{html.escape(m.get('idea',''))}</p><div class="grid"><div class="card">阶段<br><b>{html.escape(m.get('stage',''))}</b></div><div class="card">已批准章节<br><b>{m.get('approved_chapters',0)}</b></div><div class="card">待处理任务<br><b>{pending}</b></div><div class="card">未回收伏笔<br><b>{rep['unresolved_foreshadowing']}</b></div></div><h2>任务</h2><table><tr><th>Kind</th><th>Status</th><th>Title</th></tr>{rows}</table><h2>章节</h2><ul>{ch}</ul>'''
            data=body.encode(); self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(data))); self.end_headers(); self.wfile.write(data)
        def log_message(self,*args): pass
    print(f"NovelFlow dashboard: http://{host}:{port}"); ThreadingHTTPServer((host,port),H).serve_forever()
