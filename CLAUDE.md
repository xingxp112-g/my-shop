# 美妆内部销售系统 - 项目文档

## 项目简介

公司内部美妆销售管理系统，供销售/运营人员使用。
- 前台 H5：客户选品、购物车、提交订单
- 后台管理：商品/品牌/标签/订单管理 + 数据统计
- 不含库存、支付、物流、复杂权限等功能

---

## 目录结构

```
my-shop/
├── CLAUDE.md                        # 本文件
├── backend/                         # 后端（Python + FastAPI）
│   ├── main.py                      # 应用入口
│   ├── requirements.txt             # 依赖列表
│   ├── .env.example                 # 环境变量示例
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py                # 配置（数据库连接等）
│   │   ├── database.py              # SQLAlchemy 数据库连接
│   │   ├── models/                  # ORM 模型
│   │   │   ├── __init__.py
│   │   │   ├── product.py           # Product, ProductTag
│   │   │   ├── brand.py             # Brand
│   │   │   ├── tag.py               # Tag
│   │   │   └── order.py             # Order, OrderItem
│   │   ├── schemas/                 # Pydantic 请求/响应模型
│   │   │   ├── __init__.py
│   │   │   ├── product.py
│   │   │   ├── brand.py
│   │   │   ├── tag.py
│   │   │   └── order.py
│   │   ├── routers/                 # API 路由
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # POST /auth/login
│   │   │   ├── products.py          # CRUD /products
│   │   │   ├── brands.py            # CRUD /brands
│   │   │   ├── tags.py              # CRUD /tags
│   │   │   ├── orders.py            # CRUD /orders
│   │   │   └── stats.py             # GET /stats
│   │   ├── services/                # 业务逻辑层
│   │   │   ├── __init__.py
│   │   │   ├── product_service.py
│   │   │   ├── order_service.py
│   │   │   └── stats_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── auth.py              # 登录验证工具
│   └── sql/
│       └── init.sql                 # 建表 SQL
│
└── frontend/                        # 前端（HTML + TailwindCSS + 原生 JS）
    ├── h5/                          # 前台 H5（客户端）
    │   ├── index.html               # 商品列表页
    │   ├── cart.html                # 购物车页
    │   ├── checkout.html            # 提交订单页
    │   ├── success.html             # 提交成功页
    │   ├── js/
    │   │   ├── api.js               # 封装 fetch 请求
    │   │   ├── products.js          # 商品列表逻辑
    │   │   ├── cart.js              # 购物车逻辑
    │   │   └── checkout.js          # 提交订单逻辑
    │   └── css/
    │       └── custom.css           # 自定义样式（补充 Tailwind）
    │
    └── admin/                       # 后台管理系统
        ├── login.html               # 登录页
        ├── index.html               # 首页（数据统计）
        ├── products.html            # 商品列表页
        ├── products-form.html       # 新增/编辑商品页
        ├── brands.html              # 品牌管理页
        ├── tags.html                # 标签管理页
        ├── orders.html              # 订单列表页
        ├── orders-detail.html       # 订单详情页
        ├── js/
        │   ├── api.js               # 封装 fetch 请求（含 token）
        │   ├── auth.js              # 登录/登出/token 管理
        │   ├── products.js          # 商品管理逻辑
        │   ├── brands.js            # 品牌管理逻辑
        │   ├── tags.js              # 标签管理逻辑
        │   ├── orders.js            # 订单列表逻辑
        │   └── stats.js             # 统计数据逻辑
        └── css/
            └── custom.css           # 自定义样式
```

---

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | HTML5 + TailwindCSS CDN + 原生 JS | 无构建工具，直接运行 |
| 后端 | Python 3.11+ / FastAPI / Uvicorn | REST API |
| ORM | SQLAlchemy 2.x | 数据库操作 |
| 数据验证 | Pydantic v2 | 请求/响应 Schema |
| 数据库 | MySQL 8.x | 主数据库 |
| 认证 | 简单 token（Bearer）| 无复杂权限体系 |
| 跨域 | FastAPI CORSMiddleware | 前后端分离 |

---

## 数据库表结构

