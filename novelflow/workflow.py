from __future__ import annotations
from pathlib import Path
from typing import Any
from .storage import create_task, list_tasks, manifest, save_task

FOUNDATION_TASKS={
"metadata":("设计书名、简介、标签与商业定位","基于 novel.json 输出10个候选书名（标记首选）、一句话卖点、200-350字平台简介、分类/标签/关键词、目标读者、前三章核心钩子。避免抄袭现有作品标题/文案。","metadata.md",10),
"story_bible":("建立 Story Bible","建立人物、关系、世界观、能力规则、地点、组织、物品和禁改硬设定。明确主角欲望/缺陷/成长弧、主要配角功能、力量上限与代价。","story_bible.md",20),
"master_outline":("建立总纲、分卷与结局约束","输出全书主线、核心矛盾、分卷目标、关键转折、人物弧与结局承诺。只精细规划前20-30章，后续保持分卷级滚动规划。","master_outline.md",30),
"cover_brief":("生成封面创作 Brief","生成3套差异明显封面方向：构图、主体、背景、光影、字体留白、缩略图可读性、负面提示及适合图像模型的中文提示词。不要模仿在世艺术家的独特风格。","covers/cover_brief.md",40),
}

def bootstrap(root: Path) -> list[dict[str,Any]]:
    existing={t.get("kind") for t in list_tasks(root)}; made=[]
    for kind,(title,ins,target,prio) in FOUNDATION_TASKS.items():
        if kind not in existing: made.append(create_task(root,kind,title,ins,target=target,priority=prio))
    return made

def next_task(root: Path) -> dict[str,Any]|None:
    active=list_tasks(root,"in_progress")
    if active: return active[0]
    pending=list_tasks(root,"pending")
    if not pending: return None
    t=pending[0]; t["status"]="in_progress"; save_task(root,t); return t

def chapter_start(root: Path, number: int, title: str="") -> dict[str,Any]:
    kind=f"chapter_plan:{number}"
    for t in list_tasks(root):
        if t.get("kind")==kind and t.get("status")!="cancelled": return t
    ins=f"为第{number}章制定可执行细纲。章名暂定：{title or '由你建议'}。必须说明本章目标、承接点、主要冲突、信息增量、人物推进、具体场景、爽点/情绪点（如适用）、结尾继续阅读动力、需要更新的Canon/伏笔。不要直接写正文。"
    return create_task(root,kind,f"第{number}章细纲",ins,target=f"artifacts/chapter-{number:04d}-plan.md",metadata={"chapter":number,"title":title,"platform":manifest(root).get("platform")})

def task_prompt(root: Path, task: dict[str,Any], context: str) -> str:
    return f"""# NovelFlow Task Contract
Task ID: {task['id']}
Kind: {task['kind']}
Title: {task['title']}

## Project context
{context}

## Task
{task['instructions']}

## Output rules
- 只输出这个任务的最终可用结果，不讨论流程。
- 不得违反 Canon 硬事实。
- 如发现冲突，顶部写 CANON_CONFLICT: 并给最小改动方案，不自行改硬设定。
- 长篇优先连续性、因果和人物动机，不堆砌新设定。
"""
