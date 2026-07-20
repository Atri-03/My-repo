-- SAP AI Delivery Platform — PostgreSQL Schema (Phase 1)
-- Target: Azure Database for PostgreSQL Flexible Server (v15+)
-- Notes:
--   * Every tenant-scoped table carries tenant_id and is indexed on it.
--   * High-growth/audit tables are range-partitioned by created_at.
--   * UUIDs are generated application-side (ULID/UUIDv7 recommended) to
--     keep partition-key locality reasonable; gen_random_uuid() shown as
--     a safe default requiring pgcrypto.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ============================================================
-- Tenancy
-- ============================================================

CREATE TABLE tenant (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                TEXT NOT NULL,
    entra_tenant_id     TEXT NOT NULL UNIQUE,
    tier                TEXT NOT NULL CHECK (tier IN ('SHARED', 'DEDICATED')),
    status              TEXT NOT NULL CHECK (status IN ('ACTIVE', 'SUSPENDED', 'DEPROVISIONED')) DEFAULT 'ACTIVE',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE tenant_config (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenant(id),
    foundry_endpoint    TEXT NOT NULL,
    foundry_deployment_name TEXT NOT NULL,
    foundry_resource_name TEXT NOT NULL,
    auth_method         TEXT NOT NULL CHECK (auth_method IN ('MANAGED_IDENTITY', 'API_KEY', 'SERVICE_PRINCIPAL')),
    search_service_name TEXT NOT NULL,
    search_index_prefix TEXT NOT NULL,
    key_vault_uri       TEXT NOT NULL,
    max_regeneration_attempts INTEGER NOT NULL DEFAULT 5,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (tenant_id)
);

CREATE TABLE project (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenant(id),
    name                TEXT NOT NULL,
    sap_execution_repo_url TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_project_tenant ON project(tenant_id);

-- ============================================================
-- Ingestion
-- ============================================================

CREATE TABLE source_document (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenant(id),
    project_id          UUID NOT NULL REFERENCES project(id),
    source_type         TEXT NOT NULL CHECK (source_type IN ('TEAMS_TRANSCRIPT', 'SHAREPOINT', 'ONEDRIVE', 'UPLOAD')),
    origin_uri          TEXT NOT NULL,
    checksum            TEXT NOT NULL,
    blob_uri            TEXT NOT NULL,
    ingested_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, checksum)
);
CREATE INDEX idx_source_document_tenant ON source_document(tenant_id, ingested_at DESC);

CREATE TABLE transcript (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_document_id  UUID NOT NULL REFERENCES source_document(id),
    meeting_date        TIMESTAMPTZ,
    participants        JSONB NOT NULL DEFAULT '[]',
    parsed_format       TEXT NOT NULL CHECK (parsed_format IN ('TEAMS_TRANSCRIPT', 'MOM', 'BRD', 'PDF', 'DOCX', 'TXT', 'HTML')),
    raw_text            TEXT NOT NULL,
    structured_content  JSONB,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_transcript_source_document ON transcript(source_document_id);

-- ============================================================
-- Requirements
-- ============================================================

CREATE TABLE requirement_set (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenant(id),
    transcript_id       UUID NOT NULL REFERENCES transcript(id),
    version             INTEGER NOT NULL DEFAULT 1,
    status              TEXT NOT NULL CHECK (status IN ('DRAFT', 'APPROVED', 'SUPERSEDED')) DEFAULT 'DRAFT',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_requirement_set_transcript ON requirement_set(transcript_id);

CREATE TABLE requirement (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    requirement_set_id  UUID NOT NULL REFERENCES requirement_set(id),
    type                TEXT NOT NULL CHECK (type IN ('FUNCTIONAL', 'NON_FUNCTIONAL', 'ASSUMPTION', 'DEPENDENCY')),
    title               TEXT NOT NULL,
    description         TEXT NOT NULL,
    priority            TEXT CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_requirement_set ON requirement(requirement_set_id);

CREATE TABLE requirement_risk (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    requirement_set_id  UUID NOT NULL REFERENCES requirement_set(id),
    description         TEXT NOT NULL,
    severity            TEXT NOT NULL CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL'))
);

CREATE TABLE requirement_entity (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    requirement_set_id  UUID NOT NULL REFERENCES requirement_set(id),
    name                TEXT NOT NULL,
    attributes          JSONB NOT NULL DEFAULT '{}'
);

CREATE TABLE business_rule (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    requirement_set_id  UUID NOT NULL REFERENCES requirement_set(id),
    rule                TEXT NOT NULL
);

-- ============================================================
-- Templates
-- ============================================================

CREATE TABLE document_template (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenant(id),
    type                TEXT NOT NULL CHECK (type IN ('FS', 'TS')),
    name                TEXT NOT NULL,
    version             INTEGER NOT NULL DEFAULT 1,
    schema              JSONB NOT NULL,
    is_active           BOOLEAN NOT NULL DEFAULT true,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, type, name, version)
);

-- ============================================================
-- Functional / Technical Specifications (versioned, append-only)
-- ============================================================

CREATE TABLE functional_specification (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenant(id),
    requirement_set_id  UUID NOT NULL REFERENCES requirement_set(id),
    template_id         UUID NOT NULL REFERENCES document_template(id),
    version             INTEGER NOT NULL DEFAULT 1,
    parent_version_id   UUID REFERENCES functional_specification(id),
    status              TEXT NOT NULL CHECK (status IN ('DRAFT', 'IN_REVIEW', 'APPROVED', 'REJECTED', 'SUPERSEDED')) DEFAULT 'DRAFT',
    content             JSONB NOT NULL,
    blob_uri            TEXT,
    regeneration_count  INTEGER NOT NULL DEFAULT 0,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_fs_requirement_set ON functional_specification(requirement_set_id, version DESC);

CREATE TABLE technical_specification (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenant(id),
    functional_specification_id UUID NOT NULL REFERENCES functional_specification(id),
    template_id         UUID NOT NULL REFERENCES document_template(id),
    version             INTEGER NOT NULL DEFAULT 1,
    parent_version_id   UUID REFERENCES technical_specification(id),
    status              TEXT NOT NULL CHECK (status IN ('DRAFT', 'IN_REVIEW', 'APPROVED', 'REJECTED', 'SUPERSEDED')) DEFAULT 'DRAFT',
    content             JSONB NOT NULL,
    blob_uri            TEXT,
    regeneration_count  INTEGER NOT NULL DEFAULT 0,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_ts_fs ON technical_specification(functional_specification_id, version DESC);

-- ============================================================
-- Reviews
-- ============================================================

CREATE TABLE review_cycle (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenant(id),
    artefact_type       TEXT NOT NULL CHECK (artefact_type IN ('FUNCTIONAL_SPECIFICATION', 'TECHNICAL_SPECIFICATION')),
    artefact_id         UUID NOT NULL,
    gate                TEXT NOT NULL CHECK (gate IN ('GATE_1_FS', 'GATE_2_TS')),
    status              TEXT NOT NULL CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED', 'CHANGES_REQUESTED')) DEFAULT 'PENDING',
    opened_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    closed_at           TIMESTAMPTZ
);
CREATE INDEX idx_review_cycle_artefact ON review_cycle(artefact_type, artefact_id);

CREATE TABLE review_comment (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    review_cycle_id     UUID NOT NULL REFERENCES review_cycle(id),
    reviewer_id         TEXT NOT NULL,
    comment             TEXT NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_review_comment_cycle ON review_comment(review_cycle_id);

CREATE TABLE review_decision (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    review_cycle_id     UUID NOT NULL REFERENCES review_cycle(id),
    decided_by          TEXT NOT NULL,
    decision            TEXT NOT NULL CHECK (decision IN ('APPROVE', 'REJECT', 'CHANGES_REQUESTED')),
    decided_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_review_decision_cycle ON review_decision(review_cycle_id);

-- ============================================================
-- SAP Execution Package (handoff artefact)
-- ============================================================

CREATE TABLE sap_execution_package (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenant(id),
    technical_specification_id UUID NOT NULL REFERENCES technical_specification(id),
    version             INTEGER NOT NULL DEFAULT 1,
    status              TEXT NOT NULL CHECK (status IN ('DRAFT', 'VALIDATED', 'PUBLISHED', 'ACKNOWLEDGED', 'FAILED')) DEFAULT 'DRAFT',
    payload             JSONB NOT NULL,
    sap_execution_repo_ref TEXT,
    published_at        TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_sap_package_ts ON sap_execution_package(technical_specification_id);

-- ============================================================
-- Workflow (partitioned — high growth)
-- ============================================================

CREATE TABLE workflow_run (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenant(id),
    transcript_id       UUID NOT NULL REFERENCES transcript(id),
    current_state       TEXT NOT NULL,
    started_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at        TIMESTAMPTZ
);
CREATE INDEX idx_workflow_run_tenant ON workflow_run(tenant_id, started_at DESC);

CREATE TABLE workflow_event (
    id                  UUID NOT NULL DEFAULT gen_random_uuid(),
    workflow_run_id     UUID NOT NULL REFERENCES workflow_run(id),
    from_state          TEXT,
    to_state            TEXT NOT NULL,
    actor               TEXT NOT NULL,
    occurred_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (id, occurred_at)
) PARTITION BY RANGE (occurred_at);

CREATE TABLE workflow_event_default PARTITION OF workflow_event DEFAULT;
CREATE INDEX idx_workflow_event_run ON workflow_event(workflow_run_id);

-- ============================================================
-- Audit (partitioned — append-only, high growth)
-- ============================================================

CREATE TABLE audit_log_entry (
    id                  UUID NOT NULL DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenant(id),
    entity_type         TEXT NOT NULL,
    entity_id           UUID NOT NULL,
    action              TEXT NOT NULL,
    actor               TEXT NOT NULL,
    before              JSONB,
    after               JSONB,
    occurred_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (id, occurred_at)
) PARTITION BY RANGE (occurred_at);

CREATE TABLE audit_log_entry_default PARTITION OF audit_log_entry DEFAULT;
CREATE INDEX idx_audit_tenant_entity ON audit_log_entry(tenant_id, entity_type, entity_id);

-- ============================================================
-- Knowledge (RAG metadata; vectors live in Azure AI Search)
-- ============================================================

CREATE TABLE knowledge_source (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenant(id),
    source_type         TEXT NOT NULL CHECK (source_type IN (
                            'PAST_FS', 'PAST_TS', 'PAST_BRD', 'PAST_PROJECT',
                            'CODING_STANDARD', 'ARCHITECTURE_STANDARD', 'NAMING_STANDARD',
                            'SAP_STANDARD', 'REVIEW_HISTORY', 'ATC_HISTORY', 'LESSON_LEARNED')),
    uri                 TEXT NOT NULL,
    last_indexed_at     TIMESTAMPTZ,
    is_dead_link        BOOLEAN NOT NULL DEFAULT false,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_knowledge_source_tenant ON knowledge_source(tenant_id, source_type);

CREATE TABLE knowledge_chunk (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    knowledge_source_id UUID NOT NULL REFERENCES knowledge_source(id),
    chunk_index         INTEGER NOT NULL,
    text                TEXT NOT NULL,
    vector_id           TEXT NOT NULL,
    UNIQUE (knowledge_source_id, chunk_index)
);

-- ============================================================
-- Prompt / Configuration Management
-- ============================================================

CREATE TABLE prompt_template (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenant(id),
    agent_name          TEXT NOT NULL,
    name                TEXT NOT NULL,
    version             INTEGER NOT NULL DEFAULT 1,
    content             TEXT NOT NULL,
    is_active           BOOLEAN NOT NULL DEFAULT true,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, agent_name, name, version)
);
