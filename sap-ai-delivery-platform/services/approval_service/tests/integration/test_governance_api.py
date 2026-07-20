"""Integration tests for the Human-in-the-Loop Governance Framework API."""
import respx
from httpx import Response

from app.core.config import get_settings
from app.core.gates import GATE_1_BUSINESS_APPROVAL_OF_FS, GATE_2_ARCHITECT_APPROVAL_OF_TS

settings = get_settings()


def _mock_audit():
    return respx.post(f"{settings.audit_service_url}/api/v1/audit-log-entries").mock(
        return_value=Response(201, json={"id": "audit-1"})
    )


@respx.mock
def test_seed_default_gates_creates_five_gates(client):
    resp = client.post("/api/v1/tenants/tenant-1/gate-definitions/seed-defaults")
    assert resp.status_code == 201, resp.text
    gates = resp.json()
    assert len(gates) == 5
    keys = {g["gate_key"] for g in gates}
    assert GATE_1_BUSINESS_APPROVAL_OF_FS in keys
    assert GATE_2_ARCHITECT_APPROVAL_OF_TS in keys


@respx.mock
def test_seed_default_gates_is_idempotent(client):
    resp1 = client.post("/api/v1/tenants/tenant-1/gate-definitions/seed-defaults")
    assert len(resp1.json()) == 5
    resp2 = client.post("/api/v1/tenants/tenant-1/gate-definitions/seed-defaults")
    assert resp2.json() == []

    resp = client.get("/api/v1/gate-definitions", params={"tenant_id": "tenant-1"})
    assert len(resp.json()) == 5


@respx.mock
def test_gate_definitions_are_configurable(client):
    client.post("/api/v1/tenants/tenant-1/gate-definitions/seed-defaults")
    gate = client.get(
        "/api/v1/gate-definitions", params={"tenant_id": "tenant-1"}
    ).json()[0]

    resp = client.patch(
        f"/api/v1/gate-definitions/{gate['id']}",
        json={"required_role": "SENIOR_BUSINESS_APPROVER", "is_active": False},
    )
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["required_role"] == "SENIOR_BUSINESS_APPROVER"
    assert updated["is_active"] is False


@respx.mock
def test_create_gate_definition_custom(client):
    payload = {
        "tenant_id": "tenant-2",
        "gate_key": "CUSTOM_GATE",
        "name": "Custom Gate",
        "entity_type": "CustomEntity",
        "required_role": "CUSTOM_ROLE",
    }
    resp = client.post("/api/v1/gate-definitions", json=payload)
    assert resp.status_code == 201, resp.text
    assert resp.json()["gate_key"] == "CUSTOM_GATE"


@respx.mock
def test_gate_approval_request_rejected_when_gate_not_configured(client):
    _mock_audit()
    resp = client.post(
        "/api/v1/gate-approvals",
        json={
            "tenant_id": "tenant-unconfigured",
            "gate_key": GATE_1_BUSINESS_APPROVAL_OF_FS,
            "entity_type": "FunctionalSpecification",
            "entity_id": "fs-1",
            "requested_by": "alice",
            "requested_by_role": "BUSINESS_ANALYST",
        },
    )
    assert resp.status_code == 400


@respx.mock
def test_full_gate_approval_happy_path_records_audit(client):
    audit_route = _mock_audit()
    client.post("/api/v1/tenants/tenant-1/gate-definitions/seed-defaults")

    create_resp = client.post(
        "/api/v1/gate-approvals",
        json={
            "tenant_id": "tenant-1",
            "gate_key": GATE_1_BUSINESS_APPROVAL_OF_FS,
            "entity_type": "FunctionalSpecification",
            "entity_id": "fs-1",
            "requested_by": "alice",
            "requested_by_role": "BUSINESS_ANALYST",
        },
    )
    assert create_resp.status_code == 201, create_resp.text
    request_id = create_resp.json()["id"]
    assert create_resp.json()["status"] == "PENDING"

    decide_resp = client.post(
        f"/api/v1/gate-approvals/{request_id}/decide",
        json={
            "decided_by": "bob",
            "decided_by_role": "BUSINESS_APPROVER",
            "decision": "APPROVED",
            "decision_comments": "Looks good",
        },
    )
    assert decide_resp.status_code == 200, decide_resp.text
    body = decide_resp.json()
    assert body["status"] == "APPROVED"
    assert body["sod_violation"] is False
    assert audit_route.called


