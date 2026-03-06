/**
 * 前台 H5 API 请求封装（无需 token，公开接口）
 */
const API_BASE = 'http://localhost:8000/api';
const API_HOST = 'http://localhost:8000';

async function _request(method, path, body = null) {
  const headers = {};
  if (body) headers['Content-Type'] = 'application/json';
  const options = { method, headers };
  if (body) options.body = JSON.stringify(body);

  let res;
  try {
    res = await fetch(API_BASE + path, options);
  } catch (e) {
    throw new Error('网络错误，请检查后端服务是否已启动');
  }

  if (res.status === 204) return null;

  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || `请求失败 (${res.status})`);
  return data;
}

const api = {
  get: (path, params) => {
    const url = params
      ? path + '?' + new URLSearchParams(
          Object.fromEntries(
            Object.entries(params).filter(([, v]) => v !== null && v !== undefined && v !== '')
          )
        )
      : path;
    return _request('GET', url);
  },
  post: (path, body) => _request('POST', path, body),
};

/* ── 全局 Toast ─────────────────────────────────────── */
let _toastTimer = null;
function showToast(msg, type = 'success') {
  const toast = document.getElementById('toast');
  if (!toast) return;
  const icon = type === 'success' ? '✓' : '✕';
  const bgStyle = type === 'success'
    ? 'background:#2D1F1A;'
    : 'background:#9C3A3A;';
  toast.innerHTML = `
    <div style="${bgStyle}color:#fff;font-size:0.875rem;padding:0.75rem 1.25rem;border-radius:4px;box-shadow:0 4px 20px rgba(45,31,26,0.18);display:flex;align-items:center;gap:0.5rem;white-space:nowrap;font-weight:300;letter-spacing:0.04em;">
      <span>${icon}</span><span>${msg}</span>
    </div>`;
  toast.style.opacity = '0';
  toast.style.transform = 'translateY(8px)';
  toast.classList.remove('hidden');
  requestAnimationFrame(() => toast.classList.add('show'));
  clearTimeout(_toastTimer);
  _toastTimer = setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.classList.add('hidden'), 280);
  }, 2000);
}

/* ── 图片 URL 处理 ───────────────────────────────────── */
function imgUrl(url) {
  if (!url) return '';
  if (url.startsWith('http')) return url;
  return API_HOST + (url.startsWith('/') ? '' : '/') + url;
}
