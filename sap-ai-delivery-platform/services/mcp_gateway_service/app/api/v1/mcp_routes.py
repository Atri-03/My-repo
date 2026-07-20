"""Dynamic MCP tool discovery, capability listing, and invocation endpoints.

These routes never hardcode individual tool names: the list of available
tools comes entirely from the dynamic :mod:`app.mcp.registry`, which is
populated by importing every module under ``app.mcp.tools`` at startup (see
``discover_tools``). Adding a new SAP execution capability (or any other MCP
tool) only requires adding a new module there - this router, and the gateway
API surface it exposes, automatically picks it up.
"""
from __future__ import annotations

import time
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import ValidationError

from app.core.config import Settings, get_settings
from app.mcp.audit import record_tool_call
from app.mcp.registry import ToolNotFoundError, get_registry

router = APIRouter(prefix="/mcp", tags=["mcp"])


@router.get("/tools")
async def list_tools() -> Dict[str, Any]:
    """Return the full dynamic MCP capability registry."""
    registry = get_registry()
    return {"tools": [spec.as_capability() for spec in registry.list_tools()]}


@router.get("/tools/{tool_name}")
async def get_tool(tool_name: str) -> Dict[str, Any]:
    registry = get_registry()
    try:
        spec = registry.get(tool_name)
    except ToolNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"MCP tool '{tool_name}' not found") from exc
    return spec.as_capability()


@router.post("/tools/{tool_name}/invoke")
async def invoke_tool(
    tool_name: str,
    request: Request,
    payload: Dict[str, Any],
    settings: Settings = Depends(get_settings),
) -> Dict[str, Any]:
    """Validate, invoke, and audit-log a call to any registered MCP tool."""
    registry = get_registry()
    try:
        spec = registry.get(tool_name)
    except ToolNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"MCP tool '{tool_name}' not found") from exc

    actor = request.headers.get("X-Actor", "unknown")
    tenant_id = request.headers.get("X-Tenant-Id", "unknown")

    try:
        validated = spec.input_model.model_validate(payload)
    except ValidationError as exc:
        await record_tool_call(
            settings,
            tool_name=tool_name,
            actor=actor,
            tenant_id=tenant_id,
            status="VALIDATION_ERROR",
            input_payload=payload,
            error=str(exc),
        )
        raise HTTPException(status_code=422, detail=exc.errors()) from exc

    start = time.monotonic()
    try:
        result = await spec.handler(validated)
    except HTTPException as exc:
        await record_tool_call(
            settings,
            tool_name=tool_name,
            actor=actor,
            tenant_id=tenant_id,
            status="ERROR",
            input_payload=payload,
            error=str(exc.detail),
        )
        raise
    except Exception as exc:  # noqa: BLE001 - ensure all failures are audited
        await record_tool_call(
            settings,
            tool_name=tool_name,
            actor=actor,
            tenant_id=tenant_id,
            status="ERROR",
            input_payload=payload,
            error=str(exc),
        )
        raise HTTPException(status_code=500, detail=f"MCP tool '{tool_name}' failed: {exc}") from exc

    duration_ms = int((time.monotonic() - start) * 1000)
    correlation_id = await record_tool_call(
        settings,
        tool_name=tool_name,
        actor=actor,
        tenant_id=tenant_id,
        status="SUCCESS",
        input_payload=payload,
        output_payload=result,
    )

    return {
        "tool": tool_name,
        "correlation_id": correlation_id,
        "duration_ms": duration_ms,
        "result": result,
    }
