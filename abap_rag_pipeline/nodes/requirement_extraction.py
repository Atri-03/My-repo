"""Node 2: requirement_extraction.

Sends transcript chunks to Azure OpenAI (GPT-4o) with a prompt that extracts
structured requirements as JSON, using similar past FS/TS documents retrieved
from ChromaDB as few-shot context.
"""
from __future__ import annotations

from pydantic import ValidationError

from models.schemas import StructuredRequirements
from nodes.state import PipelineState
from services.azure_openai_client import chat_completion_json
from services.chroma_client import retrieve_similar_examples

_SYSTEM_PROMPT = """You are an SAP business analyst assistant. Extract structured \
functional requirements from a meeting transcript discussing an SAP change request.

Return ONLY a JSON object with these keys:
- title: short descriptive title
- summary: 2-3 sentence summary of the requirement
- process_flow: list of {step_number, description, actor}
- fields: list of {name, description, data_type, mandatory, source}
- validations: list of {description, applies_to, error_message}
- actors: list of {name, responsibility}
- open_questions: list of strings for anything ambiguous or unresolved

Use the provided examples only as a guide for the level of detail and style \
expected; do not copy their content."""


def _build_user_prompt(chunks: list[str], examples: list[str]) -> str:
    transcript_text = "\n\n".join(chunks)
    examples_text = "\n\n---\n\n".join(examples)
    return (
        f"### Similar past FS/TS examples (style/context reference only)\n"
        f"{examples_text}\n\n"
        f"### Meeting transcript\n{transcript_text}\n\n"
        "Extract the structured requirements JSON now."
    )


def requirement_extraction(state: PipelineState) -> PipelineState:
    chunks = state.get("chunks", [])
    query_text = " ".join(chunks)[:4000] if chunks else ""

    examples = retrieve_similar_examples(query_text, n_results=2)
    user_prompt = _build_user_prompt(chunks, examples)

    raw_json = chat_completion_json(_SYSTEM_PROMPT, user_prompt)

    # Validate/normalize through the Pydantic model; fall back to an empty
    # skeleton if the LLM response could not be parsed (e.g. no API key
    # configured yet during local scaffolding).
    try:
        requirements = StructuredRequirements(**raw_json)
    except (ValidationError, TypeError):
        requirements = StructuredRequirements(
            title="Untitled Requirement",
            summary="Requirement extraction failed to parse LLM output.",
            open_questions=["LLM response could not be parsed as valid structured requirements."],
        )

    return {
        **state,
        "requirements": requirements.model_dump(),
        "status": "requirements_extracted",
    }
