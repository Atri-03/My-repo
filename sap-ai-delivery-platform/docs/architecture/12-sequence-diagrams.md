# 12. End-to-End Sequence Diagrams

PlantUML sources:
[`diagrams/seq-01-ingestion-to-fs.puml`](diagrams/seq-01-ingestion-to-fs.puml),
[`diagrams/seq-02-review-gate-1.puml`](diagrams/seq-02-review-gate-1.puml),
[`diagrams/seq-03-ts-to-package.puml`](diagrams/seq-03-ts-to-package.puml).

## 12.1 Sequence 1 — Transcript Ingestion to Draft FS

```plantuml
@startuml
!include diagrams/seq-01-ingestion-to-fs.puml
@enduml
```

Covers: Graph webhook/delta-query ingestion, raw transcript persistence to
Blob + PostgreSQL, `TranscriptIngested` event publication, Orchestrator
creating the `WorkflowRun`, sequential invocation of Transcript Agent →
Requirement Agent (grounded by Knowledge Agent retrieval) → FS Agent
(grounded by Knowledge Agent retrieval of past FS/standards), ending at
`FS_DRAFTED`.

## 12.2 Sequence 2 — Review Gate 1 with Regeneration

```plantuml
@startuml
!include diagrams/seq-02-review-gate-1.puml
@enduml
```

Covers: reviewer reads the drafted FS via the UI/API, submits comments and
a `CHANGES_REQUESTED` decision, Orchestrator bounds regeneration by
`max_regeneration_attempts` (escalating to `ESCALATED` if exceeded), FS
Agent regenerates a new version referencing the prior version and review
comments, a new review cycle opens automatically, and the loop repeats
until `APPROVE` is recorded and the workflow reaches `FS_APPROVED`.

## 12.3 Sequence 3 — TS Generation, Review Gate 2, SAP Execution Package Publish

```plantuml
@startuml
!include diagrams/seq-03-ts-to-package.puml
@enduml
```

Covers: TS Agent generating architecture/data model/CDS/RAP/OData/security/
integration design grounded by Knowledge Agent retrieval of standards and
ATC history; Gate 2 review cycle (following the same approve/regenerate
pattern as Sequence 2); on approval, the Orchestrator assembles the
immutable `SapExecutionPackage` snapshot, publishes a
`SapExecutionPackageReady` event, and the MCP Artefact Server delivers the
package to the in-repo SAP Execution bounded context
(`services/sap_execution_service`, via the SAP Execution MCP tools),
recording the
acknowledgement reference before marking the workflow `COMPLETED`.

## 12.4 Cross-Cutting Notes Applicable to All Sequences

- Every state transition is persisted as an immutable `workflow_event` row
  (§4.3, §6), giving a complete, replayable history for the Audit
  Dashboard and Workflow Monitoring screens.
- Every Knowledge Agent call is tenant-scoped and returns citations,
  ensuring FS/TS content is traceable to its grounding sources (§9.3).
- All agent invocations are made exclusively by the Orchestrator Agent
  (never agent-to-agent), keeping the sequence linear, auditable, and
  simple to test in isolation (§5.1).
