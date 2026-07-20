# 7. API Contract Definitions

OpenAPI 3.1 specification: [`openapi/openapi.yaml`](openapi/openapi.yaml).

## 7.1 Conventions

- **Versioning**: all routes are prefixed `/api/v1`; breaking changes ship
  as `/api/v2` alongside the previous version until deprecated.
- **Tenancy**: every request requires the `X-Tenant-Id` header (resolved
  from the authenticated Entra ID user by the frontend) in addition to the
  bearer token; the API layer cross-validates the header tenant against
  the token's tenant claim/role assignment and rejects mismatches with
  `403`.
- **AuthN/AuthZ**: `Authorization: ****** ID JWT>` on every request;
  role-based authorization (`Reviewer`, `Approver`, `Admin`, `Contributor`)
  enforced via FastAPI dependencies reading Entra ID app roles from the
  token.
- **Async operations**: long-running operations (transcript upload/parse,
  FS/TS generation, regeneration) return `202 Accepted` with a resource
  reference; clients poll the resource or subscribe via the WebSocket
  channel (`/ws/v1/workflows/{workflowRunId}`) for state-change pushes
  used by the Workflow Monitoring screen.
- **Pagination**: `page`/`pageSize` query parameters on all list endpoints,
  capped at `pageSize=200`.
- **Errors**: RFC 7807 `application/problem+json` error bodies
  (`type`, `title`, `status`, `detail`, `instance`), not shown in the
  OpenAPI document above for brevity but implemented uniformly via a
  FastAPI exception handler.

## 7.2 Endpoint Groups

| Group | Base Path | Backing Screens |
|---|---|---|
| Transcripts | `/transcripts` | Transcript Queue, Dashboard |
| Requirements | `/requirement-sets` | Requirements Screen |
| Functional Specifications | `/functional-specifications` | FS Screen, Version Management |
| Technical Specifications | `/technical-specifications` | TS Screen, Version Management |
| Reviews | `/reviews` | Review Screen, Approval Screen |
| Workflows | `/workflows` | Workflow Monitoring, Agent Monitoring |
| Knowledge | `/knowledge` | RAG Search Screen, Knowledge Management |
| Audit | `/audit` | Audit Dashboard |
| Prompts | `/prompts` | Prompt Management |
| Config | `/config` | Configuration Management |
| Admin | `/admin` | Admin Portal |

## 7.3 WebSocket / Real-Time Channel

`/ws/v1/workflows/{workflowRunId}` streams `WorkflowEvent` push
notifications so the Workflow Monitoring and Agent Monitoring screens
update live as the Orchestrator Agent progresses a run, without polling.
Backed by FastAPI `WebSocket` routes fed from the same Service Bus topic
consumed by the Orchestrator (fan-out via a lightweight pub/sub layer,
e.g., Azure Web PubSub, to support horizontal API scale-out).

## 7.4 SAP Execution Package Handoff Contract

The `SapExecutionPackage.payload` (persisted per §6, published once Gate 2
is approved) is the formal, versioned interface to the external SAP
Execution Repository. Its JSON Schema is defined in
`shared/contracts/sap_execution_package.schema.json` (Phase 2 deliverable)
and includes: originating tenant/project identifiers, the full approved
Technical Specification content (architecture, data model, CDS/RAP/OData
design, security, integration), the approved Functional Specification and
Requirement Set references, and the complete review/approval trail
required for the downstream repository to prove governance compliance
before creating any SAP object.
