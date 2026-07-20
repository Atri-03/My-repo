# Backend Services (Phase 2)

This directory contains the production backend for the SAP AI Delivery
Platform: 12 independently deployable FastAPI microservices, each owning
its own PostgreSQL database (SQLite is used automatically for local
development and tests).

| Service | Port | Responsibility |
|---|---|---|
| `transcript_service` | 8001 | Ingests and manages source documents and transcripts. |
| `document_extraction_service` | 8002 | Extracts requirements, risks, entities and business rules. |
| `fs_service` | 8003 | Generates and versions Functional Specifications. |
| `ts_service` | 8004 | Generates and versions Technical Specifications. |
| `review_service` | 8005 | Manages review cycles and reviewer comments. |
| `approval_service` | 8006 | Records approval/rejection decisions and publishes SAP Execution Packages. |
| `audit_service` | 8007 | Append-only audit log of entity changes. |
| `rag_service` | 8008 | Knowledge source/chunk metadata backing enterprise RAG search. |
| `user_service` | 8009 | Tenants, projects and users. |
| `workflow_service` | 8010 | Workflow runs and state-transition events. |
| `mcp_gateway_service` | 8011 | MCP-style HTTP tools proxying to the services above. |
| `sap_execution_service` | 8100 | SAP Execution bounded context: packages, transports, generated objects (ABAP/RAP/CDS/OData), activation, ATC orchestration + remediation, unit testing, SAP Solution Architect Agent planning. |

## Architecture

Each of the first 10 services follows the same layout:

```
<service>/
├── app/
│   ├── main.py            # FastAPI app, router registration, health check
│   ├── core/config.py     # Pydantic settings (env-driven)
│   ├── db/base.py         # SQLAlchemy engine/session/Base
│   ├── db/models.py       # SQLAlchemy ORM models
│   ├── schemas/           # Pydantic Create/Update/Read schemas
│   └── api/v1/routes.py   # CRUD API endpoints
├── alembic/                # Migrations (versions/, env.py)
├── tests/{unit,integration}/
├── Dockerfile
├── docker-entrypoint.sh    # Runs `alembic upgrade head` then starts uvicorn
└── requirements*.txt
```

`mcp_gateway_service` has no database of its own; it proxies MCP tool
calls (`search_documents`, `get_transcript`, `get_fs`, `get_ts`,
`get_workflow_state`, `submit_review_decision`, ...) to the other
services over HTTP, per
[11-mcp-integration-architecture.md](../docs/architecture/11-mcp-integration-architecture.md).
Its dynamic SAP Execution MCP tools (`create_package`, `create_transport`,
`generate_object`/`generate_rap`/`generate_cds`/`generate_odata`,
`activate_object`, `run_atc`, `remediate_atc_findings`,
`run_unit_tests`) are backed by `sap_execution_service` — see that
service's [README](sap_execution_service/README.md).

## Running locally

Each service can run standalone against SQLite:

```bash
cd services/transcript_service
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8001
```

Or bring up the full stack (PostgreSQL + all 11 services) with Docker
Compose from the repository root:

```bash
cd sap-ai-delivery-platform
docker compose up --build
```

## Tests

```bash
cd services/<service>
pip install -r requirements-dev.txt
pytest
```

## OpenAPI documentation

Every service serves interactive docs at `/docs` and its raw schema at
`/openapi.json` once running. Static copies of each service's schema are
exported to
[`docs/architecture/openapi/services/`](../docs/architecture/openapi/services)
via:

```bash
./scripts/export_openapi.sh
```

## Migrations

```bash
cd services/<service>
alembic upgrade head          # apply
alembic revision --autogenerate -m "message"   # create a new migration
```
