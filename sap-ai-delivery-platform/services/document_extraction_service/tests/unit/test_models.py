"""Unit tests for SQLAlchemy models."""
from app.db import models


def test_create_requirement_set_model(db_session):
    obj = models.RequirementSet(tenant_id="sample", transcript_id="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.tenant_id == "sample"


def test_create_requirement_model(db_session):
    obj = models.Requirement(requirement_set_id="sample", type="sample", title="sample", description="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.requirement_set_id == "sample"


def test_create_requirement_risk_model(db_session):
    obj = models.RequirementRisk(requirement_set_id="sample", description="sample", severity="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.requirement_set_id == "sample"


def test_create_requirement_entity_model(db_session):
    obj = models.RequirementEntity(requirement_set_id="sample", name="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.requirement_set_id == "sample"


def test_create_business_rule_model(db_session):
    obj = models.BusinessRule(requirement_set_id="sample", rule="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.requirement_set_id == "sample"


