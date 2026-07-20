# 5. Agent Interaction Model

PlantUML source: [`diagrams/agent-interaction.puml`](diagrams/agent-interaction.puml).

```plantuml
@startuml
!include diagrams/agent-interaction.puml
@enduml
```

## 5.1 Orchestrator Agent

Implemented as a **Semantic Kernel Process Framework** state machine
(`agents/orchestrator_agent`). The process owns the canonical
`WorkflowState` (see §4.2) and is the only component permitted to invoke
other agents — agents never call each other directly, which keeps the
workflow auditable and independently testable.

Responsibilities:
- Consume `TranscriptIngested` events from the Service Bus.
- Sequence agent invocations per the state machine.
- Persist `WorkflowEvent` rows on every transition (append-only).
- Enforce the maximum regeneration retry policy (configurable per tenant,
  default 5) before escalating to human intervention (`Error Monitoring`
  UI screen, §8).
- Build and publish the `SapExecutionPackage` once Gate 2 is approved.

## 5.2 Agent Roles and Semantic Kernel Plugin Contracts

| Agent | SK Plugin Functions | Inputs | Outputs |
|---|---|---|---|
| Transcript Agent | `parse_transcript`, `parse_mom`, `parse_brd`, `parse_pdf`, `parse_docx`, `parse_txt`, `parse_html` | Raw file/blob URI | `StructuredTranscript` (speakers, timestamps, topics, action items) |
| Requirement Agent | `extract_requirements` | `StructuredTranscript` + RAG context | `RequirementSet` (FR, NFR, assumptions, dependencies, risks, entities, workflows, business rules) |
| FS Agent | `generate_fs`, `regenerate_fs` | `RequirementSet`, `DocumentTemplate`, review comments (on regeneration) | `FunctionalSpecification` (versioned) |
| Review Agent | `open_review`, `record_comment`, `record_decision` | Artefact reference, reviewer input | `ReviewCycle`, `ReviewComment[]`, `ReviewDecision` |
| TS Agent | `generate_ts`, `regenerate_ts` | Approved `FunctionalSpecification`, `DocumentTemplate`, review comments | `TechnicalSpecification` (architecture, data model, CDS/RAP/OData design, security, integration) |
| Knowledge Agent | `search_documents`, `get_lineage`, `check_dead_links` | Query text, metadata filters | Ranked chunks with citations, source lineage, freshness/dead-link flags |

Each plugin function is a plain, independently unit-testable Python
function decorated with `@kernel_function`; the Kernel is constructed per
tenant/session with the tenant's Azure AI Foundry deployment and Azure AI
Search index bound via dependency injection — no agent hardcodes a model
or index name.

## 5.3 Model Binding — Azure AI Foundry (GPT-5.5)

All agents share a single Semantic Kernel `AzureAIInferenceChatCompletion`
(or `AzureOpenAIChatCompletion`, pending the confirmed Foundry connector —
see open question in §1) service registration per tenant:

```
kernel.add_service(
    AzureAIInferenceChatCompletion(
        service_id="gpt-5.5",
        endpoint=tenant_settings.foundry_endpoint,
        deployment_name=tenant_settings.foundry_deployment_name,
        credential=ManagedIdentityCredential(),  # or resolved auth method
    )
)
```

No endpoint, deployment name, or credential is hardcoded; all are resolved
from the tenant configuration store (PostgreSQL `tenant_config` table) with
secret values resolved from Azure Key Vault at runtime.

## 5.4 Regeneration / Self-Healing Loop

1. `Review Agent` records a `CHANGES_REQUESTED` decision with one or more
   `ReviewComment` rows.
2. `Orchestrator Agent` increments the artefact's `regeneration_count` and,
   while under the tenant's max-retry threshold, invokes the owning agent's
   `regenerate_*` function with the prior draft + comments as context.
3. The regenerated artefact is persisted as a new version
   (`parentVersionId` set) and a new `ReviewCycle` is opened at the same
   gate.
4. If the max-retry threshold is exceeded, the workflow transitions to
   `ESCALATED` and surfaces on the **Error Monitoring** and **Workflow
   Monitoring** UI screens for human intervention.

## 5.5 Knowledge Agent — Cross-Cutting Retrieval

The Knowledge Agent is invoked by both FS Agent and TS Agent (not only via
the dedicated RAG Search UI screen), ensuring generated specifications are
always grounded in past FS/TS, BRDs, standards, and lessons learned. See
[RAG Architecture](09-rag-architecture.md) for retrieval details.
