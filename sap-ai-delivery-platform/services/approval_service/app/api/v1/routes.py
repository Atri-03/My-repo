"""API routes."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.db import models
from app import schemas

router = APIRouter()


@router.post("/review-decisions", response_model=schemas.ReviewDecisionRead, status_code=status.HTTP_201_CREATED, tags=["review-decisions"])
def create_review_decision(payload: schemas.ReviewDecisionCreate, db: Session = Depends(get_db)):
    obj = models.ReviewDecision(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/review-decisions", response_model=List[schemas.ReviewDecisionRead], tags=["review-decisions"])
def list_review_decision(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.ReviewDecision).offset(skip).limit(limit).all()


@router.get("/review-decisions/{item_id}", response_model=schemas.ReviewDecisionRead, tags=["review-decisions"])
def get_review_decision(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.ReviewDecision, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="ReviewDecision not found")
    return obj


@router.post("/sap-execution-packages", response_model=schemas.SapExecutionPackageRead, status_code=status.HTTP_201_CREATED, tags=["sap-execution-packages"])
def create_sap_execution_package(payload: schemas.SapExecutionPackageCreate, db: Session = Depends(get_db)):
    obj = models.SapExecutionPackage(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/sap-execution-packages", response_model=List[schemas.SapExecutionPackageRead], tags=["sap-execution-packages"])
def list_sap_execution_package(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.SapExecutionPackage).offset(skip).limit(limit).all()


@router.get("/sap-execution-packages/{item_id}", response_model=schemas.SapExecutionPackageRead, tags=["sap-execution-packages"])
def get_sap_execution_package(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.SapExecutionPackage, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="SapExecutionPackage not found")
    return obj


@router.patch("/sap-execution-packages/{item_id}", response_model=schemas.SapExecutionPackageRead, tags=["sap-execution-packages"])
def update_sap_execution_package(item_id: str, payload: schemas.SapExecutionPackageUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.SapExecutionPackage, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="SapExecutionPackage not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/sap-execution-packages/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["sap-execution-packages"])
def delete_sap_execution_package(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.SapExecutionPackage, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="SapExecutionPackage not found")
    db.delete(obj)
    db.commit()
    return None

