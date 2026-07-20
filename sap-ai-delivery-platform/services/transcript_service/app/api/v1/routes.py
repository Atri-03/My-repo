"""API routes."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.db import models
from app import schemas

router = APIRouter()


@router.post("/source-documents", response_model=schemas.SourceDocumentRead, status_code=status.HTTP_201_CREATED, tags=["source-documents"])
def create_source_document(payload: schemas.SourceDocumentCreate, db: Session = Depends(get_db)):
    obj = models.SourceDocument(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/source-documents", response_model=List[schemas.SourceDocumentRead], tags=["source-documents"])
def list_source_document(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.SourceDocument).offset(skip).limit(limit).all()


@router.get("/source-documents/{item_id}", response_model=schemas.SourceDocumentRead, tags=["source-documents"])
def get_source_document(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.SourceDocument, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="SourceDocument not found")
    return obj


@router.patch("/source-documents/{item_id}", response_model=schemas.SourceDocumentRead, tags=["source-documents"])
def update_source_document(item_id: str, payload: schemas.SourceDocumentUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.SourceDocument, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="SourceDocument not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/source-documents/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["source-documents"])
def delete_source_document(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.SourceDocument, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="SourceDocument not found")
    db.delete(obj)
    db.commit()
    return None


@router.post("/transcripts", response_model=schemas.TranscriptRead, status_code=status.HTTP_201_CREATED, tags=["transcripts"])
def create_transcript(payload: schemas.TranscriptCreate, db: Session = Depends(get_db)):
    obj = models.Transcript(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/transcripts", response_model=List[schemas.TranscriptRead], tags=["transcripts"])
def list_transcript(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Transcript).offset(skip).limit(limit).all()


@router.get("/transcripts/{item_id}", response_model=schemas.TranscriptRead, tags=["transcripts"])
def get_transcript(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.Transcript, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Transcript not found")
    return obj


@router.patch("/transcripts/{item_id}", response_model=schemas.TranscriptRead, tags=["transcripts"])
def update_transcript(item_id: str, payload: schemas.TranscriptUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.Transcript, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Transcript not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/transcripts/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["transcripts"])
def delete_transcript(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.Transcript, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Transcript not found")
    db.delete(obj)
    db.commit()
    return None

