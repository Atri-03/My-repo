"""Unit tests for SQLAlchemy models."""
from app.db import models


def test_create_source_document_model(db_session):
    obj = models.SourceDocument(tenant_id="sample", project_id="sample", source_type="sample", origin_uri="sample", checksum="sample", blob_uri="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.tenant_id == "sample"


def test_create_transcript_model(db_session):
    obj = models.Transcript(source_document_id="sample", parsed_format="sample", raw_text="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.source_document_id == "sample"


