"""Unit tests for the dynamic MCP capability registry."""
import pytest
from pydantic import BaseModel

from app.mcp.registry import (
    MCPRegistry,
    ToolAlreadyRegisteredError,
    ToolNotFoundError,
    ToolSpec,
    discover_tools,
    get_registry,
    mcp_tool,
)


class _DummyInput(BaseModel):
    value: str


async def _dummy_handler(payload: _DummyInput):
    return {"echo": payload.value}


def test_register_and_get():
    registry = MCPRegistry()
    spec = ToolSpec(
        name="dummy_tool",
        description="A dummy tool",
        category="testing",
        input_model=_DummyInput,
        handler=_dummy_handler,
    )
    registry.register(spec)
    assert registry.get("dummy_tool") is spec


def test_register_duplicate_raises():
    registry = MCPRegistry()
    spec = ToolSpec(
        name="dummy_tool",
        description="A dummy tool",
        category="testing",
        input_model=_DummyInput,
        handler=_dummy_handler,
    )
    registry.register(spec)
    with pytest.raises(ToolAlreadyRegisteredError):
        registry.register(spec)


def test_register_overwrite_allowed():
    registry = MCPRegistry()
    spec = ToolSpec(
        name="dummy_tool",
        description="A dummy tool",
        category="testing",
        input_model=_DummyInput,
        handler=_dummy_handler,
    )
    registry.register(spec)
    registry.register(spec, overwrite=True)


def test_get_missing_tool_raises():
    registry = MCPRegistry()
    with pytest.raises(ToolNotFoundError):
        registry.get("missing")


def test_list_tools_sorted():
    registry = MCPRegistry()
    for name in ["zebra", "alpha", "mango"]:
        registry.register(
            ToolSpec(
                name=name,
                description="d",
                category="testing",
                input_model=_DummyInput,
                handler=_dummy_handler,
            )
        )
    names = [spec.name for spec in registry.list_tools()]
    assert names == ["alpha", "mango", "zebra"]


def test_as_capability_includes_input_schema():
    spec = ToolSpec(
        name="dummy_tool",
        description="A dummy tool",
        category="testing",
        input_model=_DummyInput,
        handler=_dummy_handler,
    )
    capability = spec.as_capability()
    assert capability["name"] == "dummy_tool"
    assert "value" in capability["input_schema"]["properties"]


def test_discover_tools_registers_all_sap_execution_tools():
    # discover_tools imports every module under app.mcp.tools, which register
    # themselves against the shared global registry via @mcp_tool.
    discover_tools()
    registry = get_registry()
    tool_names = {spec.name for spec in registry.list_tools()}
    expected = {
        "create_package",
        "create_transport",
        "release_transport",
        "generate_object",
        "generate_rap",
        "generate_cds",
        "generate_odata",
        "activate_object",
        "run_unit_tests",
        "run_atc",
        "remediate_atc_findings",
    }
    assert expected.issubset(tool_names)


def test_mcp_tool_decorator_registers_on_global_registry():
    @mcp_tool(name="temp_test_tool", description="temp", input_model=_DummyInput, category="testing")
    async def handler(payload: _DummyInput):
        return {"value": payload.value}

    registry = get_registry()
    assert registry.get("temp_test_tool").handler is handler
