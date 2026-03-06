"""快速冒烟测试"""
import requests

BASE = "http://localhost:8000/api"

# 1. 登录
r = requests.post(f"{BASE}/auth/login", json={"username": "admin", "password": "admin123"})
assert r.status_code == 200, r.text
token = r.json()["token"]
headers = {"Authorization": f"Bearer {token}"}
print("✓ 登录成功")

# 2. 品牌 CRUD
r = requests.post(f"{BASE}/brands", json={"name": "雅诗兰黛"}, headers=headers)
assert r.status_code == 201, r.text
brand_id = r.json()["id"]
print(f"✓ 新增品牌 id={brand_id}")

r = requests.get(f"{BASE}/brands")
assert any(b["id"] == brand_id for b in r.json())
print("✓ 品牌列表")

# 3. 标签 CRUD
r = requests.post(f"{BASE}/tags", json={"name": "内贸"}, headers=headers)
assert r.status_code == 201, r.text
tag_id = r.json()["id"]
print(f"✓ 新增标签 id={tag_id}")

# 4. 商品 CRUD
r = requests.post(f"{BASE}/products", json={
    "name": "小棕瓶精华",
    "brand_id": brand_id,
    "price": "299.00",
    "remark": "明星单品",
    "tag_ids": [tag_id],
}, headers=headers)
assert r.status_code == 201, r.text
product_id = r.json()["id"]
print(f"✓ 新增商品 id={product_id}")

# 5. 商品列表（含搜索）
r = requests.get(f"{BASE}/products", params={"keyword": "精华"})
assert any(p["id"] == product_id for p in r.json())
print("✓ 商品列表（关键词搜索）")

# 6. 商品上下架
r = requests.patch(f"{BASE}/products/{product_id}/status", json={"status": 0}, headers=headers)
assert r.json()["status"] == 0
print("✓ 商品下架")

# 7. 提交订单（无需 token）
r = requests.post(f"{BASE}/orders", json={
    "customer_name": "张三",
    "phone": "13800138000",
    "remark": "测试订单",
    "items": [{"product_id": product_id, "quantity": 2, "price": "299.00"}],
})
assert r.status_code == 201, r.text
order_id = r.json()["id"]
assert float(r.json()["total_amount"]) == 598.0
print(f"✓ 提交订单 id={order_id}，总金额={r.json()['total_amount']}")

# 8. 订单列表 + 状态修改
r = requests.get(f"{BASE}/orders", headers=headers)
assert any(o["id"] == order_id for o in r.json())
print("✓ 订单列表")

r = requests.patch(f"{BASE}/orders/{order_id}/status", json={"status": "已确认"}, headers=headers)
assert r.json()["status"] == "已确认"
print("✓ 订单状态变更")

# 9. 统计
r = requests.get(f"{BASE}/stats", headers=headers)
d = r.json()
assert d["today_order_count"] >= 1
print(f"✓ 统计：今日订单 {d['today_order_count']} 笔，金额 {d['today_order_amount']}")

print("\n🎉 所有接口验证通过")
