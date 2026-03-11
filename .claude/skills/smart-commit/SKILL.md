---
name: smart-commit
description: 分析当前改动，生成规范提交信息并执行提交
---

分析当前 git 改动并执行规范提交：

第一步：了解改动全貌
执行：git diff --staged 和 git diff，理解本次改动内容

第二步：生成提交信息
格式遵循 Conventional Commits 规范：
- feat: 新功能
- fix: 修复 bug  
- refactor: 重构
- docs: 文档更新
- chore: 构建/工具变动

示例：feat(product): 新增商品列表分页功能

第三步：判断是否需要拆分提交
在提交前，先判断本次改动是否跨越多个模块或包含不同性质的变更：
- 如果改动同时涉及 feat/fix/chore/docs 等不同类型，或跨越多个不相关模块（如前端+后端+文档同时变动），则**不要直接提交**
- 列出拆分方案，格式如下：
  ```
  建议拆分为 N 次提交：
  1. feat(xxx): ... → 涉及文件：a.js, b.py
  2. fix(yyy): ...  → 涉及文件：c.html
  3. chore: ...     → 涉及文件：d.md
  ```
- 等我回复确认后，再按顺序逐批执行 git add <具体文件> 和 git commit
- 如果改动性质单一、模块集中，则直接进入提交流程

第四步：暂存并提交
git add <具体文件或 .>
git commit -m "生成的提交信息"

第五步：询问是否推送
告诉我提交完成，问是否需要 git push origin 当前分支。
如果当前分支是 `dev`，推送后提醒：master 分支受保护，需在 GitHub 上提 PR 才能合并到 master。

第六步：提交完成后，更新 CLAUDE.md 中的「CC 工具清单」
如果本次提交新增或删除了 .claude/ 下的文件，提醒我同步更新 CLAUDE.md。