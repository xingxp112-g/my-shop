/**
 * API 请求封装
 * 所有后台接口调用均通过此文件
 */
const API_BASE = 'http://localhost:8000/api';

function _getToken() {
  return localStorage.getItem('admin_token');
}

async function _request(method, path, body = null, isFormData = false) {
  const headers = {};
  const token = _getToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;
  if (body && !isFormData) headers['Content-Type'] = 'application/json';

  const options = { method, headers };
  if (body) options.body = isFormData ? body : JSON.stringify(body);

  let res;
  try {
    res = await fetch(API_BASE + path, options);
  } catch (e) {
    throw new Error('网络错误，请检查后端服务是否启动');
  }

  if (res.status === 401) {
    localStorage.removeItem('admin_token');
    localStorage.removeItem('admin_user');
    window.location.href = 'login.html';
    return;
  }

  if (res.status === 204) return null;

  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || `请求失败 (${res.status})`);
  return data;
}

const api = {
  get:    (path, params) => {
    const url = params ? path + '?' + new URLSearchParams(
      Object.fromEntries(Object.entries(params).filter(([,v]) => v !== null && v !== undefined && v !== ''))
    ) : path;
    return _request('GET', url);
  },
  post:   (path, body)  => _request('POST',   path, body),
  put:    (path, body)  => _request('PUT',    path, body),
  patch:  (path, body)  => _request('PATCH',  path, body),
  del:    (path)        => _request('DELETE', path),
  upload: (path, formData) => _request('POST', path, formData, true),
};

/* ── 全局 Toast ────────────────────────────────────── */
let _toastTimer = null;
function showToast(msg, type = 'success') {
  const toast = document.getElementById('toast');
  if (!toast) return;
  const icon  = type === 'success' ? '✓' : '✕';
  const bg    = type === 'success' ? 'bg-gray-900' : 'bg-red-600';
  toast.innerHTML = `
    <div class="${bg} text-white text-sm px-4 py-3 rounded-lg shadow-xl flex items-center gap-2 min-w-[200px]">
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
  }, 3000);
}