@respx.mock
def test_decide_gate_approval_role_mismatch_returns_403(client):
    _mock_audit()
    client.post("/api/v1/tenants/tenant-1/gate-definitions/seed-defaults")
    create_resp = client.post(
        "/api/v1/gate-approvals",
        json={
            "tenant_id": "tenant-1",
            "gate_key": GATE_1_BUSINESS_APPROVAL_OF_FS,
            "entity_type": "FunctionalSpecification",
            "entity_id": "fs-1",
            "requested_by": "alice",
        },
    )
    request_id = create_resp.json()["id"]

    resp = client.post(
        f"/api/v1/gate-approvals/{request_id}/decide",
        json={"decided_by": "bob", "decided_by_role": "DEVELOPER", "decision": "APPROVED"},
    )
    assert resp.status_code == 403


@respx.mock
def test_decide_gate_approval_segregation_of_duties_violation_returns_409(client):
    _mock_audit()
    client.post("/api/v1/tenants/tenant-1/gate-definitions/seed-defaults")
    create_resp = client.post(
        "/api/v1/gate-approvals",
        json={
            "tenant_id": "tenant-1",
            "gate_key": GATE_1_BUSINESS_APPROVAL_OF_FS,
            "entity_type": "FunctionalSpecification",
            "entity_id": "fs-1",
            "requested_by": "alice",
        },
    )
    request_id = create_resp.json()["id"]

    resp = client.post(
        f"/api/v1/gate-approvals/{request_id}/decide",
        json={"decided_by": "alice", "decided_by_role": "BUSINESS_APPROVER", "decision": "APPROVED"},
    )
    assert resp.status_code == 409


@respx.mock
def test_decide_gate_approval_twice_returns_400(client):
    _mock_audit()
    client.post("/api/v1/tenants/tenant-1/gate-definitions/seed-defaults")
    create_resp = client.post(
        "/api/v1/gate-approvals",
        json={
            "tenant_id": "tenant-1",
            "gate_key": GATE_1_BUSINESS_APPROVAL_OF_FS,
            "entity_type": "FunctionalSpecification",
            "entity_id": "fs-1",
            "requested_by": "alice",
        },
    )
    request_id = create_resp.json()["id"]
    client.post(
        f"/api/v1/gate-approvals/{request_id}/decide",
        json={"decided_by": "bob", "decided_by_role": "BUSINESS_APPROVER", "decision": "APPROVED"},
    )

    resp = client.post(
        f"/api/v1/gate-approvals/{request_id}/decide",
        json={"decided_by": "carol", "decided_by_role": "BUSINESS_APPROVER", "decision": "APPROVED"},
    )
    assert resp.status_code == 400


@respx.mock
def test_list_and_get_gate_approval_requests(client):
    _mock_audit()
    client.post("/api/v1/tenants/tenant-1/gate-definitions/seed-defaults")
    create_resp = client.post(
        "/api/v1/gate-approvals",
        json={
            "tenant_id": "tenant-1",
            "gate_key": GATE_1_BUSINESS_APPROVAL_OF_FS,
            "entity_type": "FunctionalSpecification",
            "entity_id": "fs-1",
            "requested_by": "alice",
        },
    )
    request_id = create_resp.json()["id"]

    list_resp = client.get("/api/v1/gate-approvals", params={"tenant_id": "tenant-1"})
    assert list_resp.status_code == 200
    assert any(item["id"] == request_id for item in list_resp.json())

    get_resp = client.get(f"/api/v1/gate-approvals/{request_id}")
    assert get_resp.status_code == 200

    missing_resp = client.get("/api/v1/gate-approvals/does-not-exist")
    assert missing_resp.status_code == 404


@respx.mock
def test_gate_approval_still_succeeds_when_audit_service_unreachable(client):
    respx.post(f"{settings.audit_service_url}/api/v1/audit-log-entries").mock(
        side_effect=Exception("audit service down")
    )
    client.post("/api/v1/tenants/tenant-1/gate-definitions/seed-defaults")
    resp = client.post(
        "/api/v1/gate-approvals",
        json={
            "tenant_id": "tenant-1",
            "gate_key": GATE_1_BUSINESS_APPROVAL_OF_FS,
            "entity_type": "FunctionalSpecification",
            "entity_id": "fs-1",
            "requested_by": "alice",
        },
    )
    assert resp.status_code == 201
