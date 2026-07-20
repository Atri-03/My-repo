"""Pydantic request/response schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class TechnicalSpecificationCreate(BaseModel):
    tenant_id: str
    functional_specification_id: str
    template_id: str
    version: Optional[int] = 1
    parent_version_id: Optional[str] = None
    status: Optional[str] = "DRAFT"
    content: dict
    blob_uri: Optional[str] = None
    regeneration_count: Optional[int] = 0


class TechnicalSpecificationUpdate(BaseModel):
    tenant_id: Optional[str] = None
    functional_specification_id: Optional[str] = None
    template_id: Optional[str] = None
    version: Optional[int] = None
    parent_version_id: Optional[str] = None
    status: Optional[str] = None
    content: Optional[dict] = None
    blob_uri: Optional[str] = None
    regeneration_count: Optional[int] = None


class TechnicalSpecificationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    functional_specification_id: str
    template_id: str
    version: Optional[int] = None
    parent_version_id: Optional[str] = None
    status: Optional[str] = None
    content: dict
    blob_uri: Optional[str] = None
    regeneration_count: Optional[int] = None
    created_at: Optional[datetime] = None


