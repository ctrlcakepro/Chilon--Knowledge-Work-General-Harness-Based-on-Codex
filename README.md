[README.md](https://github.com/user-attachments/files/29607259/README.md)
# Chilon--Knowledge-Work-General-Harness-Based-on-Codex
A layered Codex harness for long-term knowledge work, project bootstrapping, reusable workflows, and project-specific AGENTS generation.
# Codex Harness Public

一套可复用的 Codex harness 发布版，适合放进公开 GitHub 仓库。

这份公开版包含三部分：

1. `AGENTS.md`
全局层协作规则、任务分流、工具优先级、交付底线

2. `knowledge-workbench/`
中层工作台，包括模板、playbooks、评分层、校准与 benchmark

3. `skills/project-harness-bootstrap/`
一个可复用 skill。输入项目描述后，它会在项目根目录生成该项目的：
- `AGENTS.md`
- `PROJECT-WORKFLOW.md`

## 适合谁

适合想把 Codex 从“单次聊天助手”改造成“可重复启动的长期工作系统”的用户，尤其适合：

- 知识工作
- 写作与审稿
- 汇报与演示
- 结构化项目协作
- 多项目并行工作

## 目录结构

- `AGENTS.md`
- `knowledge-workbench/`
- `skills/project-harness-bootstrap/`

## 设计原则

这套 harness 采用三层结构：

1. 全局层
只保留跨项目都稳定成立的规则，例如协作方式、任务分流、工具优先级、交付底线与可靠性。

2. 工作台层
把高频 workflow 下沉到 `knowledge-workbench/`，避免把所有细节堆在顶层。

3. 项目层
每个项目再根据自身目标、交付物和工具面，生成自己的 `AGENTS.md` 与 `PROJECT-WORKFLOW.md`。

## 安装方式

把仓库中的文件复制到你的 Codex 主目录中：

1. 复制根目录 `AGENTS.md` 到：
   `~/.codex/AGENTS.md`

2. 复制 `knowledge-workbench/` 到：
   `~/.codex/knowledge-workbench/`

3. 复制 `skills/project-harness-bootstrap/` 到：
   `~/.codex/skills/project-harness-bootstrap/`

如果你已经有自己的全局 `AGENTS.md`，建议先人工合并，而不是直接覆盖。

## 如何使用项目初始化 skill

安装完成后，可以在一个新项目里直接调用：

    Use $project-harness-bootstrap to create a project-root harness from this project description.

或者中文使用：

    用 $project-harness-bootstrap 根据下面这段项目描述，在项目根目录生成 AGENTS.md 和 PROJECT-WORKFLOW.md。

推荐输入至少包含：

- 项目是做什么的
- 核心重复任务有哪些
- 主要交付物有哪些
- 希望优先使用哪些工具
- 哪些操作需要确认

## 这份公开版没有包含什么

为了适合公开发布，这个仓库没有包含你的本机环境内容，例如：

- `config.toml`
- 认证文件
- 插件缓存
- session / sqlite 状态文件
- 私人 API key
- 本机自动化与状态库

## 发布前建议

如果你要正式公开发布，建议再补两样：

1. 一个开源许可证文件，例如 `MIT` 或 `Apache-2.0`
2. 一份简单的版本记录，说明你后续如何演进这套 harness

## 推荐仓库说明

如果你准备发 GitHub，可以把这个仓库理解成：

“A layered Codex harness for long-term knowledge work, project bootstrapping, and reusable workflows.”
