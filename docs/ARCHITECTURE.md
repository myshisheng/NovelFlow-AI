# Architecture

NovelFlow separates orchestration state from model execution.

## Layers
1. Project store — transparent JSON/Markdown.
2. Workflow — durable task queue and chapter state transitions.
3. Context engine — bounded long-form context bundles.
4. Continuity engine — canon, timeline, foreshadowing and warnings.
5. Interfaces — CLI, MCP stdio, local dashboard.
6. Workers — desktop AI, humans, API models or automation.
7. Exporters — publication artifacts.

## Key rule
The model is a replaceable worker. The project files are the database.

## Chapter lifecycle
`planned -> drafted -> reviewed -> memory_updated -> approved`

v0.1 enforces the most important invariant: chapter approval requires both final chapter text and a chapter summary.
