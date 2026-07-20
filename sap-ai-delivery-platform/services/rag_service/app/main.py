"""FastAPI application entrypoint."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.v1.routes import router as v1_router
from app.db.base import Base, engine
from app.db import models  # noqa: F401  (ensures models are registered on Base)

settings = get_settings()

# Tables are managed by Alembic migrations; create_all is a safety net for local/dev use.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RAG Service",
    description="Manages knowledge sources/chunks metadata backing enterprise RAG search.",
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


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "service": "rag_service"}

