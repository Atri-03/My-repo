"""API routes."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.db import models
from app import schemas

router = APIRouter()


@router.post("/requirement-sets", response_model=schemas.RequirementSetRead, status_code=status.HTTP_201_CREATED, tags=["requirement-sets"])
def create_requirement_set(payload: schemas.RequirementSetCreate, db: Session = Depends(get_db)):
    obj = models.RequirementSet(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/requirement-sets", response_model=List[schemas.RequirementSetRead], tags=["requirement-sets"])
def list_requirement_set(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.RequirementSet).offset(skip).limit(limit).all()


@router.get("/requirement-sets/{item_id}", response_model=schemas.RequirementSetRead, tags=["requirement-sets"])
def get_requirement_set(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.RequirementSet, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="RequirementSet not found")
    return obj


@router.patch("/requirement-sets/{item_id}", response_model=schemas.RequirementSetRead, tags=["requirement-sets"])
def update_requirement_set(item_id: str, payload: schemas.RequirementSetUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.RequirementSet, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="RequirementSet not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/requirement-sets/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["requirement-sets"])
def delete_requirement_set(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.RequirementSet, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="RequirementSet not found")
    db.delete(obj)
    db.commit()
    return None


@router.post("/requirements", response_model=schemas.RequirementRead, status_code=status.HTTP_201_CREATED, tags=["requirements"])
def create_requirement(payload: schemas.RequirementCreate, db: Session = Depends(get_db)):
    obj = models.Requirement(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/requirements", response_model=List[schemas.RequirementRead], tags=["requirements"])
def list_requirement(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Requirement).offset(skip).limit(limit).all()


@router.get("/requirements/{item_id}", response_model=schemas.RequirementRead, tags=["requirements"])
def get_requirement(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.Requirement, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return obj


@router.patch("/requirements/{item_id}", response_model=schemas.RequirementRead, tags=["requirements"])
def update_requirement(item_id: str, payload: schemas.RequirementUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.Requirement, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/requirements/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["requirements"])
def delete_requirement(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.Requirement, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    db.delete(obj)
    db.commit()
    return None


@router.post("/requirement-risks", response_model=schemas.RequirementRiskRead, status_code=status.HTTP_201_CREATED, tags=["requirement-risks"])
def create_requirement_risk(payload: schemas.RequirementRiskCreate, db: Session = Depends(get_db)):
    obj = models.RequirementRisk(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/requirement-risks", response_model=List[schemas.RequirementRiskRead], tags=["requirement-risks"])
def list_requirement_risk(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.RequirementRisk).offset(skip).limit(limit).all()


@router.get("/requirement-risks/{item_id}", response_model=schemas.RequirementRiskRead, tags=["requirement-risks"])
def get_requirement_risk(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.RequirementRisk, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="RequirementRisk not found")
    return obj


@router.patch("/requirement-risks/{item_id}", response_model=schemas.RequirementRiskRead, tags=["requirement-risks"])
def update_requirement_risk(item_id: str, payload: schemas.RequirementRiskUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.RequirementRisk, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="RequirementRisk not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/requirement-risks/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["requirement-risks"])
def delete_requirement_risk(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.RequirementRisk, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="RequirementRisk not found")
    db.delete(obj)
    db.commit()
    return None


@router.post("/requirement-entities", response_model=schemas.RequirementEntityRead, status_code=status.HTTP_201_CREATED, tags=["requirement-entities"])
def create_requirement_entity(payload: schemas.RequirementEntityCreate, db: Session = Depends(get_db)):
    obj = models.RequirementEntity(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/requirement-entities", response_model=List[schemas.RequirementEntityRead], tags=["requirement-entities"])
def list_requirement_entity(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.RequirementEntity).offset(skip).limit(limit).all()


@router.get("/requirement-entities/{item_id}", response_model=schemas.RequirementEntityRead, tags=["requirement-entities"])
def get_requirement_entity(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.RequirementEntity, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="RequirementEntity not found")
    return obj


@router.patch("/requirement-entities/{item_id}", response_model=schemas.RequirementEntityRead, tags=["requirement-entities"])
def update_requirement_entity(item_id: str, payload: schemas.RequirementEntityUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.RequirementEntity, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="RequirementEntity not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/requirement-entities/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["requirement-entities"])
def delete_requirement_entity(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.RequirementEntity, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="RequirementEntity not found")
    db.delete(obj)
    db.commit()
    return None


@router.post("/business-rules", response_model=schemas.BusinessRuleRead, status_code=status.HTTP_201_CREATED, tags=["business-rules"])
def create_business_rule(payload: schemas.BusinessRuleCreate, db: Session = Depends(get_db)):
    obj = models.BusinessRule(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/business-rules", response_model=List[schemas.BusinessRuleRead], tags=["business-rules"])
def list_business_rule(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.BusinessRule).offset(skip).limit(limit).all()


@router.get("/business-rules/{item_id}", response_model=schemas.BusinessRuleRead, tags=["business-rules"])
def get_business_rule(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.BusinessRule, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="BusinessRule not found")
    return obj


@router.patch("/business-rules/{item_id}", response_model=schemas.BusinessRuleRead, tags=["business-rules"])
def update_business_rule(item_id: str, payload: schemas.BusinessRuleUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.BusinessRule, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="BusinessRule not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/business-rules/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["business-rules"])
def delete_business_rule(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.BusinessRule, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="BusinessRule not found")
    db.delete(obj)
    db.commit()
    return None

