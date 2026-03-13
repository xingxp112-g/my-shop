---
name: ship
description: 一键完成完整发布流程：smart-commit → push → gh pr create → gh pr merge --squash → 分支清理
---

# Ship Skill — 一键发布

整合 smart-commit + push + PR 创建 + squash 合并 + 分支清理，一个命令完成从提交到上线的全流程。

---

## 前置检查

**先执行，任何一步失败立刻停止并告知用户：**

```bash
gh auth status        # 未登录则提示 gh auth login 后停止
git status            # 确认有改动或了解当前状态
git branch --show-current  # 记录当前分支名
```

---

## 执行流程

### Step 1：Smart Commit

按 smart-commit skill 的逻辑分析并提交：

1. 执行 `git diff --staged` 和 `git diff` 了解改动全貌
2. 判断是否需要拆分提交：
   - 跨模块 / 跨类型（feat + fix + chore 混合）→ 列出拆分方案，**等用户确认后**再执行
   - 单一性质改动 → 直接提交
3. 按 Conventional Commits 格式生成提交信息并执行：
   ```bash
   git add <具体文件>
   git commit -m "type(scope): 描述"
   ```

### Step 2：Push 到远程

```bash
git push origin <当前分支>
```

推送失败（如远程不存在）时加 `-u`：

```bash
git push -u origin <当前分支>
```

### Step 3：创建 PR 到 master

```bash
gh pr create --base master --head <当前分支> --title "<提交信息>" --body "$(cat <<'EOF'
## 变更内容
<基于 git log 自动生成的简短摘要>

## 发布说明
通过 /ship 一键发布流程
EOF
)"
```

- 自动读取最近提交信息作为 PR 标题
- 如果 PR 已存在（报错 `already exists`），跳过创建，继续下一步

### Step 4：Squash 合并 PR

```bash
gh pr merge --admin --squash
```

**注意：不使用 `-d` 参数**，避免 worktree 存在时删除失败导致整体中断。

合并失败常见原因及处理：
- `Review required` → 已用 `--admin` 绕过，若仍失败检查仓库设置
- `No commits between master and dev` → 告知用户分支已同步，无需合并

### Step 5：同步本地 master 并重置 dev

```bash
git checkout master
git pull origin master
git checkout dev
git reset --hard origin/master
```

> 将 dev 重置到与 master 一致，避免 squash merge 导致的历史分叉问题。

### Step 6：清理已合并的源分支（如果不是 dev）

仅当发布源分支**不是 dev**（如 `feat/xxx`）时执行：

```bash
# 删除远程分支
git push origin --delete <源分支名>

# 删除本地分支
git branch -d <源分支名>
```

如果 `-d` 删除失败（未完全合并提示），**不要强制 `-D`**，告知用户手动确认后再操作。

---

## 完成后输出摘要

```
✅ Ship 完成
━━━━━━━━━━━━━━━━━━━━━━━━
📦 提交：<提交信息>
🌿 分支：<源分支> → master
🔗 PR：<PR URL>
🧹 清理：dev 已重置到 master
━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 异常中止规则

以下情况**立即停止**，不继续执行后续步骤：

| 情况 | 处理 |
|------|------|
| `gh auth status` 失败 | 提示运行 `gh auth login` |
| push 失败 | 显示错误，不创建 PR |
| PR 合并失败 | 显示错误，不执行分支清理 |
| 用户未确认拆分方案 | 等待用户回复，不自动提交 |
