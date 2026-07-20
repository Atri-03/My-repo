"""FastAPI application entrypoint."""
from fastapi import FastAPI

from app.core.config import get_settings
from app.api.v1.routes import router as v1_router
from app.db.base import Base, engine
from app.db import models  # noqa: F401  (ensures models are registered on Base)

settings = get_settings()

# Tables are managed by Alembic migrations; create_all is a safety net for local/dev use.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FS Service",
    description="Generates and versions Functional Specifications from requirement sets.",
    version="1.0.0",
)

app.include_router(v1_router, prefix=settings.api_v1_prefix)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "service": "fs_service"}

