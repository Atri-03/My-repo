"""Unit tests for SQLAlchemy models."""
from app.db import models


def test_create_sap_package_model(db_session):
    obj = models.SapPackage(tenant_id="sample", package_name="ZPKG", description="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.status == "CREATED"


def test_create_sap_transport_model(db_session):
    obj = models.SapTransport(tenant_id="sample", transport_request="TR00000001", description="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.status == "MODIFIABLE"


def test_create_generated_object_model(db_session):
    obj = models.GeneratedObject(
        tenant_id="sample",
        object_name="ZOBJ",
        object_type="PROGRAM",
        package="ZPKG",
        transport_request="TR00000001",
    )
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.status == "INACTIVE"


def test_create_execution_plan_model(db_session):
    obj = models.ExecutionPlan(tenant_id="sample", technical_specification_id="ts-1", steps=[])
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.status == "PROPOSED"
