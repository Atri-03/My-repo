"""Best-effort audit trail client for the governance framework.

Every gate configuration change, approval request, and decision is recorded
via the Audit Service so the full human-in-the-loop trail is independently
auditable outside of this service's own tables. Recording is best-effort: a
failure to reach the Audit Service must never fail (or mask the result of)
the underlying gate operation, but is logged loudly so operators can notice
a broken audit pipeline.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import httpx

from app.core.config import Settings

logger = logging.getLogger("approval_service.audit")


async def record_governance_event(
    settings: Settings,
    *,
    tenant_id: str,
    entity_type: str,
    entity_id: str,
    action: str,
    actor: str,
    before: Optional[Dict[str, Any]] = None,
    after: Optional[Dict[str, Any]] = None,
) -> None:
    entry = {
        "tenant_id": tenant_id,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "action": action,
        "actor": actor,
        "before": before,
        "after": after,
        "occurred_at": datetime.now(timezone.utc).isoformat(),
    }
    async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
        try:
            resp = await client.post(
                f"{settings.audit_service_url}/api/v1/audit-log-entries", json=entry
            )
            resp.raise_for_status()
        except Exception as exc:  # noqa: BLE001 - audit failures must never break gate operations
            logger.error(
                "Failed to record governance audit trail for action=%s entity_id=%s: %s",
                action,
                entity_id,
                exc,
            )
