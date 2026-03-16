from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.product import Product, product_tag_table
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate, TagTreeOut, MoveBody
from app.utils.auth import get_current_user

router = APIRouter()


def _build_tree_out(tag: Tag, children_override=None) -> TagTreeOut:
    """将 ORM Tag 对象转换为 TagTreeOut，可传入已过滤/排序的 children 列表"""
    if children_override is not None:
        children = children_override
    else:
        children = sorted(tag.children, key=lambda c: (c.sort, c.id))
    return TagTreeOut(
        id=tag.id,
        name=tag.name,
        parent_id=tag.parent_id,
        sort=tag.sort,
        children=[
            TagTreeOut(id=c.id, name=c.name, parent_id=c.parent_id, sort=c.sort, children=[])
            for c in children
        ],
    )


@router.get("", response_model=list[TagTreeOut])
def list_tags(only_with_products: bool = False, db: Session = Depends(get_db)):
    tags = (
        db.query(Tag)
        .options(joinedload(Tag.children))
        .filter(Tag.parent_id.is_(None))
        .order_by(Tag.sort, Tag.id)
        .all()
    )

    if not only_with_products:
        return [_build_tree_out(t) for t in tags]

    # 查询有上架商品的 tag_id 集合
    rows = db.execute(
        select(product_tag_table.c.tag_id)
        .join(Product, Product.id == product_tag_table.c.product_id)
        .where(Product.status == 1)
        .distinct()
    ).fetchall()
    active_tag_ids = {row[0] for row in rows}

    result = []
    for tag in tags:
        children_sorted = sorted(tag.children, key=lambda c: (c.sort, c.id))
        if children_sorted:
            # 有子标签：只保留有上架商品的子标签
            visible = [c for c in children_sorted if c.id in active_tag_ids]
            if visible:
                result.append(_build_tree_out(tag, children_override=visible))
        else:
            # 无子标签：自身有上架商品才显示
            if tag.id in active_tag_ids:
                result.append(_build_tree_out(tag, children_override=[]))
    return result


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
    # 自动分配 sort = 同级最大值 + 1
    siblings = db.query(Tag).filter(Tag.parent_id == body.parent_id).all()
    auto_sort = max((s.sort for s in siblings), default=-1) + 1
    tag = Tag(name=body.name, parent_id=body.parent_id, sort=auto_sort)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return _build_tree_out(tag)


@router.put("/{tag_id}", response_model=TagTreeOut)
def update_tag(tag_id: int, body: TagUpdate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    tag.name = body.name
    db.commit()
    db.refresh(tag)
    return _build_tree_out(tag)


@router.patch("/{tag_id}/move", status_code=status.HTTP_204_NO_CONTENT)
def move_tag(
    tag_id: int,
    body: MoveBody,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    if body.direction not in ("up", "down"):
        raise HTTPException(status_code=400, detail="direction 必须为 up 或 down")
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")

    siblings = (
        db.query(Tag)
        .filter(Tag.parent_id == tag.parent_id)
        .order_by(Tag.sort, Tag.id)
        .all()
    )
    idx = next((i for i, t in enumerate(siblings) if t.id == tag_id), None)
    if idx is None:
        return

    if body.direction == "up" and idx > 0:
        siblings.insert(idx - 1, siblings.pop(idx))
    elif body.direction == "down" and idx < len(siblings) - 1:
        siblings.insert(idx + 1, siblings.pop(idx))
    else:
        return  # 已在边界，不操作

    for i, t in enumerate(siblings):
        t.sort = i
    db.commit()


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
