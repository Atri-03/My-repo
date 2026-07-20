"""API routes."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.db import models
from app import schemas

router = APIRouter()


@router.post("/review-cycles", response_model=schemas.ReviewCycleRead, status_code=status.HTTP_201_CREATED, tags=["review-cycles"])
def create_review_cycle(payload: schemas.ReviewCycleCreate, db: Session = Depends(get_db)):
    obj = models.ReviewCycle(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/review-cycles", response_model=List[schemas.ReviewCycleRead], tags=["review-cycles"])
def list_review_cycle(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.ReviewCycle).offset(skip).limit(limit).all()


@router.get("/review-cycles/{item_id}", response_model=schemas.ReviewCycleRead, tags=["review-cycles"])
def get_review_cycle(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.ReviewCycle, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="ReviewCycle not found")
    return obj


@router.patch("/review-cycles/{item_id}", response_model=schemas.ReviewCycleRead, tags=["review-cycles"])
def update_review_cycle(item_id: str, payload: schemas.ReviewCycleUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.ReviewCycle, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="ReviewCycle not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/review-cycles/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["review-cycles"])
def delete_review_cycle(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.ReviewCycle, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="ReviewCycle not found")
    db.delete(obj)
    db.commit()
    return None


@router.post("/review-comments", response_model=schemas.ReviewCommentRead, status_code=status.HTTP_201_CREATED, tags=["review-comments"])
def create_review_comment(payload: schemas.ReviewCommentCreate, db: Session = Depends(get_db)):
    obj = models.ReviewComment(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/review-comments", response_model=List[schemas.ReviewCommentRead], tags=["review-comments"])
def list_review_comment(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.ReviewComment).offset(skip).limit(limit).all()


@router.get("/review-comments/{item_id}", response_model=schemas.ReviewCommentRead, tags=["review-comments"])
def get_review_comment(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.ReviewComment, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="ReviewComment not found")
    return obj

