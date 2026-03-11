# Git 规范

## 不提交的文件

| 文件/目录 | 原因 |
|-----------|------|
| `backend/.env` | 含数据库密码等敏感配置 |
| `backend/venv/` | Python 虚拟环境，本地构建 |
| `backend/uploads/` | 用户上传图片，不纳入版本控制 |

## Commit 规范

使用 Conventional Commits 格式：

```
<type>: <描述>
```

| type | 场景 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `chore` | 构建/依赖/配置等杂项 |
| `docs` | 文档变更 |
| `refactor` | 重构（不改变行为） |
| `style` | 代码格式调整 |

## 分支策略

- `master`：主分支，受保护，**必须通过 PR 合并，禁止直接 push**
- `dev`：日常开发分支，功能开发在此分支进行，完成后提 PR 合并到 master
- 工作流：在 `dev` 上开发 → push origin dev → 提 PR → 合并到 master
