# 电子代金券功能 — 完整实现规格

> 文档版本：v1.0
> 访谈日期：2026-03-10
> 状态：待开发

---

## 1. 功能概述

在后台管理系统新增「代金券管理」模块，供销售/运营人员批量生成固定面额代金券，打印或口头告知客户券码，客户在线下支付时出示券码，由销售人员在后台完成手动核销，实现抵扣记录。

---

## 2. 业务规则

### 2.1 代金券属性
| 属性 | 规则 |
|------|------|
| 类型 | 固定金额抵扣（非折扣率） |
| 面额 | 同一批次所有券面额相同，单位元，保留两位小数 |
| 券码 | 系统自动生成，6位字母+数字混合（大写字母 A-Z，数字 0-9） |
| 有效期 | 起始日期 + 截止日期（精确到天） |
| 使用限制 | 每张只能核销一次；过期后自动变为「已过期」状态，不可核销 |

### 2.2 券码生成规则
- 格式：`[A-Z0-9]{6}`，示例：`A3F9K2`
- 系统保证全局唯一（生成时查重，冲突则重新生成）
- 不区分大小写（系统内统一存储和比对时转为大写）

### 2.3 代金券状态机
```
未使用 ──核销──► 已使用（终态，不可撤销）
未使用 ──过期──► 已过期（终态）
```
- 状态共 3 种：`unused` / `used` / `expired`
- 核销时实时校验：已过期 → 拒绝核销；已使用 → 提示重复

### 2.4 核销流程
1. 销售人员在后台「核销代金券」弹窗中输入券码
2. 系统校验：存在性 → 有效期 → 是否已使用
3. 校验通过后，将状态改为 `used`，记录核销时间和操作人
4. **无需关联订单**

### 2.5 不支持的操作
- 核销后不可撤销/退回
- 不支持客户在前台 H5 自主输入券码（仅后台核销）
- 不支持绑定特定客户/商品/品牌

---

## 3. 数据库设计

### 3.1 新增表：`voucher`（代金券表）

```sql
CREATE TABLE voucher (
    id            INT PRIMARY KEY AUTO_INCREMENT,
    code          VARCHAR(6)     NOT NULL UNIQUE,   -- 券码，6位大写字母+数字
    amount        DECIMAL(10,2)  NOT NULL,           -- 面额（元）
    start_date    DATE           NOT NULL,           -- 有效期开始
    end_date      DATE           NOT NULL,           -- 有效期截止
    status        VARCHAR(10)    NOT NULL DEFAULT 'unused',  -- unused/used/expired
    used_at       DATETIME       NULL,               -- 核销时间
    used_by       VARCHAR(50)    NULL,               -- 核销操作人（冗余存储用户名）
    batch_no      VARCHAR(50)    NULL,               -- 批次号（创建时自动生成，便于追溯）
    created_at    DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_code (code),
    INDEX idx_status (status),
    INDEX idx_batch (batch_no),
    INDEX idx_end_date (end_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**字段说明：**
- `batch_no`：批次号格式 `BATCH-{YYYYMMDD}-{4位随机数}`，如 `BATCH-20260310-A3F9`，同批次创建的券共享同一批次号
- `used_by`：从 Bearer Token 中解析的当前登录用户名（通过 `get_current_user` 依赖注入获取，JWT payload 的 `sub` 字段），如 `admin`
- `status` 值 `expired` 不在数据库中自动更新，由查询/核销时实时判断 `end_date < CURDATE()`

### 3.2 状态判断逻辑（非存储态）
```
实际状态 =
  if status == 'used'   → 已使用
  elif end_date < today → 已过期
  else                  → 未使用
