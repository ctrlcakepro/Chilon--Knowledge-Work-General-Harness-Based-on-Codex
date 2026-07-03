# Harness Regression Pack

## 目的
这是一套最小回归样例，用来检查这套 knowledge-work harness 是否还保持正确分流、正确起步和基本成品感。

它不追求覆盖所有任务，只优先覆盖最常见、最容易跑偏的三类：
- 教材复习笔记
- 论文/作业提纲
- 汇报或 slides 交付

## 使用方式
1. 先运行 `tools/check_harness.py`，确认结构层没有断。
2. 再任选 1 到 3 个样例，检查模型是否按“期望路由”进入正确流程。
3. 如果输出明显跑偏，先记录偏差类型，再决定：
   - 是修正文档边界
   - 是补 `spec`
   - 还是只做一次性纠偏

## 判定原则
- 先看有没有走对入口，而不是先看措辞是否漂亮。
- 先看交付物类型是否正确，再看细节展开是否充分。
- 如果出现“能答，但答错了任务类型”，视为回归失败。

## 当前样例
- `cases/01-review-notes.md`
- `cases/02-essay-outline.md`
- `cases/03-presentation-delivery.md`
- `cases/04-document-condense.md`
- `cases/05-click-option-questioning.md`
