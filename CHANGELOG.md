# Changelog

所有重要版本变更记录在此文件中。

## 0.1.2 - 2026-08-18

### Added
- 新增 `novelflow doctor <project>` 项目自检命令。
- 新增项目结构、核心文档、Canon 状态、任务 JSON 与已批准章节完整性检查。
- 自检结果提供 `ok`、错误、警告及任务/章节/Canon 统计信息；发现结构错误时 CLI 返回非零退出码，方便桌面 AI 与自动化脚本判断项目是否可继续。
- 新增 doctor 健康项目与损坏章节摘要场景测试。

### Changed
- Python 包与 `pyproject.toml` 版本统一升级到 `0.1.2`。
- README 快速开始加入项目自检步骤，并补充 doctor 使用说明。

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
