# 3. Repository Structure

The platform is a monorepo rooted at `sap-ai-delivery-platform/`.

```
sap-ai-delivery-platform/
├── README.md
├── backend/                          FastAPI orchestration API
│   ├── app/
│   │   ├── main.py                   App factory, router registration, middleware
│   │   ├── api/                      Versioned routers
│   │   │   └── v1/
│   │   │       ├── transcripts.py
│   │   │       ├── requirements.py
│   │   │       ├── fs.py
│   │   │       ├── ts.py
│   │   │       ├── reviews.py
│   │   │       ├── workflows.py
│   │   │       ├── knowledge.py
│   │   │       ├── audit.py
│   │   │       ├── prompts.py
│   │   │       ├── config.py
│   │   │       └── admin.py
│   │   ├── core/                     Settings, security (Entra ID JWT), tenancy, telemetry
│   │   ├── db/                       SQLAlchemy models, Alembic migrations, session management
│   │   ├── schemas/                  Pydantic request/response models (mirrors shared/contracts)
│   │   ├── services/                 Business logic: workflow engine, audit service, template service
│   │   └── workers/                  Background task entrypoints (Service Bus consumers)
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   ├── alembic/
│   ├── pyproject.toml
│   └── Dockerfile
├── agents/                           Semantic Kernel agents (one package per agent)
│   ├── orchestrator_agent/           Process Framework state machine + step router
│   ├── transcript_agent/             Parsers: transcript/MOM/BRD/PDF/DOCX/TXT/HTML
│   ├── requirement_agent/            FR/NFR/assumptions/dependencies/risks/entities extraction
│   ├── fs_agent/                     FS generation, templating, versioning
│   ├── review_agent/                 Approval/rejection/comment workflow, regeneration triggers
│   ├── ts_agent/                     Architecture/data model/CDS/RAP/OData/security/integration design
│   ├── knowledge_agent/              Enterprise RAG plugin (Azure AI Search client)
│   └── tests/
│       ├── unit/
│       └── agent/                    Agent-level behavioural tests (prompt + mocked model)
├── frontend/                         React + TypeScript + Fluent UI SPA
│   ├── src/
│   │   ├── pages/                    Dashboard, TranscriptQueue, Requirements, FS, TS, Review,
│   │   │                             Approval, RagSearch, KnowledgeManagement, AgentMonitoring,
│   │   │                             AuditDashboard, PromptManagement, ConfigurationManagement,
│   │   │                             WorkflowMonitoring, VersionManagement, ErrorMonitoring, Admin
│   │   ├── components/               Shared Fluent UI components
│   │   ├── api/                      Generated/typed API client (from OpenAPI)
│   │   ├── hooks/                    Data-fetching and auth hooks
│   │   ├── store/                    Client state (React Query + Zustand/Redux Toolkit)
│   │   └── theme/                    Fluent UI theme tokens
│   ├── tests/                        Vitest + React Testing Library
│   ├── e2e/                          Playwright end-to-end tests
│   ├── package.json
│   └── Dockerfile
├── mcp/                               MCP servers exposing platform capabilities as tools
│   └── servers/
│       ├── knowledge_search_server/  search_documents, get_lineage, list_sources
│       ├── artefact_server/          get_fs, get_ts, get_transcript, list_versions
│       └── workflow_server/          get_workflow_state, submit_review_decision
├── shared/                            Cross-cutting shared code (Python + TS)
│   ├── contracts/                    JSON Schema / Pydantic models for SAP Execution Package,
│   │                                 Requirement, FS, TS — versioned, consumed by backend, agents,
│   │                                 frontend (via codegen) and the external SAP Execution Repository
│   └── prompts/                      Versioned prompt templates (system/user) per agent
├── infra/                             Infrastructure as Code
│   ├── bicep/                        Azure resource definitions (modular, per environment)
│   ├── terraform/                    Alternative/complementary IaC (state-managed) if required
│   └── scripts/                      Deployment, migration, seed scripts
├── docs/
│   ├── architecture/                 Phase 1 deliverables (this document set)
│   ├── operations-guide.md           (Phase 2+)
│   ├── admin-guide.md                (Phase 2+)
│   └── developer-guide.md            (Phase 2+)
└── .github/workflows/                CI: lint, build, unit/integration/agent tests, IaC validation
```

## 3.1 Design Rationale

- **Agent isolation**: each agent is an independently deployable/testable
  Python package under `agents/`, imported by the Orchestrator via a stable
  plugin interface (`KernelPlugin`), enabling independent versioning and
  agent-level test suites (`agents/tests/agent/`).
- **Shared contracts**: `shared/contracts/` is the single source of truth
  for cross-boundary payloads (Requirement, FS, TS, SAP Execution Package).
  Both the FastAPI backend and the frontend (via OpenAPI-generated types)
  consume the same contract, preventing drift.
- **MCP as a first-class boundary**: `mcp/servers/` exposes read/query
  tools (knowledge search, artefact retrieval, workflow state) using the
  Model Context Protocol so that both the platform's own Orchestrator Agent
  and external IDE-based coding agents (e.g., working in the SAP Execution
  Repository) can query platform state consistently. See
  [MCP Integration Architecture](11-mcp-integration-architecture.md).
- **Infra as code**: all Azure resources are declared in `infra/bicep`
  (primary) with environment-specific parameter files
  (`main.dev.bicepparam`, `main.prod.bicepparam`), enabling repeatable
  multi-tenant environment provisioning.
- **Tests colocated with owning module**: unit tests sit beside the code
  they test; integration and agent tests are grouped so CI can run them as
  separate, independently-gated jobs (see Quality/Testing strategy in
  the operations guide, Phase 2).
