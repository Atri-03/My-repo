# 9. RAG Architecture

PlantUML source: [`diagrams/rag-architecture.puml`](diagrams/rag-architecture.puml).

```plantuml
@startuml
!include diagrams/rag-architecture.puml
@enduml
```

## 9.1 Knowledge Sources

| Source Type | Ingestion Path | Update Cadence |
|---|---|---|
| Past FS / Past TS | Generated internally on approval; also bulk-imported from legacy SharePoint archives | Continuous (on approval) + one-time backfill |
| Past BRDs | SharePoint/OneDrive connector | On upload / scheduled scan |
| Past Projects | SharePoint connector (project archive libraries) | Scheduled scan |
| Coding Standards, Architecture Standards, Naming Standards, SAP Standards | SharePoint (curated standards library) | On change (Graph webhook) |
| Review History | Internal (`review_comment`, `review_decision` tables) | Continuous |
| ATC History | Uploaded/synced from SAP Execution Repository exports (out-of-band feed, format TBD with that repo's owners) | Scheduled |
| Lessons Learned | SharePoint / manual upload via Knowledge Management screen | On upload |

## 9.2 Indexing Pipeline

1. **Connector** — Microsoft Graph API delta queries + change notification
   webhooks for SharePoint/OneDrive; Teams transcript export monitoring via
   Graph `callTranscripts`/`onlineMeetings` APIs (subject to confirmed Graph
   permissions, per open questions in the solution architecture).
2. **Parsing** — reuses the Transcript Agent's document parsers
   (PDF/DOCX/TXT/HTML) to normalize content to plain text + structural
   metadata.
3. **Chunking** — semantic/recursive chunking (~500–800 tokens, ~15%
   overlap) preserving section headers as metadata for citation quality.
4. **Embedding** — Azure AI Foundry embedding deployment
   (e.g., `text-embedding-3-large`) generates vectors per chunk, batched for
   throughput.
5. **Indexing** — each chunk is upserted into Azure AI Search as a document
   with: `tenantId`, `sourceType`, `sourceUri`, `version`, `chunkText`,
   `contentVector`, `lastIndexedAt`, `lineage` (source document + parent
   version chain), `isDeadLink`.
6. **Dead link detection** — a scheduled worker re-validates `sourceUri`
   reachability (HTTP HEAD/Graph metadata check) and flags
   `is_dead_link = true`, surfaced on the Knowledge Management screen for
   remediation rather than silently serving stale citations.
7. **Lineage tracking** — every indexed chunk retains a pointer back to its
   `knowledge_source` row (and, for internally generated FS/TS, to the
   specific version), so a RAG citation can always be traced to an exact
   source and version.

## 9.3 Retrieval Strategy

- **Hybrid search**: BM25 keyword search combined with vector similarity
  (Azure AI Search hybrid query), re-ranked by the **Semantic Ranker** for
  relevance.
- **Metadata filtering**: every query is scoped by `tenantId` (mandatory)
  and optionally `sourceType`, `version`, date range — enforced server-side
  in the Knowledge Agent, never left to client-supplied filters alone.
- **Multi-tenancy in Search**: shared tenants use a single index with a
  mandatory `tenantId` filter; `DEDICATED` tier tenants (per Tenant.tier)
  are provisioned a dedicated index (`idx-{tenantId}-knowledge`) for
  stronger isolation and independent scaling.
- **Citation-first responses**: the Knowledge Agent always returns
  `sourceUri`, `sourceType`, and a relevance score alongside chunk text so
  FS/TS Agents (and the RAG Search UI) can render verifiable citations
  rather than unattributed generated text.

## 9.4 Scale Considerations (Millions of Documents)

- Azure AI Search partitions/replicas sized per tenant tier; `SHARED` tier
  tenants share partitions with quota-based throttling, `DEDICATED` tenants
  receive dedicated partitions.
- Cold/rarely-accessed knowledge (e.g., FS/TS versions superseded > 2 years)
  is moved to a lower-cost "archive" index or dropped from the vector index
  entirely (kept queryable via keyword-only search against Blob-stored
  text) to bound index size while retaining traceability through
  PostgreSQL's `knowledge_source`/`knowledge_chunk` metadata.
- Indexing is fully asynchronous (Service Bus-triggered workers) so
  ingestion spikes (e.g., bulk BRD archive import) never block the
  interactive workflow.

## 9.5 Governance

- **Version tracking**: `knowledge_source.last_indexed_at` and the FS/TS
  version chain ensure the RAG layer always know which version of a
  document a chunk represents.
- **Access control**: Knowledge Agent queries are always tenant-scoped and
  further filtered by the requesting user's role where source sensitivity
  requires it (e.g., only Approvers can retrieve unredacted Review
  History).
