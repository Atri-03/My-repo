"""SAP Execution MCP tools: transport management."""
from __future__ import annotations

from typing import Any, Dict

from app.core.config import get_settings
from app.mcp.registry import mcp_tool
from app.mcp.sap_execution_client import SAPExecutionClient
from app.mcp.tool_schemas import CreateTransportInput, ReleaseTransportInput


@mcp_tool(
    name="create_transport",
    description="Create a transport request (workbench or customizing) in the target SAP system.",
    input_model=CreateTransportInput,
    category="transport-management",
)
async def create_transport(payload: CreateTransportInput) -> Dict[str, Any]:
    client = SAPExecutionClient(get_settings())
    return await client.post("/api/v1/transports", payload.model_dump(exclude_none=True))


@mcp_tool(
    name="release_transport",
    description="Release a transport request so it can be moved along the transport route.",
    input_model=ReleaseTransportInput,
    category="transport-management",
)
async def release_transport(payload: ReleaseTransportInput) -> Dict[str, Any]:
    client = SAPExecutionClient(get_settings())
    return await client.post(
        f"/api/v1/transports/{payload.transport_request}/release", payload.model_dump(exclude_none=True)
    )