```
> 数据库中 `status` 字段只存 `unused` / `used`，`expired` 为计算态，避免批量更新过期状态的定时任务需求。

---

## 4. 后端 API 设计

### 4.1 路由文件
新建 `backend/app/routers/vouchers.py`，所有接口前缀 `/api/vouchers`，需要 Bearer Token 认证。

### 4.2 接口列表

#### POST `/api/vouchers/batch` — 批量创建代金券
**请求体：**
```json
{
  "amount": 50.00,          // 面额，必填，> 0
  "quantity": 20,           // 数量，必填，1-100
  "start_date": "2026-03-10",
  "end_date": "2026-04-10"
}
```
**响应：**
```json
{
  "batch_no": "BATCH-20260310-A3F9",
  "count": 20,
  "codes": ["A3F9K2", "B7HX19", "..."]  // 返回所有生成的券码
}
```
**校验：**
- `quantity` 范围 1-100，超出返回 400
- `end_date` 必须 >= `start_date`，否则返回 400
- `amount` 必须 > 0

#### GET `/api/vouchers` — 代金券列表（支持筛选）
**查询参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| `status` | string | `unused` / `used` / `expired` |
| `code` | string | 精确或模糊搜索（LIKE %code%） |
| `amount` | decimal | 按面额精确筛选 |
| `date_from` | date | 有效期开始 >= 该日期 |
| `date_to` | date | 有效期截止 <= 该日期 |
| `page` | int | 页码，默认 1 |
| `page_size` | int | 每页数量，默认 20 |

**响应：**
```json
{
  "total": 100,
  "items": [
    {
      "id": 1,
      "code": "A3F9K2",
      "amount": 50.00,
      "start_date": "2026-03-10",
      "end_date": "2026-04-10",
      "status": "unused",     // 计算后的实际状态
      "used_at": null,
      "used_by": null,
      "batch_no": "BATCH-20260310-A3F9",
      "created_at": "2026-03-10T10:00:00"
    }
  ]
}
```
> `status` 字段在接口层根据 `end_date` 和数据库 `status` 字段计算后返回。

#### POST `/api/vouchers/redeem` — 核销代金券
> 需要 Bearer Token 认证；后端从 Token 中提取 `current_user` 并写入 `used_by` 字段。

**请求体：**
```json
{
  "code": "A3F9K2"
}
```
**响应（成功）：**
```json
{
  "code": "A3F9K2",
  "amount": 50.00,
  "used_at": "2026-03-10T15:30:00"
}
```
**错误响应：**
| HTTP Code | 场景 |
|-----------|------|
| 404 | 券码不存在 |
| 400 | 券已使用（`detail: "该券已于 XX 核销"`） |
| 400 | 券已过期（`detail: "该券已于 XX 过期"`） |

#### GET `/api/vouchers/export` — 导出 Excel
**查询参数：** 同列表接口（按当前筛选条件导出，无分页限制）
**响应：** `Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`，文件名 `vouchers_{timestamp}.xlsx`

**导出字段：**
| 列名 | 字段 |
|------|------|
| 券码 | code |
| 面额（元） | amount |
| 有效期开始 | start_date |
| 有效期截止 | end_date |
| 状态 | 未使用/已使用/已过期 |
| 核销时间 | used_at（空时留空） |
| 批次号 | batch_no |

---

## 5. 前端页面设计

### 5.1 新增文件
```
frontend/admin/
├── vouchers.html           # 代金券列表页（含核销入口）
├── vouchers-create.html    # 批量创建代金券页
└── js/
    └── vouchers.js         # 代金券页面逻辑
```

### 5.2 导航菜单
在后台所有页面的左侧/顶部导航中，于「标签管理」后增加「代金券」入口，指向 `vouchers.html`。

### 5.3 `vouchers.html` — 代金券列表页

**页面布局（与现有后台页面风格一致：黑白灰极简）：**

```
┌──────────────────────────────────────────────────────────┐
│  代金券管理                    [批量创建] [导出 Excel]     │
├──────────────────────────────────────────────────────────┤
│  筛选栏：                                                 │
│  [状态 ▼] [面额 ____] [券码搜索 ____]                     │
│  [有效期从 ____] [至 ____]  [查询] [重置]                 │
├──────────────────────────────────────────────────────────┤
│  券码     │ 面额  │ 有效期          │ 状态  │ 核销时间 │操作│
│  A3F9K2   │ ¥50  │ 03-10 ~ 04-10  │ 未使用│         │[核销]│
│  B7HX19   │ ¥50  │ 03-10 ~ 04-10  │ 已使用│03-15     │  -  │
│  ...                                                     │
├──────────────────────────────────────────────────────────┤
│  共 100 条  < 1 2 3 ... >                                │
└──────────────────────────────────────────────────────────┘
```

**操作说明：**
- 状态「未使用」时显示 `[核销]` 按钮
- 状态「已使用」或「已过期」不显示操作按钮
- 点击「核销」弹出确认 Modal：显示券码、面额，输入框无需再输入（已知券码），点击「确认核销」调用接口
- **列表行内核销与快速核销共用同一个 JS 函数** `redeemVoucher(code)`，两个入口只是传参方式不同，不重复实现核销逻辑

**核销 Modal：**
```
┌──────────────────────────┐
│  核销代金券               │
│                          │
│  券码：A3F9K2            │
│  面额：¥50.00            │
│  有效期至：2026-04-10    │
│                          │
│  [取消]  [确认核销]       │
└──────────────────────────┘
```

> 也可支持在列表页顶部提供「输入券码快速核销」的独立入口，方便直接从客户口述的券码操作，不需要先搜索找到券再点核销。

**快速核销区（列表页顶部附加）：**
```
┌──────────────────────────────────┐
│  快速核销：[输入券码 ____] [核销] │
└──────────────────────────────────┘
```

### 5.4 `vouchers-create.html` — 批量创建页

```
┌──────────────────────────────────┐
│  批量创建代金券                   │
│                                  │
│  面额（元）  [________]          │
│  数量        [________]  (1-100) │
│  有效期开始  [日期选择]           │
│  有效期截止  [日期选择]           │
│                                  │
│  [取消]  [创建]                  │
└──────────────────────────────────┘
```

创建成功后跳转到 `vouchers.html` 并自动按本次批次号筛选，展示刚创建的券。

---

## 6. 技术实现要点

### 6.1 后端依赖
- 导出 Excel 使用 `openpyxl` 库（需加入 `requirements.txt`）
- 券码生成使用 `secrets` 或 `random` 模块，生成后查 DB 去重

### 6.2 券码生成算法
```python
import random, string

