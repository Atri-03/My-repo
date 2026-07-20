"""Pydantic request/response schemas for MCP-style tool calls."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class SearchDocumentsRequest(BaseModel):
    query: str
    source_types: Optional[List[str]] = None
    top: int = 10
    search_mode: str = "hybrid"


class SearchDocumentsResult(BaseModel):
    chunk_id: str
    source_uri: str
    source_type: str
    text: str
    score: float = 0.0
    is_dead_link: bool = False


class SearchDocumentsResponse(BaseModel):
    results: List[SearchDocumentsResult]


class ListSourcesResponse(BaseModel):
    sources: List[Dict[str, Any]]


class GetArtefactResponse(BaseModel):
    id: str
    version: int
    status: str
    content: Dict[str, Any]


class GetWorkflowStateResponse(BaseModel):
    id: str
    current_state: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class SubmitReviewDecisionRequest(BaseModel):
    review_cycle_id: str
    decided_by: str
    decision: str
