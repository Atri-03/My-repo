"""SAP Execution MCP tool: RAP (RESTful ABAP Programming) business object generation."""
from __future__ import annotations

from typing import Any, Dict

from app.core.config import get_settings
from app.mcp.registry import mcp_tool
from app.mcp.sap_execution_client import SAPExecutionClient
from app.mcp.tool_schemas import GenerateRAPInput


@mcp_tool(
    name="generate_rap",
    description="Generate a RAP business object (behavior definition/implementation + optional projection).",
    input_model=GenerateRAPInput,
    category="rap-generation",
)
async def generate_rap(payload: GenerateRAPInput) -> Dict[str, Any]:
    client = SAPExecutionClient(get_settings())
    return await client.post("/api/v1/rap-business-objects", payload.model_dump(exclude_none=True))
