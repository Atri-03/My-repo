"""Node 4: HUMAN GATE 1.

Pauses the pipeline (LangGraph interrupt) until a reviewer approves the
generated FS/TS documents. The actual interrupt is configured on the graph
via `interrupt_before=["human_gate_1"]` in app.graph; this node simply
validates/records the incoming approval decision once execution resumes.
"""
from __future__ import annotations

from nodes.state import PipelineState
from services.tracker_store import upsert_run


def human_gate_1(state: PipelineState) -> PipelineState:
    """Runs once the graph resumes after gate 1's interrupt.

    Expects `gate_1_approved` (and optionally `gate_1_comments`) to already be
    present in state, set via the FastAPI `/pipeline/{run_id}/approve/gate1`
    endpoint before resuming the graph.
    """
    approved = state.get("gate_1_approved", False)
    upsert_run(
        state["run_id"],
        status="gate_1_approved" if approved else "awaiting_gate_1_approval",
        gate_1_approved=approved,
        gate_1_comments=state.get("gate_1_comments"),
    )

    return {
        **state,
        "status": "gate_1_approved" if approved else "awaiting_gate_1_approval",
    }
