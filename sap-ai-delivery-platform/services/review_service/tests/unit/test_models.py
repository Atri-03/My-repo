"""Unit tests for SQLAlchemy models."""
from app.db import models


def test_create_review_cycle_model(db_session):
    obj = models.ReviewCycle(tenant_id="sample", artefact_type="sample", artefact_id="sample", gate="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.tenant_id == "sample"


def test_create_review_comment_model(db_session):
    obj = models.ReviewComment(review_cycle_id="sample", reviewer_id="sample", comment="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.review_cycle_id == "sample"


