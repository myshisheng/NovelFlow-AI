from __future__ import annotations
import json, re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\-\u4e00-\u9fff]+", "-", text, flags=re.UNICODE)
    return text.strip("-") or "novel"

def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists(): return default
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)

def read_text(path: Path, default: str = "") -> str:
    return path.read_text(encoding="utf-8") if path.exists() else default

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
