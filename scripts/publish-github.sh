#!/usr/bin/env bash
set -euo pipefail
REPO="${1:-NovelFlow-AI}"
VISIBILITY="${2:-public}"
if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is not installed." >&2
  exit 2
fi
if ! gh auth status >/dev/null 2>&1; then
  echo "GitHub CLI is not authenticated. Run: gh auth login" >&2
  exit 3
fi
case "$VISIBILITY" in
  public|private) ;;
  *) echo "Visibility must be public or private" >&2; exit 4;;
esac
gh repo create "$REPO" --source=. --"$VISIBILITY" --push
