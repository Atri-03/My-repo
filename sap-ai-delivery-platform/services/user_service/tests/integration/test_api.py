"""Integration tests exercising the HTTP API end-to-end (in-memory DB)."""


def test_tenant_crud_flow(client):
    payload = {"name": "sample", "entra_tenant_id": "sample", "tier": "sample", "status": "sample"}
    resp = client.post("/api/v1/tenants", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/tenants")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/tenants/{item_id}")
    assert resp.status_code == 200

    resp = client.patch(f"/api/v1/tenants/{item_id}", json={})
    assert resp.status_code == 200

    resp = client.delete(f"/api/v1/tenants/{item_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/tenants/{item_id}")
    assert resp.status_code == 404


def test_project_crud_flow(client):
    payload = {"tenant_id": "sample", "name": "sample", "sap_execution_repo_url": "sample"}
    resp = client.post("/api/v1/projects", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/projects")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/projects/{item_id}")
    assert resp.status_code == 200

    resp = client.patch(f"/api/v1/projects/{item_id}", json={})
    assert resp.status_code == 200

    resp = client.delete(f"/api/v1/projects/{item_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/projects/{item_id}")
    assert resp.status_code == 404


def test_user_crud_flow(client):
    payload = {"tenant_id": "sample", "email": "sample", "display_name": "sample", "role": "sample", "is_active": True}
    resp = client.post("/api/v1/users", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/users")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/users/{item_id}")
    assert resp.status_code == 200

    resp = client.patch(f"/api/v1/users/{item_id}", json={})
    assert resp.status_code == 200

    resp = client.delete(f"/api/v1/users/{item_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/users/{item_id}")
    assert resp.status_code == 404


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

