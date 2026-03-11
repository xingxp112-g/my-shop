from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.product import product_tag_table
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate, TagTreeOut
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("", response_model=list[TagTreeOut])
def list_tags(db: Session = Depends(get_db)):
    tags = (
        db.query(Tag)
        .options(joinedload(Tag.children))
        .filter(Tag.parent_id.is_(None))
        .order_by(Tag.id)
        .all()
    )
    return tags


@router.get("/{tag_id}/product-count")
def get_tag_product_count(tag_id: int, db: Session = Depends(get_db)):
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    rows = db.execute(
        select(product_tag_table).where(product_tag_table.c.tag_id == tag_id)
    ).fetchall()
    return {"count": len(rows)}


@router.post("", response_model=TagTreeOut, status_code=status.HTTP_201_CREATED)
def create_tag(body: TagCreate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    if body.parent_id is not None:
        parent = db.get(Tag, body.parent_id)
        if not parent:
            raise HTTPException(status_code=404, detail="父标签不存在")
        if parent.parent_id is not None:
            raise HTTPException(status_code=400, detail="不支持三级标签")
    tag = Tag(name=body.name, parent_id=body.parent_id)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.put("/{tag_id}", response_model=TagTreeOut)
def update_tag(tag_id: int, body: TagUpdate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    tag.name = body.name
    db.commit()
    db.refresh(tag)
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    if tag.parent_id is None:
        child_count = db.query(Tag).filter(Tag.parent_id == tag_id).count()
        if child_count > 0:
            raise HTTPException(status_code=400, detail="请先删除该标签下的所有子标签")
    db.delete(tag)
    db.commit()
