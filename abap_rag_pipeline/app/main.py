"""FastAPI application exposing the RAG-based ABAP pipeline POC.

Endpoints:
- POST /transcripts/upload          — upload a transcript text file
- POST /pipeline/{run_id}/trigger   — start (or resume) the pipeline
- GET  /pipeline/{run_id}/status    — check current pipeline status
- POST /pipeline/{run_id}/approve/gate1 — approve/reject FS/TS at human gate 1
- POST /pipeline/{run_id}/approve/gate2 — mark ABAP object reviewed at gate 2
"""
from __future__ import annotations

import logging
import os
import uuid

from fastapi import FastAPI, HTTPException, UploadFile
from langgraph.errors import GraphInterrupt

from app.graph import pipeline_graph
from models.schemas import ApprovalRequest
from services.tracker_store import get_run, upsert_run

logger = logging.getLogger(__name__)

app = FastAPI(
    title="ABAP RAG Agentic Pipeline (POC)",
    description="Converts a Teams meeting transcript into a draft ABAP program "
    "with human review gates.",
    version="0.1.0",
)

_TRANSCRIPT_DIR = "./data/transcripts"


def _thread_config(run_id: str) -> dict:
    return {"configurable": {"thread_id": run_id}}


@app.post("/transcripts/upload")
async def upload_transcript(file: UploadFile) -> dict:
    """Upload a raw transcript text file and register a new pipeline run."""
    os.makedirs(_TRANSCRIPT_DIR, exist_ok=True)
    run_id = str(uuid.uuid4())
    transcript_path = os.path.join(_TRANSCRIPT_DIR, f"{run_id}.txt")

    content = await file.read()
    with open(transcript_path, "wb") as fh:
        fh.write(content)

    upsert_run(run_id, status="created", transcript_path=transcript_path)
    return {"run_id": run_id, "transcript_path": transcript_path, "status": "created"}


@app.post("/pipeline/{run_id}/trigger")
async def trigger_pipeline(run_id: str) -> dict:
    """Start the pipeline for a previously uploaded transcript.

    Runs until it hits the first human-in-the-loop interrupt (gate 1) and
    then returns control, leaving the graph state checkpointed for resumption.
    """
    run = get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Unknown run_id")

    initial_state = {"run_id": run_id, "transcript_path": run["transcript_path"]}

    try:
        result = pipeline_graph.invoke(initial_state, config=_thread_config(run_id))
    except GraphInterrupt:
        result = pipeline_graph.get_state(_thread_config(run_id)).values
    except Exception as exc:  # noqa: BLE001 - surface any node/LLM/ADT failure as a failed run
        logger.exception("Pipeline run %s failed during trigger", run_id)
        upsert_run(run_id, status="failed", error=str(exc))
        raise HTTPException(status_code=500, detail=f"Pipeline run failed: {exc}") from exc

    status = result.get("status", "unknown")
    upsert_run(run_id, status=status)
    return {"run_id": run_id, "status": status}


@app.get("/pipeline/{run_id}/status")
async def pipeline_status(run_id: str) -> dict:
    run = get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Unknown run_id")
    return run


@app.post("/pipeline/{run_id}/approve/gate1")
async def approve_gate_1(approval: ApprovalRequest) -> dict:
    """Approve or reject the generated FS/TS at human gate 1, then resume."""
    run_id = approval.run_id
    if get_run(run_id) is None:
        raise HTTPException(status_code=404, detail="Unknown run_id")

    pipeline_graph.update_state(
        _thread_config(run_id),
        {"gate_1_approved": approval.approved, "gate_1_comments": approval.comments},
    )

    if not approval.approved:
        upsert_run(run_id, status="rejected_at_gate_1", gate_1_comments=approval.comments)
        return {"run_id": run_id, "status": "rejected_at_gate_1"}

    try:
        # `invoke(None, ...)` resumes a LangGraph run from its last checkpoint
        # for the given thread_id (the update_state call above already staged
        # the gate 1 approval into that checkpoint). Passing `None` (instead
        # of a new input state) is LangGraph's documented signal to resume an
        # interrupted graph rather than start a fresh run — see
        # https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/
        result = pipeline_graph.invoke(None, config=_thread_config(run_id))
    except GraphInterrupt:
        result = pipeline_graph.get_state(_thread_config(run_id)).values
    except Exception as exc:  # noqa: BLE001 - surface any node/LLM/ADT failure as a failed run
        logger.exception("Pipeline run %s failed while resuming past gate 1", run_id)
        upsert_run(run_id, status="failed", error=str(exc))
        raise HTTPException(status_code=500, detail=f"Pipeline run failed: {exc}") from exc

    status = result.get("status", "unknown")
    upsert_run(run_id, status=status)
    return {"run_id": run_id, "status": status}


@app.post("/pipeline/{run_id}/approve/gate2")
async def approve_gate_2(approval: ApprovalRequest) -> dict:
    """Resume the graph past human gate 2 and mark developer review outcome."""
    run_id = approval.run_id
    if get_run(run_id) is None:
        raise HTTPException(status_code=404, detail="Unknown run_id")

    pipeline_graph.update_state(
        _thread_config(run_id),
        {"gate_2_approved": approval.approved, "gate_2_comments": approval.comments},
    )

    # Resumes from the checkpointed state (see comment in approve_gate_1).
    try:
        result = pipeline_graph.invoke(None, config=_thread_config(run_id))
    except Exception as exc:  # noqa: BLE001 - surface any node/LLM/ADT failure as a failed run
        logger.exception("Pipeline run %s failed while resuming past gate 2", run_id)
        upsert_run(run_id, status="failed", error=str(exc))
        raise HTTPException(status_code=500, detail=f"Pipeline run failed: {exc}") from exc

    status = result.get("status", "unknown")
    upsert_run(run_id, status=status)
    return {"run_id": run_id, "status": status}


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
