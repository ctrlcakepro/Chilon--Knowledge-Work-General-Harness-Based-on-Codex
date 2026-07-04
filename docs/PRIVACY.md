# Privacy and Safety｜隐私与安全

Chilon 会鼓励用户把长期偏好、项目状态、交付规范和可复用材料显式保存下来。这个设计能提升长期协作质量，但也带来一个现实风险：如果你把私人 memory、客户信息、商业策略或本地路径提交到公开仓库，就可能造成信息泄露。

本文件说明哪些内容可以公开，哪些内容应该保留在本地，以及如何安全使用 Chilon。

## 不要提交到公共仓库的内容

不要把以下内容写入公开仓库中的 `AGENTS.md`、`.project-memory/`、examples 或 adapter 文件：

- 账号、密码、API Key、Token、Cookie
- 真实客户名称、客户资料、合同内容、报价信息
- 未公开的商业策略、运营策略、内部流程
- 私人研究材料、未发表论文、课程作业原文
- 个人身份证明、电话、邮箱、地址等敏感信息
- 本机绝对路径，例如 `C:\Users\name\...` 或 `/Users/name/...`
- 任何你不希望别人通过 GitHub 搜索到的内容

## 推荐的本地私有目录

如果你需要保存私人 memory，建议把它们放到明确的私有目录中，并通过 `.gitignore` 排除：

```text
.project-memory/private/
.project-memory/local/
.project-memory/secrets.md
.project-memory/client-notes.md
.project-memory/account-info.md
```

这些文件可以在你本地项目里使用，但不应该进入公共模板仓库。

## 推荐 `.gitignore`

可以参考：

```text
templates/.gitignore.example
```

核心规则是：公开仓库只保存通用结构和可迁移模板，私人项目状态保留在本地。

## 发布前检查清单

在把 Chilon 配置提交到公开仓库前，至少检查这些问题：

- [ ] 是否包含真实姓名、客户名、学校内部材料或未公开项目？
- [ ] 是否包含 API Key、账号、密码、Token 或 Cookie？
- [ ] 是否包含本机绝对路径？
- [ ] `.project-memory/` 中是否有私人偏好、项目状态或敏感决策？
- [ ] examples 是否已经脱敏？
- [ ] 是否已经添加 `.gitignore` 排除 private / local / secrets 文件？

## 公开模板应该怎么写

公开模板可以保留：

- 通用任务流程
- 抽象示例
- 脱敏后的项目描述
- 空白 memory 模板
- 可复用的结构骨架
- 不绑定私人环境的相对路径

公开模板不应该保留：

- 作者自己的私人工作流状态
- 作者本机路径
- 真实客户或课程材料
- 无法公开复用的项目细节

## 如果已经误提交了敏感信息

如果你已经把敏感信息提交到了 GitHub，单纯删除文件并不一定足够，因为 Git 历史里可能仍然存在这些内容。建议：

1. 立即撤销或轮换泄露的 Key / Token / 密码。
2. 删除仓库中的敏感内容。
3. 清理 Git 历史或联系平台处理敏感数据暴露。
4. 检查是否有 fork、release、issue 或缓存仍然包含泄露内容。

## Chilon 的默认安全原则

> 公开仓库保存结构，本地项目保存私人上下文。

Chilon 的价值来自可维护的知识工作结构，而不是把所有私人记忆都上传到公共仓库。
