"""API routes."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.db import models
from app import schemas

router = APIRouter()


@router.post("/document-templates", response_model=schemas.DocumentTemplateRead, status_code=status.HTTP_201_CREATED, tags=["document-templates"])
def create_document_template(payload: schemas.DocumentTemplateCreate, db: Session = Depends(get_db)):
    obj = models.DocumentTemplate(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/document-templates", response_model=List[schemas.DocumentTemplateRead], tags=["document-templates"])
def list_document_template(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.DocumentTemplate).offset(skip).limit(limit).all()


@router.get("/document-templates/{item_id}", response_model=schemas.DocumentTemplateRead, tags=["document-templates"])
def get_document_template(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.DocumentTemplate, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="DocumentTemplate not found")
    return obj


@router.patch("/document-templates/{item_id}", response_model=schemas.DocumentTemplateRead, tags=["document-templates"])
def update_document_template(item_id: str, payload: schemas.DocumentTemplateUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.DocumentTemplate, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="DocumentTemplate not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/document-templates/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["document-templates"])
def delete_document_template(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.DocumentTemplate, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="DocumentTemplate not found")
    db.delete(obj)
    db.commit()
    return None


@router.post("/functional-specifications", response_model=schemas.FunctionalSpecificationRead, status_code=status.HTTP_201_CREATED, tags=["functional-specifications"])
def create_functional_specification(payload: schemas.FunctionalSpecificationCreate, db: Session = Depends(get_db)):
    obj = models.FunctionalSpecification(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/functional-specifications", response_model=List[schemas.FunctionalSpecificationRead], tags=["functional-specifications"])
def list_functional_specification(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.FunctionalSpecification).offset(skip).limit(limit).all()


@router.get("/functional-specifications/{item_id}", response_model=schemas.FunctionalSpecificationRead, tags=["functional-specifications"])
def get_functional_specification(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.FunctionalSpecification, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="FunctionalSpecification not found")
    return obj


@router.patch("/functional-specifications/{item_id}", response_model=schemas.FunctionalSpecificationRead, tags=["functional-specifications"])
def update_functional_specification(item_id: str, payload: schemas.FunctionalSpecificationUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.FunctionalSpecification, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="FunctionalSpecification not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/functional-specifications/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["functional-specifications"])
def delete_functional_specification(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.FunctionalSpecification, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="FunctionalSpecification not found")
    db.delete(obj)
    db.commit()
    return None

