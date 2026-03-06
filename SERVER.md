# 美妆内部销售系统服务管理指南

本文件提供启动和关停项目服务的快速参考指令。

---

## 1. 启动服务

启动服务需要打开两个独立的终端窗口，并分别执行以下指令：

### 终端 A：后端 API 服务 (端口 8000)
1. **进入目录**: `cd d:\AiWorkSpace\my-shop\backend`
2. **激活环境**: `.\venv\Scripts\activate`
3. **启动指令**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

### 终端 B：前端静态服务 (端口 3000)
1. **进入目录**: `cd d:\AiWorkSpace\my-shop\frontend`
2. **启动指令**:
   ```bash
   python -m http.server 3000
   ```

---

## 2. 关停服务

### 常规关停 (推荐)
在运行上述指令的终端窗口中，直接按下键盘组合键：
**`Ctrl + C`**

### 强制关停 (如果端口被占用)
如果按下 `Ctrl + C` 后服务未退出，或者提示端口仍被占用，请在终端执行：

**清理后端端口 (8000)**:
```powershell
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess -Force
```

**清理前端端口 (3000)**:
```powershell
Stop-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess -Force
```

---

## 3. 快速访问入口

| 模块 | 访问地址 |
| :--- | :--- |
| **前台 H5 首页** | [http://localhost:3000/h5/index.html](http://localhost:3000/h5/index.html) |
| **后台管理登录** | [http://localhost:3000/admin/login.html](http://localhost:3000/admin/login.html) |
| **API 文档 (Swagger)** | [http://localhost:8000/docs](http://localhost:8000/docs) |

> **默认账号**: `admin` / `admin123`
