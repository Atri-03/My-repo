# Review Service

Manages review cycles and reviewer comments for FS/TS artefacts.

## Run locally

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8005
```

OpenAPI docs available at `http://localhost:8005/docs` and
raw schema at `http://localhost:8005/openapi.json`.

## Tests

```bash
pytest
```

## Migrations

```bash
alembic upgrade head
```
