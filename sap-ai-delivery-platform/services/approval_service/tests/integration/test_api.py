"""Integration tests exercising the HTTP API end-to-end (in-memory DB)."""


def test_review_decision_crud_flow(client):
    payload = {"review_cycle_id": "sample", "decided_by": "sample", "decision": "sample", "decided_at": None}
    resp = client.post("/api/v1/review-decisions", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/review-decisions")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/review-decisions/{item_id}")
    assert resp.status_code == 200



def test_sap_execution_package_crud_flow(client):
    payload = {"tenant_id": "sample", "technical_specification_id": "sample", "version": 1, "status": "sample", "payload": {}, "sap_execution_repo_ref": "sample", "published_at": None}
    resp = client.post("/api/v1/sap-execution-packages", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/sap-execution-packages")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/sap-execution-packages/{item_id}")
    assert resp.status_code == 200

    resp = client.patch(f"/api/v1/sap-execution-packages/{item_id}", json={})
    assert resp.status_code == 200

    resp = client.delete(f"/api/v1/sap-execution-packages/{item_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/sap-execution-packages/{item_id}")
    assert resp.status_code == 404


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

