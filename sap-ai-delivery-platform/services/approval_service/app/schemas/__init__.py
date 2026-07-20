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


class ApprovalGateDefinitionCreate(BaseModel):
    tenant_id: str
    gate_key: str
    name: str
    description: Optional[str] = None
    sequence_order: int = 1
    entity_type: str
    required_role: str
    allow_self_approval: bool = False
    is_active: bool = True


class ApprovalGateDefinitionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    sequence_order: Optional[int] = None
    entity_type: Optional[str] = None
    required_role: Optional[str] = None
    allow_self_approval: Optional[bool] = None
    is_active: Optional[bool] = None


class ApprovalGateDefinitionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    gate_key: str
    name: str
    description: Optional[str] = None
    sequence_order: int
    entity_type: str
    required_role: str
    allow_self_approval: bool
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class GateApprovalRequestCreate(BaseModel):
    tenant_id: str
    gate_key: str
    entity_type: str
    entity_id: str
    workflow_run_id: Optional[str] = None
    requested_by: str
    requested_by_role: Optional[str] = None


class GateApprovalDecide(BaseModel):
    decided_by: str
    decided_by_role: str
    decision: str = Field(..., description="APPROVED | REJECTED | CHANGES_REQUESTED")
    decision_comments: Optional[str] = None


class GateApprovalRequestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    gate_key: str
    entity_type: str
    entity_id: str
    workflow_run_id: Optional[str] = None
    requested_by: str
    requested_by_role: Optional[str] = None
    status: str
    decided_by: Optional[str] = None
    decided_by_role: Optional[str] = None
    decision_comments: Optional[str] = None
    sod_violation: bool
    created_at: Optional[datetime] = None
    decided_at: Optional[datetime] = None

