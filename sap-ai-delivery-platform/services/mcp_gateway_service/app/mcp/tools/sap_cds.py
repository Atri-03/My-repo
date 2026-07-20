"""SAP Execution MCP tool: CDS (Core Data Services) view generation."""
from __future__ import annotations

from typing import Any, Dict

from app.core.config import get_settings
from app.mcp.registry import mcp_tool
from app.mcp.sap_execution_client import SAPExecutionClient
from app.mcp.tool_schemas import GenerateCDSInput


@mcp_tool(
    name="generate_cds",
    description="Generate a CDS view (DDL source + annotations) in the target SAP system.",
    input_model=GenerateCDSInput,
    category="cds-generation",
)
async def generate_cds(payload: GenerateCDSInput) -> Dict[str, Any]:
    client = SAPExecutionClient(get_settings())
    return await client.post("/api/v1/cds-views", payload.model_dump(exclude_none=True))
