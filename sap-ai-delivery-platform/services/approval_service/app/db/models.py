"""SQLAlchemy ORM models."""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text, func

from app.db.base import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class ReviewDecision(Base):
    __tablename__ = "review_decision"

    id = Column(String(36), primary_key=True, default=_uuid)
    review_cycle_id = Column(String(36), nullable=False, index=True)
    decided_by = Column(String(64), nullable=False)
    decision = Column(String(20), nullable=False)
    decided_at = Column(DateTime(timezone=True), server_default=func.now())


class SapExecutionPackage(Base):
    __tablename__ = "sap_execution_package"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True)
    technical_specification_id = Column(String(36), nullable=False, index=True)
    version = Column(Integer, nullable=False, default=1)
    status = Column(String(16), nullable=False, default="DRAFT")
    payload = Column(JSON, nullable=False)
    sap_execution_repo_ref = Column(Text, nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)


class ApprovalGateDefinition(Base):
    """Configurable definition of a mandatory human approval gate.

    Seeded by default with the 5 mandatory gates (see the initial data
    migration), but every field is editable via the API so tenants can
    configure required roles, ordering, and whether self-approval is
    permitted for a gate without any code change.
    """

    __tablename__ = "approval_gate_definition"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True)
    gate_key = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    sequence_order = Column(Integer, nullable=False, default=1)
    entity_type = Column(String(64), nullable=False)
    required_role = Column(String(64), nullable=False)
    allow_self_approval = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class GateApprovalRequest(Base):
    """A single instance of a gate being requested/decided for an entity.

    Persists the full decision trail (requester, approver, roles, SoD
    outcome) so it can be queried directly for auditability, in addition to
    the mirrored entry pushed to the Audit Service.
    """

    __tablename__ = "gate_approval_request"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True)
    gate_key = Column(String(64), nullable=False, index=True)
    entity_type = Column(String(64), nullable=False)
    entity_id = Column(String(36), nullable=False, index=True)
    workflow_run_id = Column(String(36), nullable=True, index=True)
    requested_by = Column(String(64), nullable=False)
    requested_by_role = Column(String(64), nullable=True)
    status = Column(String(24), nullable=False, default="PENDING")
    decided_by = Column(String(64), nullable=True)
    decided_by_role = Column(String(64), nullable=True)
    decision_comments = Column(Text, nullable=True)
    sod_violation = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    decided_at = Column(DateTime(timezone=True), nullable=True)


