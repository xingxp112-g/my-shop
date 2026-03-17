# 安全重构执行计划

## 代码现状摘要

| 问题 | 当前状态 |
|------|---------|
| H-3 JWT库 | `utils/auth.py:5` 使用 `from jose import jwt, JWTError`，requirements.txt 第9行有 `python-jose[cryptography]==3.3.0` |
| H-1 订单价格 | `schemas/order.py:10` `OrderItemCreate` 含 `price: Decimal`，`routers/orders.py:34` 直接用 `item.price` 计算 total |
| H-4 密码明文 | `config.py:13` `ADMIN_PASSWORD: str = "admin123"`，`routers/auth.py:22` 明文比对。**注意：requirements.txt 已有 `passlib[bcrypt]==1.7.4`，无需新装** |
| H-2 KEY+CORS | `config.py:11` 默认值 `"change-me"` 无启动检测；`main.py:14` `allow_origins=["*"]` + `allow_credentials=True` 是非法组合（浏览器会拒绝带凭证的通配符请求） |

---

## 任务清单

### 阶段一：基础依赖替换（必须最先完成，后续任务依赖）

#### [ ] 任务 1：替换 JWT 库（H-3）

- **文件**：`backend/requirements.txt`、`backend/app/utils/auth.py`
- **做什么**：
  1. `requirements.txt`：删除 `python-jose[cryptography]==3.3.0`，新增 `PyJWT>=2.8.0`
  2. `utils/auth.py`：将 `from jose import jwt, JWTError` 替换为 `import jwt` + `from jwt.exceptions import InvalidTokenError`
  3. `create_token()`：`jwt.encode()` 返回值在 PyJWT 中直接是 `str`，无需 `.decode()`
  4. `get_current_user()`：将 `except JWTError` 改为 `except (InvalidTokenError, Exception)`，`payload.get("sub")` 逻辑不变
- **风险**：PyJWT 2.x API 与 python-jose 略有差异，需确认 `exp` 字段自动验证行为一致（PyJWT 默认验证 exp，行为一致）
- **串行依赖**：无，可作为第一步独立完成

---

### 阶段二：可并行执行的安全加固（任务 2、3、4 可同时进行）

#### [ ] 任务 2：管理员密码改为 bcrypt 哈希（H-4）

- **文件**：`backend/app/config.py`、`backend/app/routers/auth.py`
- **做什么**：
  1. `config.py`：将 `ADMIN_PASSWORD` 字段改名为 `ADMIN_PASSWORD_HASH`，类型保持 `str`，默认值改为一个预生成的 bcrypt hash（需提前用 `passlib` 生成 `admin123` 的 hash 作为占位符）
  2. `routers/auth.py`：引入 `from passlib.context import CryptContext`，初始化 `pwd_context = CryptContext(schemes=["bcrypt"])`；将明文比对 `body.password != settings.ADMIN_PASSWORD` 改为 `not pwd_context.verify(body.password, settings.ADMIN_PASSWORD_HASH)`
  3. 在 `.env.example`（若存在）或文档中说明如何生成新密码 hash
- **风险**：`passlib[bcrypt]` 已在 requirements.txt，无依赖问题。注意 `.env` 文件中 `ADMIN_PASSWORD` 旧变量名要同步改为 `ADMIN_PASSWORD_HASH`，否则启动会用默认占位符

#### [ ] 任务 3：订单价格后端验证（H-1）

- **文件**：`backend/app/schemas/order.py`、`backend/app/routers/orders.py`
- **做什么**：
  1. `schemas/order.py`：`OrderItemCreate` 删除 `price: Decimal` 字段（仅保留 `product_id` 和 `quantity`）
  2. `routers/orders.py`：`create_order()` 中，在 `db.flush()` 之前，用 `product_id` 列表批量查询 `Product` 表，构建 `{product_id: price}` 映射；循环 `body.items` 时用数据库价格替代 `item.price`；同时验证商品存在且状态为上架（status=1），否则返回 400
  3. `total` 计算改为基于数据库价格：`total = sum(db_prices[item.product_id] * item.quantity for item in body.items)`
- **风险**：前台 `order.html` 提交时携带了 `price` 字段（购物车快照），Schema 改动后后端会忽略该字段，需确认前端提交格式不会因此报验证错误（Pydantic 默认忽略额外字段，无问题）

#### [ ] 任务 4：SECRET_KEY 启动检测 + 修复 CORS（H-2）

- **文件**：`backend/app/config.py`、`backend/main.py`
- **做什么**：
  1. `config.py`：在 `Settings` 类末尾添加 `model_validator(mode='after')`，检测 `APP_SECRET_KEY == "change-me"` 则抛出 `ValueError("APP_SECRET_KEY 不能使用默认值，请在 .env 中设置强密钥")`
  2. `main.py`：CORS 修复——`allow_origins=["*"]` 与 `allow_credentials=True` 不能共存（浏览器规范禁止）。改为从环境变量读取允许的 origin 列表，例如新增 `CORS_ORIGINS: str = "http://localhost"` 配置项，`allow_origins=settings.CORS_ORIGINS.split(",")`；若仍需通配符则去掉 `allow_credentials=True`
- **风险**：CORS 改动影响前端跨域请求，需确认前台 H5 和后台管理的实际访问域名，避免改完后跨域失败。建议默认值设为 `"*"` 且移除 `allow_credentials`，让使用者按需配置

---

### 阶段三：收尾（必须在阶段二完成后执行）

#### [ ] 任务 5：更新依赖并验证

- **文件**：`backend/requirements.txt`
- **做什么**：
  1. 确认 `python-jose` 已删除，`PyJWT>=2.8.0` 已添加
  2. 在 venv 中运行 `pip install -r requirements.txt` 验证无冲突
  3. 启动后端，验证：正常密码登录成功、错误密码返回 401、默认 SECRET_KEY 拒绝启动、前台提交订单不带 price 字段能正常创建
- **串行**：必须在任务 1-4 全完成后执行

---

## 并行/串行关系

```
任务1（JWT替换）──┐
                  ├──► 任务5（验证收尾）
任务2（密码哈希）─┤
任务3（订单价格）─┤
任务4（KEY+CORS）─┘

任务1 必须最先完成（utils/auth.py 是基础）
任务2、3、4 可并行
任务5 必须最后
```

---

## 工作量估算

| 任务 | 改动量 | 复杂度 |
|------|--------|--------|
| 任务1 JWT替换 | ~10行，2个文件 | 低 |
| 任务2 密码哈希 | ~8行，2个文件 | 低 |
| 任务3 订单价格 | ~20行，2个文件 | 中（含数据库查询逻辑） |
| 任务4 KEY+CORS | ~10行，2个文件 | 低 |
| 任务5 验证 | 运行测试 | 低 |

**总计**：改动文件 6 个，代码变更约 50 行。所有改动均有明确边界，无需数据库迁移。
