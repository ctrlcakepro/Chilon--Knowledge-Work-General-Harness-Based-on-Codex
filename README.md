# Chilon Knowledge Work Harness

<p align="center">
  <b>把 AI 从一次性聊天窗口，变成可复用、可维护、可迁移的知识工作台。</b>
</p>

<p align="center">
  A portable AI workbench for reading, writing, studying, summarizing, and long-term knowledge work.
</p>

---

## Chilon 是什么？

Chilon 是一套面向长期知识工作的 AI harness。它不是单条提示词，也不是为了炫技堆出来的 agent 框架，而是一套可以放进真实学习、写作、研究和资料整理流程里的工作结构。它适合那些会反复发生的任务：读教材、整理课程材料、写论文、做文献摘要、比较理论、准备汇报、修改文档、沉淀偏好、复用模板，以及把聊天结果整理成可以继续使用的成品。

很多人一开始用 AI 会不断加提示词：要求越来越多，规则越来越长，最后模型反而更容易摇摆、忘记重点，或者每次都像重新开始。Chilon 的思路相反：顶层规则保持轻量，把 workflow、memory、交付规范、知识缓存、回归样例和维护脚本分层放好。这样 AI 不需要每次都吞下一整包规则，而是按任务加载最小必要上下文。

Chilon is a portable harness for long-term knowledge work. It is not a single mega-prompt or a heavy agent framework. It organizes workflows, memory, delivery rules, reusable structures, and maintenance checks so an AI workspace can keep producing usable results across repeated reading, writing, studying, and research tasks.

---

## 它解决什么问题？

如果你经常用 AI 做知识工作，你大概率会遇到这些问题：

- 每次都要重新解释自己的任务习惯。
- 提示词越写越长，但效果没有稳定变好。
- AI 能回答，但输出不像可以继续用的成品。
- 笔记、论文、汇报、复习材料之间没有统一工作流。
- 长期偏好和项目状态散落在聊天记录里，很难复用。
- 一套规则改多了以后，不知道有没有把原本好用的能力改坏。

Chilon 的目标不是让 AI “看起来更复杂”，而是让它更像一个有分工的知识工作台：先判断任务类型，再选择工作流，只加载必要上下文，最后产出摘要、提纲、表格、草稿、复习笔记、汇报结构或正式交付物。

The core problem Chilon addresses is workspace drift. Without structure, prompts grow longer, memory becomes unreliable, and repeated work starts from zero again and again. Chilon gives the workspace a maintainable shape.

---

## 先看这四个入口

如果你第一次看这个项目，建议先看这四个文件。它们解决“规则谁优先、是否安全、有没有真实示例、能不能轻量试用”四个最常见问题。

| 入口 | 解决的问题 | 文件 |
|---|---|---|
| 规则优先级 | 当用户要求、项目规则、workflow、memory 或 adapter 冲突时，应该听谁的？ | `docs/RULE-PRECEDENCE.md` |
| 隐私与安全 | 哪些 memory、路径、账号、客户信息不能提交到公共仓库？ | `docs/PRIVACY.md` + `templates/.gitignore.example` |
| 完整示例 | Chilon 用在真实学习项目里到底长什么样？ | `examples/academic-study-project/` |
| 轻量模式 | 不想一开始维护完整 harness，只想快速试用怎么办？ | `lite/AGENTS.lite.md` |

最简单的试用方式：如果你只有 1 到 2 个项目，先复制 `lite/AGENTS.lite.md` 到项目根目录并重命名为 `AGENTS.md`；如果你主要用 Claude Desktop，先看 `adapters/claude-desktop/`；如果你想要完整结构，再使用 Codex 主版本。

---

## 适合做什么？

Chilon 主要面向知识工作，而不是只面向代码工作。它特别适合：

- 章节总结、教材复习、课程材料整理
- 心理学、社会科学、人文社科类学习笔记
- 文献阅读摘要、理论比较、观点辨析
- 论文、作业、短评、综述的提纲与初稿
- 课堂汇报、组会汇报、slides 结构设计
- PDF / Word 文档精炼、改写、润色与检查
- 长期项目状态、偏好和可复用模板沉淀
- 个人 AI 工作流、学习助手、研究助手搭建

如果你想要的不是一句“建议你可以……”，而是一个能继续加工、复制、提交、复习或放进文档里的结果，Chilon 会更适合你。

---

## 版本说明

Chilon 现在包含一个主版本和一个轻量适配包。

| 版本 | 适合谁 | 包含内容 |
|---|---|---|
| **Chilon for Codex** | 想要完整本地 harness、项目级文件结构、自动维护和回归检查的用户 | `AGENTS.md`、`PROJECT-WORKFLOW.md`、`.project-memory/`、治理脚本、回归样例、自动化模板、安装脚本 |
| **Chilon for Claude Desktop** | 主要使用 Claude Desktop / Claude Project，希望轻量导入知识工作结构的用户 | Project instructions、Custom instructions、可上传的 workflow / memory / delivery knowledge files |
| **Chilon Lite** | 只有 1 到 2 个项目，想先快速试用 Chilon 工作方式的用户 | 单文件 `lite/AGENTS.lite.md`，不包含完整 memory、治理脚本和回归层 |

