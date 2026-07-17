"""Shared state definition passed between LangGraph nodes."""
from __future__ import annotations

from typing import Any, Optional, TypedDict


class PipelineState(TypedDict, total=False):
    run_id: str
    transcript_path: str
    raw_transcript: str
    chunks: list[str]
    requirements: dict[str, Any]
    fs_path: str
    ts_path: str
    gate_1_approved: bool
    gate_1_comments: Optional[str]
    abap_object_name: str
    abap_source: str
    adt_result: dict[str, Any]
    gate_2_approved: bool
    gate_2_comments: Optional[str]
    status: str
    error: Optional[str]
