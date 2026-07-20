"""API routes."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.db import models
from app import schemas

router = APIRouter()


@router.post("/audit-log-entrys", response_model=schemas.AuditLogEntryRead, status_code=status.HTTP_201_CREATED, tags=["audit-log-entrys"])
def create_audit_log_entry(payload: schemas.AuditLogEntryCreate, db: Session = Depends(get_db)):
    obj = models.AuditLogEntry(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/audit-log-entrys", response_model=List[schemas.AuditLogEntryRead], tags=["audit-log-entrys"])
def list_audit_log_entry(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.AuditLogEntry).offset(skip).limit(limit).all()


@router.get("/audit-log-entrys/{item_id}", response_model=schemas.AuditLogEntryRead, tags=["audit-log-entrys"])
def get_audit_log_entry(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.AuditLogEntry, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="AuditLogEntry not found")
    return obj

