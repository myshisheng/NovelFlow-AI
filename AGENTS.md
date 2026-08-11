# NovelFlow AI — Universal Agent Instructions

You are operating a NovelFlow AI repository. The novel state lives in files; never rely on chat memory as the source of truth.

## First actions
1. Run `novelflow status <project>`.
2. Run `novelflow next <project>`.
3. Run `novelflow prompt <project>` and obey the task contract.
4. Complete only the current task, save the result, then run `novelflow complete <project> TASK_ID --file RESULT`.

## Mandatory novel rules
- `state/canon.json` is authoritative continuity state.
- Do not silently change hard rules, deaths, relationships, inventory, dates, or locations. Use an explicit retcon task.
- Use `novelflow context <project> --chapter N` for bounded long-form context; do not load the whole book for routine chapter work.
- Every approved chapter requires both final chapter text and a summary.
- Update canon/foreshadowing before chapter approval.
- Preserve platform, genre, audience, target length and style in `novel.json`.
- Never overwrite human-authored content silently.

## Quality contract
Each chapter must advance plot, character, relationship, mystery, progression, or world state. Avoid repetitive hooks, generic filler and unexplained power changes. End with a deliberate continuation impulse appropriate to the genre.

## Engineering rules
- Prefer Python standard library in core.
- Persistence stays transparent JSON/Markdown.
- Add tests for state transitions.
- Never commit secrets or API keys.
