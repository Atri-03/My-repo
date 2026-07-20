"""Enterprise Knowledge Brain source type catalogue.

These are the knowledge categories the platform's Knowledge Agent / RAG
layer is expected to ingest and retrieve from (see
`docs/architecture/09-rag-architecture.md`). `KnowledgeSource.source_type`
remains a free-form string so new categories can be added without a schema
migration, but this catalogue is the canonical, documented list used to
populate the Knowledge Management UI and to validate/normalize known types.
"""
from __future__ import annotations

PAST_BRD = "PAST_BRD"
PAST_FS = "PAST_FS"
PAST_TS = "PAST_TS"
PAST_RAP_PROJECT = "PAST_RAP_PROJECT"
PAST_CDS_VIEW = "PAST_CDS_VIEW"
PAST_FIORI_APP = "PAST_FIORI_APP"
REVIEW_COMMENT = "REVIEW_COMMENT"
APPROVED_ARCHITECT_DECISION = "APPROVED_ARCHITECT_DECISION"
NAMING_STANDARD = "NAMING_STANDARD"
ATC_FINDING = "ATC_FINDING"
REUSABLE_COMPONENT = "REUSABLE_COMPONENT"
SAP_STANDARD = "SAP_STANDARD"

KNOWLEDGE_SOURCE_TYPES = [
    {"value": PAST_BRD, "label": "Past BRDs"},
    {"value": PAST_FS, "label": "Past Functional Specifications"},
    {"value": PAST_TS, "label": "Past Technical Specifications"},
    {"value": PAST_RAP_PROJECT, "label": "Past RAP Projects"},
    {"value": PAST_CDS_VIEW, "label": "Past CDS Views"},
    {"value": PAST_FIORI_APP, "label": "Past Fiori Apps"},
    {"value": REVIEW_COMMENT, "label": "Review Comments"},
    {"value": APPROVED_ARCHITECT_DECISION, "label": "Approved Architect Decisions"},
    {"value": NAMING_STANDARD, "label": "Naming Standards"},
    {"value": ATC_FINDING, "label": "ATC Findings"},
    {"value": REUSABLE_COMPONENT, "label": "Reusable Components"},
    {"value": SAP_STANDARD, "label": "SAP Standards"},
]

KNOWN_SOURCE_TYPE_VALUES = {entry["value"] for entry in KNOWLEDGE_SOURCE_TYPES}
