from decimal import Decimal
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.brand import BrandOut
from app.schemas.tag import TagOut


class ProductCreate(BaseModel):
    name: str
    brand_id: int
    price: Decimal
    image_url: Optional[str] = None
    remark: Optional[str] = None
    tag_ids: list[int] = []


class ProductUpdate(BaseModel):
    name: str
    brand_id: int
    price: Decimal
    image_url: Optional[str] = None
    remark: Optional[str] = None
    tag_ids: list[int] = []


class ProductStatusUpdate(BaseModel):
    status: int  # 1=上架 0=下架


class ProductOut(BaseModel):
    id: int
    name: str
    brand_id: int
    price: Decimal
    image_url: Optional[str]
    remark: Optional[str]
    status: int
    created_at: datetime
    brand: BrandOut
    tags: list[TagOut]

    model_config = {"from_attributes": True}
