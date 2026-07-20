# Workflow Service

Tracks workflow runs and state-transition events for the delivery pipeline.

## Run locally

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8010
```

OpenAPI docs available at `http://localhost:8010/docs` and
raw schema at `http://localhost:8010/openapi.json`.

## Tests

```bash
pytest
```

## Migrations

```bash
alembic upgrade head
```
