# SAP AI Delivery Platform

The SAP AI Delivery Platform converts Microsoft Teams meeting transcripts and
BRD discussions into SAP-ready deliverables (Functional Specifications,
Technical Specifications, SAP Execution Packages) with full traceability and
governance.

This repository is the **orchestration layer**. It does **not** create SAP
objects directly — implementation objects are created by a separate
**SAP Execution Repository** that consumes the SAP Execution Package produced
here.

## Phase 1 Status

Phase 1 delivers the complete solution architecture for the platform. All
architecture artefacts are under [`docs/architecture/`](docs/architecture/README.md):

- Solution architecture
- C4 diagrams (Context, Container, Component)
- Repository structure
- Domain model
- Agent interaction model
- Database schema
- API contract definitions (OpenAPI)
- UI wireframes
- RAG architecture
- Azure deployment architecture
- MCP integration architecture
- End-to-end sequence diagrams

## Phase 2 Status

Phase 2 delivers the production-ready backend: 11 independent FastAPI
microservices (SQLAlchemy models, Alembic migrations, Pydantic schemas,
CRUD API endpoints, Dockerfiles, unit + integration tests) plus a root
`docker-compose.yml`. See [`services/README.md`](services/README.md) for
details, and [`docs/architecture/openapi/services/`](docs/architecture/openapi/services)
for the generated OpenAPI schema of every service.

## Phase 3 Status

Phase 3 delivers the production frontend: a React + TypeScript + Fluent UI
single-page application (`frontend/`) with 13 pages — Dashboard, Transcript
Queue, Requirement View, FS Review, TS Review, RAG Search, Knowledge
Explorer, Audit Dashboard, Workflow Monitor, Agent Monitor, MCP Monitor,
Configuration and Administration — each wired to the Phase 2 backend
microservices via typed API clients, plus a Vitest/React Testing
Library/MSW test suite. See [`frontend/README.md`](frontend/README.md) for
details.

## Repository Layout

```
sap-ai-delivery-platform/
├── backend/          FastAPI orchestration API, workflow engine, audit service
├── services/          Phase 2: 11 independent FastAPI microservices (see services/README.md)
├── agents/            Semantic Kernel agent implementations
├── frontend/          React + TypeScript + Fluent UI application
├── mcp/                MCP servers exposing platform + SAP execution capabilities to agents/tools
├── shared/             Shared contracts (JSON Schema/Pydantic), prompt templates
├── infra/              Bicep/Terraform IaC and deployment scripts
├── docker-compose.yml  Brings up PostgreSQL + all 11 backend microservices
└── docs/architecture/  Phase 1 architecture artefacts (this phase's deliverables)
```

See [`docs/architecture/03-repository-structure.md`](docs/architecture/03-repository-structure.md)
for the full annotated repository structure.
