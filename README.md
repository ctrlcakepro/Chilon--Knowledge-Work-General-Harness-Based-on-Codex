# Knowledge Work Harness for Codex

<p align="center">
  <b>A layered, maintainable, automation-aware Codex harness for real-world knowledge work.</b>
</p>

<p align="center">
  面向阅读、写作、整理、汇报与长期协作的知识工作底座
</p>

---

## Overview｜项目概览

这不是一份为了把提示词写得更长而拼出来的配置包，而是一套为了长期协作而整理出来的工作结构。它服务的不是一次性问答，而是那些真正会反复发生的任务：读书、做笔记、整理课程材料、写论文、搭提纲、准备汇报、精炼文档、修正表达、检查交付质量。它试图解决的核心问题不是“怎样回答得更多”，而是“怎样在有限上下文里，持续稳定地做出像成品的结果”。

<details>
<summary>English</summary>

This is not a package assembled to make prompts longer. It is a working structure built for long-term collaboration. It is meant for the kinds of tasks that truly repeat in real life: reading, note-taking, organizing course materials, writing papers, drafting outlines, preparing presentations, condensing documents, refining expression, and checking deliverable quality. Its core concern is not “how to say more,” but “how to keep producing stable, finished-feeling results within a limited context budget.”

</details>

很多个人 harness 会在变强之前先变重：规则越来越多，职责越来越乱，最后模型不是忘了执行，就是在不同规则之间摇摆。这套结构的出发点正好相反。它尽量把顶层压轻，把细节下沉到 workflow、memory、模板、回归样例和自动维护层，让系统更像一个有分工的工作台，而不是一条越来越长的提示词。

<details>
<summary>English</summary>

Many personal harnesses become heavy before they become strong: more rules, blurrier responsibilities, and eventually a model that either stops following them or keeps oscillating between competing instructions. This project starts from the opposite assumption. It keeps the top layer light and pushes detail into workflows, memory, templates, regression samples, and automated maintenance, so the system feels more like a structured workbench than an endlessly growing prompt.

</details>

---

## What It Is For｜适用场景

这套 harness 主要面向知识工作，而不是只面向代码工作。它特别适合章节总结、教材复习、论文与作业提纲、文献阅读摘要、汇报结构设计、PDF / Word 文档精炼、内容改写，以及那些“我需要一个能直接继续用的结果，而不是一堆方法解释”的请求。

<details>
<summary>English</summary>

This harness is aimed primarily at knowledge work rather than only coding work. It is especially suitable for chapter summaries, textbook review, paper and assignment outlines, literature summaries, presentation structuring, PDF or Word document condensation, content rewriting, and any request where the real need is “give me something I can keep using,” rather than “explain the method again.”

</details>

如果你经常在聊天窗口里重复做这些事，那么你真正需要的通常不是更多 prompt，而是更稳定的任务分流、更清楚的结构层次，以及更可靠的交付路径。这套包就是为这种需求准备的。

<details>
<summary>English</summary>

If you keep repeating these tasks in a chat window, what you usually need is not more prompting, but steadier task routing, clearer structural layers, and more reliable delivery paths. That is exactly the need this package is built for.

</details>

---

## Architecture｜功能架构

### 1. Top Layer

`AGENTS.md` 负责顶层协作协议，定义默认输出风格、提问边界、任务分流原则和可靠性要求。它只保留跨任务稳定成立的规则，不承载专题 workflow、学科细节或一次性补丁。

<details>
<summary>English</summary>

`AGENTS.md` holds the top-level collaboration protocol: default output style, questioning boundaries, task-routing principles, and reliability rules. It keeps only rules that remain stable across tasks, and deliberately avoids carrying topic-specific workflows, domain detail, or one-off patches.

</details>

### 2. Project Workflow Layer

`PROJECT-WORKFLOW.md` 负责项目级默认流程，把常见请求映射到更具体的执行路径，例如阅读总结、知识整理、比较分析、论文写作、展示准备、文本修改和文件交付。

<details>
<summary>English</summary>

`PROJECT-WORKFLOW.md` defines the default project-level flows, mapping common requests into more concrete execution paths such as reading summaries, knowledge organization, comparative analysis, academic writing, presentation prep, text revision, and formal file delivery.

</details>

### 3. Explicit Memory Layer

`.project-memory/` 是显式 memory layer，用来保存长期偏好、项目状态、决策记录、知识缓存、交付规范和自动化索引。重点不在于“什么都记住”，而在于只保存那些会稳定影响后续协作的内容。

<details>
<summary>English</summary>

`.project-memory/` is the explicit memory layer. It stores durable preferences, project state, decision logs, knowledge cache, delivery specs, and automation indexes. The goal is not to remember everything, but to preserve only what will keep shaping future collaboration in a stable way.

</details>

### 4. Governance Scripts

`tools/check_harness.py` 会检查关键文件存在性、关键引用是否断裂、核心文件是否超预算、误广加载预算是否过重、全量平铺是否会明显变重，以及旧命名或实验残留是否还存在。  
`tools/auto_cold_layer_maintenance.py` 会扫描冷层文件，估算 token 压力，识别高体量候选、近重复热点和收缩优先级，并生成每周 / 每月维护报告。

<details>
<summary>English</summary>

`tools/check_harness.py` validates critical file presence, key reference integrity, file-size budgets, accidental broad-load pressure, full-flatten heaviness, and legacy naming or experimental residue.  
`tools/auto_cold_layer_maintenance.py` scans the cold layer, estimates token pressure, identifies large candidates, near-duplicate hotspots, and compression priority, then generates weekly and monthly maintenance reports.

</details>

### 5. Regression and Drills

