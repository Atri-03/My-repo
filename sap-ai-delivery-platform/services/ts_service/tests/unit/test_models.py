"""Unit tests for SQLAlchemy models."""
from app.db import models


def test_create_technical_specification_model(db_session):
    obj = models.TechnicalSpecification(tenant_id="sample", functional_specification_id="sample", template_id="sample", content={})
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.tenant_id == "sample"


