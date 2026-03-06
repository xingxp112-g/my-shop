import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import auth, brands, tags, products, orders, stats

app = FastAPI(title="美妆内部销售系统 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 图片上传目录（静态文件服务）
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(auth.router,     prefix="/api/auth",     tags=["认证"])
app.include_router(brands.router,   prefix="/api/brands",   tags=["品牌"])
app.include_router(tags.router,     prefix="/api/tags",     tags=["标签"])
app.include_router(products.router, prefix="/api/products", tags=["商品"])
app.include_router(orders.router,   prefix="/api/orders",   tags=["订单"])
app.include_router(stats.router,    prefix="/api/stats",    tags=["统计"])


@app.get("/")
def root():
    return {"message": "美妆内部销售系统 API 正常运行"}
