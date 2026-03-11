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
├── .claude/rules/          # 规范文档
│   ├── git.md
│   ├── backend.md
│   └── frontend.md
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
