"""Dynamic MCP capability registry.

Tools are never hardcoded into the gateway's routing layer. Instead, each
tool module under ``app.mcp.tools`` registers itself with the shared
:class:`MCPRegistry` singleton via the :func:`mcp_tool` decorator at import
time. ``discover_tools`` walks the ``app.mcp.tools`` package and imports every
module it finds, so dropping a new ``*.py`` file into that package (with a
``@mcp_tool`` decorated handler) is enough for the gateway to expose it -
no route, schema registration, or dispatcher changes required.

This makes the gateway's tool surface -- and therefore its ability to support
future MCP tools -- entirely data-driven.
"""
from __future__ import annotations

import importlib
import pkgutil
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, List, Optional, Type

from pydantic import BaseModel

ToolHandler = Callable[[BaseModel], Awaitable[Dict[str, Any]]]


@dataclass(frozen=True)
class ToolSpec:
    """Metadata + handler describing a single MCP capability."""

    name: str
    description: str
    category: str
    input_model: Type[BaseModel]
    handler: ToolHandler

    def input_schema(self) -> Dict[str, Any]:
        return self.input_model.model_json_schema()

    def as_capability(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "input_schema": self.input_schema(),
        }


class ToolAlreadyRegisteredError(RuntimeError):
    pass


class ToolNotFoundError(KeyError):
    pass


@dataclass
class MCPRegistry:
    """In-memory registry of dynamically discovered MCP tools."""

    _tools: Dict[str, ToolSpec] = field(default_factory=dict)

    def register(self, spec: ToolSpec, *, overwrite: bool = False) -> None:
        if not overwrite and spec.name in self._tools:
            raise ToolAlreadyRegisteredError(f"MCP tool '{spec.name}' is already registered")
        self._tools[spec.name] = spec

    def get(self, name: str) -> ToolSpec:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise ToolNotFoundError(name) from exc

    def list_tools(self) -> List[ToolSpec]:
        return sorted(self._tools.values(), key=lambda t: t.name)

    def clear(self) -> None:
        self._tools.clear()


registry = MCPRegistry()


def mcp_tool(
    name: str,
    description: str,
    input_model: Type[BaseModel],
    category: str = "general",
) -> Callable[[ToolHandler], ToolHandler]:
    """Decorator that registers ``handler`` as an MCP tool on import.

    Any module under ``app.mcp.tools`` that decorates a coroutine function
    with ``@mcp_tool(...)`` is automatically picked up by ``discover_tools``
    with no further wiring.
    """

    def decorator(handler: ToolHandler) -> ToolHandler:
        registry.register(
            ToolSpec(
                name=name,
                description=description,
                category=category,
                input_model=input_model,
                handler=handler,
            ),
            overwrite=True,
        )
        return handler

    return decorator


def discover_tools(package_name: str = "app.mcp.tools") -> List[str]:
    """Import every module in ``package_name`` so its ``@mcp_tool`` handlers register.

    Returns the list of imported module names. Safe to call multiple times
    (e.g. on app startup and again in tests) - already-imported modules are
    simply re-used by Python's import cache.
    """
    package = importlib.import_module(package_name)
    imported: List[str] = []
    for module_info in pkgutil.iter_modules(package.__path__, prefix=f"{package_name}."):
        importlib.import_module(module_info.name)
        imported.append(module_info.name)
    return imported


def get_registry() -> MCPRegistry:
    return registry
