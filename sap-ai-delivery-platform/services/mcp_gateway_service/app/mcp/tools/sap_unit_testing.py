"""SAP Execution MCP tool: ABAP Unit testing."""
from __future__ import annotations

from typing import Any, Dict

from app.core.config import get_settings
from app.mcp.registry import mcp_tool
from app.mcp.sap_execution_client import SAPExecutionClient
from app.mcp.tool_schemas import RunUnitTestsInput


@mcp_tool(
    name="run_unit_tests",
    description="Run ABAP Unit tests for an object (optionally scoped to specific test classes).",
    input_model=RunUnitTestsInput,
    category="unit-testing",
)
async def run_unit_tests(payload: RunUnitTestsInput) -> Dict[str, Any]:
    client = SAPExecutionClient(get_settings())
    return await client.post("/api/v1/unit-test-runs", payload.model_dump(exclude_none=True))
