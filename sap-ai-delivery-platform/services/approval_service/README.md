# Approval Service

Records approval/rejection decisions and publishes SAP Execution Packages.

## Human-in-the-Loop Governance Framework

Nothing may enter SAP automatically. This service implements the platform's
mandatory human approval gates as a **configurable** framework - gate
identity/order/required-role/self-approval policy live in the database, not
in code, so gates can be added, retired, or reconfigured without a
deployment.

### The 5 mandatory gates

Seeded by default (see `app/core/gates.py` and `POST
/api/v1/tenants/{tenant_id}/gate-definitions/seed-defaults`), each tenant can
subsequently reconfigure any field via `PATCH /api/v1/gate-definitions/{id}`:

1. **Business Approval of FS** - `GATE_1_BUSINESS_APPROVAL_OF_FS` (role: `BUSINESS_APPROVER`)
2. **Architect Approval of TS** - `GATE_2_ARCHITECT_APPROVAL_OF_TS` (role: `ARCHITECT`)
3. **Developer Approval of Generated SAP Design** - `GATE_3_DEVELOPER_APPROVAL_OF_SAP_DESIGN` (role: `DEVELOPER`)
4. **Developer Approval Before Object Creation** - `GATE_4_DEVELOPER_APPROVAL_BEFORE_OBJECT_CREATION` (role: `DEVELOPER`)
5. **Lead Approval Before Activation** - `GATE_5_LEAD_APPROVAL_BEFORE_ACTIVATION` (role: `LEAD`)

### Role-based workflows & segregation of duties

`POST /api/v1/gate-approvals/{id}/decide` is the single choke point for
every gate decision (see `app/services/governance.py`):

- **RBAC**: the decision is rejected (`403`) unless the decider's role
  matches the gate definition's `required_role`.
- **Segregation of duties**: the decision is rejected (`409`) if the
  decider is the same person who requested the approval, unless the gate
  is explicitly configured with `allow_self_approval: true`.
- Gate approval requests can only be decided once (`400` if already
  decided) and only against an active gate (`400` if inactive).

### Auditability

Every gate configuration event and decision (including rejected attempts)
is pushed to the Audit Service (`app/services/audit_client.py`) in addition
to being persisted on the `gate_approval_request` row itself
(`requested_by`, `decided_by`, roles, `sod_violation`, timestamps) -
recording is best-effort and never blocks the underlying gate operation.

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
