# 美妆内部销售系统

公司内部美妆销售管理系统，供销售/运营人员使用。

- **前台 H5**：客户选品、购物车、提交订单
- **后台管理**：商品/品牌/标签/订单管理 + 数据统计

---

## 环境要求

| 依赖 | 版本要求 |
|------|----------|
| Python | 3.11+ |
| MySQL | 8.x |
| pip | 最新版 |

> 前端无需任何构建工具，直接用浏览器打开 HTML 文件即可。

---

## 首次部署步骤

### 第一步：初始化数据库

登录 MySQL，执行建表脚本：

```bash
mysql -u root -p < backend/sql/init.sql
```

或在 MySQL 客户端中手动执行：

```sql
source /path/to/my-shop/backend/sql/init.sql;
```

### 第二步：配置环境变量

```bash
cd backend
cp .env.example .env
```

编辑 `.env` 文件，填入实际配置：

```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=你的数据库密码
DB_NAME=my_shop

# 应用配置（管理后台登录账号）
APP_SECRET_KEY=替换为随机字符串
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# 图片上传目录
UPLOAD_DIR=./uploads
```

### 第三步：安装 Python 依赖

```bash
cd backend

# 推荐使用虚拟环境
python -m venv venv

# 激活虚拟环境（Windows）
venv\Scripts\activate

# 激活虚拟环境（Linux / macOS）
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

---

## 启动服务

### 启动后端 API 服务

```bash
cd backend

# 确保虚拟环境已激活（Windows）
venv\Scripts\activate

# 启动服务（开发模式，含热重载）
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

启动成功后终端会显示：

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process ...
INFO:     Started server process ...
INFO:     Application startup complete.
```

**生产模式（不含热重载，性能更好）：**

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 访问地址汇总

| 服务 | 地址 |
|------|------|
| API 接口文档（Swagger） | http://localhost:8000/docs |
| API 接口文档（Redoc） | http://localhost:8000/redoc |
| 后台管理 - 登录页 | 用浏览器打开 `frontend/admin/login.html` |
| 前台 H5 - 商品列表 | 用浏览器打开 `frontend/h5/index.html` |

> 前端为纯静态文件，直接双击 HTML 文件或通过本地 Web Server 访问均可。

### 前端本地 Web Server（可选）

如需避免浏览器跨域限制，可用 Python 快速起一个静态文件服务：

```bash
# 在 frontend 目录下执行
cd frontend
python -m http.server 3000
```

访问地址：
- 后台管理：http://localhost:3000/admin/login.html
- 前台 H5：http://localhost:3000/h5/index.html

---

## 关停服务

### 关停后端 API 服务

在运行 `uvicorn` 的终端窗口中按：

```
Ctrl + C
```

终端显示以下内容表示已正常关停：

```
INFO:     Shutting down
INFO:     Finished server process ...
INFO:     Stopping reloader process ...
```

### 退出虚拟环境

```bash
deactivate
```

---

## 日常启动（快速参考）

每次启动服务只需以下三步：

```bash
# 1. 进入后端目录并激活虚拟环境
cd backend
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / macOS

# 2. 启动后端
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 3. 用浏览器打开前端页面（无需额外操作）
```

---

## 后台管理默认账号

| 字段 | 默认值 |
|------|--------|
| 用户名 | admin |
| 密码 | admin123 |

> 可在 `.env` 文件中修改 `ADMIN_USERNAME` 和 `ADMIN_PASSWORD`。

---

## 目录结构

```
my-shop/
├── backend/                # 后端（Python + FastAPI）
│   ├── main.py             # 应用入口
│   ├── requirements.txt    # Python 依赖
│   ├── .env                # 环境变量（本地配置，不提交）
│   ├── .env.example        # 环境变量示例
│   ├── app/                # 业务代码
│   │   ├── models/         # ORM 模型
│   │   ├── schemas/        # Pydantic 请求/响应模型
│   │   ├── routers/        # API 路由
│   │   ├── services/       # 业务逻辑层
│   │   └── utils/          # 工具函数
│   └── sql/
│       └── init.sql        # 建表 SQL
│
└── frontend/               # 前端（HTML + TailwindCSS + 原生 JS）
    ├── h5/                 # 前台 H5（客户端）
    │   ├── index.html      # 商品列表
    │   ├── cart.html       # 购物车
    │   ├── checkout.html   # 提交订单
    │   └── success.html    # 提交成功
    └── admin/              # 后台管理系统
        ├── login.html      # 登录页
        ├── index.html      # 首页（数据统计）
        ├── products.html   # 商品管理
        ├── brands.html     # 品牌管理
        ├── tags.html       # 标签管理
        └── orders.html     # 订单管理
```

---

## 常见问题

**Q：启动时报 `ModuleNotFoundError`？**
确认虚拟环境已激活，并已执行 `pip install -r requirements.txt`。

**Q：数据库连接失败？**
检查 `.env` 中的 `DB_HOST`、`DB_PORT`、`DB_USER`、`DB_PASSWORD`、`DB_NAME` 是否正确，确认 MySQL 服务正在运行。

**Q：前端请求后端报跨域错误？**
确认后端已启动（默认端口 8000），前端 `js/api.js` 中的 `BASE_URL` 与后端地址一致。
