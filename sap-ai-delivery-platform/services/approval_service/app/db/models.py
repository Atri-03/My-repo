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

