"""Unit tests for SQLAlchemy models."""
from app.db import models


def test_create_tenant_model(db_session):
    obj = models.Tenant(name="sample", entra_tenant_id="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.name == "sample"


def test_create_project_model(db_session):
    obj = models.Project(tenant_id="sample", name="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.tenant_id == "sample"


def test_create_user_model(db_session):
    obj = models.User(tenant_id="sample", email="sample", display_name="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.tenant_id == "sample"


