"""Integration tests exercising the HTTP API end-to-end (in-memory DB)."""


def test_requirement_set_crud_flow(client):
    payload = {"tenant_id": "sample", "transcript_id": "sample", "version": 1, "status": "sample"}
    resp = client.post("/api/v1/requirement-sets", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/requirement-sets")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/requirement-sets/{item_id}")
    assert resp.status_code == 200

    resp = client.patch(f"/api/v1/requirement-sets/{item_id}", json={})
    assert resp.status_code == 200

    resp = client.delete(f"/api/v1/requirement-sets/{item_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/requirement-sets/{item_id}")
    assert resp.status_code == 404


def test_requirement_crud_flow(client):
    payload = {"requirement_set_id": "sample", "type": "sample", "title": "sample", "description": "sample", "priority": "sample"}
    resp = client.post("/api/v1/requirements", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/requirements")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/requirements/{item_id}")
    assert resp.status_code == 200

    resp = client.patch(f"/api/v1/requirements/{item_id}", json={})
    assert resp.status_code == 200

    resp = client.delete(f"/api/v1/requirements/{item_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/requirements/{item_id}")
    assert resp.status_code == 404


def test_requirement_risk_crud_flow(client):
    payload = {"requirement_set_id": "sample", "description": "sample", "severity": "sample"}
    resp = client.post("/api/v1/requirement-risks", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/requirement-risks")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/requirement-risks/{item_id}")
    assert resp.status_code == 200

    resp = client.patch(f"/api/v1/requirement-risks/{item_id}", json={})
    assert resp.status_code == 200

    resp = client.delete(f"/api/v1/requirement-risks/{item_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/requirement-risks/{item_id}")
    assert resp.status_code == 404


def test_requirement_entity_crud_flow(client):
    payload = {"requirement_set_id": "sample", "name": "sample", "attributes": {}}
    resp = client.post("/api/v1/requirement-entities", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/requirement-entities")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/requirement-entities/{item_id}")
    assert resp.status_code == 200

    resp = client.patch(f"/api/v1/requirement-entities/{item_id}", json={})
    assert resp.status_code == 200

    resp = client.delete(f"/api/v1/requirement-entities/{item_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/requirement-entities/{item_id}")
    assert resp.status_code == 404


def test_business_rule_crud_flow(client):
    payload = {"requirement_set_id": "sample", "rule": "sample"}
    resp = client.post("/api/v1/business-rules", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/business-rules")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/business-rules/{item_id}")
    assert resp.status_code == 200

    resp = client.patch(f"/api/v1/business-rules/{item_id}", json={})
    assert resp.status_code == 200

    resp = client.delete(f"/api/v1/business-rules/{item_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/business-rules/{item_id}")
    assert resp.status_code == 404


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

