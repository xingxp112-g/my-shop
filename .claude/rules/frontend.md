# 前端规范

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 标记语言 | HTML5 | 无模板引擎，原生 HTML |
| 样式 | TailwindCSS CDN + custom.css | 无构建工具，CDN 引入 |
| 脚本 | 原生 JS（ES6+） | 无框架，无打包工具 |

## 设计系统

详见 `frontend/design-system.md`，页面风格为**黑白灰极简**。

## 页面清单

### 前台 H5（frontend/h5/）

| 文件 | 说明 |
|------|------|
| index.html | 商品列表页（关键词搜索 + 标签筛选） |
| cart.html | 购物车页（金额实时计算） |
| order.html | 提交订单页 |
| success.html | 提交成功页 |

### 后台管理（frontend/admin/）

| 文件 | 说明 |
|------|------|
| login.html | 登录页 |
| index.html | 首页（今日/本月统计数据） |
| products.html | 商品列表页 |
| products-form.html | 新增/编辑商品页 |
| brands.html | 品牌管理页 |
| tags.html | 标签管理页 |
| orders.html | 订单列表页 |
| orders-detail.html | 订单详情页 |

## JS 结构约定

| 文件 | 职责 |
|------|------|
| `js/api.js` | 封装 fetch 请求，统一处理 baseURL 和错误 |
| `admin/js/auth.js` | 登录/登出/token 读写，页面鉴权跳转 |
| 各页面 js | 只处理当前页面的业务逻辑 |

## 业务规则

- 购物车金额在**前端实时计算**，提交订单时连同商品快照价格一起发送给后端
- 后台所有请求需在 Header 携带 `Authorization: Bearer <token>`，由 `auth.js` 统一注入
- 前台 H5 无需登录，直接访问
