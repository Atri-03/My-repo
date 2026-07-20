"""Integration tests exercising the HTTP API end-to-end (in-memory DB).

These payload shapes intentionally mirror the exact request bodies sent by
`mcp_gateway_service`'s SAP Execution MCP tools, so a passing test here is
strong evidence the gateway's `SAPExecutionClient` calls will succeed.
"""


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_create_package(client):
    resp = client.post(
        "/api/v1/packages",
        json={"package_name": "ZRAG_POC", "description": "POC package", "software_component": "LOCAL"},
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["package_name"] == "ZRAG_POC"
    assert body["status"] == "CREATED"
    assert body["tenant_id"] == "default"


def test_create_and_release_transport(client):
    resp = client.post("/api/v1/transports", json={"description": "Feature transport", "transport_type": "workbench"})
    assert resp.status_code == 201, resp.text
    transport = resp.json()
    assert transport["status"] == "MODIFIABLE"
    transport_request = transport["transport_request"]
    assert transport_request

    resp = client.post(
        f"/api/v1/transports/{transport_request}/release",
        json={"transport_request": transport_request},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["status"] == "RELEASED"


def test_generate_object_rap_cds_odata(client):
    transport = client.post("/api/v1/transports", json={"description": "t"}).json()["transport_request"]

    resp = client.post(
        "/api/v1/objects",
        json={
            "object_name": "ZPROGRAM",
            "object_type": "PROGRAM",
            "package": "ZPKG",
            "transport_request": transport,
            "source_code": "REPORT zprogram.",
        },
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["object_type"] == "PROGRAM"

    resp = client.post(
        "/api/v1/rap-business-objects",
        json={
            "business_object_name": "ZI_TRAVEL",
            "package": "ZPKG",
            "transport_request": transport,
            "root_entity": "Travel",
        },
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["object_type"] == "RAP_BUSINESS_OBJECT"

    resp = client.post(
        "/api/v1/cds-views",
        json={
            "view_name": "ZI_TRAVEL_VIEW",
            "package": "ZPKG",
            "transport_request": transport,
            "ddl_source": "define view ZI_TRAVEL_VIEW as select from travel {}",
        },
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["object_type"] == "CDS_VIEW"

    resp = client.post(
        "/api/v1/odata-services",
        json={
            "service_name": "ZTRAVEL_SRV",
            "package": "ZPKG",
            "transport_request": transport,
            "odata_version": "v4",
        },
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["object_type"] == "ODATA_SERVICE"


def test_activate_object_flips_generated_object_status(client):
    transport = client.post("/api/v1/transports", json={"description": "t"}).json()["transport_request"]
    client.post(
        "/api/v1/objects",
        json={"object_name": "ZOBJ", "object_type": "PROGRAM", "package": "ZPKG", "transport_request": transport},
    )

    resp = client.post("/api/v1/activations", json={"object_name": "ZOBJ", "object_type": "PROGRAM"})
    assert resp.status_code == 201, resp.text
    assert resp.json()["status"] == "ACTIVATED"

    objects = client.get("/api/v1/objects").json()
    assert any(o["object_name"] == "ZOBJ" and o["status"] == "ACTIVE" for o in objects)


def test_run_atc_and_remediate(client):
    resp = client.post("/api/v1/atc-runs", json={"object_name": "ZOBJ", "object_type": "PROGRAM", "variant": "DEFAULT"})
    assert resp.status_code == 201, resp.text
    assert resp.json()["status"] == "COMPLETED"
    assert resp.json()["findings"] == []

    resp = client.post(
        "/api/v1/atc-remediations",
        json={"object_name": "ZOBJ", "object_type": "PROGRAM", "finding_ids": ["F1", "F2"], "auto_apply": True},
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["status"] == "APPLIED"

    resp = client.post(
        "/api/v1/atc-remediations",
        json={"object_name": "ZOBJ", "object_type": "PROGRAM", "finding_ids": ["F3"], "auto_apply": False},
    )
    assert resp.json()["status"] == "PROPOSED"


def test_run_unit_tests(client):
    resp = client.post(
        "/api/v1/unit-test-runs",
        json={"object_name": "ZOBJ", "object_type": "CLASS", "test_classes": ["LTC_TEST"]},
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["status"] == "PASSED"


def test_architect_plan_orders_steps(client):
    resp = client.post(
        "/api/v1/architect/plans",
        json={
            "technical_specification_id": "ts-1",
            "package_name": "ZPKG",
            "needs_cds": True,
            "needs_rap": True,
            "needs_odata": True,
            "object_names": ["ZEXTRA_PROGRAM"],
        },
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    tools = [s["tool"] for s in body["steps"]]
    assert tools == [
        "create_package",
        "create_transport",
        "generate_cds",
        "generate_rap",
        "generate_odata",
        "generate_object",
        "run_unit_tests",
        "run_atc",
        "remediate_atc_findings",
        "activate_object",
    ]

    resp = client.get(f"/api/v1/architect/plans/{body['id']}")
    assert resp.status_code == 200


def test_tenant_id_from_header(client):
    resp = client.post(
        "/api/v1/packages",
        json={"package_name": "ZPKG2", "description": "d"},
        headers={"X-Tenant-Id": "acme-corp"},
    )
    assert resp.status_code == 201
    assert resp.json()["tenant_id"] == "acme-corp"
