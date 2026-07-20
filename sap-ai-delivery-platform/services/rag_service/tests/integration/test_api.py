"""Integration tests exercising the HTTP API end-to-end (in-memory DB)."""


def test_knowledge_source_crud_flow(client):
    payload = {"tenant_id": "sample", "source_type": "sample", "uri": "sample", "last_indexed_at": None, "is_dead_link": True}
    resp = client.post("/api/v1/knowledge-sources", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/knowledge-sources")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/knowledge-sources/{item_id}")
    assert resp.status_code == 200

    resp = client.patch(f"/api/v1/knowledge-sources/{item_id}", json={})
    assert resp.status_code == 200

    resp = client.delete(f"/api/v1/knowledge-sources/{item_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/knowledge-sources/{item_id}")
    assert resp.status_code == 404


def test_knowledge_chunk_crud_flow(client):
    payload = {"knowledge_source_id": "sample", "chunk_index": 1, "text": "sample", "vector_id": "sample"}
    resp = client.post("/api/v1/knowledge-chunks", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/knowledge-chunks")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/knowledge-chunks/{item_id}")
    assert resp.status_code == 200

    resp = client.patch(f"/api/v1/knowledge-chunks/{item_id}", json={})
    assert resp.status_code == 200

    resp = client.delete(f"/api/v1/knowledge-chunks/{item_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/knowledge-chunks/{item_id}")
    assert resp.status_code == 404


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

