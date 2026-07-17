"""Simple JSON-file-backed tracker/store for pipeline run state.

This is intentionally minimal for the POC: no concurrency control, no DB
migrations. Swap for SQLite/Postgres once the pipeline is production-bound.
"""
from __future__ import annotations

import json
import os
import threading
from datetime import datetime
from typing import Any

from app.config import settings

_lock = threading.Lock()


def _tracker_path() -> str:
    path = settings.tracker_db_path
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    return path


def _load() -> dict[str, Any]:
    path = _tracker_path()
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as fh:
        try:
            return json.load(fh)
        except json.JSONDecodeError:
            return {}


def _save(data: dict[str, Any]) -> None:
    path = _tracker_path()
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, default=str)


def upsert_run(run_id: str, **fields: Any) -> dict[str, Any]:
    with _lock:
        data = _load()
        record = data.get(run_id, {"run_id": run_id, "created_at": datetime.utcnow().isoformat()})
        record.update(fields)
        record["updated_at"] = datetime.utcnow().isoformat()
        data[run_id] = record
        _save(data)
        return record


def get_run(run_id: str) -> dict[str, Any] | None:
    with _lock:
        return _load().get(run_id)


def list_runs() -> dict[str, Any]:
    with _lock:
        return _load()
