from __future__ import annotations
from pathlib import Path
from .storage import manifest
from .util import read_json, read_text

def _clip(text:str,limit:int)->str:
    text=text.strip(); return text if len(text)<=limit else text[:limit]+"\n…[truncated]"
def _chars(chars:dict)->str:
    if not chars:return "(none recorded)"
    lines=[]
    for name,data in chars.items():
        if isinstance(data,dict): lines.append(f"- {name}: status={data.get('status','active')}; location={data.get('location','')}; {data.get('notes','')}")
        else: lines.append(f"- {name}: {data}")
    return "\n".join(lines)
def _foreshadow(items:list[dict])->str:
    if not items:return "(none)"
    return "\n".join(f"- [{x.get('id')}] ch{x.get('introduced_chapter')}: {x.get('text')} (target {x.get('target_chapter','?')})" for x in items)
def build_context(root:Path,chapter:int|None=None,last:int=5)->str:
    m=manifest(root); c=read_json(root/"state"/"canon.json",{}); sums=c.get("chapter_summaries",{})
    nums=sorted(int(k) for k in sums if str(k).isdigit() and (chapter is None or int(k)<chapter))[-last:]
    recent="\n".join(f"### Chapter {n}\n{sums.get(str(n),'')}" for n in nums) or "(none yet)"
    facts=[x for x in c.get("facts",[]) if x.get("active",True)][-80:]; unresolved=[x for x in c.get("foreshadowing",[]) if x.get("status")!="resolved"]
    return f"""## Project
Title: {m.get('title') or '(working title)'}
Idea: {m.get('idea')}
Platform: {m.get('platform')}
Genre: {m.get('genre')}
Target: {m.get('target_words')} words / {m.get('target_chapters')} chapters
Approved chapters: {m.get('approved_chapters',0)}

## Metadata
{_clip(read_text(root/'metadata.md'),5000)}

## Story Bible
{_clip(read_text(root/'story_bible.md'),9000)}

## Master Outline
{_clip(read_text(root/'master_outline.md'),9000)}

## Active hard facts
{chr(10).join('- '+x.get('text','') for x in facts) or '- none recorded'}

## Character state
{_clip(_chars(c.get('characters',{})),7000)}

## Unresolved foreshadowing
{_clip(_foreshadow(unresolved),5000)}

## Recent chapter summaries
{recent}
"""