### brand（品牌表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK AUTO_INCREMENT | 主键 |
| name | VARCHAR(100) NOT NULL | 品牌名称 |

### tag（标签表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK AUTO_INCREMENT | 主键 |
| name | VARCHAR(100) NOT NULL | 标签名称 |

### product（商品表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK AUTO_INCREMENT | 主键 |
| name | VARCHAR(200) NOT NULL | 商品名称 |
| brand_id | INT FK | 关联 brand.id |
| price | DECIMAL(10,2) NOT NULL | 销售价格 |
| image_url | VARCHAR(500) | 商品图片 URL |
| remark | TEXT | 商品备注 |
| status | TINYINT DEFAULT 1 | 1=上架 0=下架 |
| created_at | DATETIME DEFAULT NOW() | 创建时间 |

### product_tag（商品标签多对多）
| 字段 | 类型 | 说明 |
|------|------|------|
| product_id | INT FK | 关联 product.id |
| tag_id | INT FK | 关联 tag.id |

### orders（订单表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK AUTO_INCREMENT | 主键 |
| customer_name | VARCHAR(100) NOT NULL | 客户姓名 |
| phone | VARCHAR(20) NOT NULL | 联系方式 |
| total_amount | DECIMAL(10,2) NOT NULL | 订单总金额 |
| remark | TEXT | 订单备注 |
| status | VARCHAR(20) DEFAULT '待处理' | 待处理/已确认/已完成/已取消 |
| created_at | DATETIME DEFAULT NOW() | 创建时间 |

### order_items（订单明细表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK AUTO_INCREMENT | 主键 |
| order_id | INT FK | 关联 orders.id |
| product_id | INT FK | 关联 product.id |
| quantity | INT NOT NULL | 数量 |
| price | DECIMAL(10,2) NOT NULL | 下单时单价（快照） |

---

## 开发阶段划分

### 阶段 1：数据库 + 后台商品管理
- [ ] 建表 SQL（init.sql）
- [ ] 后端：brand / tag / product CRUD API
- [ ] 后台页面：品牌管理、标签管理、商品管理（列表 + 新增/编辑）

### 阶段 2：订单模块 + 前台 H5
- [ ] 后端：orders / order_items API
- [ ] 前台 H5：商品列表、购物车、提交订单、成功页
- [ ] 后台页面：订单列表、订单详情

### 阶段 3：数据统计 + 联调测试
- [ ] 后端：stats API（今日/本月订单数 + 金额）
- [ ] 后台首页：统计数据展示
- [ ] 联调测试 + 验收

---

## 当前进度

> **状态：V1.0 开发完成**
>
> 最后更新：2026-03-03

### 已完成（全部）
- [x] 数据库建库建表（6 张表，含外键）
- [x] 后端基础层：config / database / models / schemas
- [x] 后端 API：auth / brands / tags / products / orders / stats
- [x] 图片上传接口 + 静态文件服务
- [x] 后台管理前端：登录 / 首页统计 / 商品管理 / 品牌 / 标签 / 订单列表 / 订单详情
- [x] 前台 H5：商品列表（index.html）/ 购物车（cart.html）/ 提交订单（order.html）
- [x] 完整联调测试通过（10 项全部 ✅，2026-03-03）

### 联调测试结论（2026-03-03）
| # | 测试项 | 结果 |
|---|--------|------|
| 1 | 后台登录（admin/admin123） | ✅ |
| 2 | 新增品牌×2、标签×2 | ✅ |
| 3 | 新增3个商品（含品牌、标签） | ✅ |
| 4 | 前台H5商品列表正常显示 | ✅ |
| 5 | 关键词搜索 + 标签筛选 | ✅ |
| 6 | 购物车金额实时计算正确 | ✅ |
| 7 | 提交订单（POST /api/orders） | ✅ |
| 8 | 后台订单列表显示新订单 | ✅ |
| 9 | 订单状态流转（待处理→已确认→已完成，非法状态拒绝） | ✅ |
| 10 | 首页统计数据（今日/本月订单数和金额） | ✅ |

### 启动命令
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# API 文档：http://localhost:8000/docs
```
