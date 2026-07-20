"""Unit tests for SQLAlchemy models."""
from app.db import models


def test_create_review_decision_model(db_session):
    obj = models.ReviewDecision(review_cycle_id="sample", decided_by="sample", decision="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.review_cycle_id == "sample"


def test_create_sap_execution_package_model(db_session):
    obj = models.SapExecutionPackage(tenant_id="sample", technical_specification_id="sample", payload={})
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.tenant_id == "sample"


