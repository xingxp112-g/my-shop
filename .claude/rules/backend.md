# 后端规范

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 框架 | Python 3.11+ / FastAPI / Uvicorn | REST API |
| ORM | SQLAlchemy 2.x | 数据库操作 |
| 数据验证 | Pydantic v2 | 请求/响应 Schema |
| 数据库 | MySQL 8.x | 主数据库 |
| 认证 | 简单 Bearer token | 无复杂权限体系 |
| 跨域 | FastAPI CORSMiddleware | 前后端分离 |

## 启动命令

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# API 文档：http://localhost:8000/docs
```

## 目录分层职责

| 目录 | 职责 |
|------|------|
| `app/models/` | SQLAlchemy ORM 模型 |
| `app/schemas/` | Pydantic 请求/响应模型 |
| `app/routers/` | API 路由，只做参数接收和响应返回 |
| `app/services/` | 业务逻辑层，复杂逻辑写在这里 |
| `app/utils/` | 通用工具（如 token 验证） |

## API 路由清单

| 路由 | 文件 | 说明 |
|------|------|------|
| `POST /auth/login` | routers/auth.py | 登录获取 token |
| `CRUD /brands` | routers/brands.py | 品牌管理 |
| `CRUD /tags` | routers/tags.py | 标签管理 |
| `CRUD /products` | routers/products.py | 商品管理 |
| `CRUD /orders` | routers/orders.py | 订单管理 |
| `GET /stats` | routers/stats.py | 统计数据 |

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

## 业务规则

- 订单状态流转：`待处理 → 已确认 → 已完成`，非法状态转换拒绝
- `order_items.price` 为下单时的价格快照，不随商品价格变更
- 不做库存、支付、物流、复杂权限功能
