"""MCP-style HTTP tool endpoints.

Each endpoint wraps a single, well-defined capability (mirroring the MCP
tool contracts documented in docs/architecture/11-mcp-integration-architecture.md)
and proxies to the backing microservice over HTTP.
"""
from typing import Any, Dict, List

import httpx
from fastapi import APIRouter, Depends, HTTPException

from app import schemas
from app.core.config import Settings, get_settings

router = APIRouter()


async def _get(base_url: str, path: str, settings: Settings, params: Dict[str, Any] | None = None) -> Any:
    async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
        try:
            resp = await client.get(f"{base_url}{path}", params=params)
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"Upstream request failed: {exc}") from exc
    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


async def _post(base_url: str, path: str, settings: Settings, json: Dict[str, Any]) -> Any:
    async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
        try:
            resp = await client.post(f"{base_url}{path}", json=json)
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"Upstream request failed: {exc}") from exc
    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


# ---------------------------------------------------------------------------
# Knowledge Search MCP tools -> RAG Service
# ---------------------------------------------------------------------------


@router.post("/tools/search_documents", response_model=schemas.SearchDocumentsResponse, tags=["knowledge-search"])
async def search_documents(payload: schemas.SearchDocumentsRequest, settings: Settings = Depends(get_settings)):
    chunks = await _get(settings.rag_service_url, "/api/v1/knowledge-chunks", settings, params={"limit": payload.top})
    results: List[dict] = [
        {
            "chunk_id": c["id"],
            "source_uri": c.get("knowledge_source_id", ""),
            "source_type": "UNKNOWN",
            "text": c.get("text", ""),
            "score": 0.0,
            "is_dead_link": False,
        }
        for c in chunks
    ]
    return {"results": results}


@router.get("/tools/list_sources", response_model=schemas.ListSourcesResponse, tags=["knowledge-search"])
async def list_sources(settings: Settings = Depends(get_settings)):
    sources = await _get(settings.rag_service_url, "/api/v1/knowledge-sources", settings)
    return {"sources": sources}


@router.get("/tools/get_lineage/{knowledge_source_id}", tags=["knowledge-search"])
async def get_lineage(knowledge_source_id: str, settings: Settings = Depends(get_settings)):
    return await _get(settings.rag_service_url, f"/api/v1/knowledge-sources/{knowledge_source_id}", settings)


# ---------------------------------------------------------------------------
# Artefact MCP tools -> Transcript / Document Extraction / FS / TS services
# ---------------------------------------------------------------------------


@router.get("/tools/get_transcript/{transcript_id}", tags=["artefact"])
async def get_transcript(transcript_id: str, settings: Settings = Depends(get_settings)):
    return await _get(settings.transcript_service_url, f"/api/v1/transcripts/{transcript_id}", settings)


@router.get("/tools/get_requirement_set/{requirement_set_id}", tags=["artefact"])
async def get_requirement_set(requirement_set_id: str, settings: Settings = Depends(get_settings)):
    return await _get(
        settings.document_extraction_service_url,
        f"/api/v1/requirement-sets/{requirement_set_id}",
        settings,
    )


@router.get("/tools/get_fs/{fs_id}", response_model=schemas.GetArtefactResponse, tags=["artefact"])
async def get_fs(fs_id: str, settings: Settings = Depends(get_settings)):
    return await _get(settings.fs_service_url, f"/api/v1/functional-specifications/{fs_id}", settings)


@router.get("/tools/get_ts/{ts_id}", response_model=schemas.GetArtefactResponse, tags=["artefact"])
async def get_ts(ts_id: str, settings: Settings = Depends(get_settings)):
    return await _get(settings.ts_service_url, f"/api/v1/technical-specifications/{ts_id}", settings)


# ---------------------------------------------------------------------------
# Workflow MCP tools -> Workflow / Review services
# ---------------------------------------------------------------------------


@router.get("/tools/get_workflow_state/{workflow_run_id}", response_model=schemas.GetWorkflowStateResponse, tags=["workflow"])
async def get_workflow_state(workflow_run_id: str, settings: Settings = Depends(get_settings)):
    return await _get(settings.workflow_service_url, f"/api/v1/workflow-runs/{workflow_run_id}", settings)


@router.get("/tools/list_active_runs", tags=["workflow"])
async def list_active_runs(settings: Settings = Depends(get_settings)):
    runs = await _get(settings.workflow_service_url, "/api/v1/workflow-runs", settings)
    return [r for r in runs if not r.get("completed_at")]


@router.post("/tools/submit_review_decision", tags=["workflow"])
async def submit_review_decision(payload: schemas.SubmitReviewDecisionRequest, settings: Settings = Depends(get_settings)):
    return await _post(settings.approval_service_url, "/api/v1/review-decisions", settings, json=payload.model_dump())
