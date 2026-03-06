from pydantic import BaseModel


class BrandCreate(BaseModel):
    name: str


class BrandUpdate(BaseModel):
    name: str


class BrandOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
