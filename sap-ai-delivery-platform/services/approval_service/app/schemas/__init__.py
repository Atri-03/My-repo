"""Pydantic request/response schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class ReviewDecisionCreate(BaseModel):
    review_cycle_id: str
    decided_by: str
    decision: str
    decided_at: Optional[datetime] = None


class ReviewDecisionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    review_cycle_id: str
    decided_by: str
    decision: str
    decided_at: Optional[datetime] = None


class SapExecutionPackageCreate(BaseModel):
    tenant_id: str
    technical_specification_id: str
    version: Optional[int] = 1
    status: Optional[str] = "DRAFT"
    payload: dict
    sap_execution_repo_ref: Optional[str] = None
    published_at: Optional[datetime] = None


class SapExecutionPackageUpdate(BaseModel):
    tenant_id: Optional[str] = None
    technical_specification_id: Optional[str] = None
    version: Optional[int] = None
    status: Optional[str] = None
    payload: Optional[dict] = None
    sap_execution_repo_ref: Optional[str] = None
    published_at: Optional[datetime] = None


class SapExecutionPackageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    technical_specification_id: str
    version: Optional[int] = None
    status: Optional[str] = None
    payload: dict
    sap_execution_repo_ref: Optional[str] = None
    published_at: Optional[datetime] = None


