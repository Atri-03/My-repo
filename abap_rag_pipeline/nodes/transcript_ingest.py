"""Node 1: transcript_ingest.

Accepts a raw transcript text file path, cleans it, and chunks it for
downstream LLM processing. Real Teams Graph API ingestion is stubbed in
services.teams_graph_client and is NOT wired in here yet.
"""
from __future__ import annotations

import re

from nodes.state import PipelineState

_CHUNK_SIZE_CHARS = 2000
_CHUNK_OVERLAP_CHARS = 200


def _clean_transcript(raw_text: str) -> str:
    """Strip Teams-style timestamps/speaker noise artifacts and collapse whitespace."""
    text = re.sub(r"\r\n?", "\n", raw_text)
    # Remove common Teams transcript timestamp patterns like [00:01:23]
    text = re.sub(r"\[\d{2}:\d{2}:\d{2}(\.\d+)?\]", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _chunk_text(text: str, chunk_size: int = _CHUNK_SIZE_CHARS, overlap: int = _CHUNK_OVERLAP_CHARS) -> list[str]:
    if len(text) <= chunk_size:
        return [text] if text else []

    overlap = min(overlap, chunk_size - 1)  # guard against overlap >= chunk_size
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(end - overlap, start + 1)  # always make forward progress
    return chunks


def transcript_ingest(state: PipelineState) -> PipelineState:
    """Load, clean, and chunk the transcript referenced by `transcript_path`."""
    transcript_path = state["transcript_path"]
    with open(transcript_path, "r", encoding="utf-8") as fh:
        raw_text = fh.read()

    cleaned = _clean_transcript(raw_text)
    chunks = _chunk_text(cleaned)

    return {
        **state,
        "raw_transcript": cleaned,
        "chunks": chunks,
        "status": "ingested",
    }


# TODO: implement Teams Graph API ingestion path, e.g.:
# def transcript_ingest_from_teams(state: PipelineState, meeting_id: str) -> PipelineState:
#     from services.teams_graph_client import fetch_teams_transcript
#     raw_text = fetch_teams_transcript(meeting_id)
#     ...
