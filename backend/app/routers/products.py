import os
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session, joinedload

from app.config import settings
from app.database import get_db
from app.models.product import Product
from app.models.tag import Tag
from app.schemas.product import ProductCreate, ProductUpdate, ProductStatusUpdate, ProductOut
from app.utils.auth import get_current_user

router = APIRouter()


def _get_product_or_404(product_id: int, db: Session) -> Product:
    product = (
        db.query(Product)
        .options(joinedload(Product.brand), joinedload(Product.tags))
        .filter(Product.id == product_id)
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product


def _set_tags(product: Product, tag_ids: list[int], db: Session):
    if tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
    else:
        tags = []
    product.tags = tags


@router.get("", response_model=list[ProductOut])
def list_products(
    keyword: Optional[str] = None,
    tag_id: Optional[int] = None,
    status: Optional[int] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Product).options(joinedload(Product.brand), joinedload(Product.tags))

    if keyword:
        q = q.filter(Product.name.like(f"%{keyword}%"))
    if tag_id is not None:
        q = q.filter(Product.tags.any(Tag.id == tag_id))
    if status is not None:
        q = q.filter(Product.status == status)

    return q.order_by(Product.id.desc()).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return _get_product_or_404(product_id, db)


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(body: ProductCreate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    product = Product(
        name=body.name,
        brand_id=body.brand_id,
        price=body.price,
        image_url=body.image_url,
        remark=body.remark,
    )
    _set_tags(product, body.tag_ids, db)
    db.add(product)
    db.commit()
    db.refresh(product)
    return _get_product_or_404(product.id, db)


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int, body: ProductUpdate, db: Session = Depends(get_db), _: str = Depends(get_current_user)
):
    product = _get_product_or_404(product_id, db)
    product.name = body.name
    product.brand_id = body.brand_id
    product.price = body.price
    product.image_url = body.image_url
    product.remark = body.remark
    _set_tags(product, body.tag_ids, db)
    db.commit()
    return _get_product_or_404(product_id, db)


@router.patch("/{product_id}/status", response_model=ProductOut)
def update_product_status(
    product_id: int, body: ProductStatusUpdate, db: Session = Depends(get_db), _: str = Depends(get_current_user)
):
    product = _get_product_or_404(product_id, db)
    product.status = body.status
    db.commit()
    return _get_product_or_404(product_id, db)


@router.post("/upload-image", status_code=status.HTTP_200_OK)
async def upload_image(file: UploadFile = File(...), _: str = Depends(get_current_user)):
    """上传商品图片，返回可访问的 URL 路径"""
    ext = os.path.splitext(file.filename or "")[-1].lower()
    if ext not in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
        raise HTTPException(status_code=400, detail="仅支持 jpg/png/webp/gif 格式")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    filename = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(settings.UPLOAD_DIR, filename)

    content = await file.read()
    with open(save_path, "wb") as f:
        f.write(content)

    return {"url": f"/uploads/{filename}"}
