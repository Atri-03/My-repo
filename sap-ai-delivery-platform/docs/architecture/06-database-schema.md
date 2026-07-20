# 6. Database Schema

PostgreSQL DDL: [`sql/schema.sql`](sql/schema.sql).
ER diagram source: [`diagrams/er-diagram.puml`](diagrams/er-diagram.puml).

```plantuml
@startuml
!include diagrams/er-diagram.puml
@enduml
```

## 6.1 Design Principles

- **Tenant isolation at the row level**: every table (directly or via a
  parent FK chain) carries `tenant_id`; all repository queries are built
  through a tenant-scoped session helper that injects a `WHERE tenant_id = :tenant_id`
  predicate, preventing accidental cross-tenant leakage.
- **Append-only governance tables**: `workflow_event` and `audit_log_entry`
  are `INSERT`-only, range-partitioned by `occurred_at`, matching the
  scale requirement of millions of documents/events. Partition maintenance
  is automated with `pg_partman` (monthly partitions, configurable
  retention/archival to Blob via Azure Data Factory — see
  [Azure Deployment Architecture](10-azure-deployment-architecture.md)).
- **Version chains, never mutation**: `functional_specification` and
  `technical_specification` are never updated in place after creation;
  regeneration inserts a new row with `parent_version_id` set, preserving
  full history for traceability and audit.
- **Vectors live in Azure AI Search, not PostgreSQL**: `knowledge_chunk`
  stores the chunk text and a `vector_id` foreign reference into the
  Azure AI Search index — PostgreSQL remains the transactional system of
  record while Search owns retrieval performance at scale (see
  [RAG Architecture](09-rag-architecture.md)).
- **Templates and prompts are versioned, tenant-scoped configuration**,
  editable via the Prompt Management / Configuration Management UI screens
  without a code deployment.

## 6.2 Table Summary

| Table | Purpose | Growth Profile |
|---|---|---|
| `tenant`, `tenant_config`, `project` | Tenant registry & per-tenant Azure AI Foundry/Search config | Low |
| `source_document`, `transcript` | Ingested raw content and parsed structure | High (millions) |
| `requirement_set`, `requirement`, `requirement_risk`, `requirement_entity`, `business_rule` | Extracted requirements | High |
| `document_template` | Versioned FS/TS templates | Low |
| `functional_specification`, `technical_specification` | Versioned generated specs | High |
| `review_cycle`, `review_comment`, `review_decision` | Governance/review trail | High |
| `sap_execution_package` | Handoff artefact to SAP Execution Repository | Medium |
| `workflow_run`, `workflow_event` | Workflow state + append-only transitions | Very high (partitioned) |
| `audit_log_entry` | Immutable audit ledger | Very high (partitioned) |
| `knowledge_source`, `knowledge_chunk` | RAG source registry + chunk metadata | Very high |
| `prompt_template` | Versioned per-agent prompts | Low |

## 6.3 Indexing Strategy

- Every FK used in hot-path lookups (e.g., `requirement_set_id`,
  `functional_specification_id`, `review_cycle_id`) has a supporting
  B-tree index.
- `(tenant_id, created_at DESC)`/`(tenant_id, started_at DESC)` composite
  indexes support the Dashboard/Queue screens' "recent items per tenant"
  queries without full scans.
- JSONB columns (`content`, `payload`, `attributes`) use GIN indexes where
  ad-hoc filtering on generated content is required (added via migration
  once concrete query patterns from Phase 2 UI are confirmed).