Codex 版本是完整主版本。Claude Desktop 版本不是另一个独立项目，而是把同一套 Chilon 思路转换成 Claude Project 更容易使用的形式。Lite 版本则是最低门槛入口，用来先体验 Chilon 的任务分流和输出风格。

---

## 平台适配状态

| 平台 / 工作台 | 当前状态 | 说明 |
|---|---|---|
| **Codex** | ✅ 已支持，主版本 | 当前最完整版本，包含项目文件、显式 memory、治理脚本、回归样例、自动化模板和安装脚本。 |
| **Claude Desktop / Claude Project** | ✅ 已支持，轻量适配包 | 已提供 `adapters/claude-desktop/`，可复制 Project instructions，并上传 workflow / memory / delivery 文件作为 Project Knowledge。 |
| **Claude Code** | 🟡 可扩展，暂未单独适配 | 理论上可以基于 `AGENTS.md` 和 Claude Desktop 指令改成 `CLAUDE.md`，但当前仓库还没有单独提供 Claude Code 版。 |
| **Cherry Studio** | 🟡 计划中 | 适合做成助手预设 + 知识库文件 + 可选 MCP 配置，后续会放在 `adapters/cherry-studio/`。 |
| **ChatGPT Projects / Custom GPT** | 🟡 计划评估 | 可以迁移核心 workflow 和 memory 思路，但需要重新设计为 ChatGPT 项目指令或 Custom GPT knowledge 文件。 |
| **Dify / AnythingLLM / RAGFlow** | ⚪ 暂未适配 | 这些更偏应用编排或知识库平台，适配方式会不同，当前不是优先目标。 |
| **纯提示词复制使用** | 🟡 可用但不推荐作为主方式 | 可以复制核心指令临时使用，但 Chilon 的价值主要来自分层结构，而不是单条 prompt。 |

如果你不确定该用哪个版本，可以先这样选：想要完整结构和本地项目维护，选 Codex；主要在 Claude Desktop 里学习、写作、整理资料，选 Claude Desktop；只是想试试理念，可以先看 `lite/AGENTS.lite.md` 或 `adapters/claude-desktop/custom-instructions.md`。

---

## 快速开始

### 方式一：用轻量模式快速试用

如果你只有 1 到 2 个项目，或者只是想先体验 Chilon 的工作方式，不需要立刻安装完整 harness。

复制：

```text
lite/AGENTS.lite.md
```

到你的项目根目录，并重命名为：

```text
AGENTS.md
```

这会给项目提供最小可用的 Chilon 行为协议：任务分流、追问边界、输出风格、记忆原则和交付前自检。

### 方式二：在 Codex 项目中使用完整版本

克隆仓库后，把 harness 安装到你的目标项目目录。

Windows 下最简单的方式是双击：

```text
install.cmd
```

