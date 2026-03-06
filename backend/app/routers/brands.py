from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.brand import Brand
from app.schemas.brand import BrandCreate, BrandUpdate, BrandOut
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("", response_model=list[BrandOut])
def list_brands(db: Session = Depends(get_db)):
    return db.query(Brand).order_by(Brand.id).all()


@router.post("", response_model=BrandOut, status_code=status.HTTP_201_CREATED)
def create_brand(body: BrandCreate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    brand = Brand(name=body.name)
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand


@router.put("/{brand_id}", response_model=BrandOut)
def update_brand(brand_id: int, body: BrandUpdate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    brand = db.get(Brand, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    brand.name = body.name
    db.commit()
    db.refresh(brand)
    return brand


@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_brand(brand_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    brand = db.get(Brand, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    db.delete(brand)
    db.commit()
