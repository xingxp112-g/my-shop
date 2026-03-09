#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
美妆内部销售系统 - API 健康检查脚本

用法：python scripts/check_api.py [--base-url http://localhost:8000]
输出：JSON 格式到 stdout（供 /check-api 命令解析出报告）

只依赖标准库 + requests，不引入其他第三方库。
"""

import json
import sys
import time
import datetime
import argparse

try:
    import requests
except ImportError:
    print(json.dumps({
        "error": "requests 库未安装，请运行：pip install requests",
        "results": []
    }, ensure_ascii=False))
    sys.exit(1)


# ── 默认配置 ────────────────────────────────────────────────────────────────
DEFAULT_BASE_URL = "http://localhost:8000"
ADMIN_USERNAME   = "admin"
ADMIN_PASSWORD   = "admin123"
TIMEOUT          = 10  # 秒


# ── 单次请求封装 ─────────────────────────────────────────────────────────────
def _request(session: requests.Session, method: str, path: str, base_url: str, **kwargs) -> dict:
    url = base_url.rstrip("/") + path
    start = time.time()
    try:
        resp = session.request(method, url, timeout=TIMEOUT, **kwargs)
        elapsed_ms = round((time.time() - start) * 1000)
        return {
            "path":        path,
            "method":      method,
            "status_code": resp.status_code,
            "elapsed_ms":  elapsed_ms,
            "ok":          resp.status_code < 400,
            "error":       None,
        }
    except requests.exceptions.ConnectionError:
        elapsed_ms = round((time.time() - start) * 1000)
        return {
            "path":        path,
            "method":      method,
            "status_code": None,
            "elapsed_ms":  elapsed_ms,
            "ok":          False,
            "error":       "连接失败（服务可能未启动）",
        }
    except requests.exceptions.Timeout:
        elapsed_ms = round((time.time() - start) * 1000)
        return {
            "path":        path,
            "method":      method,
            "status_code": None,
            "elapsed_ms":  elapsed_ms,
            "ok":          False,
            "error":       f"请求超时（>{TIMEOUT}s）",
        }
    except Exception as exc:
        elapsed_ms = round((time.time() - start) * 1000)
        return {
            "path":        path,
            "method":      method,
            "status_code": None,
            "elapsed_ms":  elapsed_ms,
            "ok":          False,
            "error":       str(exc),
        }


def main():
    parser = argparse.ArgumentParser(description="API 健康检查")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="后端服务地址")
    args = parser.parse_args()
    base_url = args.base_url.rstrip("/")

    checked_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session    = requests.Session()
    results    = []

    # ── 1. 根路径（无需认证）──────────────────────────────────────────────
    results.append(_request(session, "GET", "/", base_url))

    # 如果根路径已连接失败，后续全部会失败，直接输出
    if results[0]["error"] and "连接失败" in results[0]["error"]:
        output = {
            "checked_at":     checked_at,
            "base_url":       base_url,
            "service_up":     False,
            "token_obtained": False,
            "results":        results,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    # ── 2. 登录，获取 token ──────────────────────────────────────────────
    login_result = _request(
        session, "POST", "/api/auth/login", base_url,
        json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD},
    )
    # 登录接口：200=成功，401=密码错误，均视为服务正常
    login_result["ok"] = login_result["status_code"] in (200, 401)
    results.append(login_result)

    token = None
    if login_result["status_code"] == 200:
        try:
            resp = requests.post(
                base_url + "/api/auth/login",
                json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD},
                timeout=TIMEOUT,
            )
            token = resp.json().get("token")
        except Exception:
            pass

    if token:
        session.headers["Authorization"] = f"Bearer {token}"

    # ── 3. 无需认证的只读接口 ─────────────────────────────────────────────
    results.append(_request(session, "GET", "/api/brands",   base_url))
    results.append(_request(session, "GET", "/api/tags",     base_url))
    results.append(_request(session, "GET", "/api/products", base_url))

    # ── 4. 需要认证的只读接口 ─────────────────────────────────────────────
    results.append(_request(session, "GET", "/api/orders",   base_url))
    results.append(_request(session, "GET", "/api/stats",    base_url))

    # ── 5. 写接口：仅做存在性验证（不实际写入数据）──────────────────────
    # POST /api/brands —— 传空 body，期望 422 (Unprocessable Entity)，表明路由存在
    r = _request(session, "POST", "/api/brands", base_url, json={})
    r["ok"] = r["status_code"] in (201, 400, 422)  # 422=参数校验失败，路由存在
    r["note"] = "existence check only (no data written)"
    results.append(r)

    r = _request(session, "POST", "/api/tags", base_url, json={})
    r["ok"] = r["status_code"] in (201, 400, 422)
    r["note"] = "existence check only (no data written)"
    results.append(r)

    r = _request(session, "POST", "/api/products", base_url, json={})
    r["ok"] = r["status_code"] in (201, 400, 422)
    r["note"] = "existence check only (no data written)"
    results.append(r)

    # ── 输出 ──────────────────────────────────────────────────────────────
    output = {
        "checked_at":     checked_at,
        "base_url":       base_url,
        "service_up":     True,
        "token_obtained": token is not None,
        "results":        results,
    }
    print(json.dumps(output, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
