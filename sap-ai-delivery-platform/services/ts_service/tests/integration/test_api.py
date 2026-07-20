"""Integration tests exercising the HTTP API end-to-end (in-memory DB)."""


def test_technical_specification_crud_flow(client):
    payload = {"tenant_id": "sample", "functional_specification_id": "sample", "template_id": "sample", "version": 1, "parent_version_id": "sample", "status": "sample", "content": {}, "blob_uri": "sample", "regeneration_count": 1}
    resp = client.post("/api/v1/technical-specifications", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/technical-specifications")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/technical-specifications/{item_id}")
    assert resp.status_code == 200

    resp = client.patch(f"/api/v1/technical-specifications/{item_id}", json={})
    assert resp.status_code == 200

    resp = client.delete(f"/api/v1/technical-specifications/{item_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/technical-specifications/{item_id}")
    assert resp.status_code == 404


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

