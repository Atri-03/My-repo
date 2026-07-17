"""Node 5: abap_code_generation.

Takes the approved TS and generates ABAP source code via LLM (a simple report
skeleton is sufficient for this POC), then creates the object in SAP via the
ADT REST API as INACTIVE in the configured package.
"""
from __future__ import annotations

import textwrap
import uuid

from app.config import settings
from models.schemas import StructuredRequirements
from nodes.state import PipelineState
from services.adt_client import create_adt_object
from services.azure_openai_client import chat_completion

_SYSTEM_PROMPT = """You are an ABAP developer assistant. Generate a simple, \
readable ABAP report skeleton (not production code) that reflects the given \
functional/technical requirements. Include:
- REPORT statement with a sensible Z-program name
- Comment header summarizing the requirement
- Basic field/data declarations reflecting the listed fields
- Placeholder validation logic (as comments or simple IF checks) for each rule
- A TODO comment where the real business logic should go

Return ONLY the ABAP source code, no markdown fences, no explanation."""


def _generate_object_name(title: str, run_id: str) -> str:
    slug = "".join(ch for ch in title.upper().replace(" ", "_") if ch.isalnum() or ch == "_")
    slug = slug[:16] or "PROGRAM"
    # Append a short, deterministic-per-run suffix so object names stay unique
    # even for empty/short/duplicate titles (ABAP report names allow <= 30 chars).
    suffix = run_id.replace("-", "")[:6].upper() or uuid.uuid4().hex[:6].upper()
    return f"Z_{slug}_{suffix}"


def _build_user_prompt(requirements: StructuredRequirements, object_name: str) -> str:
    fields = "\n".join(f"- {f.name} ({f.data_type}): {f.description}" for f in requirements.fields)
    validations = "\n".join(f"- {v.description}" for v in requirements.validations)
    return (
        f"Program name: {object_name}\n"
        f"Title: {requirements.title}\n"
        f"Summary: {requirements.summary}\n\n"
        f"Fields:\n{fields or '- (none specified)'}\n\n"
        f"Validations:\n{validations or '- (none specified)'}\n"
    )


def abap_code_generation(state: PipelineState) -> PipelineState:
    requirements = StructuredRequirements(**state.get("requirements", {}))
    object_name = _generate_object_name(requirements.title, state["run_id"])

    abap_source = chat_completion(
        _SYSTEM_PROMPT,
        _build_user_prompt(requirements, object_name),
        temperature=0.1,
    )

    adt_result = create_adt_object(
        object_name=object_name,
        source_code=abap_source,
        package=settings.adt_target_package,
        object_type="PROG",
        description=textwrap.shorten(f"POC draft: {requirements.title}", width=60, placeholder="..."),
    )

    return {
        **state,
        "abap_object_name": object_name,
        "abap_source": abap_source,
        "adt_result": adt_result,
        "status": "abap_generated",
    }
