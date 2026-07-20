"""Integration tests exercising the HTTP API end-to-end (in-memory DB)."""


def test_audit_log_entry_crud_flow(client):
    payload = {"tenant_id": "sample", "entity_type": "sample", "entity_id": "sample", "action": "sample", "actor": "sample", "before": {}, "after": {}, "occurred_at": None}
    resp = client.post("/api/v1/audit-log-entries", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/audit-log-entries")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/audit-log-entries/{item_id}")
    assert resp.status_code == 200



def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

