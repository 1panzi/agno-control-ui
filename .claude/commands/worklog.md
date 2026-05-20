---
allowed-tools: Bash(git log:*), Bash(git diff:*), Bash(git status:*), Bash(mkdir:*), Bash(cat:*), Bash(date:*)
description: 生成今日工作总结并追加写入 worklogs/worklog-YYYY-MM-DD.md
---

## Context

- 今日日期: !`date +%Y-%m-%d`
- 今日提交记录（含 diff 摘要）: !`git log --oneline --since="00:00" --author="$(git config user.name)"`
- 各提交详情: !`git log --since="00:00" --author="$(git config user.name)" --stat --no-merges`
- 当前未提交变更: !`git status --short`
- 当前分支: !`git branch --show-current`
- 已有工作日志（如存在）: !`cat worklogs/worklog-$(date +%Y-%m-%d).md 2>/dev/null || echo "(今日暂无日志)"`

## Your task

根据以上 git 提交信息和本次 session 的对话内容，生成一份有深度的技术工作日志，追加写入 `worklogs/worklog-YYYY-MM-DD.md`。

**如果文件不存在**，先执行：
```bash
mkdir -p worklogs
```

**如果文件已存在**，在末尾追加，不要覆盖已有内容。

---

## 工作日志结构

### 必须包含的节

**1. 概述**（2-4 句话）
- 这个 session 解决了什么问题，达到了什么结果
- 如果有可量化指标（测试通过数、评分变化、文件数量等），必须写出来

**2. 主要改动**（按问题/模块分块）

每个改动块包含：
- **问题**：根因是什么，为什么会出现这个问题
- **改动**：具体做了什么，引用真实的文件名、函数名、类名
- **结果**：改动后的效果（可量化优先）

**3. 关键技术决策**（如有）
- 为什么选择方案 A 而不是方案 B
- 这是日志最有价值的部分，不要省略真实的权衡理由

**4. 当前状态与下一步**
- 已稳定/已完成的部分
- 遗留问题或已知风险
- 建议下次 session 优先处理的事项

**5. 提交记录表**
```
| 提交 hash | 内容 |
|-----------|------|
```

---

## 写作要求

- 具体，不泛泛：引用真实文件名、函数名、变量名、错误信息
- 有根因，不只列现象：说清楚"为什么出问题"而不只是"出了什么问题"
- 保留决策依据：技术选择背后的理由比选择本身更重要
- 面向未来的自己：写完这份日志，三个月后的自己能快速理解当时的上下文

