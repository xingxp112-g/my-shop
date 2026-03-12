// 代金券管理 - 页面逻辑

let currentPage = 1;
const PAGE_SIZE = 20;
let redeemingCode = null;  // 当前核销 Modal 中的券码

// ── 筛选参数 ─────────────────────────────────────────────────────────────────

function getFilters() {
  return {
    status:    document.getElementById('filter-status').value || undefined,
    code:      document.getElementById('filter-code').value.trim().toUpperCase() || undefined,
    amount:    document.getElementById('filter-amount').value || undefined,
    date_from: document.getElementById('filter-date-from').value || undefined,
    date_to:   document.getElementById('filter-date-to').value || undefined,
    page:      currentPage,
    page_size: PAGE_SIZE,
  };
}

function resetFilters() {
  document.getElementById('filter-status').value = '';
  document.getElementById('filter-code').value = '';
  document.getElementById('filter-amount').value = '';
  document.getElementById('filter-date-from').value = '';
  document.getElementById('filter-date-to').value = '';
  currentPage = 1;
  loadVouchers();
}

// ── 列表加载 ──────────────────────────────────────────────────────────────────

async function loadVouchers() {
  const tbody = document.getElementById('voucher-list');
  tbody.innerHTML = `<tr><td colspan="7" style="padding:32px 0;text-align:center;color:var(--color-text-muted);font-size:13px;">加载中...</td></tr>`;

  try {
    const params = {};
    const f = getFilters();
    Object.keys(f).forEach(k => { if (f[k] !== undefined) params[k] = f[k]; });

    const data = await api.get('/vouchers', params);
    renderTable(data.items);
    renderPagination(data.total, currentPage, PAGE_SIZE);
    document.getElementById('total-count').textContent = `共 ${data.total} 条`;
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="7" style="padding:48px 0;text-align:center;color:var(--color-danger);font-size:13px;">加载失败：${err.message}</td></tr>`;
  }
}

function renderTable(items) {
  const tbody = document.getElementById('voucher-list');
  if (!items.length) {
    tbody.innerHTML = `
      <tr><td colspan="7">
        <div class="empty-state">
          <svg class="empty-state-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"/>
          </svg>
          <p class="empty-state-text">暂无代金券</p>
        </div>
      </td></tr>`;
    return;
  }

  const statusLabel = { unused: '未使用', used: '已使用', expired: '已过期' };
  const statusClass = { unused: 'badge-success', used: 'badge-neutral', expired: 'badge-danger' };

  tbody.innerHTML = items.map(v => {
    const dateRange = `${v.start_date} ~ ${v.end_date}`;
    const usedAt = v.used_at ? v.used_at.replace('T', ' ').slice(0, 16) : '—';
    const usedBy = v.used_by || '—';
    const badge = `<span class="status-badge ${statusClass[v.status] || 'badge-neutral'}">${statusLabel[v.status] || v.status}</span>`;
    const action = v.status === 'unused'
      ? `<button onclick="openRedeemModal('${v.code}', '${v.amount}', '${v.end_date}')" class="btn-edit-text">核销</button>`
      : `<span style="color:var(--color-text-muted);font-size:12px;">—</span>`;
    return `
      <tr>
        <td style="font-family:monospace;font-size:13px;font-weight:600;letter-spacing:0.05em;">${v.code}</td>
        <td style="font-size:14px;">¥${parseFloat(v.amount).toFixed(2)}</td>
        <td style="font-size:12px;color:var(--color-text-secondary);">${dateRange}</td>
        <td>${badge}</td>
        <td style="font-size:12px;color:var(--color-text-secondary);">${usedAt}</td>
        <td style="font-size:12px;color:var(--color-text-secondary);">${usedBy}</td>
        <td class="col-right">${action}</td>
      </tr>`;
  }).join('');
}

function renderPagination(total, page, pageSize) {
  const container = document.getElementById('pagination');
  const totalPages = Math.ceil(total / pageSize);
  if (totalPages <= 1) { container.innerHTML = ''; return; }

  let html = '';
  const btn = (p, label, disabled, active) =>
    `<button onclick="goPage(${p})" class="page-btn${active ? ' active' : ''}"${disabled ? ' disabled' : ''}>${label}</button>`;

  html += btn(page - 1, '‹', page === 1, false);
  for (let i = 1; i <= totalPages; i++) {
    if (i === 1 || i === totalPages || Math.abs(i - page) <= 2) {
      html += btn(i, i, false, i === page);
    } else if (Math.abs(i - page) === 3) {
      html += `<span class="page-ellipsis">…</span>`;
    }
  }
  html += btn(page + 1, '›', page === totalPages, false);
  container.innerHTML = html;
}

function goPage(p) {
  currentPage = p;
  loadVouchers();
}

// ── 核销（列表行内 + 快速核销共用此函数）────────────────────────────────────

async function redeemVoucher(code) {
  const btn = document.getElementById('redeem-confirm-btn');
  if (btn) { btn.disabled = true; btn.textContent = '核销中...'; }

  try {
    const result = await api.post('/vouchers/redeem', { code: code.toUpperCase() });
    closeRedeemModal();
    showToast(`券码 ${result.code} 核销成功，面额 ¥${parseFloat(result.amount).toFixed(2)}`);
    loadVouchers();
  } catch (err) {
    showToast(err.message, 'error');
  } finally {
    if (btn) { btn.disabled = false; btn.textContent = '确认核销'; }
  }
}

// ── 核销 Modal ────────────────────────────────────────────────────────────────

function openRedeemModal(code, amount, endDate) {
  redeemingCode = code;
  document.getElementById('redeem-code').textContent = code;
  document.getElementById('redeem-amount').textContent = `¥${parseFloat(amount).toFixed(2)}`;
  document.getElementById('redeem-end-date').textContent = endDate;
  document.getElementById('redeem-modal').classList.remove('hidden');
  document.body.classList.add('modal-open');
}

function closeRedeemModal() {
  document.getElementById('redeem-modal').classList.add('hidden');
  document.body.classList.remove('modal-open');
  redeemingCode = null;
}

function handleRedeemOverlayClick(e) {
  if (e.target === document.getElementById('redeem-modal')) closeRedeemModal();
}

// ── 快速核销 ──────────────────────────────────────────────────────────────────

async function quickRedeem() {
  const input = document.getElementById('quick-code');
  const code = input.value.trim().toUpperCase();
  if (!code) { showToast('请输入券码', 'error'); return; }
  if (code.length !== 6) { showToast('券码为 6 位字母+数字', 'error'); return; }

  const btn = document.getElementById('quick-redeem-btn');
  btn.disabled = true;
  btn.textContent = '核销中...';

  try {
    const result = await api.post('/vouchers/redeem', { code });
    input.value = '';
    showToast(`券码 ${result.code} 核销成功，面额 ¥${parseFloat(result.amount).toFixed(2)}`);
    loadVouchers();
  } catch (err) {
    showToast(err.message, 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = '核销';
  }
}

// ── 导出 Excel ────────────────────────────────────────────────────────────────

async function exportVouchers() {
  const f = getFilters();
  const params = new URLSearchParams();
  if (f.status)    params.set('status', f.status);
  if (f.code)      params.set('code', f.code);
  if (f.amount)    params.set('amount', f.amount);
  if (f.date_from) params.set('date_from', f.date_from);
  if (f.date_to)   params.set('date_to', f.date_to);

  const token = localStorage.getItem('admin_token');
  const url = `http://localhost:8000/api/vouchers/export?${params.toString()}`;

  try {
    const resp = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
    if (!resp.ok) {
      const data = await resp.json().catch(() => ({}));
      showToast(data.detail || '导出失败', 'error');
      return;
    }
    const blob = await resp.blob();
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `vouchers_${Date.now()}.xlsx`;
    a.click();
    URL.revokeObjectURL(a.href);
    showToast('导出成功');
  } catch (err) {
    showToast('网络错误，导出失败', 'error');
  }
}

// ── URL 参数初始化（创建页跳转后按 batch_no 筛选）─────────────────────────

function initFromUrl() {
  const params = new URLSearchParams(location.search);
  const batchNo = params.get('batch_no');
  if (batchNo) {
    // batch_no 作为 code 模糊搜索（batch 筛选暂无独立字段，用提示替代）
    // 实际上 batch_no 不在前端筛选项里，直接展示成功消息即可
    showToast(`批次 ${batchNo} 创建成功`);
  }
}
