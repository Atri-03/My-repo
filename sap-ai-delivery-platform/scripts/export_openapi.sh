#!/bin/bash
# Regenerates docs/architecture/openapi/services/<service>.json for every
# FastAPI microservice under services/, without needing a running server.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT_DIR/docs/architecture/openapi/services"
mkdir -p "$OUT_DIR"

SERVICES=(
  transcript_service
  document_extraction_service
  fs_service
  ts_service
  review_service
  approval_service
  audit_service
  rag_service
  user_service
  workflow_service
  mcp_gateway_service
)

for svc in "${SERVICES[@]}"; do
  echo "Exporting OpenAPI schema for $svc"
  (
    cd "$ROOT_DIR/services/$svc"
    PYTHONPATH=. python3 -c "
import json
from app.main import app
with open('$OUT_DIR/${svc}.json', 'w') as f:
    json.dump(app.openapi(), f, indent=2)
"
    rm -f "${svc}.db"
  )
done

echo "Done. Schemas written to $OUT_DIR"
