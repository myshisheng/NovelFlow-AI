# Changelog

所有重要版本变更记录在此文件中。

## 0.1.1 - 2026-08-12

### Added
- 新增 `novelflow --version`，可直接查看当前 CLI 版本。
- 新增本文件，开始记录版本更新历史。

### Changed
- 将 Python 包版本与 `pyproject.toml` 统一升级到 `0.1.1`。
- MCP Server 握手中的版本号改为读取统一的 `novelflow.__version__`，避免多处版本漂移。
- README 快速开始补充版本检查命令。

## 0.1.0 - 2026-08-11

### Added
- 项目状态、任务队列与多阶段小说工作流。
- Canon 长期记忆、伏笔管理、章节摘要与上下文打包。
- 封面、导出、CLI、本地 Dashboard 与 MCP stdio server。
- 桌面 AI 兼容规则、测试与 GitHub Actions。
