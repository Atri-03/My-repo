"""Pydantic request/response schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class ReviewCycleCreate(BaseModel):
    tenant_id: str
    artefact_type: str
    artefact_id: str
    gate: str
    status: Optional[str] = "PENDING"
    opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None


class ReviewCycleUpdate(BaseModel):
    tenant_id: Optional[str] = None
    artefact_type: Optional[str] = None
    artefact_id: Optional[str] = None
    gate: Optional[str] = None
    status: Optional[str] = None
    opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None


class ReviewCycleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    artefact_type: str
    artefact_id: str
    gate: str
    status: Optional[str] = None
    opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None


class ReviewCommentCreate(BaseModel):
    review_cycle_id: str
    reviewer_id: str
    comment: str


class ReviewCommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    review_cycle_id: str
    reviewer_id: str
    comment: str
    created_at: Optional[datetime] = None


