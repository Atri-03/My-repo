# Transcript Service

Ingests and manages source documents and transcripts (Teams transcript, MOM, BRD, PDF, DOCX, TXT, HTML).

## Run locally

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8001
```

OpenAPI docs available at `http://localhost:8001/docs` and
raw schema at `http://localhost:8001/openapi.json`.

## Tests

```bash
pytest
```

## Migrations

```bash
alembic upgrade head
```
