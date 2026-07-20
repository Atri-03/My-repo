# 2. C4 Diagrams

PlantUML sources: [`diagrams/c4-context.puml`](diagrams/c4-context.puml),
[`diagrams/c4-container.puml`](diagrams/c4-container.puml),
[`diagrams/c4-component-agents.puml`](diagrams/c4-component-agents.puml).

## 2.1 Level 1 — System Context

Actors: Business Analyst/SME, Reviewer/Approver, SAP Architect/Developer,
Platform Admin.

External systems: Microsoft Teams, SharePoint Online, OneDrive, Microsoft
Entra ID, Azure AI Foundry (GPT-5.5), and Azure AI Search. The
**SAP Execution bounded context** (`services/sap_execution_service`) is
an in-repository component, not an external system.

```plantuml
@startuml
!include diagrams/c4-context.puml
@enduml
```

Key relationships:
- The platform reads transcripts/documents from Teams, SharePoint and
  OneDrive via Microsoft Graph.
- The platform authenticates all users through Entra ID.
- The platform calls Azure AI Foundry for GPT-5.5 chat completion/embeddings
  and Azure AI Search for retrieval-augmented generation.
- On approval of the Technical Specification, the platform publishes a
  versioned **SAP Execution Package** to the external SAP Execution
  Repository. This platform never connects directly to an SAP system.

## 2.2 Level 2 — Container Diagram

```plantuml
@startuml
!include diagrams/c4-container.puml
@enduml
```

Containers:

| Container | Technology | Responsibility |
|---|---|---|
| Web Application | React, TypeScript, Fluent UI | All UI screens (§8) |
| Orchestration API | FastAPI | REST/WebSocket surface, tenant/RBAC enforcement, audit writes |
| Orchestrator Agent | Semantic Kernel Process Framework | Workflow state machine driving all agents |
| Agent Runtime | Semantic Kernel plugins | Transcript/Requirement/FS/Review/TS/Knowledge agents |
| MCP Servers | Python MCP SDK | Tool surface for search/artefact/workflow, reusable by IDE agents |
| Operational Database | Azure Database for PostgreSQL | System of record for all structured/audit data |
| Artefact Store | Azure Blob Storage | Raw transcripts, generated DOCX/PDF, execution packages |
| Ingestion & Indexing Workers | Python (Azure Functions/Container Apps Jobs) | Graph connectors, chunking, embeddings, Search index writes |
| Message Bus | Azure Service Bus | Decouples ingestion, workflow transitions, regeneration requests |

## 2.3 Level 3 — Component Diagram (Agent Runtime)

```plantuml
@startuml
!include diagrams/c4-component-agents.puml
@enduml
```

The Orchestrator Agent's **Workflow Process** (a Semantic Kernel Process
Framework state machine) drives a **Step Router** that invokes the
appropriate agent plugin for the current workflow state. Each agent plugin
is independently testable, uses the **Template Store** for FS/TS templates,
the **MCP Tool Client** for retrieval/artefact/workflow tool calls, and
**Azure Key Vault** (via Managed Identity) for credential resolution — no
credentials are embedded in agent code or configuration.

## 2.4 Level 4 — Code (representative)

Code-level detail is intentionally deferred to source code and inline
docstrings under `agents/*/`, `backend/app/*`, and `frontend/src/*`, per C4
guidance that Level 4 is optional and best expressed as IDE-navigable code
rather than a diagram maintained separately from the implementation.
