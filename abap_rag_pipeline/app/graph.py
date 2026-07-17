"""LangGraph state machine wiring the pipeline nodes together, with explicit
human-in-the-loop interrupts before each human gate.
"""
from __future__ import annotations

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from nodes.abap_code_generation import abap_code_generation
from nodes.fs_ts_generation import fs_ts_generation
from nodes.human_gate_1 import human_gate_1
from nodes.human_gate_2 import human_gate_2
from nodes.requirement_extraction import requirement_extraction
from nodes.state import PipelineState
from nodes.transcript_ingest import transcript_ingest

# A single shared in-memory checkpointer so runs can be paused at the human
# gates and resumed later via the FastAPI approval endpoints. For a real
# deployment, swap MemorySaver for a persistent checkpointer (SQLite/Postgres).
_checkpointer = MemorySaver()


def build_graph():
    graph = StateGraph(PipelineState)

    graph.add_node("transcript_ingest", transcript_ingest)
    graph.add_node("requirement_extraction", requirement_extraction)
    graph.add_node("fs_ts_generation", fs_ts_generation)
    graph.add_node("human_gate_1", human_gate_1)
    graph.add_node("abap_code_generation", abap_code_generation)
    graph.add_node("human_gate_2", human_gate_2)

    graph.set_entry_point("transcript_ingest")
    graph.add_edge("transcript_ingest", "requirement_extraction")
    graph.add_edge("requirement_extraction", "fs_ts_generation")
    graph.add_edge("fs_ts_generation", "human_gate_1")
    graph.add_edge("human_gate_1", "abap_code_generation")
    graph.add_edge("abap_code_generation", "human_gate_2")
    graph.add_edge("human_gate_2", END)

    # Interrupt BEFORE each human gate node so the graph pauses and waits for
    # an external approval call (via the FastAPI endpoints) before resuming.
    return graph.compile(
        checkpointer=_checkpointer,
        interrupt_before=["human_gate_1", "human_gate_2"],
    )


pipeline_graph = build_graph()
