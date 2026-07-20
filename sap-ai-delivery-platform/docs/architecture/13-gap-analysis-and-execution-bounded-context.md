# 13. Gap Analysis & SAP Execution Bounded Context

## 13.1 Purpose

Per the implementation directive: **before creating any new code, services,
database entities, APIs, UI pages, workflows, or architecture documents**,
perform a repository-wide gap analysis, inventory existing capabilities,
and reuse/extend rather than duplicate. This document is that gap analysis
report, followed by the architecture decision and the implementation plan
that was executed from it.

## 13.2 Architecture Decision

> SAP Execution will be implemented as an **in-repository bounded
> context**. No separate repository is created.

```
SAP AI Delivery Platform
    ├── Existing Delivery Components   (fs_service, ts_service, transcript
    │                                   processing, requirement extraction,
    │                                   document generation)
    ├── Existing Governance Components (approval_service: 5 gates, RBAC,
    │                                   SoD, audit_service)
    ├── Existing Knowledge Brain       (knowledge_service: 12 source types,
    │                                   lineage, standards library)
    ├── Existing RAG Components        (knowledge_service search, Azure AI
    │                                   Search integration point)
    └── New Execution Bounded Context  (services/sap_execution_service +
                                        SAP Execution MCP tools already in
                                        mcp_gateway_service + frontend
                                        SapExecutionPage)
```

`services/sap_execution_service` is a new, independently deployable
microservice under the existing `services/` monorepo layout (same
conventions as `fs_service`, `ts_service`, `approval_service`, etc.) — it
is **not** a new repository, and it reuses the platform's existing
Postgres-per-service pattern, Docker Compose wiring, and CI conventions.

## 13.3 Gap Analysis Summary

Classification per requirement area, based on a full repository inventory
(`abap_rag_pipeline/`, all 11 pre-existing services under
`sap-ai-delivery-platform/services/`, and `frontend/`).

| Area | Classification | Notes |
|---|---|---|
| Governance framework (approval gates, RBAC, SoD) | **IMPLEMENTED** | `approval_service`: 5 gates defined in `app/core/gates.py`, fully wired. Reused as-is. |
| Audit framework | **IMPLEMENTED** | `audit_service` / `AuditLogEntry` pattern reused as-is; no changes made. |
| Knowledge Brain (source registry, lineage) | **IMPLEMENTED** | `knowledge_service`: 12 source types, lineage tracking. Reused as-is. |
| RAG search | **PARTIALLY IMPLEMENTED** | `search_documents` exists but returns stubbed/hardcoded relevance scores; no live Azure AI Search integration. Not addressed in this pass (out of scope for SAP Execution directive; flagged for future work). |
| MCP Discovery / MCP Registry | **IMPLEMENTED** | `mcp_gateway_service/app/mcp/registry.py` already provides dynamic tool discovery (`discover_tools()`) and category-based registration. Reused as-is; no changes made. |
| SAP Execution MCP tools (package/transport/generate/activate/ATC/remediate/unit-test) | **IMPLEMENTED (gateway side)** | 11 tools already existed in `mcp_gateway_service/app/mcp/tools/*.py`, calling `SAPExecutionClient` against a `sap-execution-service` backend that **did not exist**. This was the single largest concrete gap — the gateway layer was complete, but had nothing to call. |
| SAP Execution backend service | **NOT IMPLEMENTED** | No `sap_execution_service` existed anywhere in the repo. **Built new** (`services/sap_execution_service`), matching the exact contract already expected by `mcp_gateway_service`. |
| Execution Package Model | **PARTIALLY IMPLEMENTED** | A basic `SapExecutionPackage` model already existed in `approval_service` (governance handoff record). The new service adds the execution-side models it does not overlap with: `SapPackage`, `SapTransport`, `GeneratedObject`, `Activation`, `AtcRun`, `AtcRemediation`, `UnitTestRun`, `ExecutionPlan`. Both are kept — one is the governance artefact, the other is execution-state. |
| Package/Transport Services | **NOT IMPLEMENTED** | Built new: `SapPackage`/`SapTransport` models + `/packages`, `/transports`, `/transports/{transport_request}/release` endpoints. |
| Generator Orchestrator (ABAP/RAP/CDS/OData) | **NOT IMPLEMENTED** | Built new: unified `GeneratedObject` model (discriminated by `object_type`) + `/objects`, `/rap-business-objects`, `/cds-views`, `/odata-services` endpoints. |
| ATC Orchestration | **NOT IMPLEMENTED** | Built new: `AtcRun` model + `/atc-runs` endpoint. No live ATC connectivity exists anywhere in the repo (consistent with other services, which are metadata/state stores, not live external integrations); returns empty findings by default, documented as a future integration point. |
| Remediation Engine | **NOT IMPLEMENTED** | Built new: `AtcRemediation` model + `/atc-remediations` endpoint. |
| Activation Engine | **NOT IMPLEMENTED** | Built new: `Activation` model + `/activations` endpoint; on activation, flips the matching `GeneratedObject.status` to `ACTIVE`. |
| Unit test tracking | **NOT IMPLEMENTED** | Built new: `UnitTestRun` model + `/unit-test-runs` endpoint (backs the existing `run_unit_tests` MCP tool). |
| SAP Solution Architect Agent | **NOT IMPLEMENTED** | No Semantic Kernel `agents/` package exists anywhere in the repo (only referenced in docs). Implemented as a lightweight, deterministic rule-based planner (`POST /api/v1/architect/plans`) satisfying the existing MCP tool contract, intentionally scoped down rather than introducing a new agent framework; upgradeable later without breaking the API. |
| Execution UI | **NOT IMPLEMENTED** | Frontend previously only had a read-only `SapExecutionPackage` table inside `AdministrationPage`. Built new: `frontend/src/pages/SapExecutionPage.tsx` with dedicated sections for packages/transports, generated objects/activation, ATC runs/remediations, and execution plans, plus nav entry, route, and dashboard health monitoring. |
| ADT integration / live SAP connectivity | **PARTIALLY IMPLEMENTED (elsewhere)** | `abap_rag_pipeline` already has an ADT client for retrieval purposes. Not duplicated; `sap_execution_service` remains a metadata/state store consistent with sibling services, with ADT/live-SAP calls left as a documented future integration point rather than rebuilt here. |

