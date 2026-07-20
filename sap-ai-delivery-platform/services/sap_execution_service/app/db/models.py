"""SQLAlchemy ORM models for the SAP Execution bounded context.

These models back the SAP Execution MCP tools already defined in
`mcp_gateway_service/app/mcp/tools/` (package/transport management,
object/RAP/CDS/OData generation, activation, ATC + remediation, unit
testing) plus a lightweight execution-planning capability (the "SAP
Solution Architect Agent"). They intentionally mirror the same
conventions used by every other service in this platform.
"""
import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, JSON, String, Text, func

from app.db.base import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class SapPackage(Base):
    __tablename__ = "sap_package"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default")
    package_name = Column(String(128), nullable=False, index=True)
    description = Column(Text, nullable=False)
    software_component = Column(String(64), nullable=False, default="LOCAL")
    parent_package = Column(String(128), nullable=True)
    transport_request = Column(String(64), nullable=True)
    status = Column(String(16), nullable=False, default="CREATED")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SapTransport(Base):
    __tablename__ = "sap_transport"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default")
    transport_request = Column(String(64), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=False)
    transport_type = Column(String(16), nullable=False, default="workbench")
    target_system = Column(String(64), nullable=True)
    owner = Column(String(128), nullable=True)
    status = Column(String(16), nullable=False, default="MODIFIABLE")
    released_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class GeneratedObject(Base):
    """A generated ABAP repository object: generic object, RAP BO, CDS view or OData service."""

    __tablename__ = "generated_object"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default")
    object_name = Column(String(128), nullable=False, index=True)
    object_type = Column(String(32), nullable=False, index=True)
    package = Column(String(128), nullable=False)
    transport_request = Column(String(64), nullable=False)
    description = Column(Text, nullable=True)
    source_code = Column(Text, nullable=True)
    extra = Column(JSON, nullable=True)
    status = Column(String(16), nullable=False, default="INACTIVE")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Activation(Base):
    __tablename__ = "activation"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default")
    object_name = Column(String(128), nullable=False, index=True)
    object_type = Column(String(32), nullable=False)
    status = Column(String(16), nullable=False, default="ACTIVATED")
    activated_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AtcRun(Base):
    __tablename__ = "atc_run"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default")
    object_name = Column(String(128), nullable=False, index=True)
    object_type = Column(String(32), nullable=False)
    variant = Column(String(32), nullable=False, default="DEFAULT")
    status = Column(String(16), nullable=False, default="COMPLETED")
    findings = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AtcRemediation(Base):
    __tablename__ = "atc_remediation"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default")
    object_name = Column(String(128), nullable=False, index=True)
    object_type = Column(String(32), nullable=False)
    finding_ids = Column(JSON, nullable=False, default=list)
    auto_apply = Column(Boolean, nullable=False, default=False)
    status = Column(String(16), nullable=False, default="PROPOSED")
    remediated_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UnitTestRun(Base):
    __tablename__ = "unit_test_run"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default")
    object_name = Column(String(128), nullable=False, index=True)
    object_type = Column(String(32), nullable=False)
    test_classes = Column(JSON, nullable=True)
    status = Column(String(16), nullable=False, default="PASSED")
    results = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ExecutionPlan(Base):
    """Output of the SAP Solution Architect Agent: a proposed, ordered execution plan."""

    __tablename__ = "execution_plan"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default")
    technical_specification_id = Column(String(36), nullable=False, index=True)
    package_name = Column(String(128), nullable=True)
    transport_description = Column(Text, nullable=True)
    steps = Column(JSON, nullable=False, default=list)
    status = Column(String(16), nullable=False, default="PROPOSED")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
