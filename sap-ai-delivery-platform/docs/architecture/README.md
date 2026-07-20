# Architecture Documentation Index

Phase 1 deliverables for the **SAP AI Delivery Platform**.

| # | Document | Description |
|---|----------|-------------|
| 1 | [Solution Architecture](01-solution-architecture.md) | End-to-end architecture, quality attributes, tenancy, scale model |
| 2 | [C4 Diagrams](02-c4-diagrams.md) | Context, Container, and Component views |
| 3 | [Repository Structure](03-repository-structure.md) | Annotated monorepo layout |
| 4 | [Domain Model](04-domain-model.md) | Core entities, aggregates, invariants |
| 5 | [Agent Interaction Model](05-agent-interaction-model.md) | Semantic Kernel agent roles, plugins, orchestration |
| 6 | [Database Schema](06-database-schema.md) | PostgreSQL schema, DDL, ER diagram |
| 7 | [API Contract Definitions](07-api-contracts.md) | REST/WebSocket API contracts, OpenAPI spec |
| 8 | [UI Wireframes](08-ui-wireframes.md) | Screen inventory, layout, component map |
| 9 | [RAG Architecture](09-rag-architecture.md) | Azure AI Search indexing, retrieval, lineage |
| 10 | [Azure Deployment Architecture](10-azure-deployment-architecture.md) | Multi-tenant Azure topology |
| 11 | [MCP Integration Architecture](11-mcp-integration-architecture.md) | MCP servers/tools exposed to agents and IDEs |
| 12 | [Sequence Diagrams](12-sequence-diagrams.md) | End-to-end flows |

## Diagram sources

All PlantUML sources are under [`diagrams/`](diagrams/). Render with:

```bash
plantuml -tsvg docs/architecture/diagrams/*.puml
```

or paste into https://www.plantuml.com/plantuml (offline: use the `plantuml`
CLI / VS Code PlantUML extension — no external service required in CI).

## SQL and OpenAPI artefacts

- [`sql/schema.sql`](sql/schema.sql) — executable PostgreSQL DDL for the schema described in document 6.
- [`openapi/openapi.yaml`](openapi/openapi.yaml) — OpenAPI 3.1 contract described in document 7.
