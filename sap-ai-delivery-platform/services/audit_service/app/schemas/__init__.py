"""Pydantic request/response schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class AuditLogEntryCreate(BaseModel):
    tenant_id: str
    entity_type: str
    entity_id: str
    action: str
    actor: str
    before: Optional[dict] = None
    after: Optional[dict] = None
    occurred_at: Optional[datetime] = None


class AuditLogEntryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    entity_type: str
    entity_id: str
    action: str
    actor: str
    before: Optional[dict] = None
    after: Optional[dict] = None
    occurred_at: Optional[datetime] = None


