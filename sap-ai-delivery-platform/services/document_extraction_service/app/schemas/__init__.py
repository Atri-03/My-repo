"""Pydantic request/response schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class RequirementSetCreate(BaseModel):
    tenant_id: str
    transcript_id: str
    version: Optional[int] = 1
    status: Optional[str] = "DRAFT"


class RequirementSetUpdate(BaseModel):
    tenant_id: Optional[str] = None
    transcript_id: Optional[str] = None
    version: Optional[int] = None
    status: Optional[str] = None


class RequirementSetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    transcript_id: str
    version: Optional[int] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None


class RequirementCreate(BaseModel):
    requirement_set_id: str
    type: str
    title: str
    description: str
    priority: Optional[str] = None


class RequirementUpdate(BaseModel):
    requirement_set_id: Optional[str] = None
    type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None


class RequirementRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    requirement_set_id: str
    type: str
    title: str
    description: str
    priority: Optional[str] = None
    created_at: Optional[datetime] = None


class RequirementRiskCreate(BaseModel):
    requirement_set_id: str
    description: str
    severity: str


class RequirementRiskUpdate(BaseModel):
    requirement_set_id: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None


class RequirementRiskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    requirement_set_id: str
    description: str
    severity: str
    created_at: Optional[datetime] = None


class RequirementEntityCreate(BaseModel):
    requirement_set_id: str
    name: str
    attributes: Optional[dict] = Field(default_factory=dict)


class RequirementEntityUpdate(BaseModel):
    requirement_set_id: Optional[str] = None
    name: Optional[str] = None
    attributes: Optional[dict] = None


class RequirementEntityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    requirement_set_id: str
    name: str
    attributes: Optional[dict] = None
    created_at: Optional[datetime] = None


class BusinessRuleCreate(BaseModel):
    requirement_set_id: str
    rule: str


class BusinessRuleUpdate(BaseModel):
    requirement_set_id: Optional[str] = None
    rule: Optional[str] = None


class BusinessRuleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    requirement_set_id: str
    rule: str
    created_at: Optional[datetime] = None


