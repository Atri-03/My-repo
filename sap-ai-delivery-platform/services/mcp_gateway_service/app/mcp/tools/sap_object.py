"""SAP Execution MCP tool: generic ABAP object generation."""
from __future__ import annotations

from typing import Any, Dict

from app.core.config import get_settings
from app.mcp.registry import mcp_tool
from app.mcp.sap_execution_client import SAPExecutionClient
from app.mcp.tool_schemas import GenerateObjectInput


@mcp_tool(
    name="generate_object",
    description="Generate (create/update source of) a generic ABAP repository object, e.g. a program or class.",
    input_model=GenerateObjectInput,
    category="object-generation",
)
async def generate_object(payload: GenerateObjectInput) -> Dict[str, Any]:
    client = SAPExecutionClient(get_settings())
    return await client.post("/api/v1/objects", payload.model_dump(exclude_none=True))
