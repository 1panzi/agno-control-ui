---
alwaysApply: true
scene: git_message
---

在此处编写规则，自定义 AI 生成提交信息的风格。

allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git commit:*)
description: 按项目规范生成 commit message 并提交

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## 提交规范

格式：`<type>(<scope>): <subject>`

**type 类型**：`feat` / `fix` / `docs` / `style` / `refactor` / `perf` / `test` / `chore` / `ci`

**subject**：祈使句，中文，不加句号，50 字以内

**判断用哪种风格**：

| 条件 | 风格 |
|------|------|
| 改动 ≤ 2 个文件，原因一句话说清 | 单行 |
| 涉及根因分析、多模块联动、测试结果变化 | 复杂结构 |
| 纯文档/工作日志更新 | 单行 |

**复杂改动模板**（多文件/根因分析时使用）：

```
<type>(<scope>): <subject>

## 问题
<根因描述，bullet 列举>

## 改动
### <文件/模块名>
- <具体改动>

## 结果
<可量化的结果>

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>
```

**Co-Authored-By**：有 AI 协作生成代码时，footer 必须加此行。

## Your task

根据以上变更和规范，生成符合项目规范的 commit message 并提交。

**暂存区策略**：
- 如果暂存区（staged）已有文件，直接对这些文件生成 commit message 并提交，不追加任何其他文件
- 如果暂存区为空，列出当前工作区的变更文件，**停下来告知用户**，请用户手动 `git add` 需要提交的文件后再执行 `/commit`，不要自动 `git add .`

**重要约束**：`worklogs/` 目录下的文件必须单独提交，不能混入代码提交。即使该目录已在暂存区也要排除（用 `git restore --staged worklogs/` 移出）。

不要输出其他文字，只执行工具调用。
