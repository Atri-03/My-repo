"""API routes for the SAP Execution bounded context.

Endpoint paths match exactly what `mcp_gateway_service`'s SAP Execution
MCP tools already call (see
`services/mcp_gateway_service/app/mcp/tools/*.py` and
`app/mcp/sap_execution_client.py`), so no changes are required on the
gateway side to light this service up.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app import schemas
from app.db import models
from app.db.base import get_db

router = APIRouter()


def _resolve_tenant_id(request: Request, tenant_id: str | None) -> str:
    return tenant_id or request.headers.get("x-tenant-id") or "default"


def _new_transport_request() -> str:
    return f"TR{uuid.uuid4().hex[:8].upper()}"


# ---------------------------------------------------------------------------
# Packages
# ---------------------------------------------------------------------------
@router.post(
    "/packages",
    response_model=schemas.SapPackageRead,
    status_code=status.HTTP_201_CREATED,
    tags=["packages"],
)
def create_package(payload: schemas.SapPackageCreate, request: Request, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude_none=True)
    data["tenant_id"] = _resolve_tenant_id(request, data.get("tenant_id"))
    obj = models.SapPackage(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/packages", response_model=List[schemas.SapPackageRead], tags=["packages"])
def list_packages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.SapPackage).offset(skip).limit(limit).all()


@router.get("/packages/{item_id}", response_model=schemas.SapPackageRead, tags=["packages"])
def get_package(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.SapPackage, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="SapPackage not found")
    return obj


# ---------------------------------------------------------------------------
# Transports
# ---------------------------------------------------------------------------
@router.post(
    "/transports",
    response_model=schemas.SapTransportRead,
    status_code=status.HTTP_201_CREATED,
    tags=["transports"],
)
def create_transport(payload: schemas.SapTransportCreate, request: Request, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude_none=True)
    data["tenant_id"] = _resolve_tenant_id(request, data.get("tenant_id"))
    data["transport_request"] = _new_transport_request()
    obj = models.SapTransport(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/transports", response_model=List[schemas.SapTransportRead], tags=["transports"])
def list_transports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.SapTransport).offset(skip).limit(limit).all()


@router.get("/transports/{item_id}", response_model=schemas.SapTransportRead, tags=["transports"])
def get_transport(item_id: str, db: Session = Depends(get_db)):
    obj = _get_transport_by_id_or_request(db, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="SapTransport not found")
    return obj


def _get_transport_by_id_or_request(db: Session, item_id: str):
    obj = db.get(models.SapTransport, item_id)
    if obj is not None:
        return obj
    return db.query(models.SapTransport).filter(models.SapTransport.transport_request == item_id).first()


@router.post(
    "/transports/{transport_request}/release",
    response_model=schemas.SapTransportRead,
    tags=["transports"],
)
def release_transport(transport_request: str, payload: schemas.SapTransportRelease, db: Session = Depends(get_db)):
    obj = _get_transport_by_id_or_request(db, transport_request)
    if obj is None:
        raise HTTPException(status_code=404, detail="SapTransport not found")
    obj.status = "RELEASED"
    obj.released_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(obj)
    return obj


# ---------------------------------------------------------------------------
# Generated objects: generic, RAP, CDS, OData
# ---------------------------------------------------------------------------
@router.post(
    "/objects",
    response_model=schemas.GeneratedObjectRead,
    status_code=status.HTTP_201_CREATED,
    tags=["generated-objects"],
)
def generate_object(payload: schemas.GenerateObjectCreate, request: Request, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude_none=True)
    data["tenant_id"] = _resolve_tenant_id(request, data.get("tenant_id"))
    obj = models.GeneratedObject(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.post(
    "/rap-business-objects",
    response_model=schemas.GeneratedObjectRead,
    status_code=status.HTTP_201_CREATED,
    tags=["generated-objects"],
)
def generate_rap(payload: schemas.GenerateRAPCreate, request: Request, db: Session = Depends(get_db)):
    obj = models.GeneratedObject(
        tenant_id=_resolve_tenant_id(request, payload.tenant_id),
        object_name=payload.business_object_name,
        object_type="RAP_BUSINESS_OBJECT",
        package=payload.package,
        transport_request=payload.transport_request,
        description="Generated by SAP Execution MCP Gateway",
        extra={
            "root_entity": payload.root_entity,
            "behavior_definition": payload.behavior_definition,
            "projection_needed": payload.projection_needed,
        },
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.post(
    "/cds-views",
    response_model=schemas.GeneratedObjectRead,
    status_code=status.HTTP_201_CREATED,
    tags=["generated-objects"],
)
def generate_cds(payload: schemas.GenerateCDSCreate, request: Request, db: Session = Depends(get_db)):
    obj = models.GeneratedObject(
        tenant_id=_resolve_tenant_id(request, payload.tenant_id),
        object_name=payload.view_name,
        object_type="CDS_VIEW",
        package=payload.package,
        transport_request=payload.transport_request,
        description="Generated by SAP Execution MCP Gateway",
        source_code=payload.ddl_source,
        extra={"annotations": payload.annotations},
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.post(
    "/odata-services",
    response_model=schemas.GeneratedObjectRead,
    status_code=status.HTTP_201_CREATED,
    tags=["generated-objects"],
)
def generate_odata(payload: schemas.GenerateODataCreate, request: Request, db: Session = Depends(get_db)):
    obj = models.GeneratedObject(
        tenant_id=_resolve_tenant_id(request, payload.tenant_id),
        object_name=payload.service_name,
        object_type="ODATA_SERVICE",
        package=payload.package,
        transport_request=payload.transport_request,
        description="Generated by SAP Execution MCP Gateway",
        extra={"odata_version": payload.odata_version, "entity_set": payload.entity_set},
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/objects", response_model=List[schemas.GeneratedObjectRead], tags=["generated-objects"])
def list_generated_objects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.GeneratedObject).offset(skip).limit(limit).all()


@router.get("/objects/{item_id}", response_model=schemas.GeneratedObjectRead, tags=["generated-objects"])
def get_generated_object(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.GeneratedObject, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="GeneratedObject not found")
    return obj


# ---------------------------------------------------------------------------
# Activation
# ---------------------------------------------------------------------------
@router.post(
    "/activations",
    response_model=schemas.ActivationRead,
    status_code=status.HTTP_201_CREATED,
    tags=["activation"],
)
def activate_object(payload: schemas.ActivationCreate, request: Request, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude_none=True)
    data["tenant_id"] = _resolve_tenant_id(request, data.get("tenant_id"))
    obj = models.Activation(**data)
    db.add(obj)

    # Best-effort: flip the matching generated object (if any) to ACTIVE.
    generated = (
        db.query(models.GeneratedObject)
        .filter(
            models.GeneratedObject.object_name == payload.object_name,
            models.GeneratedObject.object_type == payload.object_type,
        )
        .order_by(models.GeneratedObject.created_at.desc())
        .first()
    )
    if generated is not None:
        generated.status = "ACTIVE"

    db.commit()
    db.refresh(obj)
    return obj


@router.get("/activations", response_model=List[schemas.ActivationRead], tags=["activation"])
def list_activations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Activation).offset(skip).limit(limit).all()


# ---------------------------------------------------------------------------
# ATC (ABAP Test Cockpit) orchestration + remediation engine
# ---------------------------------------------------------------------------
@router.post(
    "/atc-runs",
    response_model=schemas.AtcRunRead,
    status_code=status.HTTP_201_CREATED,
    tags=["atc"],
)
def run_atc(payload: schemas.AtcRunCreate, request: Request, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude_none=True)
    data["tenant_id"] = _resolve_tenant_id(request, data.get("tenant_id"))
    # No live ATC connectivity in this sandbox; record a completed run with
    # no findings by default, findings are populated once a real ATC
    # integration (or abap_rag_pipeline's ADT client) is wired in.
    data.setdefault("findings", [])
    obj = models.AtcRun(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/atc-runs", response_model=List[schemas.AtcRunRead], tags=["atc"])
def list_atc_runs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.AtcRun).offset(skip).limit(limit).all()


@router.post(
    "/atc-remediations",
    response_model=schemas.AtcRemediationRead,
    status_code=status.HTTP_201_CREATED,
    tags=["atc"],
)
def remediate_atc_findings(payload: schemas.AtcRemediationCreate, request: Request, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude_none=True)
    data["tenant_id"] = _resolve_tenant_id(request, data.get("tenant_id"))
    obj = models.AtcRemediation(**data)
    if obj.auto_apply:
        obj.status = "APPLIED"
        obj.remediated_at = datetime.now(timezone.utc)
    else:
        obj.status = "PROPOSED"
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/atc-remediations", response_model=List[schemas.AtcRemediationRead], tags=["atc"])
def list_atc_remediations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.AtcRemediation).offset(skip).limit(limit).all()


# ---------------------------------------------------------------------------
# Unit testing
# ---------------------------------------------------------------------------
@router.post(
    "/unit-test-runs",
    response_model=schemas.UnitTestRunRead,
    status_code=status.HTTP_201_CREATED,
    tags=["unit-testing"],
)
def run_unit_tests(payload: schemas.UnitTestRunCreate, request: Request, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude_none=True)
    data["tenant_id"] = _resolve_tenant_id(request, data.get("tenant_id"))
    data.setdefault("results", {})
    obj = models.UnitTestRun(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/unit-test-runs", response_model=List[schemas.UnitTestRunRead], tags=["unit-testing"])
def list_unit_test_runs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.UnitTestRun).offset(skip).limit(limit).all()


# ---------------------------------------------------------------------------
# SAP Solution Architect Agent - execution planning
# ---------------------------------------------------------------------------
def _build_plan_steps(payload: schemas.ExecutionPlanCreate) -> List[Dict[str, Any]]:
    steps: List[Dict[str, Any]] = [
        {"order": 1, "tool": "create_package", "rationale": "Isolate generated artefacts in a dedicated package."},
        {"order": 2, "tool": "create_transport", "rationale": "Every change must travel via a transport request."},
    ]
    order = 3
    if payload.needs_cds:
        steps.append({"order": order, "tool": "generate_cds", "rationale": "Data model exposure via CDS view."})
        order += 1
    if payload.needs_rap:
        steps.append({"order": order, "tool": "generate_rap", "rationale": "Business logic via RAP business object."})
        order += 1
    if payload.needs_odata:
        steps.append({"order": order, "tool": "generate_odata", "rationale": "Expose service for UI/API consumption."})
        order += 1
    for object_name in payload.object_names or []:
        steps.append(
            {
                "order": order,
                "tool": "generate_object",
                "object_name": object_name,
                "rationale": "Generic ABAP object required by the Technical Specification.",
            }
        )
        order += 1
    steps.append({"order": order, "tool": "run_unit_tests", "rationale": "Validate generated logic before ATC/activation."})
    order += 1
    steps.append({"order": order, "tool": "run_atc", "rationale": "Mandatory ATC quality gate."})
    order += 1
    steps.append({"order": order, "tool": "remediate_atc_findings", "rationale": "Address ATC findings, if any."})
    order += 1
    steps.append(
        {
            "order": order,
            "tool": "activate_object",
            "rationale": "Activation requires Gate 5 (Lead Approval Before Activation) per the governance framework.",
        }
    )
    return steps


@router.post(
    "/architect/plans",
    response_model=schemas.ExecutionPlanRead,
    status_code=status.HTTP_201_CREATED,
    tags=["architect"],
)
def create_execution_plan(payload: schemas.ExecutionPlanCreate, request: Request, db: Session = Depends(get_db)):
    """SAP Solution Architect Agent: propose an ordered execution plan for a Technical Specification.

    This is a deterministic, rule-based planner (consistent with the rest
    of this platform's backend services, which do not call external LLMs
    directly). It can later be swapped for an LLM/Semantic-Kernel-backed
    planner without changing the API contract.
    """
    obj = models.ExecutionPlan(
        tenant_id=_resolve_tenant_id(request, payload.tenant_id),
        technical_specification_id=payload.technical_specification_id,
        package_name=payload.package_name,
        steps=_build_plan_steps(payload),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/architect/plans", response_model=List[schemas.ExecutionPlanRead], tags=["architect"])
def list_execution_plans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.ExecutionPlan).offset(skip).limit(limit).all()


@router.get("/architect/plans/{item_id}", response_model=schemas.ExecutionPlanRead, tags=["architect"])
def get_execution_plan(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.ExecutionPlan, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="ExecutionPlan not found")
    return obj
