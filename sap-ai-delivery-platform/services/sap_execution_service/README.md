# SAP Execution Service

The in-repository **SAP Execution bounded context**: package/transport
management, ABAP/RAP/CDS/OData object generation, activation, ATC
(ABAP Test Cockpit) orchestration + remediation, ABAP Unit testing, and a
lightweight **SAP Solution Architect Agent** execution planner.

This service is the backing implementation for the SAP Execution MCP
tools already exposed by `mcp_gateway_service`
(`app/mcp/tools/*.py`, proxied via `SAPExecutionClient` to
`SAP_EXECUTION_SERVICE_URL`, default `http://sap-execution-service:8100`).
No changes were required on the gateway side — its tool payloads already
match the endpoints below.

## Endpoints

| Endpoint | Purpose |
|---|---|
| `POST /api/v1/packages` | Create an ABAP development package |
| `POST /api/v1/transports` | Create a transport request (server-generates the transport ID) |
| `POST /api/v1/transports/{transport_request}/release` | Release a transport |
| `POST /api/v1/objects` | Generate a generic ABAP object (program, class, ...) |
| `POST /api/v1/rap-business-objects` | Generate a RAP business object |
| `POST /api/v1/cds-views` | Generate a CDS view |
| `POST /api/v1/odata-services` | Generate/expose an OData service |
| `POST /api/v1/activations` | Activate an inactive object (flips matching generated object to `ACTIVE`) |
| `POST /api/v1/atc-runs` | Run an ATC check variant against an object |
| `POST /api/v1/atc-remediations` | Propose or auto-apply remediations for ATC findings |
| `POST /api/v1/unit-test-runs` | Run ABAP Unit tests |
| `POST /api/v1/architect/plans` | SAP Solution Architect Agent: propose an ordered execution plan for a Technical Specification |

All `GET` list/detail endpoints mirror the sibling services' CRUD
conventions for observability (used by the frontend Execution page).

Every create endpoint accepts an optional `tenant_id`; when omitted it
falls back to the `X-Tenant-Id` header (already sent by the MCP gateway),
then `"default"`.

## Governance

Objects generated here are subject to the existing Human-in-the-Loop
governance framework in `approval_service` (Gates 3-5: developer approval
of SAP design, developer approval before object creation, lead approval
before activation) — this service does not bypass or duplicate that
enforcement.

## Run locally

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8100
```

OpenAPI docs available at `http://localhost:8100/docs`.

## Tests

```bash
pytest
```

## Migrations

```bash
alembic upgrade head
```
