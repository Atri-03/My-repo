"""API routes."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.db import models
from app import schemas

router = APIRouter()


@router.post("/technical-specifications", response_model=schemas.TechnicalSpecificationRead, status_code=status.HTTP_201_CREATED, tags=["technical-specifications"])
def create_technical_specification(payload: schemas.TechnicalSpecificationCreate, db: Session = Depends(get_db)):
    obj = models.TechnicalSpecification(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/technical-specifications", response_model=List[schemas.TechnicalSpecificationRead], tags=["technical-specifications"])
def list_technical_specification(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.TechnicalSpecification).offset(skip).limit(limit).all()


@router.get("/technical-specifications/{item_id}", response_model=schemas.TechnicalSpecificationRead, tags=["technical-specifications"])
def get_technical_specification(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.TechnicalSpecification, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="TechnicalSpecification not found")
    return obj


@router.patch("/technical-specifications/{item_id}", response_model=schemas.TechnicalSpecificationRead, tags=["technical-specifications"])
def update_technical_specification(item_id: str, payload: schemas.TechnicalSpecificationUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.TechnicalSpecification, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="TechnicalSpecification not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/technical-specifications/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["technical-specifications"])
def delete_technical_specification(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.TechnicalSpecification, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="TechnicalSpecification not found")
    db.delete(obj)
    db.commit()
    return None

