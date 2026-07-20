"""SAP Execution MCP tool: package creation."""
from __future__ import annotations

from typing import Any, Dict

from app.core.config import get_settings
from app.mcp.registry import mcp_tool
from app.mcp.sap_execution_client import SAPExecutionClient
from app.mcp.tool_schemas import CreatePackageInput


@mcp_tool(
    name="create_package",
    description="Create an ABAP development package in the target SAP system.",
    input_model=CreatePackageInput,
    category="package-management",
)
async def create_package(payload: CreatePackageInput) -> Dict[str, Any]:
    client = SAPExecutionClient(get_settings())
    return await client.post("/api/v1/packages", payload.model_dump(exclude_none=True))
