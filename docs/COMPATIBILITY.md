# Compatibility Matrix

NovelFlow's stable interface is CLI + MCP + file-backed state. Vendor-specific rule files are conveniences, not dependencies.

| Desktop AI / agent family | Included path | Primary route |
|---|---|---|
| OpenAI Codex CLI / terminal agents | AGENTS.md | CLI / MCP where available |
| Claude Code | CLAUDE.md + AGENTS.md | CLI / MCP |
| Gemini CLI | GEMINI.md + AGENTS.md | CLI / MCP |
| Cursor | .cursor/rules + AGENTS.md | MCP / terminal |
| Windsurf Cascade | .windsurf/rules + AGENTS.md | MCP / terminal |
| Cline | .clinerules + AGENTS.md | MCP / terminal |
| OpenCode | AGENTS.md | terminal / MCP configuration |
| GitHub Copilot coding agent/editor | .github/copilot-instructions.md | terminal/file tools |
| Aider | .aider.conf.yml + AGENTS.md | terminal |
| Other terminal-capable AI | AGENTS.md | CLI |
| Other MCP-capable AI | AGENTS.md | MCP |
| Pure chat AI | generated task prompt | manual copy in/out |

A product that cannot read local files, execute a terminal, or connect to MCP cannot automatically operate a local NovelFlow project. It can still be used manually as a worker.
