"""Unit tests for SQLAlchemy models."""
from app.db import models


def test_create_document_template_model(db_session):
    obj = models.DocumentTemplate(tenant_id="sample", name="sample", schema_={})
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.tenant_id == "sample"


def test_create_functional_specification_model(db_session):
    obj = models.FunctionalSpecification(tenant_id="sample", requirement_set_id="sample", template_id="sample", content={})
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.tenant_id == "sample"


