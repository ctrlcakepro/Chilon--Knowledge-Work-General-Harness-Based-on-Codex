# Knowledge Work Harness for Codex

这是一套面向知识工作场景的 Codex harness 配置包。它的目标不是单纯增加提示词，而是把长期协作中真正稳定有效的部分整理成一套**可复用、可维护、可扩展**的工作结构。

This package is a Codex harness designed for knowledge work. Its goal is not to pile on more prompts, but to turn the stable, reusable parts of long-term collaboration into a maintainable and extensible working structure.

---

## 🚀 适用场景 | Target Scenarios

本配置包非常适合以下需要一定**结构判断**与**交付意识**的任务：
*   📚 **中文：** 阅读总结、课程学习、论文写作、资料整理、汇报准备、文档精炼。
*   🌍 **English:** Reading summaries, course study, academic writing, research organization, presentation prep, document condensation.

和“只会回答问题”的项目配置不同，这套 harness 更强调**任务分流、成品交付、规则治理、自动维护**，以及在上下文预算内稳定运行。
Unlike project setups that only optimize for answering questions, this harness focuses on task routing, production-quality outputs, rule governance, automated maintenance, and stable operation within a controlled context budget.

---

## 🏗️ 核心架构 | Architecture

项目的核心架构采用分层设计，重点在于**让顶层保持轻量，细节尽量下沉**，从而最大程度减少规则平铺带来的上下文污染（Context Pollution）。
The architecture is intentionally layered to keep the top level light, push detail downward, and reduce context pollution caused by flattening too many rules into one place.
