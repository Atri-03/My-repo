"""Integration tests exercising the HTTP API end-to-end (in-memory DB)."""


def test_review_cycle_crud_flow(client):
    payload = {"tenant_id": "sample", "artefact_type": "sample", "artefact_id": "sample", "gate": "sample", "status": "sample", "opened_at": None, "closed_at": None}
    resp = client.post("/api/v1/review-cycles", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/review-cycles")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/review-cycles/{item_id}")
    assert resp.status_code == 200

    resp = client.patch(f"/api/v1/review-cycles/{item_id}", json={})
    assert resp.status_code == 200

    resp = client.delete(f"/api/v1/review-cycles/{item_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/review-cycles/{item_id}")
    assert resp.status_code == 404


def test_review_comment_crud_flow(client):
    payload = {"review_cycle_id": "sample", "reviewer_id": "sample", "comment": "sample"}
    resp = client.post("/api/v1/review-comments", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    item_id = created["id"]

    resp = client.get("/api/v1/review-comments")
    assert resp.status_code == 200
    assert any(item['id'] == item_id for item in resp.json())

    resp = client.get(f"/api/v1/review-comments/{item_id}")
    assert resp.status_code == 200



def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

