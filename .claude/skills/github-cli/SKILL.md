---
name: github-cli
description: 使用 GitHub CLI（gh 命令）操作 GitHub，包括：创建PR、合并PR、查看PR状态、分支管理、仓库查看、强制合并（绕过保护规则）。当用户提到"提PR"、"合并PR"、"查看PR"、"gh命令"、"GitHub操作"、"推送代码后提交PR"、"dev合并到master"、"分支保护绕过"时，必须触发此 Skill。也适用于用户说"帮我走完PR流程"、"提交完了下一步怎么做"、"怎么合并分支"等场景。Windows/macOS/Linux 均适用。
---

# GitHub CLI Skill

## 前置检查

每次使用前，先确认环境：

```bash
gh auth status        # 检查是否已登录
gh --version          # 确认版本
```

未登录时运行 `gh auth login`，按交互提示完成认证。

---

## 核心场景

### 场景一：提交代码后创建 PR

**标准流程（feat 分支 → dev）：**

```bash
# 确认当前分支和状态
git status
git branch

# 推送当前分支到远程
git push origin HEAD

# 创建 PR（自动读取当前分支，推荐用 --fill 自动填充标题和描述）
gh pr create --base dev --fill

# 或者手动指定标题和描述
gh pr create --base dev --title "feat: 新增代金券模块" --body "按 SPEC.md 实现，验收7项全部通过"
```

**dev → master 的发版 PR：**

```bash
gh pr create --base master --head dev --title "release: v1.1.0 代金券功能上线"
```

---

### 场景二：查看和管理 PR

```bash
gh pr list                        # 查看所有开放的 PR
gh pr list --state all            # 包含已关闭的 PR
gh pr view                        # 查看当前分支的 PR
gh pr view 1                      # 查看指定编号的 PR
gh pr view --web                  # 在浏览器中打开 PR 页面
gh pr checks                      # 查看当前 PR 的 CI 检查状态
```

---

### 场景三：合并 PR

**普通合并（无保护规则限制）：**

```bash
gh pr merge 1 --merge             # merge commit（保留完整历史）
gh pr merge 1 --squash            # squash（合并为单条 commit，推荐）
gh pr merge 1 --rebase            # rebase
```

**管理员强制合并（绕过分支保护规则，个人项目常用）：**

```bash
gh pr merge 1 --admin --squash
```

合并后会自动：
- 更新本地对应分支
- 删除已合并的功能分支（加 `-d` 参数）

```bash
gh pr merge 1 --squash -d         # 合并后自动删除分支
```

---

### 场景四：本项目标准 Git 工作流

结合项目的 dev/master 分支策略：

```bash
# Step 1：从 dev 切出功能分支
git checkout dev
git pull origin dev
git checkout -b feat/xxx

# Step 2：开发完成，推送
git add .
git commit -m "feat: xxx"
git push origin feat/xxx

# Step 3：创建 PR（feat/xxx → dev）
gh pr create --base dev --fill

# Step 4：合并 PR（管理员强制，个人项目）
gh pr merge --admin --squash -d

# Step 5：切回 dev，拉取最新
git checkout dev
git pull origin dev
```

---

### 场景五：其他常用操作

```bash
# 查看仓库基本信息
gh repo view

# 在浏览器中打开当前仓库
gh repo view --web

# 查看 issue 列表
gh issue list

# 查看 Actions 工作流运行状态
gh run list
gh run view <run-id>
```

---

## Windows 注意事项

- 命令与 macOS/Linux 完全一致，无需修改
- 推荐在 Windows Terminal 或 PowerShell 中使用
- 安装方式：`winget install --id GitHub.cli`

---

## 常见报错处理

| 报错 | 原因 | 解决方式 |
|------|------|---------|
| `Review required / Merging is blocked` | 分支保护要求 Code Review | 加 `--admin` 参数强制合并 |
| `gh: command not found` | 未安装 gh | `winget install --id GitHub.cli` |
| `You are not logged into any GitHub hosts` | 未认证 | `gh auth login` |
| `No commits between master and dev` | 两分支内容一致 | 无需 PR，分支已同步 |
