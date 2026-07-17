"""Node 6: HUMAN GATE 2.

Logs the created ADT object name/package and marks the run as "pending
developer review" in the JSON tracker file. This gate is a logging/notify
checkpoint rather than a blocking content approval: the graph still pauses
here (see interrupt_before in app.graph) so a caller can explicitly resume it
once ready, but the node itself always records the object as pending review.
If a developer marks `gate_2_approved`, the run is additionally flagged as
reviewed/closed-out in the tracker.
"""
from __future__ import annotations

from nodes.state import PipelineState
from services.tracker_store import upsert_run


def human_gate_2(state: PipelineState) -> PipelineState:
    adt_result = state.get("adt_result", {})
    approved = state.get("gate_2_approved", False)

    upsert_run(
        state["run_id"],
        status="gate_2_approved" if approved else "awaiting_gate_2_review",
        abap_object_name=state.get("abap_object_name"),
        adt_package=adt_result.get("package"),
        adt_status_code=adt_result.get("status_code"),
        pending_developer_review=not approved,
        gate_2_comments=state.get("gate_2_comments"),
    )

    return {
        **state,
        "status": "gate_2_approved" if approved else "awaiting_gate_2_review",
    }
