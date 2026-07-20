# 10. Azure Deployment Architecture

PlantUML source: [`diagrams/azure-deployment.puml`](diagrams/azure-deployment.puml).

```plantuml
@startuml
!include diagrams/azure-deployment.puml
@enduml
```

## 10.1 Resource Topology

| Resource Group | Contents | Notes |
|---|---|---|
| `rg-sapaidp-shared-<env>` | Static Web App/App Service (SPA), Container Apps Environment (API, Orchestrator, Agents, MCP servers, ingestion worker jobs), Azure Database for PostgreSQL (shared schema), Service Bus, Azure Web PubSub, Blob Storage, Key Vault, Azure Monitor/App Insights | One per environment (`dev`, `test`, `prod`); hosts all `SHARED` tier tenants |
| `rg-sapaidp-ai-<env>` | Azure AI Foundry project (GPT-5.5 deployment + embedding deployment), Azure AI Search service (shared + dedicated indexes) | Isolated from compute RG to allow independent scaling/quota management of AI resources |
| `rg-sapaidp-tenant-<tenantId>` | Dedicated PostgreSQL schema/instance, dedicated Azure AI Search index | Provisioned only for `DEDICATED` tier tenants via the same Bicep modules parameterized per tenant |

## 10.2 Compute Choice: Azure Container Apps

- **API**, **Orchestrator**, **Agent Runtime**, and **MCP Servers** are
  deployed as Azure Container Apps for consumption-based autoscaling
  (HTTP concurrency for API, KEDA queue-length scaling for the
  Orchestrator/Agents driven by Service Bus queue depth).
- **Ingestion Worker Jobs** run as Container Apps Jobs (event-driven,
  triggered by Service Bus messages), enabling burst ingestion (e.g., bulk
  historical BRD import) without impacting interactive API latency.
- Each container app uses a **user-assigned Managed Identity** scoped via
  Azure RBAC to exactly the resources it needs (Key Vault secrets, Blob
  containers, Service Bus queues/topics, Azure AI Search, Azure AI
  Foundry) — no shared credentials across services.

## 10.3 Networking & Security

- **Azure Front Door** provides global routing, WAF, and TLS termination
  in front of the SPA and API.
- All backend services (Container Apps, PostgreSQL, Search, Key Vault) sit
  behind **VNet integration** with private endpoints; only Front Door and
  the SPA's public endpoint are internet-facing.
- **Entra ID** is the sole identity provider: interactive users
  authenticate via OIDC (MSAL.js); service-to-service calls use Managed
  Identity; no client secrets/API keys are stored in application
  configuration — Key Vault references only, resolved at runtime.
- **Per-tenant secret namespace** in Key Vault
  (`tenant/{tenantId}/foundry-api-key`, etc.) supports tenants that require
  API-key auth to Azure AI Foundry (if Managed Identity is not available
  for their Foundry resource) without cross-tenant secret exposure.

## 10.4 Data Tier

- **Azure Database for PostgreSQL Flexible Server**: zone-redundant HA,
  automated backups, read replica for reporting/audit-heavy queries (Audit
  Dashboard, Workflow Monitoring), `pg_partman` for partition maintenance
  on `audit_log_entry`/`workflow_event`.
- **Azure Blob Storage**: hot tier for active transcripts/artefacts,
  lifecycle policy moves artefacts older than the tenant's retention
  window to cool/archive tiers.
- **Azure AI Search**: standard tier (or higher, sized per tenant volume)
  with shared partitions for `SHARED` tenants and dedicated partitions for
  `DEDICATED` tenants.

## 10.5 Observability & Operations

- **Azure Monitor + Application Insights**: distributed tracing
  (OpenTelemetry) correlated by `workflow_run_id`; custom dashboards for
  agent latency, regeneration rate, review-gate SLA.
- **Alerting**: Service Bus dead-letter queue depth, Container App
  restart/error rate, PostgreSQL replica lag, Azure AI Search query
  latency/error rate — routed to the Error Monitoring UI screen and
  ops on-call via Azure Monitor action groups.

## 10.6 IaC & Environments

- Bicep modules under `infra/bicep/` (one module per resource category:
  `network.bicep`, `data.bicep`, `ai.bicep`, `compute.bicep`,
  `messaging.bicep`, `security.bicep`) composed by `main.bicep`, with
  `main.<env>.bicepparam` parameter files for `dev`/`test`/`prod`.
- Tenant onboarding for `DEDICATED` tier is a parameterized re-run of the
  `tenant.bicep` module against `rg-sapaidp-tenant-<tenantId>`, invoked by
  the Admin Portal's tenant-provisioning workflow (Phase 2).
- CI/CD (`.github/workflows/`) validates Bicep (`az bicep build`, `what-if`)
  on PR and applies on merge to environment branches, gated by manual
  approval for `prod`.

## 10.7 Open Items Requiring Confirmation

As stated in the solution architecture, the following must be confirmed
before provisioning: Azure AI Foundry endpoint/deployment/resource names,
authentication method, tenant/subscription details, existing vs.
greenfield Azure AI Search service, and Microsoft Graph app registration
scope for Teams/SharePoint/OneDrive ingestion.
