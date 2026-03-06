/**
 * 购物车逻辑
 * - 从 localStorage 读取购物车数据并渲染
 * - 支持：修改数量（+/-）、删除单条、清空
 * - 实时计算总金额
 * - "去提交订单"跳转到 order.html
 */

const CART_KEY = 'h5_cart';

/* ── localStorage 读写 ─────────────────────────────── */
function getCart() {
  try {
    return JSON.parse(localStorage.getItem(CART_KEY) || '[]');
  } catch {
    return [];
  }
}

function saveCart(cart) {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
}

/* ── 渲染购物车列表 ───────────────────────────────── */
function renderCart() {
  const cart = getCart();
  const listEl   = document.getElementById('cart-list');
  const emptyEl  = document.getElementById('empty-state');
  const checkoutBtn = document.getElementById('checkout-btn');
  const clearBtn    = document.getElementById('clear-btn');

  if (cart.length === 0) {
    listEl.innerHTML = '';
    emptyEl.classList.remove('hidden');
    checkoutBtn.disabled = true;
    clearBtn.classList.add('invisible');
    updateTotal(0);
    return;
  }

  emptyEl.classList.add('hidden');
  checkoutBtn.disabled = false;
  clearBtn.classList.remove('invisible');

  listEl.innerHTML = cart.map(renderItem).join('');
  updateTotal(cart.reduce((sum, item) => sum + item.price * item.quantity, 0));
}

function renderItem(item) {
  const imgHtml = item.image_url
    ? `<img
        src="${imgUrl(item.image_url)}"
        alt="${item.name}"
        class="w-20 h-20 object-cover flex-none"
        style="border-radius:6px;"
        loading="lazy"
        onerror="this.replaceWith(noImgEl())"
      />`
    : noImgElHtml();

  return `
    <div class="card p-3 mb-3 flex gap-3" data-id="${item.id}">

      ${imgHtml}

      <div class="flex-1 min-w-0 flex flex-col">
        <!-- 品牌 + 名称 -->
        <div class="text-xs truncate font-light tracking-wide" style="color:#9C7B6E;">${item.brand || ''}</div>
        <div class="text-sm line-clamp-2 leading-snug mt-0.5 mb-2 font-light tracking-wide" style="color:#2D1F1A;">${item.name}</div>

        <!-- 单价 + 数量控制 -->
        <div class="flex items-center justify-between mt-auto">
          <span class="text-base font-medium" style="color:#C4845A;">¥${item.price.toFixed(2)}</span>

          <div class="flex items-center gap-2">
            <button
              class="qty-btn qty-minus"
              data-id="${item.id}"
              aria-label="减少数量"
            >−</button>
            <span class="qty-num w-6 text-center text-sm font-light select-none" style="color:#2D1F1A;">${item.quantity}</span>
            <button
              class="qty-btn qty-plus"
              data-id="${item.id}"
              aria-label="增加数量"
            >+</button>
          </div>
        </div>

        <!-- 小计 + 删除 -->
        <div class="flex items-center justify-between mt-1.5">
          <span class="text-xs font-light" style="color:#9C7B6E;">小计 ¥${(item.price * item.quantity).toFixed(2)}</span>
          <button
            class="del-btn text-xs font-light"
            style="color:rgba(196,132,90,0.45);"
            data-id="${item.id}"
            aria-label="删除"
          >移除</button>
        </div>
      </div>

    </div>
  `;
}

function noImgElHtml() {
  return `<div class="w-20 h-20 flex-none flex items-center justify-center" style="background:#FAF7F5;border-radius:6px;">
    <svg class="w-8 h-8" style="color:#D9A882;opacity:0.45;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
        d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14
           m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
    </svg>
  </div>`;
}

function noImgEl() {
  const div = document.createElement('div');
  div.className = 'w-20 h-20 flex-none flex items-center justify-center';
  div.style.cssText = 'background:#FAF7F5;border-radius:6px;';
  div.innerHTML = `<svg class="w-8 h-8" style="color:#D9A882;opacity:0.45;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
      d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14
         m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
  </svg>`;
  return div;
}

/* ── 更新总金额 ─────────────────────────────────────── */
function updateTotal(amount) {
  document.getElementById('total-amount').textContent = `¥${Number(amount).toFixed(2)}`;
}

/* ── 修改数量 ───────────────────────────────────────── */
function changeQty(id, delta) {
  const cart = getCart();
  const item = cart.find(i => i.id === id);
  if (!item) return;
  item.quantity = Math.max(1, item.quantity + delta);
  saveCart(cart);
  renderCart();
}

/* ── 删除单条 ───────────────────────────────────────── */
function removeItem(id) {
  saveCart(getCart().filter(i => i.id !== id));
  renderCart();
}

/* ── 事件委托（数量 + 删除） ──────────────────────── */
document.getElementById('cart-list').addEventListener('click', e => {
  const btn = e.target.closest('[data-id]');
  if (!btn) return;
  const id = parseInt(btn.dataset.id, 10);

  if (e.target.closest('.qty-minus')) {
    changeQty(id, -1);
  } else if (e.target.closest('.qty-plus')) {
    changeQty(id, 1);
  } else if (e.target.closest('.del-btn')) {
    removeItem(id);
    showToast('已删除');
  }
});

/* ── 清空购物车 ─────────────────────────────────────── */
document.getElementById('clear-btn').addEventListener('click', () => {
  if (getCart().length === 0) return;
  saveCart([]);
  renderCart();
  showToast('购物车已清空');
});

/* ── 去提交订单 ─────────────────────────────────────── */
document.getElementById('checkout-btn').addEventListener('click', () => {
  if (getCart().length === 0) return;
  location.href = 'order.html';
});

/* ── 初始化 ─────────────────────────────────────────── */
renderCart();
