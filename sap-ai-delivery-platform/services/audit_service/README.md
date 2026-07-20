# Audit Service

Append-only audit log of entity changes across the platform.

## Run locally

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8007
```

OpenAPI docs available at `http://localhost:8007/docs` and
raw schema at `http://localhost:8007/openapi.json`.

## Tests

```bash
pytest
```

## Migrations

```bash
alembic upgrade head
```
