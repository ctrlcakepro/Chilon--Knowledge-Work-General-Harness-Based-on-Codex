# PROJECT-WORKFLOW

## 项目目标
把这个工作区作为长期知识工作的协作底座，用尽量少的顶层规则，稳定产出摘要、提纲、比较表、初稿、复习笔记、汇报结构与正式文件交付物。

这份文件负责说明“平时怎么跑”，而不是重复 `AGENTS.md` 的所有规则。

## 主要工作流
### 1. 阅读与知识整理
适用场景：
- 读文章、书章、课程材料
- 做摘要、结构梳理、概念区分、复习提要

默认动作：
- 先压缩理解，再结构化整理
- 优先调用 `reading-summary.md`、`review-outline.md` 或 `review-notes-spec.md`
- 输出先给主题、核心论点、关键概念，再补证据和可展开角度
- 如果任务明确是教材复习，优先给主线、考点、易混点和速记版

### 2. 比较与判断
适用场景：
- 理论比较
- 观点辨析
- 文本差异判断
- 方案优劣分析

默认动作：
- 先列比较维度
- 再给表格
- 最后给总结判断与适用边界

### 3. 论文、作业与长文写作
适用场景：
- 课程论文
- 作业分析
- 综述、短评、结构化写作

默认动作：
- 先明确题目与目标
- 再给论点路径与提纲
- 只有用户明确要求时再扩成完整正文

### 4. 汇报与展示
适用场景：
- 组会
- 课堂汇报
- 演讲型 slides
- 需要结构与气质判断的呈现任务

默认动作：
- 先判断听众与主信息
- 再设计展示顺序
- 每部分先给一句主旨
- 如果要交付演示文件，按演讲交付处理，不降级成普通网页或纯文本

### 5. 修改与评审
适用场景：
- 改一段文字
- 审稿规范检查
- 评审一版内容是否达标

默认动作：
- 先给总体判断
- 再指出主要问题
- 最后给修改建议或直接修改版本

## 默认处理顺序
1. 先看是否命中高频入口。
   优先参考 [`.project-memory\automation-entrypoints.md`](C:\Users\ROG\Documents\杂务\.project-memory\automation-entrypoints.md)。
2. 识别任务类型与主交付物。
3. 只加载当前任务需要的最小上下文。
   如果需要复用概念、比较维度或结构骨架，先看 [`.project-memory\knowledge-cache\index.md`](C:\Users\ROG\Documents\杂务\.project-memory\knowledge-cache\index.md)。
4. 判断是否需要模板、工具或联网核对。
   如果涉及明确交付物，先看 [`.project-memory\tool-delivery-routing.md`](C:\Users\ROG\Documents\杂务\.project-memory\tool-delivery-routing.md)。
   如果涉及插件、MCP、浏览器验证或专用运行时，再看 [`.project-memory\plugin-mcp-governance.md`](C:\Users\ROG\Documents\杂务\.project-memory\plugin-mcp-governance.md)。
   如果担心某类能力当前不可用，再看 [`.project-memory\capability-fallback-matrix.md`](C:\Users\ROG\Documents\杂务\.project-memory\capability-fallback-matrix.md)。
   如果必须追问关键分叉，先看 [`.project-memory\text-selector-questioning-protocol.md`](C:\Users\ROG\Documents\杂务\.project-memory\text-selector-questioning-protocol.md)。
5. 中等及以上复杂任务先给轻量计划。
6. 先产出可用骨架，再补展开或文件化交付。
7. 交付前做一次轻量自检。
8. 完成后给出自然下一步。
9. 如果近期新增了规则、spec 或 memory 文件，优先运行 `tools/check_harness.py`，必要时再抽查 `harness-regression/` 里的最小回归样例。

## 高频请求 -> 默认动作
- “整理一下这份材料”
  默认转成结构化摘要或复习提要。
- “帮我写一下这个题”
  默认先给论点路径与提纲，再视需要扩写。
- “比较一下这两个理论/观点”
  默认先列维度，再做表格与判断。
- “改一下这段话”
  默认同时检查表达、逻辑、结构与概念清晰度，不只做表面润色。
- “查一下这个说法”
  默认先判断是事实、出处、争议还是观点，再决定是否联网核对。
- “做一版 PPT / slides / 展示”
  默认按演讲交付处理，优先设计讲述路径与信息主次。
- “帮我做成 Word / PDF / 表格文件”
  默认先确认主交付物类型，再按 `tool-delivery-routing.md` 和对应 delivery spec 走专用能力。

## 上下文与记忆使用方式
- 宿主自带 memory 只当基础底座，不当项目唯一记忆。
- 项目内显式记忆默认放在 [`.project-memory/`](C:\Users\ROG\Documents\杂务\.project-memory)。
- 每次优先读取与当前任务直接相关的材料、模板和最近承接点，不平铺所有历史内容。
- 如果任务需要长期承接，默认按这个顺序找：
  1. [`.project-memory\project-state.md`](C:\Users\ROG\Documents\杂务\.project-memory\project-state.md)
  2. [`.project-memory\user-preferences.md`](C:\Users\ROG\Documents\杂务\.project-memory\user-preferences.md)
  3. [`.project-memory\decision-log.md`](C:\Users\ROG\Documents\杂务\.project-memory\decision-log.md)
  4. [`.project-memory\reusable-assets.md`](C:\Users\ROG\Documents\杂务\.project-memory\reusable-assets.md)
- 只有会稳定影响后续协作的偏好、约束和结构，才应被视为长期项目记忆。
- 明显可能过期的信息默认重新核对，不直接沿用旧上下文。
- 任务收尾时，如果形成了新的长期偏好、长期状态变化或可复用经验，优先更新 `.project-memory/` 既有文件，而不是新建散落笔记。
- 如果感觉 harness 本身开始跑偏，先运行 `tools/check_harness.py`，再决定是删重复、并近义，还是补空白。

## 常见交付物
- 摘要
- 提纲
- 比较表
- 初稿
- 修改稿
- 复习笔记
- 汇报结构
- Word / PDF / 表格 / PPT 等正式文件

## 启动示例
- “把这篇文章整理成适合复习的笔记。”
- “按课程作业语气，先给我这道题的分析提纲。”
- “比较 A 和 B 的核心差异，先做表格，再给判断。”
- “把这份材料改成 8 分钟汇报的 slides 结构。”
- “核对这个说法是否准确，并区分已确认信息和待核对信息。”
