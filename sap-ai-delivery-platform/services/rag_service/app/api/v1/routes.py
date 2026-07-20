"""API routes."""
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.knowledge_source_types import KNOWLEDGE_SOURCE_TYPES
from app.db.base import get_db
from app.db import models
from app import schemas

router = APIRouter()


@router.get("/knowledge-source-types", tags=["knowledge-sources"])
def list_knowledge_source_types() -> Dict[str, List[Dict[str, Any]]]:
    """List the Enterprise Knowledge Brain's documented knowledge categories.

    `KnowledgeSource.source_type` remains free-form (new categories can be
    ingested without a migration), but this endpoint surfaces the canonical
    catalogue - Past BRDs/FS/TS/RAP/CDS/Fiori, review comments, approved
    architect decisions, naming standards, ATC findings, and reusable
    components - for the Knowledge Management UI.
    """
    return {"source_types": KNOWLEDGE_SOURCE_TYPES}


@router.post("/knowledge-sources", response_model=schemas.KnowledgeSourceRead, status_code=status.HTTP_201_CREATED, tags=["knowledge-sources"])
def create_knowledge_source(payload: schemas.KnowledgeSourceCreate, db: Session = Depends(get_db)):
    obj = models.KnowledgeSource(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/knowledge-sources", response_model=List[schemas.KnowledgeSourceRead], tags=["knowledge-sources"])
def list_knowledge_source(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.KnowledgeSource).offset(skip).limit(limit).all()


@router.get("/knowledge-sources/{item_id}", response_model=schemas.KnowledgeSourceRead, tags=["knowledge-sources"])
def get_knowledge_source(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.KnowledgeSource, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="KnowledgeSource not found")
    return obj


@router.patch("/knowledge-sources/{item_id}", response_model=schemas.KnowledgeSourceRead, tags=["knowledge-sources"])
def update_knowledge_source(item_id: str, payload: schemas.KnowledgeSourceUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.KnowledgeSource, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="KnowledgeSource not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/knowledge-sources/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["knowledge-sources"])
def delete_knowledge_source(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.KnowledgeSource, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="KnowledgeSource not found")
    db.delete(obj)
    db.commit()
    return None


@router.post("/knowledge-chunks", response_model=schemas.KnowledgeChunkRead, status_code=status.HTTP_201_CREATED, tags=["knowledge-chunks"])
def create_knowledge_chunk(payload: schemas.KnowledgeChunkCreate, db: Session = Depends(get_db)):
    obj = models.KnowledgeChunk(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/knowledge-chunks", response_model=List[schemas.KnowledgeChunkRead], tags=["knowledge-chunks"])
def list_knowledge_chunk(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.KnowledgeChunk).offset(skip).limit(limit).all()


@router.get("/knowledge-chunks/{item_id}", response_model=schemas.KnowledgeChunkRead, tags=["knowledge-chunks"])
def get_knowledge_chunk(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.KnowledgeChunk, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="KnowledgeChunk not found")
    return obj


@router.patch("/knowledge-chunks/{item_id}", response_model=schemas.KnowledgeChunkRead, tags=["knowledge-chunks"])
def update_knowledge_chunk(item_id: str, payload: schemas.KnowledgeChunkUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.KnowledgeChunk, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="KnowledgeChunk not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/knowledge-chunks/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["knowledge-chunks"])
def delete_knowledge_chunk(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.KnowledgeChunk, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="KnowledgeChunk not found")
    db.delete(obj)
    db.commit()
    return None