或者手动运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -TargetDir "C:\path\to\your\project"
```

macOS / Linux 下运行：

```bash
chmod +x ./install.sh
./install.sh --target /path/to/your/project
```

安装脚本会把核心 harness 文件复制到目标项目，并在覆盖同名文件前自动备份。

### 方式三：在 Claude Desktop 中使用

打开：

```text
adapters/claude-desktop/
```

推荐用法：

1. 在 Claude Desktop 里创建一个 Claude Project，例如 `Chilon Knowledge Work`。
2. 把 `adapters/claude-desktop/project-instructions.md` 的内容复制到 Project instructions。
3. 把 `adapters/claude-desktop/import-files/` 下的文件上传为 Project Knowledge。
4. 从真实任务开始测试，例如整理一章教材、规划一篇论文、修改一份文档。

如果你不使用 Claude Project，也可以把 `adapters/claude-desktop/custom-instructions.md` 复制到 Claude Desktop 的自定义指令里，作为轻量版使用。

---

## 工作原理

Chilon 的核心原则是：不要把所有东西都塞进当前上下文。稳定规则放在热路径，细节规则放在冷路径；常用 workflow 保持可复用，长期偏好显式保存，低频知识按需加载。

### 1. 顶层协议：`AGENTS.md`

`AGENTS.md` 定义 AI 的基本协作方式：默认输出风格、任务分流原则、追问边界、可靠性要求和文件约定。它只保留跨任务稳定成立的规则，不承载一次性补丁。

### 2. 项目工作流：`PROJECT-WORKFLOW.md`

`PROJECT-WORKFLOW.md` 把常见请求映射到具体流程，例如阅读总结、知识整理、比较分析、论文写作、汇报准备、文本修改、事实核对和正式文件交付。

### 3. 显式记忆层：`.project-memory/`

`.project-memory/` 用来保存长期偏好、项目状态、决策记录、可复用素材、交付规范、能力路由和知识缓存。重点不是“什么都记住”，而是只保存那些会稳定影响后续协作的内容。

### 4. 治理脚本：`tools/`

`tools/check_harness.py` 和 `tools/auto_cold_layer_maintenance.py` 用来检查结构健康、文件预算、引用完整性、冷层体量和维护优先级。Chilon 把规则本身也当作需要维护的对象，而不是默认越多越好。

### 5. 回归样例：`harness-regression/`

`harness-regression/` 保存最小回归样例和专项演练材料。每次修改规则、压缩 memory 或调整路由后，可以用它检查高频能力有没有被改坏。

---

## 项目结构

```text
.
├─ AGENTS.md
├─ PROJECT-WORKFLOW.md
├─ .project-memory/
│  ├─ README.md
│  ├─ user-preferences.md
│  ├─ project-state.md
│  ├─ decision-log.md
│  ├─ reusable-assets.md
│  ├─ tool-delivery-routing.md
│  └─ knowledge-cache/
├─ docs/
│  ├─ RULE-PRECEDENCE.md
│  └─ PRIVACY.md
├─ templates/
│  └─ .gitignore.example
├─ lite/
│  └─ AGENTS.lite.md
├─ examples/
│  └─ academic-study-project/
├─ tools/
│  ├─ check_harness.py
│  └─ auto_cold_layer_maintenance.py
├─ harness-regression/
│  ├─ cases/
│  └─ drills/
├─ automations/
│  ├─ weekly-harness-maintenance.toml
│  └─ monthly-harness-deep-audit.toml
├─ adapters/
│  └─ claude-desktop/
│     ├─ README.md
│     ├─ project-instructions.md
│     ├─ custom-instructions.md
│     └─ import-files/
│        ├─ workflow-guide.md
│        ├─ memory-guide.md
│        └─ delivery-style.md
├─ install.ps1
├─ install.sh
└─ install.cmd
```

---

## 使用示例

安装或导入 Chilon 后，可以直接这样用：

```text
把这篇文章整理成适合复习的笔记。先给主线，再给关键概念、易混点和速记版。
```

```text
比较这两个理论。先列比较维度，再用表格整理，最后给适用场景判断。
```

```text
帮我把这份材料改成 8 分钟课堂汇报结构。重点是讲述顺序和每页主旨。
```

```text
检查这份文档是否像一个可提交版本。先指出主要问题，再给修改方向。
```

```text
基于我已有的笔记，帮我整理一个论文提纲。先给中心论点，再给章节结构和每部分要解决的问题。
```

想看完整落地例子，可以查看：

```text
examples/academic-study-project/
```

---

## 适合谁使用？

Chilon 适合把 AI 当作长期学习、研究、写作或知识管理伙伴的个人用户，尤其适合：

- 高校学生、研究生、教师和研究者
- 经常阅读教材、论文、报告和课程材料的人
- 需要写作业、论文、汇报、讲稿和文档的人
- 想搭建个人 AI 学习助手或研究助手的人
- 不想每次从零开始写提示词的人
- 希望 AI 输出更像成品，而不是只给建议的人

它不太适合只想偶尔问一句简短问题的用户，也不是一个完整的企业级 agent 平台。

---

## 安全提醒

不要把包含私人路径、账号信息、API Key、客户资料、商业策略、未公开研究材料或个人敏感信息的 `AGENTS.md` / `.project-memory/` 提交到公共仓库。

公开仓库应该保存结构和模板，私人上下文应该保存在本地。详见：

```text
docs/PRIVACY.md
templates/.gitignore.example
```

---

## 设计原则

- 顶层规则要轻，不要把所有东西都写进一个大 prompt。
- 任务先分流，再决定模板、工具和输出结构。
- memory 要显式、可维护、可复查，而不是无限堆积。
- 能用最小上下文完成的任务，不要平铺所有历史材料。
- 输出优先像成品，而不是像过程解释。
- 当前任务优先于历史记忆，项目规则优先于平台默认。
- 新增规则前先判断是否可以合并、下沉或删除旧规则。
- 尽量让同一套知识工作结构迁移到不同 AI 工作台。

---

## Roadmap

- [x] 公开 Codex harness 主版本
- [x] Claude Desktop 适配包
- [x] 规则优先级说明
- [x] 隐私与安全说明
- [x] `.gitignore` 安全模板
- [x] 轻量模式 `AGENTS.lite.md`
- [x] 第一个完整学术学习示例
- [ ] Claude Code 适配包
- [ ] Cherry Studio 适配包
- [ ] ChatGPT Projects / Custom GPT 适配评估
- [ ] 更完整的示例 workflow
- [ ] GitHub Actions 自动健康检查
- [ ] 5 分钟上手演示
- [ ] 中文使用案例与截图说明

---

## 为什么值得 Star？

如果你也觉得“不断堆提示词”不是长期方案，Chilon 可能值得一个 Star。

它尝试解决的是一个很真实的问题：如何把 AI 从一次性聊天工具，变成一个能长期协作、能复用结构、能沉淀偏好、能持续交付的知识工作台。

Star this project if you are interested in AI workspaces that are lighter than full agent frameworks, more durable than one-off prompts, and more practical than vague productivity advice.

---

## License

你可以把这个项目作为自己知识工作 harness 的起点。发布自己的修改版本前，请移除 `.project-memory/` 中的私人路径、账号信息、本地项目状态和任何个人材料。
