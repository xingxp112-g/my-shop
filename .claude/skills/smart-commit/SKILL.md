---
name: smart-commit
description: 分析当前改动，生成规范提交信息并执行提交
disable-model-invocation: true
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

第三步：暂存并提交
git add .
git commit -m "生成的提交信息"

第四步：询问是否推送
告诉我提交完成，问是否需要 git push origin 当前分支