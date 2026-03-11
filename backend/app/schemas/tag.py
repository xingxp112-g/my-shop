from __future__ import annotations

from pydantic import BaseModel


class TagCreate(BaseModel):
    name: str
    parent_id: int | None = None


class TagUpdate(BaseModel):
    name: str


class TagOut(BaseModel):
    id: int
    name: str
    parent_id: int | None = None

    model_config = {"from_attributes": True}


class TagTreeOut(TagOut):
    children: list[TagTreeOut] = []

    model_config = {"from_attributes": True}


TagTreeOut.model_rebuild()
