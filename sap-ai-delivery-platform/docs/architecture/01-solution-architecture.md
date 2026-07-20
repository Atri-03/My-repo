# 1. Solution Architecture

## 1.1 Purpose and Scope

The **SAP AI Delivery Platform** is the orchestration and AI-authoring layer
that converts Microsoft Teams meeting transcripts and Business Requirement
Documents (BRDs) into governed SAP delivery artefacts:

```
Transcript → Requirement Extraction → Functional Specification → Review Gate 1
           → Technical Specification → Review Gate 2 → SAP Execution Package
```

This repository owns the full lifecycle end to end, including SAP
Execution: the SAP Execution Package is handed off to the **SAP Execution
bounded context** — `services/sap_execution_service` — which is part of
this repository (not a separate repository) and performs
ABAP/CDS/RAP/OData object generation, package/transport management, ATC
orchestration + remediation, unit testing, and activation via the SAP
Execution MCP tools already exposed by `mcp_gateway_service`. Live
connectivity to a real SAP system (ADT REST calls) is provided by
`abap_rag_pipeline` today and is intended to be integrated behind
`sap_execution_service` rather than duplicated.

## 1.2 Architectural Drivers

| Driver | Requirement | Architectural Response |
|---|---|---|
| Scale | Millions of documents (transcripts, FS/TS versions, RAG corpus) | Azure AI Search (partitioned indexes), PostgreSQL with partitioned audit/version tables, Blob Storage for binary artefacts, async workers for ingestion |
| Multi-tenancy | Multiple SAP customers/business units on shared infrastructure | Tenant Id on every row and search document, per-tenant RBAC via Entra ID app roles/groups, per-tenant Key Vault secret namespace, tenant-scoped Azure AI Search indexes (or index-per-large-tenant) |
| AI | Azure AI Foundry, GPT-5.5 | Semantic Kernel `AzureAIInferenceChatCompletion`/`AzureOpenAIChatCompletion` connector configured against Foundry project endpoint + deployment name, model-agnostic prompt templates |
| Ingestion | SharePoint, OneDrive, Teams transcripts | Microsoft Graph API connectors (change notifications/webhooks + delta query polling fallback) |
| Orchestration | Semantic Kernel | Kernel per tenant/session, plugins per agent, planner-driven or explicit process (Semantic Kernel Process Framework) state machine |
| API | FastAPI | Async, OpenAPI-first, versioned `/api/v1` |
| Frontend | React + Fluent UI | SPA, MSAL.js for Entra ID auth, Fluent UI v9 (React) component library |
| Data | PostgreSQL | Azure Database for PostgreSQL Flexible Server, partitioned by tenant_id + created_at for audit/version-heavy tables |
| Search | Azure AI Search | Hybrid (BM25 + vector) + semantic reranking, metadata filters, vector fields via `text-embedding-3-large` |
| Governance | Full traceability | Immutable audit ledger (append-only table + event stream), version chain (parent_version_id) on every generated artefact |
| Tool integration | MCP | MCP servers exposing platform capabilities (search, workflow, artefact retrieval) to IDE agents and the Orchestrator Agent's tool-calling surface |

## 1.3 Logical Architecture (Layered View)

```
┌───────────────────────────────────────────────────────────────────────┐
│  Presentation Layer                                                    │
│  React + TypeScript + Fluent UI SPA  (MSAL.js / Entra ID)              │
└───────────────────────────────────────────────────────────────────────┘
                         │ HTTPS / REST + WebSocket (SignalR-style)
┌───────────────────────────────────────────────────────────────────────┐
│  API Layer — FastAPI                                                   │
│  Routers: transcripts, requirements, fs, ts, reviews, workflows,        │
│  knowledge, audit, prompts, config, admin                              │
│  Cross-cutting: Entra ID JWT validation, tenant resolution, rate limit  │
└───────────────────────────────────────────────────────────────────────┘
                         │
┌───────────────────────────────────────────────────────────────────────┐
│  Orchestration Layer — Semantic Kernel                                  │
│  Orchestrator Agent (Process Framework state machine)                  │
│  ├─ Transcript Agent   ├─ Requirement Agent   ├─ FS Agent               │
│  ├─ Review Agent       ├─ TS Agent            └─ Knowledge Agent (RAG)  │
│  Tool-calling via MCP servers (search, artefact-store, sap-execution)   │
└───────────────────────────────────────────────────────────────────────┘
         │                          │                         │
┌────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐
│ Ingestion Layer     │  │ Knowledge/RAG Layer    │  │ Persistence Layer      │
│ MS Graph connectors │  │ Azure AI Search        │  │ PostgreSQL (OLTP)      │
│ (SharePoint,        │  │ (hybrid/semantic/      │  │ Blob Storage           │
│ OneDrive, Teams)    │  │ vector, metadata,      │  │ (artefacts, transcripts)│
│ Event Grid / Queue  │  │ lineage, versioning)   │  │ Event Hub (audit sink) │
└────────────────────┘  └───────────────────────┘  └───────────────────────┘
                         │
┌───────────────────────────────────────────────────────────────────────┐
│  AI Model Layer — Azure AI Foundry (GPT-5.5)                            │
│  Foundry Project → Deployment → Model; Managed Identity auth            │
└───────────────────────────────────────────────────────────────────────┘
                         │
┌───────────────────────────────────────────────────────────────────────┐
│  SAP Execution Bounded Context — sap_execution_service (in-repo)       │
│  Packages/Transports · Generator Orchestrator (ABAP/RAP/CDS/OData)     │
│  Activation Engine · ATC Orchestration · Remediation Engine            │
│  SAP Solution Architect Agent (execution planning)                     │
└───────────────────────────────────────────────────────────────────────┘
```

