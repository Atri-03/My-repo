"""Integration tests exercising the HTTP API end-to-end (in-memory DB)."""


def test_workflow_run_crud_flow(client):
    payload = {"tenant_id": "sample", "transcript_id": "sample", "current_state": "sample", "started_at": None, "completed_at": None}
    resp = client.post("/api/v1/workflow-runs", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/workflow-runs")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/workflow-runs/{item_id}")
    assert resp.status_code == 200

    resp = client.patch(f"/api/v1/workflow-runs/{item_id}", json={})
    assert resp.status_code == 200

    resp = client.delete(f"/api/v1/workflow-runs/{item_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/workflow-runs/{item_id}")
    assert resp.status_code == 404


def test_workflow_event_crud_flow(client):
    payload = {"workflow_run_id": "sample", "from_state": "sample", "to_state": "sample", "actor": "sample", "occurred_at": None}
    resp = client.post("/api/v1/workflow-events", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/workflow-events")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/workflow-events/{item_id}")
    assert resp.status_code == 200



def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

