# FS Service

Generates and versions Functional Specifications from requirement sets.

## Run locally

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8003
```

OpenAPI docs available at `http://localhost:8003/docs` and
raw schema at `http://localhost:8003/openapi.json`.

## Tests

```bash
pytest
```

## Migrations

```bash
alembic upgrade head
```
