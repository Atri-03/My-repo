# Approval Service

Records approval/rejection decisions and publishes SAP Execution Packages.

## Run locally

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8006
```

OpenAPI docs available at `http://localhost:8006/docs` and
raw schema at `http://localhost:8006/openapi.json`.

## Tests

```bash
pytest
```

## Migrations

```bash
alembic upgrade head
```
