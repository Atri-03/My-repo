"""Unit tests for SQLAlchemy models."""
from app.db import models


def test_create_workflow_run_model(db_session):
    obj = models.WorkflowRun(tenant_id="sample", transcript_id="sample", current_state="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.tenant_id == "sample"


def test_create_workflow_event_model(db_session):
    obj = models.WorkflowEvent(workflow_run_id="sample", to_state="sample", actor="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.workflow_run_id == "sample"


