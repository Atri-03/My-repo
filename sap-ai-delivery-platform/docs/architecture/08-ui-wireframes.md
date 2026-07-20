# 8. UI Wireframes

Frontend: React + TypeScript + Fluent UI v9. Global layout: left navigation
rail (Fluent `Nav`), top app bar (tenant switcher, user profile via
MSAL.js, notifications bell fed by the WebSocket channel), main content
area, and a persistent breadcrumb.

## 8.1 Screen Inventory

| Screen | Route | Primary Fluent UI Components |
|---|---|---|
| Dashboard | `/` | `Card` KPI tiles (active workflows, pending reviews, SLA breaches), `DonutChart`/`Chart` (Fluent Charts), recent activity `List` |
| Transcript Queue | `/transcripts` | `DetailsList` (status, source, ingested-at), filter `Dropdown`/`SearchBox`, upload `Button` + `Dialog` |
| Requirements Screen | `/requirements/:requirementSetId` | Tabbed `Pivot` (FR/NFR/Assumptions/Dependencies/Risks/Entities/Rules), editable `DetailsList` rows |
| FS Screen | `/fs/:fsId` | Document preview pane (rendered `content` JSON → structured sections), version `Dropdown`, "Regenerate" `Button`, diff view vs. prior version |
| TS Screen | `/ts/:tsId` | Same pattern as FS Screen, plus dedicated sub-tabs: Architecture, Data Model, CDS Design, RAP Design, OData Design, Security, Integration |
| Review Screen | `/reviews/:reviewCycleId` | Comment thread (`MessageBar`/`Persona` avatars), inline comment anchors, "Request changes" `Button` |
| Approval Screen | `/reviews/:reviewCycleId/approve` | Decision `ChoiceGroup` (Approve/Reject/Changes Requested), confirmation `Dialog`, e-signature-style approval capture |
| RAG Search Screen | `/knowledge/search` | `SearchBox` with mode toggle (Hybrid/Semantic/Vector/Keyword), source-type filter `Dropdown` (multi-select), ranked result `List` with citation + lineage `Tooltip` |
| Knowledge Management | `/knowledge/sources` | `DetailsList` of `KnowledgeSource` (type, last indexed, dead-link flag), "Re-index" `Button`, upload/connect source `Dialog` |
| Agent Monitoring | `/agents` | Per-agent status `Card` (last invocation, avg latency, error rate), live log `Panel` |
| Audit Dashboard | `/audit` | Filterable `DetailsList` (entity type/id/action/actor/time), before/after JSON diff `Dialog` |
| Prompt Management | `/prompts` | Per-agent prompt version list, Monaco-style text editor, "Activate version" `Button`, diff view |
| Configuration Management | `/config` | Form (`TextField`/`Dropdown`) for tenant Azure AI Foundry endpoint/deployment/resource/auth method, Azure AI Search bindings — secrets masked, edited via Key Vault reference only |
| Workflow Monitoring | `/workflows` | Timeline/stepper visual of `WorkflowState` per run, live updates via WebSocket, escalation banner for `ESCALATED` runs |
| Version Management | `/versions/:artefactType/:artefactId` | Version chain visual (linked list of versions), restore/compare actions |
| Error Monitoring | `/errors` | `DetailsList` of failed workflow runs/regeneration-exhausted artefacts, "Assign to me" / "Retry" `Button` |
| Admin Portal | `/admin` | Tenant list `DetailsList`, tenant provisioning `Dialog`, role assignment management |

## 8.2 Representative Wireframe — Review Screen

```
┌──────────────────────────────────────────────────────────────────────┐
│ SAP AI Delivery Platform        [Tenant: Contoso ▾]   🔔  [Persona]   │
├───────────┬──────────────────────────────────────────────────────────┤
│ Dashboard │  Requirements ▸ FS v3 ▸ Review (Gate 1)                   │
│ Transcripts│ ┌───────────────────────────┬──────────────────────────┐ │
│ Requirements│ │ FS Document Preview       │ Review Comments          │ │
│ FS        │ │ 1. Overview                │ [Persona] "Section 3      │ │
│ TS        │ │ 2. Business Process        │  missing tax handling"    │ │
│ Reviews ◄ │ │ 3. Functional Design ◄─────┼──────────────────────────┤ │
│ Approvals │ │ 4. Interfaces              │ [+ Add comment ...]      │ │
│ RAG Search│ │ 5. Data Requirements       │                          │ │
│ Knowledge │ └───────────────────────────┴──────────────────────────┘ │
│ Agents    │  [Request Changes]   [Approve]            v3 of 3 ▾      │
│ Audit     │                                                          │
│ Prompts   │                                                          │
│ Config    │                                                          │
│ Workflows │                                                          │
│ Versions  │                                                          │
│ Errors    │                                                          │
│ Admin     │                                                          │
└───────────┴──────────────────────────────────────────────────────────┘
```

## 8.3 Representative Wireframe — Workflow Monitoring

```
┌──────────────────────────────────────────────────────────────────────┐
│ Workflow Monitoring                                                   │
│ Run #WF-2044  Transcript: "Sprint Planning 12-Jul"                    │
│                                                                        │
│  Ingested ● ── Requirements ● ── FS Draft ● ── Gate 1 ● ── TS Draft ◐ │
│                                              (regenerated x1)          │
│                                                        ── Gate 2 ○     │
│                                                        ── Package ○    │
│                                                                        │
│  [View Requirement Set]  [View FS v2]  [View Audit Trail]             │
└──────────────────────────────────────────────────────────────────────┘
```

## 8.4 Accessibility & Theming

- Fluent UI v9 theming (`FluentProvider` + `webLightTheme`/`webDarkTheme`)
  with tenant-brandable accent color stored in `tenant_config`.
- All interactive components use Fluent UI's built-in ARIA support;
  `DetailsList` columns are keyboard-sortable; color is never the sole
  indicator of workflow/review status (icon + text label always paired).

## 8.5 Frontend State & Data Flow

- **Auth**: `@azure/msal-react` wraps the app; access tokens attached via
  an Axios/`fetch` interceptor.
- **Data fetching**: TanStack React Query per resource (transcripts,
  requirement sets, FS/TS, reviews) with cache invalidation triggered by
  WebSocket `WorkflowEvent` pushes.
- **Typed API client**: generated from `openapi/openapi.yaml` via
  `openapi-typescript` / `orval`, ensuring the frontend contract never
  drifts from the FastAPI backend.
