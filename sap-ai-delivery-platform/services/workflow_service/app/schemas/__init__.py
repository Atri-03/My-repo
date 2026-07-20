"""Pydantic request/response schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class WorkflowRunCreate(BaseModel):
    tenant_id: str
    transcript_id: str
    current_state: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class WorkflowRunUpdate(BaseModel):
    tenant_id: Optional[str] = None
    transcript_id: Optional[str] = None
    current_state: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class WorkflowRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    transcript_id: str
    current_state: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class WorkflowEventCreate(BaseModel):
    workflow_run_id: str
    from_state: Optional[str] = None
    to_state: str
    actor: str
    occurred_at: Optional[datetime] = None


class WorkflowEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    workflow_run_id: str
    from_state: Optional[str] = None
    to_state: str
    actor: str
    occurred_at: Optional[datetime] = None


