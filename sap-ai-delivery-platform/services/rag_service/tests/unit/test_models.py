"""Unit tests for SQLAlchemy models."""
from app.db import models


def test_create_knowledge_source_model(db_session):
    obj = models.KnowledgeSource(tenant_id="sample", source_type="sample", uri="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.tenant_id == "sample"


def test_create_knowledge_chunk_model(db_session):
    obj = models.KnowledgeChunk(knowledge_source_id="sample", chunk_index=1, text="sample", vector_id="sample")
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    assert obj.id is not None
    assert obj.knowledge_source_id == "sample"


