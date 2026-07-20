"""Pydantic request/response schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class DocumentTemplateCreate(BaseModel):
    tenant_id: str
    type: Optional[str] = "FS"
    name: str
    version: Optional[int] = 1
    schema_: dict
    is_active: Optional[bool] = True


class DocumentTemplateUpdate(BaseModel):
    tenant_id: Optional[str] = None
    type: Optional[str] = None
    name: Optional[str] = None
    version: Optional[int] = None
    schema_: Optional[dict] = None
    is_active: Optional[bool] = None


class DocumentTemplateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    type: Optional[str] = None
    name: str
    version: Optional[int] = None
    schema_: dict
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None


class FunctionalSpecificationCreate(BaseModel):
    tenant_id: str
    requirement_set_id: str
    template_id: str
    version: Optional[int] = 1
    parent_version_id: Optional[str] = None
    status: Optional[str] = "DRAFT"
    content: dict
    blob_uri: Optional[str] = None
    regeneration_count: Optional[int] = 0


class FunctionalSpecificationUpdate(BaseModel):
    tenant_id: Optional[str] = None
    requirement_set_id: Optional[str] = None
    template_id: Optional[str] = None
    version: Optional[int] = None
    parent_version_id: Optional[str] = None
    status: Optional[str] = None
    content: Optional[dict] = None
    blob_uri: Optional[str] = None
    regeneration_count: Optional[int] = None


class FunctionalSpecificationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    requirement_set_id: str
    template_id: str
    version: Optional[int] = None
    parent_version_id: Optional[str] = None
    status: Optional[str] = None
    content: dict
    blob_uri: Optional[str] = None
    regeneration_count: Optional[int] = None
    created_at: Optional[datetime] = None


