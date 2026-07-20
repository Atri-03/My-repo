"""SAP Execution MCP tool: object activation."""
from __future__ import annotations

from typing import Any, Dict

from app.core.config import get_settings
from app.mcp.registry import mcp_tool
from app.mcp.sap_execution_client import SAPExecutionClient
from app.mcp.tool_schemas import ActivateObjectInput


@mcp_tool(
    name="activate_object",
    description="Activate an inactive ABAP repository object (program, class, CDS view, behavior definition, etc.).",
    input_model=ActivateObjectInput,
    category="activation",
)
async def activate_object(payload: ActivateObjectInput) -> Dict[str, Any]:
    client = SAPExecutionClient(get_settings())
    return await client.post("/api/v1/activations", payload.model_dump(exclude_none=True))
