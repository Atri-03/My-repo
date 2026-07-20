"""Integration tests exercising the HTTP API end-to-end (in-memory DB)."""


def test_source_document_crud_flow(client):
    payload = {"tenant_id": "sample", "project_id": "sample", "source_type": "sample", "origin_uri": "sample", "checksum": "sample", "blob_uri": "sample", "ingested_at": None}
    resp = client.post("/api/v1/source-documents", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/source-documents")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/source-documents/{item_id}")
    assert resp.status_code == 200

    resp = client.patch(f"/api/v1/source-documents/{item_id}", json={})
    assert resp.status_code == 200

    resp = client.delete(f"/api/v1/source-documents/{item_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/source-documents/{item_id}")
    assert resp.status_code == 404


def test_transcript_crud_flow(client):
    payload = {"source_document_id": "sample", "meeting_date": None, "participants": [], "parsed_format": "sample", "raw_text": "sample", "structured_content": {}}
    resp = client.post("/api/v1/transcripts", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/transcripts")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/transcripts/{item_id}")
    assert resp.status_code == 200

    resp = client.patch(f"/api/v1/transcripts/{item_id}", json={})
    assert resp.status_code == 200

    resp = client.delete(f"/api/v1/transcripts/{item_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/transcripts/{item_id}")
    assert resp.status_code == 404


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