def generate_code() -> str:
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=6))

def generate_unique_codes(db, count: int) -> list[str]:
    codes = set()
    while len(codes) < count:
        code = generate_code()
        # 排除已存在的码
        if not db.query(Voucher).filter_by(code=code).first():
            codes.add(code)
    return list(codes)
```

### 6.3 状态计算逻辑（Python）
```python
from datetime import date

def get_actual_status(voucher) -> str:
    if voucher.status == 'used':
        return 'used'
    if voucher.end_date < date.today():
        return 'expired'
    return 'unused'
```

### 6.4 列表接口的 expired 筛选
由于 `expired` 是计算态，当前端传 `status=expired` 时，后端转换为：
```python
# status=expired 时的查询条件
query = query.filter(Voucher.status == 'unused', Voucher.end_date < date.today())
# status=unused 时的查询条件
query = query.filter(Voucher.status == 'unused', Voucher.end_date >= date.today())
```

---

## 7. 新增文件清单

| 文件 | 说明 |
|------|------|
| `backend/app/models/voucher.py` | Voucher ORM 模型 |
| `backend/app/schemas/voucher.py` | Pydantic 请求/响应 Schema |
| `backend/app/routers/vouchers.py` | API 路由 |
| `backend/app/services/voucher_service.py` | 业务逻辑（生成码、核销、导出） |
| `backend/sql/voucher.sql` | 建表 SQL（增量，不重建已有表） |
| `frontend/admin/vouchers.html` | 代金券列表页 |
| `frontend/admin/vouchers-create.html` | 批量创建页 |
| `frontend/admin/js/vouchers.js` | 前端逻辑 |

### 需修改的现有文件
| 文件 | 改动 |
|------|------|
| `backend/main.py` | 注册 `vouchers` router |
| `backend/requirements.txt` | 新增 `openpyxl` |
| `frontend/admin/*.html` | 导航菜单加「代金券」入口 |

---

## 8. 边界情况与风险

| 场景 | 处理方式 |
|------|----------|
| 生成 100 张时极小概率生成重复码 | 生成后逐个查库去重，重复则重新生成，最多重试 10 次 |
| 导出筛选结果超大量数据 | 上限 10000 条；超出时返回提示"结果过多，请缩小筛选范围" |
| 券码大小写混淆 | 接口接收时统一 `.upper()` 处理，前端输入框自动转大写 |
| 有效期结束日当天是否可用 | `end_date` 当天 23:59:59 前均可核销（`end_date >= today`） |
| 并发核销同一张券 | 更新时加 `WHERE status='unused'` 条件，利用数据库行锁保证幂等 |
| `openpyxl` 未安装导致导出失败 | 接口返回 500 并在日志记录，提示管理员安装依赖 |

---

## 9. 验收标准

- [ ] 批量创建 20 张 ¥50 代金券，有效期 30 天，系统生成 20 个不重复 6 位券码
- [ ] 列表页按状态、面额、券码、有效期筛选均正常
- [ ] 输入未使用的有效券码完成核销，状态变为「已使用」，核销时间正确记录
- [ ] 重复核销同一张券，提示已核销，不改变数据
- [ ] 核销已过期券，提示已过期，不允许核销
- [ ] 按当前筛选条件导出 Excel，包含券码、面额、有效期、状态、核销时间字段
- [ ] 导航菜单「代金券」入口可正常跳转
