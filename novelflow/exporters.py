from __future__ import annotations
import html
from pathlib import Path
from .chapters import list_chapters
from .storage import manifest
from .util import read_text, write_text

def _parts(root:Path):
    m=manifest(root); parts=[]
    for n,p in list_chapters(root):
        text=read_text(p).strip(); title=f"第{n}章"
        for line in text.splitlines():
            s=line.strip().lstrip("#").strip()
            if s: title=s; break
        parts.append((n,title,text))
    return m,parts

def export_book(root:Path,fmt:str)->Path:
    fmt=fmt.lower(); m,parts=_parts(root); out=root/"exports"; out.mkdir(exist_ok=True); title=m.get("title") or "novel"
    if fmt=="txt":
        p=out/"book.txt"; write_text(p,title+"\n\n"+"\n\n".join(x[2] for x in parts)); return p
    if fmt=="md":
        p=out/"book.md"; write_text(p,f"# {title}\n\n"+"\n\n---\n\n".join(x[2] for x in parts)); return p
    if fmt=="html":
        p=out/"book.html"; toc="".join(f'<li><a href="#ch{n}">{html.escape(t)}</a></li>' for n,t,_ in parts); ch="".join(f'<section id="ch{n}"><h2>{html.escape(t)}</h2><pre>{html.escape(text)}</pre></section>' for n,t,text in parts); write_text(p,f'<!doctype html><meta charset="utf-8"><title>{html.escape(title)}</title><style>body{{max-width:820px;margin:40px auto;font-family:serif;line-height:1.8}}pre{{white-space:pre-wrap;font:inherit}}</style><h1>{html.escape(title)}</h1><ol>{toc}</ol>{ch}'); return p
    if fmt=="docx":
        try: from docx import Document
        except ImportError as e: raise RuntimeError("DOCX export requires: pip install -e '.[export]'") from e
        p=out/"book.docx"; d=Document(); d.add_heading(title,0)
        for _,t,text in parts:
            d.add_heading(t,1)
            for para in text.split("\n\n"):
                if para.strip() and not para.lstrip().startswith("#"): d.add_paragraph(para.strip())
        d.save(p); return p
    if fmt=="epub":
        try: from ebooklib import epub
        except ImportError as e: raise RuntimeError("EPUB export requires: pip install -e '.[export]'") from e
        p=out/"book.epub"; book=epub.EpubBook(); book.set_identifier(m.get("id","novelflow")); book.set_title(title); book.set_language("zh-CN"); eps=[]
        for n,t,text in parts:
            c=epub.EpubHtml(title=t,file_name=f"ch{n}.xhtml",lang="zh-CN"); c.content=f"<h1>{html.escape(t)}</h1><p>"+html.escape(text).replace("\n","<br/>")+"</p>"; book.add_item(c); eps.append(c)
        book.toc=tuple(eps); book.spine=["nav",*eps]; book.add_item(epub.EpubNcx()); book.add_item(epub.EpubNav()); epub.write_epub(str(p),book); return p
    if fmt=="pdf":
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
        except ImportError as e: raise RuntimeError("PDF export requires: pip install -e '.[export]'") from e
        p=out/"book.pdf"; c=canvas.Canvas(str(p),pagesize=A4); _,h=A4; y=h-60; c.setFont("Helvetica",14)
        for _,t,text in parts:
            for line in [t,*text.splitlines()]:
                if y<60: c.showPage(); c.setFont("Helvetica",10); y=h-60
                safe=line.encode("latin-1","replace").decode("latin-1")[:100]; c.drawString(50,y,safe); y-=14
        c.save(); return p
    raise ValueError(f"Unsupported format: {fmt}")
