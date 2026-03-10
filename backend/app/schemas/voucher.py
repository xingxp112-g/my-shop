from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, field_validator


class VoucherBatchCreate(BaseModel):
    amount: Decimal
    quantity: int
    start_date: date
    end_date: date

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError("面额必须大于 0")
        return v

    @field_validator("quantity")
    @classmethod
    def quantity_range(cls, v):
        if v < 1 or v > 100:
            raise ValueError("数量必须在 1-100 之间")
        return v

    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, v, info):
        start = info.data.get("start_date")
        if start and v < start:
            raise ValueError("截止日期必须 >= 开始日期")
        return v


class VoucherBatchResponse(BaseModel):
    batch_no: str
    count: int
    codes: List[str]


class VoucherOut(BaseModel):
    id: int
    code: str
    amount: Decimal
    start_date: date
    end_date: date
    status: str          # 计算后的实际状态：unused / used / expired
    used_at: Optional[datetime]
    used_by: Optional[str]
    batch_no: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class VoucherListResponse(BaseModel):
    total: int
    items: List[VoucherOut]


class VoucherRedeemRequest(BaseModel):
    code: str


class VoucherRedeemResponse(BaseModel):
    code: str
    amount: Decimal
    used_at: datetime
