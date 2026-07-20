# Document Extraction Service

Extracts functional/non-functional requirements, risks, entities and business rules from transcripts.

## Run locally

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8002
```

OpenAPI docs available at `http://localhost:8002/docs` and
raw schema at `http://localhost:8002/openapi.json`.

## Tests

```bash
pytest
```

## Migrations

```bash
alembic upgrade head
```
