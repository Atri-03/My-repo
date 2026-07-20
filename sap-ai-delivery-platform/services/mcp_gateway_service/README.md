# MCP Gateway Service

Exposes platform capabilities (knowledge search, artefact retrieval, workflow state) as MCP-style HTTP tools, proxying to backing services.

## Run locally

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8011
```

OpenAPI docs available at `http://localhost:8011/docs` and
raw schema at `http://localhost:8011/openapi.json`.

## Tests

```bash
pytest
```

## Migrations

```bash
alembic upgrade head
```
