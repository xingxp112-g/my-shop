/**
 * 提交订单页逻辑
 * - 从 localStorage 读取购物车数据，渲染商品明细
 * - 表单校验：姓名、手机号必填
 * - 提交 POST /api/orders，成功后清空购物车并跳转首页
 */

const CART_KEY = 'h5_cart';

function getCart() {
  try {
    return JSON.parse(localStorage.getItem(CART_KEY) || '[]');
  } catch {
    return [];
  }
}

/* ── 购物车为空则直接跳回商品列表 ──────────────────── */
const cart = getCart();
if (cart.length === 0) {
  location.replace('index.html');
}

/* ── 渲染商品明细 ──────────────────────────────────── */
function renderItems() {
  const container = document.getElementById('order-items');
  container.innerHTML = cart.map(item => `
    <div class="flex items-center gap-3 px-4 py-3" style="border-bottom:1px solid #F5EDE8;">
      <div class="flex-1 min-w-0">
        <div class="text-xs truncate mb-0.5 font-light tracking-wide" style="color:#9C7B6E;">${item.brand || ''}</div>
        <div class="text-sm line-clamp-2 leading-snug font-light tracking-wide" style="color:#2D1F1A;">${item.name}</div>
        <div class="text-xs mt-1 font-light" style="color:#9C7B6E;">¥${item.price.toFixed(2)} × ${item.quantity}</div>
      </div>
      <span class="text-sm font-medium flex-none" style="color:#C4845A;">
        ¥${(item.price * item.quantity).toFixed(2)}
      </span>
    </div>
  `).join('');

  const total = cart.reduce((sum, i) => sum + i.price * i.quantity, 0);
  const totalCount = cart.reduce((sum, i) => sum + i.quantity, 0);
  const totalStr = `¥${total.toFixed(2)}`;

  document.getElementById('item-count').textContent = totalCount;
  document.getElementById('total-amount').textContent = totalStr;
  document.getElementById('total-amount-bottom').textContent = totalStr;
}

/* ── 表单校验 ──────────────────────────────────────── */
function validate() {
  let ok = true;

  const name = document.getElementById('customer-name').value.trim();
  const errName = document.getElementById('err-name');
  if (!name) {
    errName.classList.remove('hidden');
    ok = false;
  } else {
    errName.classList.add('hidden');
  }

  const phone = document.getElementById('phone').value.trim();
  const errPhone = document.getElementById('err-phone');
  if (!phone) {
    errPhone.classList.remove('hidden');
    ok = false;
  } else {
    errPhone.classList.add('hidden');
  }

  return ok;
}

/* ── 提交订单 ──────────────────────────────────────── */
document.getElementById('submit-btn').addEventListener('click', async () => {
  if (!validate()) return;

  const btn = document.getElementById('submit-btn');
  btn.disabled = true;
  btn.innerHTML = `
    <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
      <path class="opacity-75" fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
    </svg>
    提交中...
  `;

  const payload = {
    customer_name: document.getElementById('customer-name').value.trim(),
    phone:         document.getElementById('phone').value.trim(),
    remark:        document.getElementById('remark').value.trim() || null,
    items: cart.map(item => ({
      product_id: item.id,
      quantity:   item.quantity,
      price:      item.price,
    })),
  };

  try {
    await api.post('/orders', payload);

    // 清空购物车
    localStorage.removeItem(CART_KEY);

    // 提示后跳回首页
    showToast('订单提交成功！');
    setTimeout(() => location.replace('index.html'), 1200);

  } catch (e) {
    showToast(e.message, 'error');
    btn.disabled = false;
    btn.textContent = '提交订单';
  }
});

/* ── 输入时清除对应错误提示 ───────────────────────── */
document.getElementById('customer-name').addEventListener('input', () => {
  document.getElementById('err-name').classList.add('hidden');
});
document.getElementById('phone').addEventListener('input', () => {
  document.getElementById('err-phone').classList.add('hidden');
});

/* ── 初始化 ─────────────────────────────────────────── */
renderItems();
