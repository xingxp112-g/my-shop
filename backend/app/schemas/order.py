from decimal import Decimal
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    price: Decimal


class OrderCreate(BaseModel):
    customer_name: str
    phone: str
    remark: Optional[str] = None
    items: list[OrderItemCreate]


class OrderStatusUpdate(BaseModel):
    status: str  # 待处理 / 已确认 / 已完成 / 已取消


class ProductSimple(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: Decimal
    product: ProductSimple

    model_config = {"from_attributes": True}


class OrderOut(BaseModel):
    id: int
    customer_name: str
    phone: str
    total_amount: Decimal
    remark: Optional[str]
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class OrderDetailOut(OrderOut):
    items: list[OrderItemOut]