## 13.4 Explicitly Not Rebuilt / Reused As-Is

Per directive item 5, the following were inventoried, confirmed to already
exist, and were **not** recreated:

- Governance framework (`approval_service` gates, RBAC, SoD)
- Approval framework (review cycles, decisions)
- Audit framework (`audit_service`, `AuditLogEntry`)
- Knowledge Brain (`knowledge_service`)
- Existing RAG services (`knowledge_service` search endpoints)
- Existing APIs (all 11 pre-existing services' REST APIs — untouched)
- Existing data models (no pre-existing model was altered or dropped)
- Existing migrations (no pre-existing Alembic migration was altered)
- Existing tests (no pre-existing test was modified or removed)
- MCP Discovery/Registry (`mcp_gateway_service/app/mcp/registry.py`)

## 13.5 Known Gaps Deliberately Left Unaddressed

Flagged during the gap analysis but out of scope for the SAP Execution
directive (not required to satisfy "MCP Discovery, MCP Registry, SAP
Solution Architect Agent, Execution Package Model, Package/Transport
Services, Generator Orchestrator, ATC Orchestration, Remediation Engine,
Activation Engine, Execution UI"):

- Governance gate sequencing is not enforced (gates can currently be
  approved out of order in `approval_service`).
- Gates 4 and 5 in `approval_service/app/core/gates.py` reference
  `entity_type: "SapObject"`, which has no corresponding model in
  `approval_service`. `sap_execution_service`'s `GeneratedObject` model is
  the natural candidate to close this gap in a future pass, but doing so
  was judged to require a cross-service governance-linking change beyond
  the scope of this directive.
- No enforcement currently links `approval_service` gate approvals to
  `sap_execution_service` actions (e.g., blocking `create_transport` or
  `activate_object` calls until Gate 4/5 are approved). Flagged for future
  work.
- `knowledge_service.search_documents` is a stub (hardcoded relevance
  score); no live Azure AI Search integration exists.

## 13.6 Backward Compatibility

- No existing service's API, database model, or migration was modified.
- No existing test was modified or removed.
- `docker-compose.yml` changes are additive (new service block, new
  `POSTGRES_MULTIPLE_DATABASES` entry, new frontend build arg) and do not
  change existing service configuration.
- `mcp_gateway_service` required no code changes — its SAP Execution tools
  already targeted the exact contract implemented by the new service.
