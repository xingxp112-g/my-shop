# 美妆内部销售系统

公司内部美妆销售管理系统，供销售/运营人员使用。
- 前台 H5：客户选品、购物车、提交订单
- 后台管理：商品/品牌/标签/订单管理 + 数据统计
- 不含库存、支付、物流、复杂权限等功能

**当前状态：V1.0 开发完成（2026-03-03 联调测试 10 项全部通过）**

---

## 规范文档

- Git 规范：[.claude/rules/git.md](.claude/rules/git.md)
- 后端规范（技术栈 / API / 数据库表结构 / 业务规则）：[.claude/rules/backend.md](.claude/rules/backend.md)
- 前端规范（页面清单 / JS 结构 / 设计系统）：[.claude/rules/frontend.md](.claude/rules/frontend.md)

---

## 目录结构

```
my-shop/
├── CLAUDE.md
├── .claude/
│   ├── rules/              # 规范文档（git / backend / frontend）
│   ├── skills/             # 可调用 Skill（smart-commit / ship / github-cli / diagnose / review-page 等）
│   ├── commands/           # 自定义斜杠命令（/diagnose / /review-page）
│   ├── agents/             # 自定义 Agent（check-api）
│   ├── hooks/              # 生命周期钩子（session-logger 等）
│   └── session-log.md      # Claude 会话日志
├── backend/                # 后端（Python + FastAPI）
│   ├── main.py
│   ├── requirements.txt
│   ├── .env                # 不提交 git
│   ├── venv/               # 不提交 git
│   ├── uploads/            # 不提交 git
│   ├── app/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   ├── services/
│   │   └── utils/
│   └── sql/
│       └── init.sql
└── frontend/
    ├── design-system.md    # 设计系统规范
    ├── h5/                 # 前台 H5
    └── admin/              # 后台管理
```
## Environment
- Windows machine, but shell is **bash** (Git Bash / MSYS2) — use Unix syntax, NOT PowerShell
- For Python scripts, force UTF-8 encoding（encoding='utf-8'）
- Use ASCII-safe JSON output when terminal encoding is uncertain

## Planning
- When user says 'don't write code yet', do NOT proceed to implementation
- Always confirm before moving from planning to implementation

## Git Workflow
- Always use gh CLI for PR creation and merging
- When dev/master diverge, prefer git reset --hard over rebase
- After merging PRs, do NOT use -d flag when worktrees exist