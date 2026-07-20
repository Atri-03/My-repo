# MCP Gateway Service

Exposes platform capabilities (knowledge search, artefact retrieval, workflow state) as MCP-style HTTP tools, proxying to backing services.

## SAP Execution Integration (dynamic MCP capability registry)

In addition to the fixed platform tool endpoints above, the gateway exposes a
**dynamic MCP capability registry** for SAP execution capabilities (package
creation, transport management, ABAP object/RAP/CDS/OData generation,
activation, unit testing, and ATC execution/remediation). These tools are
never hardcoded into the routing layer:

- Each tool is implemented as a small module under `app/mcp/tools/` that
  registers itself with `app.mcp.registry` via the `@mcp_tool` decorator.
- `app/mcp/registry.discover_tools()` imports every module in that package on
  startup, so the registry is always built dynamically from whatever tool
  modules exist - **no route, schema, or dispatcher changes are needed** to
  add a new tool. Dropping in a new `*.py` file with a `@mcp_tool`-decorated
  handler is enough for it to show up automatically.
- Tool wrappers call out to the backing SAP execution system via
  `app/mcp/sap_execution_client.py`, configured through
  `SAP_EXECUTION_SERVICE_URL`.

### Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/v1/mcp/tools` | List the full dynamic capability registry (name, description, category, input schema) |
| `GET` | `/api/v1/mcp/tools/{tool_name}` | Get the schema/metadata for a single tool |
| `POST` | `/api/v1/mcp/tools/{tool_name}/invoke` | Validate the request body against the tool's schema, invoke it, and return the result |

Built-in SAP execution tools: `create_package`, `create_transport`,
`release_transport`, `generate_object`, `generate_rap`, `generate_cds`,
`generate_odata`, `activate_object`, `run_unit_tests`, `run_atc`,
`remediate_atc_findings`.

### Audit trail

Every call to `POST /api/v1/mcp/tools/{tool_name}/invoke` - success, upstream
error, or validation error - is recorded as an entry in the Audit Service
(`app/mcp/audit.py`), including the tool name, actor (`X-Actor` header),
tenant (`X-Tenant-Id` header), input payload, and outcome. Audit recording is
best-effort and never blocks or fails the underlying tool call.

## Run locally

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8011
```

OpenAPI docs available at `http://localhost:8011/docs` and
raw schema at `http://localhost:8011/openapi.json`.

## Tests

```bash
pytest
```

## Migrations

```bash
alembic upgrade head
```
