# 11. MCP Integration Architecture

PlantUML source: [`diagrams/mcp-integration.puml`](diagrams/mcp-integration.puml).

```plantuml
@startuml
!include diagrams/mcp-integration.puml
@enduml
```

## 11.1 Purpose

The platform exposes read/query (and a small, tightly-scoped set of
write) capabilities via the **Model Context Protocol (MCP)** so that:

1. The platform's own **Orchestrator Agent** and individual agents
   consume MCP tools in-process (stdio transport) as their primary
   integration surface for retrieval, artefact access, and workflow
   state — keeping agent code decoupled from direct database/Search SDK
   calls.
2. **External IDE-based coding agents** (e.g., a developer's Copilot/IDE
   agent, or the in-repo SAP Execution bounded context described in §11.5)
   can query this platform's knowledge and artefacts (SSE/HTTP
   transport, Entra ID-authenticated) without needing direct database
   access or bespoke API clients.

## 11.2 MCP Servers

| Server | Transport | Tools | Backing Store |
|---|---|---|---|
| Knowledge Search MCP Server | stdio (internal), SSE/HTTP (external) | `search_documents`, `get_lineage`, `list_sources`, `check_dead_links` | Azure AI Search, PostgreSQL (`knowledge_source`, `knowledge_chunk`) |
| Artefact MCP Server | stdio (internal), SSE/HTTP (external, read-only) | `get_transcript`, `get_requirement_set`, `get_fs`, `get_ts`, `list_versions` | PostgreSQL read replica, Blob Storage |
| Workflow MCP Server | stdio (internal only) | `get_workflow_state`, `submit_review_decision`, `list_active_runs` | Orchestration API (internal authenticated call) |

## 11.3 Design Principles

- **Tools, not endpoints**: each MCP tool wraps a single, well-defined
  capability with a typed schema (mirroring the OpenAPI schemas in §7),
  so the same contract underlies both the REST API and the MCP surface.
- **Tenant scoping enforced server-side**: every MCP tool call requires a
  resolved tenant context (derived from the calling agent's session for
  internal calls, or from the Entra ID token for external SSE/HTTP calls)
  — no tool accepts a client-supplied `tenantId` without validating it
  against the caller's authorized tenants.
- **Read-heavy, write-minimal surface**: only `submit_review_decision` is a
  write operation, and only via the internal Workflow MCP Server (not
  exposed externally), keeping the external-facing MCP surface safe for
  third-party IDE agents to call without governance risk.
- **External exposure is explicit and authenticated**: the Knowledge
  Search and Artefact MCP servers are exposed over SSE/HTTP only when a
  tenant explicitly enables cross-repository integration (e.g., to let the
  SAP Execution Repository's agents look up "why was this CDS view
  designed this way" by querying lineage back to the approved TS) —
  disabled by default, gated by the same Entra ID app roles as the REST
  API.
- **Consistency with Semantic Kernel**: agents register MCP servers as
  Semantic Kernel plugins via the MCP client SDK, so tool-calling from the
  LLM (GPT-5.5) uses the exact same function signatures whether invoked
  in-process or over the network.

## 11.4 Example Tool Contracts

```json
// search_documents
{
  "name": "search_documents",
  "input": {
    "query": "string",
    "sourceTypes": ["PAST_FS", "SAP_STANDARD"],
    "top": 10,
    "searchMode": "hybrid"
  },
  "output": {
    "results": [
      { "chunkId": "uuid", "sourceUri": "string", "sourceType": "string", "text": "string", "score": 0.0, "isDeadLink": false }
    ]
  }
}
```

```json
// get_ts
{
  "name": "get_ts",
  "input": { "technicalSpecificationId": "uuid" },
  "output": { "id": "uuid", "version": 1, "status": "APPROVED", "content": { "...": "..." } }
}
```

## 11.5 Relationship to the SAP Execution Bounded Context

The SAP Execution bounded context (`services/sap_execution_service`) is
implemented **in this repository**, not a separate repository. The MCP
Artefact/Knowledge servers remain the mechanism by which SAP Execution
(and any external IDE-based coding agents) retrieve the approved Technical
Specification, lineage, and applicable SAP/architecture standards while
generating SAP objects — avoiding duplication of the FS/TS content and
keeping this platform the single source of truth. SAP Execution's own
capabilities (package/transport management, ABAP/RAP/CDS/OData generation,
activation, ATC orchestration + remediation, unit testing) are exposed as
MCP tools (§11.2 dynamic registry, category `package-management` /
`transport-management` / `*-generation` / `activation` / `atc` /
`unit-testing`) backed by `sap_execution_service`.
