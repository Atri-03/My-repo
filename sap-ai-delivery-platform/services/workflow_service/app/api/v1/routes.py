"""API routes."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.db import models
from app import schemas

router = APIRouter()


@router.post("/workflow-runs", response_model=schemas.WorkflowRunRead, status_code=status.HTTP_201_CREATED, tags=["workflow-runs"])
def create_workflow_run(payload: schemas.WorkflowRunCreate, db: Session = Depends(get_db)):
    obj = models.WorkflowRun(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/workflow-runs", response_model=List[schemas.WorkflowRunRead], tags=["workflow-runs"])
def list_workflow_run(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.WorkflowRun).offset(skip).limit(limit).all()


@router.get("/workflow-runs/{item_id}", response_model=schemas.WorkflowRunRead, tags=["workflow-runs"])
def get_workflow_run(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.WorkflowRun, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="WorkflowRun not found")
    return obj


@router.patch("/workflow-runs/{item_id}", response_model=schemas.WorkflowRunRead, tags=["workflow-runs"])
def update_workflow_run(item_id: str, payload: schemas.WorkflowRunUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.WorkflowRun, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="WorkflowRun not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/workflow-runs/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["workflow-runs"])
def delete_workflow_run(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.WorkflowRun, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="WorkflowRun not found")
    db.delete(obj)
    db.commit()
    return None


@router.post("/workflow-events", response_model=schemas.WorkflowEventRead, status_code=status.HTTP_201_CREATED, tags=["workflow-events"])
def create_workflow_event(payload: schemas.WorkflowEventCreate, db: Session = Depends(get_db)):
    obj = models.WorkflowEvent(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/workflow-events", response_model=List[schemas.WorkflowEventRead], tags=["workflow-events"])
def list_workflow_event(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.WorkflowEvent).offset(skip).limit(limit).all()


@router.get("/workflow-events/{item_id}", response_model=schemas.WorkflowEventRead, tags=["workflow-events"])
def get_workflow_event(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.WorkflowEvent, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="WorkflowEvent not found")
    return obj

