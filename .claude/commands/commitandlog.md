---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git commit:*), Bash(git log:*), Bash(mkdir:*), Bash(cat:*), Bash(date:*)
description: 一键完成 session 收尾：提交代码 → 撰写工作日志 → 提交日志
---

## Context

- 今日日期: !`date +%Y-%m-%d %H:%M`
- Current git status: !`git status`
- Current git diff (staged and unstaged): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- 今日提交记录: !`git log --oneline --since="00:00" --author="$(git config user.name)"`
- 各提交详情: !`git log --since="00:00" --author="$(git config user.name)" --stat --no-merges`
- 已有工作日志（如存在）: !`cat worklogs/worklog-$(date +%Y-%m-%d).md 2>/dev/null || echo "(今日暂无日志)"`

## Your task

按以下顺序执行，**不要跳步，不要合并步骤**：

---

### 第一步：提交代码（排除 worklogs/）

检查暂存区和工作区状态：

- **如果暂存区已有文件**（排除 `worklogs/`）：直接对这些文件生成 commit message 并提交。如果 `worklogs/` 在暂存区，先用 `git restore --staged worklogs/` 移出。
- **如果暂存区为空，工作区有变更**：列出变更文件，告知用户需要手动 `git add` 要提交的文件，**等待用户操作后**再继续提交。不要自动 `git add .`。
- **如果暂存区为空，工作区也无变更**：跳过此步。

**提交规范**：格式 `<type>(<scope>): <subject>`，subject 中文祈使句不加句号 50 字以内。

| 条件 | 风格 |
|------|------|
| 改动 ≤ 2 个文件，原因一句话说清 | 单行 |
| 涉及根因分析、多模块联动、测试结果变化 | 复杂结构 |
| 纯文档/工作日志更新 | 单行 |

复杂结构模板：
```
<type>(<scope>): <subject>

## 问题
<根因描述>

## 改动
### <文件/模块>
- <具体改动>

## 结果
<可量化结果>

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>
```

---

### 第二步：撰写工作日志

根据本次 session 的对话内容和今日所有提交记录，生成技术工作日志。

如果 `worklogs/` 不存在，先执行 `mkdir -p worklogs`。

如果今日日志已存在，追加到末尾；否则创建新文件 `worklogs/worklog-YYYY-MM-DD.md`。

**日志结构**：

```markdown
# 工作日志 YYYY-MM-DD

## 概述
（2-4 句话：这个 session 干了什么，达到了什么结果，有可量化指标必须写出来）

## 主要改动

### 1. <模块/问题名>

**问题**：根因是什么，为什么出现

**改动**：具体做了什么（引用真实文件名、函数名）

**结果**：效果（可量化优先）

（按需重复此块）

## 关键技术决策
（为什么选方案 A 而不是 B，省略则删除此节）

## 当前状态与下一步
- 已完成/已稳定：
- 遗留问题：
- 下次优先：

## 提交记录

| 提交 | 内容 |
|------|------|
| hash | message |
```

**写作要求**：具体不泛泛，有根因不只列现象，保留决策依据，面向三个月后的自己。

---

### 第三步：提交工作日志

```
git add worklogs/
git commit -m "docs(worklog): YYYY-MM-DD 工作日志"
```

日期用实际日期替换。
