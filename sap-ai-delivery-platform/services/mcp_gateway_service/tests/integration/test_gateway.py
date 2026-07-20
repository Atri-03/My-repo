"""Integration tests for MCP-style gateway tool endpoints, mocking downstream HTTP calls."""
import respx
from httpx import Response

from app.core.config import get_settings

settings = get_settings()


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


@respx.mock
def test_list_sources(client):
    respx.get(f"{settings.rag_service_url}/api/v1/knowledge-sources").mock(
        return_value=Response(200, json=[{"id": "src-1", "source_type": "SAP_STANDARD"}])
    )
    resp = client.get("/api/v1/tools/list_sources")
    assert resp.status_code == 200
    assert resp.json()["sources"][0]["id"] == "src-1"


@respx.mock
def test_search_documents(client):
    respx.get(f"{settings.rag_service_url}/api/v1/knowledge-chunks").mock(
        return_value=Response(200, json=[{"id": "chunk-1", "knowledge_source_id": "src-1", "text": "hello"}])
    )
    resp = client.post("/api/v1/tools/search_documents", json={"query": "hello", "top": 5})
    assert resp.status_code == 200
    assert resp.json()["results"][0]["chunk_id"] == "chunk-1"


@respx.mock
def test_get_transcript(client):
    respx.get(f"{settings.transcript_service_url}/api/v1/transcripts/t-1").mock(
        return_value=Response(200, json={"id": "t-1", "raw_text": "hi"})
    )
    resp = client.get("/api/v1/tools/get_transcript/t-1")
    assert resp.status_code == 200
    assert resp.json()["id"] == "t-1"


@respx.mock
def test_get_transcript_upstream_error(client):
    respx.get(f"{settings.transcript_service_url}/api/v1/transcripts/missing").mock(
        return_value=Response(404, json={"detail": "not found"})
    )
    resp = client.get("/api/v1/tools/get_transcript/missing")
    assert resp.status_code == 404


@respx.mock
def test_submit_review_decision(client):
    respx.post(f"{settings.approval_service_url}/api/v1/review-decisions").mock(
        return_value=Response(201, json={"id": "d-1", "decision": "APPROVE"})
    )
    resp = client.post(
        "/api/v1/tools/submit_review_decision",
        json={"review_cycle_id": "rc-1", "decided_by": "alice", "decision": "APPROVE"},
    )
    assert resp.status_code == 200
    assert resp.json()["decision"] == "APPROVE"
