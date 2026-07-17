"""Pydantic schemas shared across the pipeline."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class FieldSpec(BaseModel):
    name: str
    description: str = ""
    data_type: str = "string"
    mandatory: bool = False
    source: Optional[str] = Field(
        default=None, description="Origin table/field or business term, if known"
    )


class ValidationRule(BaseModel):
    description: str
    applies_to: list[str] = Field(default_factory=list)
    error_message: Optional[str] = None


class ActorRole(BaseModel):
    name: str
    responsibility: str = ""


class ProcessStep(BaseModel):
    step_number: int
    description: str
    actor: Optional[str] = None


class StructuredRequirements(BaseModel):
    """Structured output produced by the requirement_extraction node."""

    title: str = "Untitled Requirement"
    summary: str = ""
    process_flow: list[ProcessStep] = Field(default_factory=list)
    fields: list[FieldSpec] = Field(default_factory=list)
    validations: list[ValidationRule] = Field(default_factory=list)
    actors: list[ActorRole] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)


class FSTSDocumentPaths(BaseModel):
    fs_path: str
    ts_path: str


class ADTCreationResult(BaseModel):
    object_name: str
    object_type: str
    package: str
    status_code: int
    inactive: bool = True
    raw_response: Optional[str] = None


class PipelineStatus(str, Enum):
    CREATED = "created"
    INGESTED = "ingested"
    REQUIREMENTS_EXTRACTED = "requirements_extracted"
    FS_TS_GENERATED = "fs_ts_generated"
    AWAITING_GATE_1 = "awaiting_gate_1_approval"
    GATE_1_APPROVED = "gate_1_approved"
    ABAP_GENERATED = "abap_generated"
    AWAITING_GATE_2 = "awaiting_gate_2_review"
    GATE_2_APPROVED = "gate_2_approved"
    FAILED = "failed"


class PipelineRunSummary(BaseModel):
    run_id: str
    status: PipelineStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    detail: dict[str, Any] = Field(default_factory=dict)


class ApprovalRequest(BaseModel):
    run_id: str
    approved: bool
    comments: Optional[str] = None
