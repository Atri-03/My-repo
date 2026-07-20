# 4. Domain Model

PlantUML source: [`diagrams/domain-model.puml`](diagrams/domain-model.puml).

```plantuml
@startuml
!include diagrams/domain-model.puml
@enduml
```

## 4.1 Aggregates

| Aggregate Root | Members | Invariants |
|---|---|---|
| `Tenant` | `Project`, `KnowledgeSource` | Every child entity carries `tenant_id`; cross-tenant reads are forbidden at the query-builder level |
| `RequirementSet` | `Requirement`, `Entity_`, `BusinessRule`, `Risk` | Immutable once a `FunctionalSpecification` referencing it is approved; a new version is created for changes |
| `FunctionalSpecification` | version chain via `parentVersionId` | Cannot transition to `APPROVED` without a `ReviewDecision` of `APPROVE` on its Gate 1 `ReviewCycle` |
| `TechnicalSpecification` | version chain via `parentVersionId` | Cannot transition to `APPROVED` without a `ReviewDecision` of `APPROVE` on its Gate 2 `ReviewCycle`; requires an approved `FunctionalSpecification` |
| `SapExecutionPackage` | payload snapshot | Immutable once `PUBLISHED`; always references exactly one approved `TechnicalSpecification` version |
| `WorkflowRun` | `WorkflowEvent` (append-only) | State transitions follow the finite state machine in §5; no state may be skipped |

## 4.2 Core Enumerations

- `RequirementType`: `FUNCTIONAL`, `NON_FUNCTIONAL`, `ASSUMPTION`, `DEPENDENCY`
- `ArtefactType`: `FUNCTIONAL_SPECIFICATION`, `TECHNICAL_SPECIFICATION`
- `ReviewGate`: `GATE_1_FS`, `GATE_2_TS`
- `ReviewStatus` / `DecisionType`: `PENDING`, `APPROVED`, `REJECTED`, `CHANGES_REQUESTED`
- `DocumentStatus`: `DRAFT`, `IN_REVIEW`, `APPROVED`, `REJECTED`, `SUPERSEDED`
- `PackageStatus`: `DRAFT`, `VALIDATED`, `PUBLISHED`, `ACKNOWLEDGED`, `FAILED`
- `WorkflowState`: `INGESTED` → `REQUIREMENTS_EXTRACTED` → `FS_DRAFTED` →
  `FS_IN_REVIEW` → `FS_APPROVED` → `TS_DRAFTED` → `TS_IN_REVIEW` →
  `TS_APPROVED` → `PACKAGE_PUBLISHED` → `COMPLETED` (with `REGENERATING`
  sub-states re-entering `FS_DRAFTED`/`TS_DRAFTED` on rejection)
- `TenantTier`: `SHARED`, `DEDICATED`
- `KnowledgeSourceType`: `PAST_FS`, `PAST_TS`, `PAST_BRD`, `PAST_PROJECT`,
  `CODING_STANDARD`, `ARCHITECTURE_STANDARD`, `NAMING_STANDARD`,
  `SAP_STANDARD`, `REVIEW_HISTORY`, `ATC_HISTORY`, `LESSON_LEARNED`

## 4.3 Versioning & Traceability Rules

1. Every `FunctionalSpecification` and `TechnicalSpecification` row is
   append-only; regeneration always creates a new row with
   `parentVersionId` pointing at the prior version and `version = parent.version + 1`.
2. `ReviewComment` and `ReviewDecision` rows are never deleted or mutated;
   corrections are recorded as new rows.
3. `AuditLogEntry` captures a before/after snapshot for every mutation to a
   governed entity (`RequirementSet`, `FunctionalSpecification`,
   `TechnicalSpecification`, `ReviewCycle`, `SapExecutionPackage`), enabling
   full reconstruction of decision history per the audit requirements.
4. `SapExecutionPackage.payload` is a point-in-time immutable snapshot of
   the approved `TechnicalSpecification` plus the originating
   `RequirementSet` and `FunctionalSpecification` references — the
   downstream SAP Execution Repository never needs to re-query this
   platform to know what was approved.
