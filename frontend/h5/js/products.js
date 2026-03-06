/**
 * 前台 H5 商品列表逻辑
 * - 加载标签列表、商品列表
 * - 标签筛选、关键词搜索（防抖）
 * - 加入购物车（localStorage）
 * - 购物车角标更新
 */

/* ── 购物车 localStorage 操作 ───────────────────────── */
const CART_KEY = 'h5_cart';

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

function addToCart(product) {
  const cart = getCart();
  const existing = cart.find(item => item.id === product.id);
  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({
      id: product.id,
      name: product.name,
      brand: product.brand?.name || '',
      price: parseFloat(product.price),
      image_url: product.image_url || '',
      quantity: 1,
    });
  }
  saveCart(cart);
  updateCartBadge();
}

function updateCartBadge() {
  const cart = getCart();
  const total = cart.reduce((sum, item) => sum + item.quantity, 0);
  const badge = document.getElementById('cart-badge');
  if (!badge) return;
  if (total > 0) {
    badge.textContent = total > 99 ? '99+' : String(total);
    badge.classList.remove('hidden');
  } else {
    badge.classList.add('hidden');
  }
}

/* ── 标签筛选 ───────────────────────────────────────── */
let currentTagId = '';

async function loadTags() {
  try {
    const tags = await api.get('/tags');
    const container = document.getElementById('tag-list');
    tags.forEach(tag => {
      const btn = document.createElement('button');
      btn.className = 'tag-btn flex-none px-4 py-1 text-xs transition-colors';
      btn.style.borderRadius = '4px';
      btn.dataset.tagId = String(tag.id);
      btn.textContent = tag.name;
      btn.addEventListener('click', () => selectTag(String(tag.id), btn));
      container.appendChild(btn);
    });
  } catch (e) {
    console.error('加载标签失败', e);
  }
}

function selectTag(tagId, btn) {
  currentTagId = tagId;
  document.querySelectorAll('.tag-btn').forEach(b => b.classList.remove('tag-btn-active'));
  btn.classList.add('tag-btn-active');
  loadProducts();
}

/* ── 商品列表 ───────────────────────────────────────── */
const productsMap = new Map();

function renderSkeleton() {
  return Array(6).fill(0).map(() => `
    <div class="card overflow-hidden">
      <div class="skeleton" style="aspect-ratio:3/4;width:100%"></div>
      <div class="p-3 space-y-2">
        <div class="skeleton h-2.5 w-2/5 rounded"></div>
        <div class="skeleton h-4 w-4/5 rounded"></div>
        <div class="skeleton h-2.5 w-3/5 rounded"></div>
        <div class="flex justify-between items-center mt-2">
          <div class="skeleton h-5 w-1/3 rounded"></div>
          <div class="skeleton w-7 h-7" style="border-radius:4px;"></div>
        </div>
      </div>
    </div>
  `).join('');
}

function renderProductCard(p) {
  const imgHtml = p.image_url
    ? `<img
        class="product-img"
        src="${imgUrl(p.image_url)}"
        alt="${p.name}"
        loading="lazy"
        onerror="this.parentElement.innerHTML=noImgHtml()"
      />`
    : `<div class="product-img-placeholder">${svgPlaceholder()}</div>`;

  const tagsHtml = p.tags && p.tags.length
    ? `<div class="flex gap-1 overflow-hidden mb-1.5">
        ${p.tags.map(t =>
          `<span style="flex:none;font-size:10px;color:#C4845A;border:1px solid rgba(196,132,90,0.28);border-radius:3px;padding:2px 6px;line-height:1.5;font-weight:300;letter-spacing:0.04em;white-space:nowrap;">${t.name}</span>`
        ).join('')}
       </div>`
    : '';

  return `
    <div class="card overflow-hidden">
      <div class="overflow-hidden">${imgHtml}</div>
      <div style="padding:12px 16px 16px;">
        <div class="truncate mb-1" style="font-family:var(--font-display);font-style:italic;font-size:0.72rem;letter-spacing:0.10em;color:var(--color-text-muted);">${p.brand?.name || ''}</div>
        <div class="line-clamp-2 mb-1.5" style="font-size:0.875rem;line-height:1.4;color:var(--color-text-primary);">${p.name}</div>
        ${tagsHtml}
        <div class="flex items-center justify-between">
          <span style="font-family:var(--font-display);font-size:1.1rem;font-weight:500;color:var(--color-primary);letter-spacing:0.02em;">¥${parseFloat(p.price).toFixed(2)}</span>
          <button
            class="add-btn w-7 h-7 flex items-center justify-center"
            style="border-radius:4px;"
            data-id="${p.id}"
            aria-label="加入购物车"
          >
            <svg class="w-3.5 h-3.5 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  `;
}

function svgPlaceholder() {
  return `<svg class="w-10 h-10" style="color:#D9A882;opacity:0.45;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
      d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14
         m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
  </svg>`;
}

function noImgHtml() {
  return `<div class="product-img-placeholder">${svgPlaceholder()}</div>`;
}

async function loadProducts() {
  const keyword = document.getElementById('search-kw').value.trim();
  const list = document.getElementById('product-list');
  const empty = document.getElementById('empty-state');

  list.innerHTML = renderSkeleton();
  empty.classList.add('hidden');

  try {
    const products = await api.get('/products', {
      status: 1,
      keyword: keyword || undefined,
      tag_id: currentTagId || undefined,
    });

    productsMap.clear();
    products.forEach(p => productsMap.set(p.id, p));

    if (products.length === 0) {
      list.innerHTML = '';
      empty.classList.remove('hidden');
      return;
    }

    list.innerHTML = products.map(p => renderProductCard(p)).join('');
  } catch (e) {
    list.innerHTML = '';
    showToast(e.message, 'error');
  }
}

/* ── 事件委托：加入购物车 ────────────────────────────── */
document.getElementById('product-list').addEventListener('click', e => {
  const btn = e.target.closest('.add-btn');
  if (!btn) return;
  const id = parseInt(btn.dataset.id, 10);
  const product = productsMap.get(id);
  if (!product) return;
  addToCart(product);
  showToast('已加入购物车');
});

/* ── 搜索防抖 ────────────────────────────────────────── */
let searchTimer = null;
document.getElementById('search-kw').addEventListener('input', () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(loadProducts, 400);
});

/* ── 初始化 ──────────────────────────────────────────── */
updateCartBadge();
loadTags();
loadProducts();
