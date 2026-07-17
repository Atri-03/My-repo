# ABAP RAG Agentic Pipeline (POC)

A proof-of-concept pipeline that converts a Teams meeting transcript into a
draft ABAP program, with two human-in-the-loop review gates:

1. **Gate 1** — after the Functional Spec (FS) and Technical Spec (TS) `.docx`
   documents are generated, before ABAP code generation starts.
2. **Gate 2** — after the ABAP object is created (INACTIVE) in SAP via the
   ADT REST API, marking it "pending developer review".

## Tech stack

| Concern              | Tool                                                |
|-----------------------|------------------------------------------------------|
| Orchestration         | [LangGraph](https://langchain-ai.github.io/langgraph/) (state machine + `interrupt_before`) |
| LLM                   | Azure OpenAI (GPT-4o) via the `openai` Python SDK   |
| Vector store          | ChromaDB (local persistent store, offline embedding for the POC) |
| API layer             | FastAPI                                             |
| Document generation   | python-docx                                         |
| SAP integration       | SAP ADT REST API via `requests` (no PyRFC)          |

## Project layout

```
abap_rag_pipeline/
├── app/
│   ├── config.py       # Settings loaded from .env
│   ├── graph.py        # LangGraph state machine wiring the nodes together
│   └── main.py         # FastAPI app + endpoints
├── nodes/              # LangGraph node functions (one stage each)
│   ├── state.py
│   ├── transcript_ingest.py
│   ├── requirement_extraction.py
│   ├── fs_ts_generation.py
│   ├── human_gate_1.py
│   ├── abap_code_generation.py
│   └── human_gate_2.py
├── services/           # External integrations
│   ├── azure_openai_client.py
│   ├── chroma_client.py
│   ├── adt_client.py           # ADT REST API + auth stub
│   ├── teams_graph_client.py   # Teams Graph API — TODO stub only
│   └── tracker_store.py        # JSON-file run/status tracker
├── models/
│   └── schemas.py       # Pydantic schemas (StructuredRequirements, etc.)
├── data/
│   ├── transcripts/     # Uploaded transcript files
│   ├── output/          # Generated FS/TS .docx files
│   ├── tracker/         # tracker.json (run status + gate log)
│   └── chroma/          # ChromaDB persistent store
├── requirements.txt
└── .env.example
```

## Pipeline stages (LangGraph nodes)

1. **transcript_ingest** — cleans and chunks an uploaded transcript text file.
   Real Teams Graph API ingestion is a TODO stub in
   `services/teams_graph_client.py` (`fetch_teams_transcript`) — not wired in.
2. **requirement_extraction** — sends transcript chunks + few-shot examples
   (retrieved from ChromaDB) to Azure OpenAI and parses the JSON response into
   a `StructuredRequirements` Pydantic model.
3. **fs_ts_generation** — renders the structured requirements into FS and TS
   `.docx` files with python-docx.
4. **HUMAN GATE 1** — the graph is compiled with
   `interrupt_before=["human_gate_1"]`, so execution pauses here until the
   `/pipeline/{run_id}/approve/gate1` endpoint is called with `approved=true`.
5. **abap_code_generation** — generates a simple ABAP report skeleton via
   Azure OpenAI, then calls `create_adt_object()` (in `services/adt_client.py`)
   to POST the object to the SAP ADT REST API as **INACTIVE** in the
   configured package.
6. **HUMAN GATE 2** — the graph interrupts again before this node. Once
   resumed (`/pipeline/{run_id}/approve/gate2`), it logs the created object
   name/package to `data/tracker/tracker.json` and marks the run "pending
   developer review" (or "gate_2_approved" if a reviewer already signed off).

## Running locally

1. Create a virtualenv and install dependencies:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in real values (see "Where stubs
   need real credentials" below). For a first dry run you can leave the Azure
   OpenAI / ADT values as placeholders — LLM calls will fail with an auth
   error but the FastAPI routes, LangGraph wiring, and docx generation can
   still be exercised.
3. Start the API:
   ```bash
   uvicorn app.main:app --reload --app-dir abap_rag_pipeline
   ```
   (or `cd abap_rag_pipeline && uvicorn app.main:app --reload`)
4. Exercise the pipeline:
   ```bash
   # 1. Upload a transcript
   curl -F "file=@sample_transcript.txt" http://localhost:8000/transcripts/upload
   # -> {"run_id": "...", ...}

   # 2. Trigger the pipeline (runs until gate 1 interrupt)
   curl -X POST http://localhost:8000/pipeline/<run_id>/trigger

   # 3. Check status / review the generated FS/TS docx in data/output/
   curl http://localhost:8000/pipeline/<run_id>/status

   # 4. Approve gate 1 (resumes through ABAP generation + ADT object creation)
   curl -X POST http://localhost:8000/pipeline/<run_id>/approve/gate1 \
     -H "Content-Type: application/json" \
     -d '{"run_id": "<run_id>", "approved": true}'

   # 5. Approve/mark-reviewed gate 2
   curl -X POST http://localhost:8000/pipeline/<run_id>/approve/gate2 \
     -H "Content-Type: application/json" \
     -d '{"run_id": "<run_id>", "approved": true}'
   ```
   API docs are available at `http://localhost:8000/docs`.

## Where each stub needs real credentials/wiring

| File | Stub | What to wire up |
|------|------|------------------|
| `.env` | `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT` | Real Azure OpenAI resource + GPT-4o deployment name. |
| `services/adt_client.py` → `get_adt_session()` | ADT auth | Currently supports HTTP basic auth only (`ADT_AUTH_MODE=basic`). Implement the `snc` branch for SNC/X.509-based session or SSO cookie auth. |
| `.env` | `ADT_BASE_URL`, `ADT_SAP_CLIENT`, `ADT_USERNAME`/`ADT_PASSWORD`, `ADT_TARGET_PACKAGE` | Real SAP system connection details and target package. |
| `services/teams_graph_client.py` → `fetch_teams_transcript()` | Teams Graph API | Not implemented — raises `NotImplementedError`. Requires an MSAL app registration and `GRAPH_TENANT_ID`/`GRAPH_CLIENT_ID`/`GRAPH_CLIENT_SECRET` (placeholders in `.env.example`) plus `OnlineMeetingTranscript.Read.All` permission. |
| `services/chroma_client.py` | Seed data | Seeded with 3 dummy FS/TS examples on first run and uses an offline hashing embedding function so the POC runs without internet access. Replace with a real document ingestion job and a hosted embedding model (e.g. `text-embedding-3-small`) before production use. |
| `services/tracker_store.py` | Run/gate tracking | Plain JSON file (`TRACKER_DB_PATH`). Swap for SQLite/Postgres if concurrent runs or durability are needed. |
| `app/graph.py` | Checkpointer | Uses LangGraph's in-memory `MemorySaver`, so pipeline state is lost on process restart. Swap for a persistent checkpointer (e.g. SQLite) for real usage. |

## Notes / limitations (by design, for a POC)

- No authentication/authorization on the FastAPI endpoints.
- No retry/backoff around Azure OpenAI or ADT calls.
- The generated ABAP is a simple report skeleton, not validated ABAP syntax.
- `create_adt_object()` targets `/sap/bc/adt/programs/programs`; extend it
  (or add a parallel function) to target `/sap/bc/adt/oo/classes` if you need
  class skeletons instead of reports.
