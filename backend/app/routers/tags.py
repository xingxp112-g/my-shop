from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate, TagOut
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("", response_model=list[TagOut])
def list_tags(db: Session = Depends(get_db)):
    return db.query(Tag).order_by(Tag.id).all()


@router.post("", response_model=TagOut, status_code=status.HTTP_201_CREATED)
def create_tag(body: TagCreate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    tag = Tag(name=body.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.put("/{tag_id}", response_model=TagOut)
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
    db.delete(tag)
    db.commit()
