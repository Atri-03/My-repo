# TS Service

Generates and versions Technical Specifications from Functional Specifications.

## Run locally

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8004
```

OpenAPI docs available at `http://localhost:8004/docs` and
raw schema at `http://localhost:8004/openapi.json`.

## Tests

```bash
pytest
```

## Migrations

```bash
alembic upgrade head
```
