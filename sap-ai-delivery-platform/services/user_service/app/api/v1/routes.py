"""API routes."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.db import models
from app import schemas

router = APIRouter()


@router.post("/tenants", response_model=schemas.TenantRead, status_code=status.HTTP_201_CREATED, tags=["tenants"])
def create_tenant(payload: schemas.TenantCreate, db: Session = Depends(get_db)):
    obj = models.Tenant(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/tenants", response_model=List[schemas.TenantRead], tags=["tenants"])
def list_tenant(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Tenant).offset(skip).limit(limit).all()


@router.get("/tenants/{item_id}", response_model=schemas.TenantRead, tags=["tenants"])
def get_tenant(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.Tenant, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return obj


@router.patch("/tenants/{item_id}", response_model=schemas.TenantRead, tags=["tenants"])
def update_tenant(item_id: str, payload: schemas.TenantUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.Tenant, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/tenants/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tenants"])
def delete_tenant(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.Tenant, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    db.delete(obj)
    db.commit()
    return None


@router.post("/projects", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED, tags=["projects"])
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db)):
    obj = models.Project(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/projects", response_model=List[schemas.ProjectRead], tags=["projects"])
def list_project(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Project).offset(skip).limit(limit).all()


@router.get("/projects/{item_id}", response_model=schemas.ProjectRead, tags=["projects"])
def get_project(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.Project, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return obj


@router.patch("/projects/{item_id}", response_model=schemas.ProjectRead, tags=["projects"])
def update_project(item_id: str, payload: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.Project, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/projects/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["projects"])
def delete_project(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.Project, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(obj)
    db.commit()
    return None


@router.post("/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    obj = models.User(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/users", response_model=List[schemas.UserRead], tags=["users"])
def list_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.User).offset(skip).limit(limit).all()


@router.get("/users/{item_id}", response_model=schemas.UserRead, tags=["users"])
def get_user(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.User, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="User not found")
    return obj


@router.patch("/users/{item_id}", response_model=schemas.UserRead, tags=["users"])
def update_user(item_id: str, payload: schemas.UserUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.User, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/users/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.User, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(obj)
    db.commit()
    return None

