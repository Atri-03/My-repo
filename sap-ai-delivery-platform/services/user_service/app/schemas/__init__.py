"""Pydantic request/response schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class TenantCreate(BaseModel):
    name: str
    entra_tenant_id: str
    tier: Optional[str] = "SHARED"
    status: Optional[str] = "ACTIVE"


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    entra_tenant_id: Optional[str] = None
    tier: Optional[str] = None
    status: Optional[str] = None


class TenantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    entra_tenant_id: str
    tier: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None


class ProjectCreate(BaseModel):
    tenant_id: str
    name: str
    sap_execution_repo_url: Optional[str] = None


class ProjectUpdate(BaseModel):
    tenant_id: Optional[str] = None
    name: Optional[str] = None
    sap_execution_repo_url: Optional[str] = None


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    name: str
    sap_execution_repo_url: Optional[str] = None
    created_at: Optional[datetime] = None


class UserCreate(BaseModel):
    tenant_id: str
    email: str
    display_name: str
    role: Optional[str] = "CONTRIBUTOR"
    is_active: Optional[bool] = True


class UserUpdate(BaseModel):
    tenant_id: Optional[str] = None
    email: Optional[str] = None
    display_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    email: str
    display_name: str
    role: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None


