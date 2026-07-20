"""SQLAlchemy ORM models."""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text, func

from app.db.base import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class Tenant(Base):
    __tablename__ = "tenant"

    id = Column(String(36), primary_key=True, default=_uuid)
    name = Column(String(255), nullable=False)
    entra_tenant_id = Column(String(128), nullable=False, unique=True)
    tier = Column(String(16), nullable=False, default="SHARED")
    status = Column(String(16), nullable=False, default="ACTIVE")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Project(Base):
    __tablename__ = "project"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(36), ForeignKey("tenant.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    sap_execution_repo_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = "platform_user"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(36), ForeignKey("tenant.id"), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True)
    display_name = Column(String(255), nullable=False)
    role = Column(String(32), nullable=False, default="CONTRIBUTOR")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

