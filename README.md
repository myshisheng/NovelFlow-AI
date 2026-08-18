# NovelFlow AI 📚🤖

**一个脑洞 → 书名/简介 → 人设/世界观 → 总纲/分卷/细纲 → 封面 → 连载正文 → 审稿/连贯性 → 伏笔回收 → 大结局/番外 → TXT/Markdown/HTML/DOCX/EPUB/PDF。**

NovelFlow AI 不绑定某一家模型。它把小说工程状态独立保存，所以可以随时换 Codex、Claude Code、Gemini CLI、Cursor、Windsurf、Cline、Roo、OpenCode、Aider，或任何能够读取文件、执行终端命令或调用 MCP 的桌面 AI。

> v0.1.2 新增项目健康检查：使用 `novelflow doctor` 可以在继续写作、迁移项目或交给桌面 AI 接管前，检查目录、Canon、任务与已批准章节是否完整。

## 快速开始

```bash
python -m pip install -e .
novelflow --version

novelflow init ./my-book \
  --idea "都市异能：主角每天可以暂停时间十秒" \
  --platform "番茄" \
  --genre "都市异能" \
  --target-words 1500000 \
  --chapters 600

novelflow bootstrap ./my-book
novelflow doctor ./my-book
novelflow status ./my-book
novelflow prompt ./my-book
```

然后对桌面 AI 说：

```text
继续 NovelFlow 项目。读取 AGENTS.md，先运行 novelflow doctor 检查项目，再领取下一个任务，按任务提示完成并提交，然后继续推进。
```

## 一条龙工作流

```text
创意/平台定位
   ↓
metadata（书名、简介、标签、卖点）
   ├────────→ cover_brief → 生成/导入封面
   ↓
story_bible（人物、世界观、能力规则）
   ↓
master_outline（总纲、分卷、结局约束）
   ↓
chapter_plan:N
   ↓
正文 → 审稿 → 连贯性/Canon → 摘要 → 批准
   ↓
chapter_plan:N+1 → ... → finale → epilogue → final audit → export
```

## 项目自检

```bash
novelflow doctor ./my-book
```

`doctor` 会检查：

- `novel.json` 的关键字段和项目目录是否完整；
- `metadata.md`、`story_bible.md`、`master_outline.md` 是否存在；
- `state/canon.json` 是否可解析、关键数据结构是否存在；
- `tasks/*.json` 是否损坏、任务状态是否合法；
- 已批准章节是否同时存在正文和摘要；
- `approved_chapters` 与批准章节编号列表是否一致。

检查通过时输出 `"ok": true`。发现会破坏工作流的错误时输出 `"ok": false`，并返回非零退出码，方便脚本、CI 和桌面 AI 自动判断是否应停止继续生成。

## 通用兼容策略

1. **CLI**：只要桌面 AI 能运行终端，就能使用 `novelflow`。
2. **MCP**：支持 MCP 的客户端直接调用 NovelFlow 工具。
3. **规则文件**：仓库附带 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、Cursor/Windsurf/Cline/Copilot/Aider 配置。
4. **纯聊天 AI**：人工运行 `novelflow prompt` 后复制提示词过去，结果保存回来即可。

无法读取文件、不能执行终端、也不支持 MCP 的产品无法做到自动接管，但仍可作为人工 Worker 使用。

## 长篇记忆

NovelFlow 不把百万字全文反复塞给模型。`novelflow context` 组合：

- 项目定位与平台
- Metadata
- Story Bible
- Master Outline
- 硬事实
- 当前角色状态
- 未回收伏笔
- 最近 N 章摘要

```bash
novelflow context ./my-book --chapter 287 --last 5
```

## Canon / 伏笔

```bash
novelflow canon-fact ./my-book "林川每天最多暂停时间10秒" --source story_bible
novelflow foreshadow-add ./my-book "黑色怀表来源" --chapter 3 --target 320
novelflow foreshadow-resolve ./my-book FS_ID --chapter 318 --note "秦老揭示来源"
novelflow canon-report ./my-book
```

## 章节

```bash
novelflow chapter-start ./my-book 1 --title "十秒"
novelflow prompt ./my-book
novelflow chapter-set ./my-book 1 --file chapter-001.md
novelflow summary-set ./my-book 1 --file summary-001.md
novelflow approve ./my-book 1
```

`approve` 强制要求正文和摘要同时存在，避免正文推进了但长期记忆没更新。

## 封面

```bash
novelflow cover-placeholder ./my-book
novelflow cover-set ./my-book ./generated-cover.png
```

Bootstrap 会生成 `cover_brief` 任务，可交给任意图像模型/桌面 AI 生成封面。

## 导出

基础格式无需额外依赖：

```bash
novelflow export ./my-book txt
novelflow export ./my-book md
novelflow export ./my-book html
```

可选：

```bash
pip install -e '.[export]'
novelflow export ./my-book docx
novelflow export ./my-book epub
novelflow export ./my-book pdf
```

## 本地 Dashboard

```bash
novelflow serve ./my-book --port 8765
```

浏览器访问 `http://127.0.0.1:8765`。

## MCP

```bash
novelflow-mcp
```

示例配置见 `examples/mcp.json`。MCP tools 包含：项目初始化/状态、任务领取、任务提示、提交、上下文、章节、摘要、Canon、伏笔、导出等。

## 测试

```bash
python -m unittest discover -s tests -v
```

版本变更见 `CHANGELOG.md`。更多说明见 `docs/ARCHITECTURE.md`、`docs/DESKTOP_AI.md`、`docs/WORKFLOW.md`。
