"""Thin wrapper around the Azure OpenAI (GPT-4o) chat completion API."""
from __future__ import annotations

import json
from typing import Any

from openai import AzureOpenAI

from app.config import settings


def get_client() -> AzureOpenAI:
    """Build an AzureOpenAI SDK client from configured settings.

    TODO: swap in a real key vault / managed identity lookup for production use.
    """
    return AzureOpenAI(
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version,
        azure_endpoint=settings.azure_openai_endpoint,
    )


def chat_completion(
    system_prompt: str,
    user_prompt: str,
    *,
    temperature: float = 0.2,
    response_format_json: bool = False,
) -> str:
    """Call the configured GPT-4o deployment and return the raw text response."""
    client = get_client()
    kwargs: dict[str, Any] = {}
    if response_format_json:
        kwargs["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(
        model=settings.azure_openai_deployment,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        **kwargs,
    )
    return response.choices[0].message.content or ""


def chat_completion_json(system_prompt: str, user_prompt: str) -> dict[str, Any]:
    """Call chat_completion and parse the result as JSON.

    Falls back to an empty dict if the model output is not valid JSON, which can
    happen with smaller/mock models used during local development.
    """
    raw = chat_completion(system_prompt, user_prompt, response_format_json=True)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}
