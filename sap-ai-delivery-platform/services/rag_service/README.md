# RAG Service

Manages knowledge sources/chunks metadata backing enterprise RAG search.

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
