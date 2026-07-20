"""FastAPI application entrypoint for the MCP Gateway Service."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.mcp_routes import router as mcp_router
from app.api.v1.routes import router as v1_router
from app.core.config import get_settings
from app.mcp.registry import discover_tools

settings = get_settings()

# Populate the dynamic MCP capability registry by importing every tool
# module under app/mcp/tools. No tool name is hardcoded here - new tool
# modules are picked up automatically without touching this file.
discover_tools()

app = FastAPI(
    title="MCP Gateway Service",
    description=(
        "Exposes platform capabilities (knowledge search, artefact retrieval, "
        "workflow state) and SAP execution capabilities (package creation, "
        "transport management, object/RAP/CDS/OData generation, activation, "
        "unit testing, ATC) as MCP-style HTTP tools via a dynamic capability "
        "registry, proxying to backing services."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix=settings.api_v1_prefix)
app.include_router(mcp_router, prefix=settings.api_v1_prefix)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "service": "mcp_gateway_service"}
