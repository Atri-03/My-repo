"""SQLAlchemy ORM models."""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text, func

from app.db.base import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class RequirementSet(Base):
    __tablename__ = "requirement_set"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True)
    transcript_id = Column(String(36), nullable=False, index=True)
    version = Column(Integer, nullable=False, default=1)
    status = Column(String(16), nullable=False, default="DRAFT")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Requirement(Base):
    __tablename__ = "requirement"

    id = Column(String(36), primary_key=True, default=_uuid)
    requirement_set_id = Column(String(36), ForeignKey("requirement_set.id"), nullable=False, index=True)
    type = Column(String(32), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(16), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RequirementRisk(Base):
    __tablename__ = "requirement_risk"

    id = Column(String(36), primary_key=True, default=_uuid)
    requirement_set_id = Column(String(36), ForeignKey("requirement_set.id"), nullable=False, index=True)
    description = Column(Text, nullable=False)
    severity = Column(String(16), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RequirementEntity(Base):
    __tablename__ = "requirement_entity"

    id = Column(String(36), primary_key=True, default=_uuid)
    requirement_set_id = Column(String(36), ForeignKey("requirement_set.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    attributes = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BusinessRule(Base):
    __tablename__ = "business_rule"

    id = Column(String(36), primary_key=True, default=_uuid)
    requirement_set_id = Column(String(36), ForeignKey("requirement_set.id"), nullable=False, index=True)
    rule = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

