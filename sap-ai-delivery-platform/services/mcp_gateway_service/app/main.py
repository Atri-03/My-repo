"""FastAPI application entrypoint for the MCP Gateway Service."""
from fastapi import FastAPI

from app.api.v1.routes import router as v1_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="MCP Gateway Service",
    description=(
        "Exposes platform capabilities (knowledge search, artefact retrieval, "
        "workflow state) as MCP-style HTTP tools, proxying to backing services."
    ),
    version="1.0.0",
)

app.include_router(v1_router, prefix=settings.api_v1_prefix)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "service": "mcp_gateway_service"}
