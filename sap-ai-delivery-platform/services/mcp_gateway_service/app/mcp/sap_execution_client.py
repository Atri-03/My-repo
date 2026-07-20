"""HTTP client wrapping the backing SAP execution system/service.

The actual SAP Execution Repository (ABAP/RAP/CDS/OData generation, ATC,
transports, etc.) lives outside this platform's codebase - see
`docs/architecture/11-mcp-integration-architecture.md` §11.5. This client is
the single integration seam MCP tool wrappers use to call out to that system
(or to a facade service in front of it), configured via
`settings.sap_execution_service_url`.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

import httpx
from fastapi import HTTPException

from app.core.config import Settings


class SAPExecutionClient:
    """Thin async HTTP wrapper around the SAP execution backend."""

    def __init__(self, settings: Settings):
        self._base_url = settings.sap_execution_service_url.rstrip("/")
        self._timeout = settings.request_timeout_seconds

    async def post(self, path: str, payload: Dict[str, Any]) -> Any:
        return await self._request("POST", path, json=payload)

    async def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return await self._request("GET", path, params=params)

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            try:
                resp = await client.request(method, f"{self._base_url}{path}", json=json, params=params)
            except httpx.HTTPError as exc:
                raise HTTPException(
                    status_code=502, detail=f"SAP execution backend request failed: {exc}"
                ) from exc
        if resp.status_code >= 400:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        if not resp.content:
            return {}
        return resp.json()
