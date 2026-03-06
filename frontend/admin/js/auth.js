/**
 * 认证工具
 * - requireAuth()：在需要登录的页面顶部调用
 * - authLogout()：退出登录
 */
function requireAuth() {
  if (!localStorage.getItem('admin_token')) {
    window.location.href = 'login.html';
  }
}

function authLogout() {
  localStorage.removeItem('admin_token');
  localStorage.removeItem('admin_user');
  window.location.href = 'login.html';
}

function getAdminUser() {
  return localStorage.getItem('admin_user') || 'admin';
}
