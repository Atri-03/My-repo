"""Integration tests for the dynamic SAP Execution MCP tool endpoints."""
import respx
from httpx import Response

from app.core.config import get_settings

settings = get_settings()


def _mock_audit():
    return respx.post(f"{settings.audit_service_url}/api/v1/audit-log-entries").mock(
        return_value=Response(201, json={"id": "audit-1"})
    )


@respx.mock
def test_list_tools_includes_sap_execution_capabilities(client):
    _mock_audit()
    resp = client.get("/api/v1/mcp/tools")
    assert resp.status_code == 200
    names = {tool["name"] for tool in resp.json()["tools"]}
    expected = {
        "create_package",
        "create_transport",
        "release_transport",
        "generate_object",
        "generate_rap",
        "generate_cds",
        "generate_odata",
        "activate_object",
        "run_unit_tests",
        "run_atc",
        "remediate_atc_findings",
    }
    assert expected.issubset(names)


@respx.mock
def test_get_tool_schema(client):
    resp = client.get("/api/v1/mcp/tools/create_package")
    assert resp.status_code == 200
    body = resp.json()
    assert body["name"] == "create_package"
    assert "package_name" in body["input_schema"]["properties"]


def test_get_unknown_tool_returns_404(client):
    resp = client.get("/api/v1/mcp/tools/does_not_exist")
    assert resp.status_code == 404


@respx.mock
def test_invoke_create_package_success_records_audit(client):
    respx.post(f"{settings.sap_execution_service_url}/api/v1/packages").mock(
        return_value=Response(201, json={"package_name": "ZPKG_TEST", "status": "CREATED"})
    )
    audit_route = _mock_audit()

    resp = client.post(
        "/api/v1/mcp/tools/create_package/invoke",
        json={"package_name": "ZPKG_TEST", "description": "Test package"},
        headers={"X-Actor": "alice", "X-Tenant-Id": "tenant-1"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["tool"] == "create_package"
    assert body["result"]["package_name"] == "ZPKG_TEST"
    assert "correlation_id" in body
    assert audit_route.called


@respx.mock
def test_invoke_generate_rap(client):
    respx.post(f"{settings.sap_execution_service_url}/api/v1/rap-business-objects").mock(
        return_value=Response(201, json={"business_object_name": "TRAVEL", "status": "GENERATED"})
    )
    _mock_audit()

    resp = client.post(
        "/api/v1/mcp/tools/generate_rap/invoke",
        json={
            "business_object_name": "TRAVEL",
            "package": "ZPKG_TRAVEL",
            "transport_request": "DEVK900001",
            "root_entity": "ZI_Travel",
        },
    )
    assert resp.status_code == 200
    assert resp.json()["result"]["business_object_name"] == "TRAVEL"


@respx.mock
def test_invoke_run_atc_and_remediate(client):
    respx.post(f"{settings.sap_execution_service_url}/api/v1/atc-runs").mock(
        return_value=Response(201, json={"run_id": "atc-1", "findings": ["F1", "F2"]})
    )
    respx.post(f"{settings.sap_execution_service_url}/api/v1/atc-remediations").mock(
        return_value=Response(200, json={"remediated": ["F1", "F2"]})
    )
    _mock_audit()

    run_resp = client.post(
        "/api/v1/mcp/tools/run_atc/invoke",
        json={"object_name": "ZCL_TEST", "object_type": "CLAS"},
    )
    assert run_resp.status_code == 200
    assert run_resp.json()["result"]["findings"] == ["F1", "F2"]

    remediate_resp = client.post(
        "/api/v1/mcp/tools/remediate_atc_findings/invoke",
        json={"object_name": "ZCL_TEST", "object_type": "CLAS", "finding_ids": ["F1", "F2"]},
    )
    assert remediate_resp.status_code == 200
    assert remediate_resp.json()["result"]["remediated"] == ["F1", "F2"]


@respx.mock
def test_invoke_unknown_tool_returns_404(client):
    resp = client.post("/api/v1/mcp/tools/does_not_exist/invoke", json={})
    assert resp.status_code == 404


@respx.mock
def test_invoke_with_invalid_payload_returns_422_and_audits(client):
    audit_route = _mock_audit()
    resp = client.post(
        "/api/v1/mcp/tools/create_package/invoke",
        json={"description": "missing package_name"},
    )
    assert resp.status_code == 422
    assert audit_route.called


@respx.mock
def test_invoke_upstream_failure_returns_error_and_audits(client):
    respx.post(f"{settings.sap_execution_service_url}/api/v1/packages").mock(
        return_value=Response(500, text="boom")
    )
    audit_route = _mock_audit()

    resp = client.post(
        "/api/v1/mcp/tools/create_package/invoke",
        json={"package_name": "ZPKG_FAIL", "description": "will fail"},
    )
    assert resp.status_code == 500
    assert audit_route.called


@respx.mock
def test_invoke_still_succeeds_when_audit_service_unreachable(client):
    respx.post(f"{settings.sap_execution_service_url}/api/v1/packages").mock(
        return_value=Response(201, json={"package_name": "ZPKG_OK", "status": "CREATED"})
    )
    respx.post(f"{settings.audit_service_url}/api/v1/audit-log-entries").mock(
        side_effect=Exception("audit service down")
    )

    resp = client.post(
        "/api/v1/mcp/tools/create_package/invoke",
        json={"package_name": "ZPKG_OK", "description": "ok"},
    )
    assert resp.status_code == 200
    assert resp.json()["result"]["package_name"] == "ZPKG_OK"
