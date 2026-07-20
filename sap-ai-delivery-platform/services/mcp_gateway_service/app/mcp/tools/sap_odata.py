"""SAP Execution MCP tool: OData service generation/exposure."""
from __future__ import annotations

from typing import Any, Dict

from app.core.config import get_settings
from app.mcp.registry import mcp_tool
from app.mcp.sap_execution_client import SAPExecutionClient
from app.mcp.tool_schemas import GenerateODataInput


@mcp_tool(
    name="generate_odata",
    description="Generate and expose an OData service (v2 or v4) for a CDS view or RAP business object.",
    input_model=GenerateODataInput,
    category="odata-generation",
)
async def generate_odata(payload: GenerateODataInput) -> Dict[str, Any]:
    client = SAPExecutionClient(get_settings())
    return await client.post("/api/v1/odata-services", payload.model_dump(exclude_none=True))
