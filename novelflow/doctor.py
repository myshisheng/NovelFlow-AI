from __future__ import annotations
from pathlib import Path
from typing import Any

from .chapters import chapter_path, summary_path
from .storage import REQUIRED_DIRS, ensure_project, manifest
from .util import read_json

REQUIRED_MANIFEST_KEYS = ("schema_version", "id", "idea", "target_words", "target_chapters", "stage")
REQUIRED_CANON_KEYS = ("facts", "characters", "locations", "items", "foreshadowing", "timeline", "chapter_summaries")
VALID_TASK_STATUS = {"pending", "in_progress", "done"}


def diagnose(path: str | Path) -> dict[str, Any]:
    root = ensure_project(path)
    errors: list[str] = []
    warnings: list[str] = []

    data = manifest(root)
    missing_manifest = [key for key in REQUIRED_MANIFEST_KEYS if key not in data]
    if missing_manifest:
        errors.append("novel.json missing keys: " + ", ".join(missing_manifest))

    for dirname in REQUIRED_DIRS:
        if not (root / dirname).is_dir():
            errors.append(f"missing directory: {dirname}/")

    for filename in ("metadata.md", "story_bible.md", "master_outline.md"):
        if not (root / filename).is_file():
            warnings.append(f"missing project document: {filename}")

    canon_path = root / "state" / "canon.json"
    canon: dict[str, Any] = {}
    if not canon_path.exists():
        errors.append("missing canon state: state/canon.json")
    else:
        try:
            loaded = read_json(canon_path, {})
            if not isinstance(loaded, dict):
                errors.append("state/canon.json must contain a JSON object")
            else:
                canon = loaded
                missing_canon = [key for key in REQUIRED_CANON_KEYS if key not in canon]
                if missing_canon:
                    warnings.append("canon missing keys: " + ", ".join(missing_canon))
        except Exception as exc:
            errors.append(f"invalid state/canon.json: {exc}")

    task_count = 0
    task_errors = 0
    task_dir = root / "tasks"
    if task_dir.is_dir():
        for task_file in sorted(task_dir.glob("*.json")):
            task_count += 1
            try:
                task = read_json(task_file, {})
                if not isinstance(task, dict):
                    raise ValueError("task must be a JSON object")
                for key in ("id", "kind", "status"):
                    if not task.get(key):
                        raise ValueError(f"missing {key}")
                if task.get("status") not in VALID_TASK_STATUS:
                    raise ValueError(f"invalid status {task.get('status')!r}")
            except Exception as exc:
                task_errors += 1
                errors.append(f"invalid task {task_file.name}: {exc}")

    approved = data.get("approved_chapter_numbers", [])
    if not isinstance(approved, list):
        errors.append("approved_chapter_numbers must be a list")
        approved = []
    approved_numbers: list[int] = []
    for value in approved:
        try:
            approved_numbers.append(int(value))
        except (TypeError, ValueError):
            errors.append(f"invalid approved chapter number: {value!r}")

    for number in approved_numbers:
        if not chapter_path(root, number).is_file():
            errors.append(f"approved chapter missing text: {number}")
        if not summary_path(root, number).is_file():
            errors.append(f"approved chapter missing summary: {number}")

    declared_approved = data.get("approved_chapters")
    if isinstance(declared_approved, int) and declared_approved != len(set(approved_numbers)):
        warnings.append(
            f"approved_chapters={declared_approved} but approved_chapter_numbers has {len(set(approved_numbers))} unique entries"
        )

    return {
        "ok": not errors,
        "project": str(root),
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "tasks": task_count,
            "invalid_tasks": task_errors,
            "approved_chapters": len(set(approved_numbers)),
            "canon_facts": len(canon.get("facts", [])) if isinstance(canon.get("facts", []), list) else 0,
            "unresolved_foreshadowing": sum(
                1
                for item in canon.get("foreshadowing", [])
                if isinstance(item, dict) and not item.get("resolved")
            )
            if isinstance(canon.get("foreshadowing", []), list)
            else 0,
        },
    }
