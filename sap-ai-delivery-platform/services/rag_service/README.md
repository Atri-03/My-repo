# RAG Service

Manages knowledge sources/chunks metadata backing enterprise RAG search.

## Enterprise Knowledge Brain

`GET /api/v1/knowledge-source-types` lists the platform's documented
knowledge categories (`app/core/knowledge_source_types.py`) for the
Knowledge Management UI:

Past BRDs, Past FS, Past TS, Past RAP Projects, Past CDS Views, Past Fiori
Apps, Review Comments, Approved Architect Decisions, Naming Standards, ATC
Findings, Reusable Components, SAP Standards.

`KnowledgeSource.source_type` remains a free-form string so new categories
can be ingested without a schema migration; this endpoint is the canonical,
documented list rather than a hard constraint.

## Run locally

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8008
```

OpenAPI docs available at `http://localhost:8008/docs` and
raw schema at `http://localhost:8008/openapi.json`.

## Tests

```bash
pytest
```

## Migrations

```bash
alembic upgrade head
```
