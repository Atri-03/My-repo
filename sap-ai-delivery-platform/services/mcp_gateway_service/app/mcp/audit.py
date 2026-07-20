"""Audit trail recording for every MCP tool invocation.

Every call made through the dynamic MCP dispatcher (`app/api/v1/mcp_routes.py`)
is recorded here. Recording is best-effort: a failure to reach the audit
service must never fail (or mask the result of) the underlying tool call, but
is logged loudly so operators can notice a broken audit pipeline.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import httpx

from app.core.config import Settings

logger = logging.getLogger("mcp_gateway.audit")


async def record_tool_call(
    settings: Settings,
    *,
    tool_name: str,
    actor: str,
    tenant_id: str,
    status: str,
    input_payload: Dict[str, Any],
    output_payload: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None,
    correlation_id: Optional[str] = None,
) -> str:
    """Persist an audit log entry for an MCP tool call via the audit service.

    Returns the correlation id used for this audit entry (generated if not
    supplied) so callers can surface it to clients for traceability.
    """
    correlation_id = correlation_id or str(uuid.uuid4())
    entry = {
        "tenant_id": tenant_id,
        "entity_type": "mcp_tool_call",
        "entity_id": correlation_id,
        "action": tool_name,
        "actor": actor,
        "before": {"input": input_payload},
        "after": {"status": status, "output": output_payload, "error": error},
        "occurred_at": datetime.now(timezone.utc).isoformat(),
    }

    async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
        try:
            resp = await client.post(
                f"{settings.audit_service_url}/api/v1/audit-log-entries", json=entry
            )
            resp.raise_for_status()
        except Exception as exc:  # noqa: BLE001 - audit failures must never break tool calls
            logger.error(
                "Failed to record MCP audit trail for tool=%s correlation_id=%s: %s",
                tool_name,
                correlation_id,
                exc,
            )

    return correlation_id
