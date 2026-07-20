# User Service

Manages tenants, projects and users.

## Run locally

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8009
```

OpenAPI docs available at `http://localhost:8009/docs` and
raw schema at `http://localhost:8009/openapi.json`.

## Tests

```bash
pytest
```

## Migrations

```bash
alembic upgrade head
```
