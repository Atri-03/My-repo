"""Unit tests for SQLAlchemy models."""
from app.db import models


def test_create_audit_log_entry_model(db_session):
    obj = models.AuditLogEntry(tenant_id="sample", entity_type="sample", entity_id="sample", action="sample", actor="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.tenant_id == "sample"


