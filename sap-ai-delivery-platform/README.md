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

## Repository Layout

```
sap-ai-delivery-platform/
├── backend/          FastAPI orchestration API, workflow engine, audit service
├── agents/            Semantic Kernel agent implementations
├── frontend/          React + TypeScript + Fluent UI application
├── mcp/                MCP servers exposing platform + SAP execution capabilities to agents/tools
├── shared/             Shared contracts (JSON Schema/Pydantic), prompt templates
├── infra/              Bicep/Terraform IaC and deployment scripts
└── docs/architecture/  Phase 1 architecture artefacts (this phase's deliverables)
```

See [`docs/architecture/03-repository-structure.md`](docs/architecture/03-repository-structure.md)
for the full annotated repository structure.