`harness-regression/` 是这套结构的安全网。这里保存最小回归样例和专项演练材料，帮助你在调整规则、收缩文件或修改路由之后，确认高频能力没有被悄悄做坏。

<details>
<summary>English</summary>

`harness-regression/` is the safety net for the structure. It stores minimal regression cases and targeted drills so that after changing rules, compressing files, or modifying routing, you can confirm that high-frequency capabilities have not been quietly damaged.

</details>

---

## Technical Design｜技术设计细节

这套 harness 明确区分了热路径和冷路径。热路径包括 `AGENTS.md`、`PROJECT-WORKFLOW.md`、`.project-memory/README.md` 和少数几个高频路由文件，它们负责在任务开始时提供最小可用上下文。冷路径则由更细的 memory、delivery spec、knowledge cache 和回归材料组成，只在真正需要时再读取。这种设计不是装饰性的分层，而是直接服务于 token 预算控制。

<details>
<summary>English</summary>

This harness explicitly separates hot paths from cold paths. The hot path includes `AGENTS.md`, `PROJECT-WORKFLOW.md`, `.project-memory/README.md`, and a small set of high-frequency routing files that provide the minimum viable context at task start. The cold path contains more detailed memory files, delivery specs, knowledge cache, and regression material, which are only read when actually needed. This is not decorative layering; it directly serves token-budget control.

</details>

治理逻辑上，它也不是默认“规则越多越好”。相反，它把规则本身当成需要持续检查的对象。`check_harness.py` 提供结构健康检查，`auto_cold_layer_maintenance.py` 提供冷层压缩报告，而两个 Codex 自动化任务会基于这些报告做每周轻维护和每月深检。这意味着这套系统不仅能工作，还会持续检查自己有没有变重、变乱或变得不值得继续扩张。

<details>
<summary>English</summary>

From a governance perspective, the system does not assume “more rules are better.” Instead, it treats the rules themselves as something that must be inspected continuously. `check_harness.py` provides structural health checks, `auto_cold_layer_maintenance.py` provides cold-layer compression reports, and the two Codex automation jobs use those reports for weekly light maintenance and monthly deep audits. In other words, the system is designed not only to work, but to keep checking whether it has become too heavy, too messy, or no longer worth expanding.

</details>

---

## Package Structure｜目录结构

```text
.
├─ AGENTS.md
├─ PROJECT-WORKFLOW.md
├─ .project-memory/
│  ├─ README.md
│  ├─ decision-log.md
│  ├─ project-state.md
│  ├─ capability-fallback-matrix.md
│  ├─ tool-delivery-routing.md
│  └─ knowledge-cache/
├─ tools/
│  ├─ check_harness.py
│  └─ auto_cold_layer_maintenance.py
├─ harness-regression/
│  ├─ cases/
│  └─ drills/
├─ automations/
│  ├─ weekly-harness-maintenance.toml
│  └─ monthly-harness-deep-audit.toml
├─ install.ps1
└─ install.cmd
```

---

## Installation｜安装方式

### Quick Install

Windows 下最简单的安装方式是直接双击 `install.cmd`。

<details>
<summary>English</summary>

The simplest installation path on Windows is to double-click `install.cmd`.

</details>

### Manual Install

如果你更习惯手动执行，可以运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

安装脚本会要求你输入目标项目目录，然后自动安装以下内容：

- `AGENTS.md`
- `PROJECT-WORKFLOW.md`
- `.project-memory/`
- `harness-regression/`
- `tools/`
- `automations/*.toml`（默认安装）

<details>
<summary>English</summary>

If you prefer a manual path, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

The installer will ask for the target project directory and then install:

- `AGENTS.md`
- `PROJECT-WORKFLOW.md`
- `.project-memory/`
- `harness-regression/`
- `tools/`
- `automations/*.toml` (installed by default)

</details>

### Skip Automations

如果你暂时不想安装自动化任务，可以运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -SkipAutomations
```

### Safety Behavior

安装时，脚本会自动把目标目录内同名文件和目录备份到 `.harness-install-backup/<timestamp>/`，因此即使是在已有项目上覆盖安装，也保留了回退空间。

<details>
<summary>English</summary>

During installation, the script automatically backs up existing files and directories with the same names into `.harness-install-backup/<timestamp>/`, so even if you install over an existing project, you still keep a rollback path.

</details>

---

## Recommended First Checks｜安装后建议

安装完成后，建议先运行一次结构检查：

```bash
python tools/check_harness.py
```

如果你想快速看一眼冷层压力，再运行一次：

```bash
python tools/auto_cold_layer_maintenance.py --mode weekly
```

这样你在真正开始使用之前，就能知道这套 harness 当前是“结构健康”“接近扩张边界”还是“已经需要收缩”。

<details>
<summary>English</summary>

After installation, it is a good idea to run a structural check:

```bash
python tools/check_harness.py
```

If you also want a quick view of cold-layer pressure, run:

```bash
python tools/auto_cold_layer_maintenance.py --mode weekly
```

That way, before real use begins, you already know whether the harness is structurally healthy, approaching expansion limits, or already due for compression.

</details>

---

## Closing Note｜最后的话

如果你想要的不是一个“看起来很全”的提示词合集，而是一套能随着真实任务一起成长、还能持续检查自己有没有变重的工作结构，那么这份包会是一个不错的起点。它不假装自己已经是成熟产品，但它已经把最重要的事情做对了：分层、治理、交付意识、自动维护，以及对上下文预算的尊重。

<details>
<summary>English</summary>

If what you want is not a prompt bundle that merely looks comprehensive, but a working structure that can grow alongside real tasks and keep checking whether it has become too heavy, this package is a strong starting point. It does not pretend to be a finished product, but it already gets the important things right: layering, governance, deliverable awareness, automated maintenance, and respect for context budgets.

</details>
