"""SAP Execution MCP tools: ATC (ABAP Test Cockpit) execution and remediation."""
from __future__ import annotations

from typing import Any, Dict

from app.core.config import get_settings
from app.mcp.registry import mcp_tool
from app.mcp.sap_execution_client import SAPExecutionClient
from app.mcp.tool_schemas import RemediateATCInput, RunATCInput


@mcp_tool(
    name="run_atc",
    description="Run an ABAP Test Cockpit (ATC) check run against an object using the given check variant.",
    input_model=RunATCInput,
    category="atc",
)
async def run_atc(payload: RunATCInput) -> Dict[str, Any]:
    client = SAPExecutionClient(get_settings())
    return await client.post("/api/v1/atc-runs", payload.model_dump(exclude_none=True))


@mcp_tool(
    name="remediate_atc_findings",
    description="Apply (or propose) remediations for a set of ATC findings raised against an object.",
    input_model=RemediateATCInput,
    category="atc",
)
async def remediate_atc_findings(payload: RemediateATCInput) -> Dict[str, Any]:
    client = SAPExecutionClient(get_settings())
    return await client.post("/api/v1/atc-remediations", payload.model_dump(exclude_none=True))