## 1.4 Multi-Tenancy Model

- **Isolation strategy**: pooled compute (shared FastAPI/Agent containers),
  siloed data at the row level (`tenant_id` on every table) plus siloed
  secrets (per-tenant Key Vault secret prefix `tenant/{tenant_id}/...`).
- **Large tenants** may be promoted to a dedicated Azure AI Search index and
  a dedicated PostgreSQL schema (`tenant_<id>`) via the same codebase —
  selected by a `TenantTier` (`shared` | `dedicated`) flag in the tenant
  registry.
- **Entra ID**: platform is registered as a multi-tenant (or CIAM) app;
  tenant resolution is derived from the authenticated user's Entra tenant
  ID or an explicit `X-Tenant-Id` claim mapped in the tenant registry.
- Every Semantic Kernel invocation, Azure AI Search query, and audit record
  carries `tenant_id` end to end.

## 1.5 Scale Model (Millions of Documents)

| Concern | Approach |
|---|---|
| Ingestion throughput | Queue-based (Azure Service Bus) decoupling of Graph webhook receipt from processing; horizontally scaled worker pool (KEDA autoscaling on queue depth) |
| Search index size | Azure AI Search partitioned by tenant + document type; index rotation/archival policy for cold BRD/FS/TS versions (> N years) moved to a "cold" index or Blob-only with re-index-on-demand |
| Relational data growth | PostgreSQL native partitioning (`PARTITION BY RANGE (created_at)`) on `audit_log`, `document_version`, `workflow_event`; monthly partitions with automated retention/archival to Blob (Parquet) via `pg_partman` + Azure Data Factory |
| Binary artefacts | Azure Blob Storage (hot tier) with lifecycle policies to cool/archive tiers |
| Read scaling | PostgreSQL read replicas for reporting/audit dashboards; Redis cache for hot workflow state and prompt/template lookups |
| Vector embeddings | Batched embedding generation via Azure AI Foundry embedding deployment, written asynchronously to Azure AI Search vector fields |

## 1.6 Quality Attributes

- **Traceability**: every artefact (Requirement, FS, TS, Execution Package)
  has an immutable version chain and links back to its source transcript(s)
  and the review decisions that approved it.
- **Governance**: five mandatory human review gates (Gate 1 business
  approval of FS, Gate 2 architect approval of TS, Gate 3 developer
  approval of SAP design, Gate 4 developer approval before object
  creation, Gate 5 lead approval before activation); no artefact is
  activated in SAP without all applicable gates recorded in the audit
  ledger (`approval_service`).
- **Security**: Entra ID (OIDC/OAuth2) for user auth, Managed Identity for
  service-to-service (Key Vault, Azure AI Search, Azure AI Foundry, Storage),
  no credentials in source or config files.
- **Resilience**: idempotent workflow steps, retry with exponential backoff
  on Graph/Foundry/Search calls, dead-letter queues for poison messages,
  self-healing regeneration loop bounded by a max-retry policy with
  escalation to human intervention.
- **Observability**: OpenTelemetry traces across API → Orchestrator →
  Agents → external services; Azure Monitor/Application Insights dashboards
  correlated by `correlation_id`/`workflow_run_id`.

## 1.7 Related Documents

- [C4 Diagrams](02-c4-diagrams.md)
- [Repository Structure](03-repository-structure.md)
- [Domain Model](04-domain-model.md)
- [Agent Interaction Model](05-agent-interaction-model.md)
- [Database Schema](06-database-schema.md)
- [API Contract Definitions](07-api-contracts.md)
- [UI Wireframes](08-ui-wireframes.md)
- [RAG Architecture](09-rag-architecture.md)
- [Azure Deployment Architecture](10-azure-deployment-architecture.md)
- [MCP Integration Architecture](11-mcp-integration-architecture.md)
- [Sequence Diagrams](12-sequence-diagrams.md)
