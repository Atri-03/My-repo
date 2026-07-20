/** Shared TypeScript models mirroring the backend Pydantic schemas. */

export interface SourceDocument {
  id: string;
  tenant_id: string;
  project_id: string;
  source_type: string;
  origin_uri: string;
  checksum: string;
  blob_uri: string;
  ingested_at?: string | null;
}

export interface Transcript {
  id: string;
  source_document_id: string;
  meeting_date?: string | null;
  participants?: string[] | null;
  parsed_format: string;
  raw_text: string;
  structured_content?: Record<string, unknown> | null;
  created_at?: string | null;
}

export interface RequirementSet {
  id: string;
  tenant_id: string;
  transcript_id: string;
  version?: number | null;
  status?: string | null;
  created_at?: string | null;
}

export interface Requirement {
  id: string;
  requirement_set_id: string;
  type: string;
  title: string;
  description: string;
  priority?: string | null;
  created_at?: string | null;
}

export interface RequirementRisk {
  id: string;
  requirement_set_id: string;
  description: string;
  severity: string;
  created_at?: string | null;
}

export interface RequirementEntity {
  id: string;
  requirement_set_id: string;
  name: string;
  attributes?: Record<string, unknown> | null;
  created_at?: string | null;
}

export interface BusinessRule {
  id: string;
  requirement_set_id: string;
  rule: string;
  created_at?: string | null;
}

export interface DocumentTemplate {
  id: string;
  tenant_id: string;
  type?: string | null;
  name: string;
  version?: number | null;
  schema_: Record<string, unknown>;
  is_active?: boolean | null;
  created_at?: string | null;
}

export interface FunctionalSpecification {
  id: string;
  tenant_id: string;
  requirement_set_id: string;
  template_id: string;
  version?: number | null;
  parent_version_id?: string | null;
  status?: string | null;
  content: Record<string, unknown>;
  blob_uri?: string | null;
  regeneration_count?: number | null;
  created_at?: string | null;
}

export interface TechnicalSpecification {
  id: string;
  tenant_id: string;
  functional_specification_id: string;
  template_id: string;
  version?: number | null;
  parent_version_id?: string | null;
  status?: string | null;
  content: Record<string, unknown>;
  blob_uri?: string | null;
  regeneration_count?: number | null;
  created_at?: string | null;
}

export interface ReviewCycle {
  id: string;
  tenant_id: string;
  artefact_type: string;
  artefact_id: string;
  gate: string;
  status?: string | null;
  opened_at?: string | null;
  closed_at?: string | null;
}

export interface ReviewComment {
  id: string;
  review_cycle_id: string;
  reviewer_id: string;
  comment: string;
  created_at?: string | null;
}

export interface ReviewDecision {
  id: string;
  review_cycle_id: string;
  decided_by: string;
  decision: string;
  decided_at?: string | null;
}

export interface SapExecutionPackage {
  id: string;
  tenant_id: string;
  technical_specification_id: string;
  version?: number | null;
  status?: string | null;
  payload: Record<string, unknown>;
  sap_execution_repo_ref?: string | null;
  published_at?: string | null;
}

export interface SapPackage {
  id: string;
  tenant_id: string;
  package_name: string;
  description: string;
  software_component: string;
  parent_package?: string | null;
  transport_request?: string | null;
  status: string;
  created_at?: string | null;
}

export interface SapTransport {
  id: string;
  tenant_id: string;
  transport_request: string;
  description: string;
  transport_type: string;
  target_system?: string | null;
  owner?: string | null;
  status: string;
  released_at?: string | null;
  created_at?: string | null;
}

export interface GeneratedObject {
  id: string;
  tenant_id: string;
  object_name: string;
  object_type: string;
  package: string;
  transport_request: string;
  description?: string | null;
  source_code?: string | null;
  extra?: Record<string, unknown> | null;
  status: string;
  created_at?: string | null;
}

export interface Activation {
  id: string;
  tenant_id: string;
  object_name: string;
  object_type: string;
  status: string;
  activated_at?: string | null;
  created_at?: string | null;
}

export interface AtcRun {
  id: string;
  tenant_id: string;
  object_name: string;
  object_type: string;
  variant: string;
  status: string;
  findings: Record<string, unknown>[];
  created_at?: string | null;
}

export interface AtcRemediation {
  id: string;
  tenant_id: string;
  object_name: string;
  object_type: string;
  finding_ids: string[];
  auto_apply: boolean;
  status: string;
  remediated_at?: string | null;
  created_at?: string | null;
}

export interface ExecutionPlan {
  id: string;
  tenant_id: string;
  technical_specification_id: string;
  package_name?: string | null;
  transport_description?: string | null;
  steps: Record<string, unknown>[];
  status: string;
  created_at?: string | null;
}

export interface AuditLogEntry {
  id: string;
  tenant_id: string;
  entity_type: string;
  entity_id: string;
  action: string;
  actor: string;
  before?: Record<string, unknown> | null;
  after?: Record<string, unknown> | null;
  occurred_at?: string | null;
}

export interface KnowledgeSource {
  id: string;
  tenant_id: string;
  source_type: string;
  uri: string;
  last_indexed_at?: string | null;
  is_dead_link?: boolean | null;
}

export interface KnowledgeChunk {
  id: string;
  knowledge_source_id: string;
  chunk_index: number;
  text: string;
  vector_id: string;
  created_at?: string | null;
}

export interface Tenant {
  id: string;
  name: string;
  entra_tenant_id: string;
  tier?: string | null;
  status?: string | null;
  created_at?: string | null;
}

export interface Project {
  id: string;
  tenant_id: string;
  name: string;
  sap_execution_repo_url?: string | null;
  created_at?: string | null;
}

export interface User {
  id: string;
  tenant_id: string;
  email: string;
  display_name: string;
  role?: string | null;
  is_active?: boolean | null;
  created_at?: string | null;
}

export interface WorkflowRun {
  id: string;
  tenant_id: string;
  transcript_id: string;
  current_state: string;
  started_at?: string | null;
  completed_at?: string | null;
}

export interface WorkflowEvent {
  id: string;
  workflow_run_id: string;
  from_state?: string | null;
  to_state: string;
  actor: string;
  occurred_at?: string | null;
}

export interface SearchDocumentsResult {
  chunk_id: string;
  source_uri: string;
  source_type: string;
  text: string;
  score: number;
  is_dead_link: boolean;
}

export interface SearchDocumentsResponse {
  results: SearchDocumentsResult[];
}

export interface ListSourcesResponse {
  sources: Array<Record<string, unknown>>;
}

export interface GetArtefactResponse {
  id: string;
  version: number;
  status: string;
  content: Record<string, unknown>;
}

export interface GetWorkflowStateResponse {
  id: string;
  current_state: string;
  started_at?: string | null;
  completed_at?: string | null;
}

export interface HealthStatus {
  status: string;
  service: string;
}
