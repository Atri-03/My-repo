"""API routes."""
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.gates import DEFAULT_GATES
from app.db.base import get_db
from app.db import models
from app import schemas
from app.services import governance
from app.services.audit_client import record_governance_event

router = APIRouter()


@router.post("/review-decisions", response_model=schemas.ReviewDecisionRead, status_code=status.HTTP_201_CREATED, tags=["review-decisions"])
def create_review_decision(payload: schemas.ReviewDecisionCreate, db: Session = Depends(get_db)):
    obj = models.ReviewDecision(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/review-decisions", response_model=List[schemas.ReviewDecisionRead], tags=["review-decisions"])
def list_review_decision(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.ReviewDecision).offset(skip).limit(limit).all()


@router.get("/review-decisions/{item_id}", response_model=schemas.ReviewDecisionRead, tags=["review-decisions"])
def get_review_decision(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.ReviewDecision, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="ReviewDecision not found")
    return obj


@router.post("/sap-execution-packages", response_model=schemas.SapExecutionPackageRead, status_code=status.HTTP_201_CREATED, tags=["sap-execution-packages"])
def create_sap_execution_package(payload: schemas.SapExecutionPackageCreate, db: Session = Depends(get_db)):
    obj = models.SapExecutionPackage(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/sap-execution-packages", response_model=List[schemas.SapExecutionPackageRead], tags=["sap-execution-packages"])
def list_sap_execution_package(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.SapExecutionPackage).offset(skip).limit(limit).all()


@router.get("/sap-execution-packages/{item_id}", response_model=schemas.SapExecutionPackageRead, tags=["sap-execution-packages"])
def get_sap_execution_package(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.SapExecutionPackage, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="SapExecutionPackage not found")
    return obj


@router.patch("/sap-execution-packages/{item_id}", response_model=schemas.SapExecutionPackageRead, tags=["sap-execution-packages"])
def update_sap_execution_package(item_id: str, payload: schemas.SapExecutionPackageUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.SapExecutionPackage, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="SapExecutionPackage not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/sap-execution-packages/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["sap-execution-packages"])
def delete_sap_execution_package(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.SapExecutionPackage, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="SapExecutionPackage not found")
    db.delete(obj)
    db.commit()
    return None


# ---------------------------------------------------------------------------
# Human-in-the-Loop Governance Framework: configurable approval gates
# ---------------------------------------------------------------------------


@router.post(
    "/tenants/{tenant_id}/gate-definitions/seed-defaults",
    response_model=List[schemas.ApprovalGateDefinitionRead],
    status_code=status.HTTP_201_CREATED,
    tags=["gate-definitions"],
)
def seed_default_gate_definitions(tenant_id: str, db: Session = Depends(get_db)):
    """Seed the 5 mandatory gates for a tenant if not already configured.

    Idempotent: gate keys already configured for the tenant are left
    untouched (edit them via PATCH instead of re-seeding).
    """
    existing_keys = {
        g.gate_key
        for g in db.query(models.ApprovalGateDefinition).filter_by(tenant_id=tenant_id).all()
    }
    created = []
    for gate in DEFAULT_GATES:
        if gate["gate_key"] in existing_keys:
            continue
        obj = models.ApprovalGateDefinition(tenant_id=tenant_id, **gate)
        db.add(obj)
        created.append(obj)
    db.commit()
    for obj in created:
        db.refresh(obj)
    return created


@router.post(
    "/gate-definitions",
    response_model=schemas.ApprovalGateDefinitionRead,
    status_code=status.HTTP_201_CREATED,
    tags=["gate-definitions"],
)
def create_gate_definition(payload: schemas.ApprovalGateDefinitionCreate, db: Session = Depends(get_db)):
    obj = models.ApprovalGateDefinition(**payload.model_dump(exclude_none=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get(
    "/gate-definitions", response_model=List[schemas.ApprovalGateDefinitionRead], tags=["gate-definitions"]
)
def list_gate_definitions(
    tenant_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = db.query(models.ApprovalGateDefinition)
    if tenant_id is not None:
        query = query.filter_by(tenant_id=tenant_id)
    return query.order_by(models.ApprovalGateDefinition.sequence_order).offset(skip).limit(limit).all()


@router.get(
    "/gate-definitions/{item_id}", response_model=schemas.ApprovalGateDefinitionRead, tags=["gate-definitions"]
)
def get_gate_definition(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.ApprovalGateDefinition, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="ApprovalGateDefinition not found")
    return obj


@router.patch(
    "/gate-definitions/{item_id}", response_model=schemas.ApprovalGateDefinitionRead, tags=["gate-definitions"]
)
def update_gate_definition(
    item_id: str, payload: schemas.ApprovalGateDefinitionUpdate, db: Session = Depends(get_db)
):
    obj = db.get(models.ApprovalGateDefinition, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="ApprovalGateDefinition not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.post(
    "/gate-approvals",
    response_model=schemas.GateApprovalRequestRead,
    status_code=status.HTTP_201_CREATED,
    tags=["gate-approvals"],
)
async def create_gate_approval_request(
    payload: schemas.GateApprovalRequestCreate,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    gate_definition = (
        db.query(models.ApprovalGateDefinition)
        .filter_by(tenant_id=payload.tenant_id, gate_key=payload.gate_key)
        .first()
    )
    if gate_definition is None:
        raise HTTPException(
            status_code=400, detail=f"Gate '{payload.gate_key}' is not configured for this tenant"
        )
    if not gate_definition.is_active:
        raise HTTPException(status_code=400, detail=f"Gate '{payload.gate_key}' is not active")

    obj = models.GateApprovalRequest(**payload.model_dump(exclude_none=True), status="PENDING")
    db.add(obj)
    db.commit()
    db.refresh(obj)

    await record_governance_event(
        settings,
        tenant_id=obj.tenant_id,
        entity_type="gate_approval_request",
        entity_id=obj.id,
        action="GATE_APPROVAL_REQUESTED",
        actor=obj.requested_by,
        after={
            "gate_key": obj.gate_key,
            "entity_type": obj.entity_type,
            "entity_id": obj.entity_id,
            "status": obj.status,
        },
    )
    return obj


@router.get(
    "/gate-approvals", response_model=List[schemas.GateApprovalRequestRead], tags=["gate-approvals"]
)
def list_gate_approval_requests(
    tenant_id: Optional[str] = None,
    gate_key: Optional[str] = None,
    entity_id: Optional[str] = None,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = db.query(models.GateApprovalRequest)
    if tenant_id is not None:
        query = query.filter_by(tenant_id=tenant_id)
    if gate_key is not None:
        query = query.filter_by(gate_key=gate_key)
    if entity_id is not None:
        query = query.filter_by(entity_id=entity_id)
    if status_filter is not None:
        query = query.filter_by(status=status_filter)
    return query.offset(skip).limit(limit).all()


@router.get(
    "/gate-approvals/{item_id}", response_model=schemas.GateApprovalRequestRead, tags=["gate-approvals"]
)
def get_gate_approval_request(item_id: str, db: Session = Depends(get_db)):
    obj = db.get(models.GateApprovalRequest, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="GateApprovalRequest not found")
    return obj


@router.post(
    "/gate-approvals/{item_id}/decide",
    response_model=schemas.GateApprovalRequestRead,
    tags=["gate-approvals"],
)
async def decide_gate_approval_request(
    item_id: str,
    payload: schemas.GateApprovalDecide,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    gate_request = db.get(models.GateApprovalRequest, item_id)
    if gate_request is None:
        raise HTTPException(status_code=404, detail="GateApprovalRequest not found")

    gate_definition = (
        db.query(models.ApprovalGateDefinition)
        .filter_by(tenant_id=gate_request.tenant_id, gate_key=gate_request.gate_key)
        .first()
    )
    if gate_definition is None:
        raise HTTPException(
            status_code=400, detail=f"Gate '{gate_request.gate_key}' is not configured for this tenant"
        )

    before_state = {"status": gate_request.status}
    try:
        outcome = governance.evaluate_decision(
            gate_definition,
            gate_request,
            decided_by=payload.decided_by,
            decided_by_role=payload.decided_by_role,
            decision=payload.decision,
        )
    except governance.RoleMismatchError as exc:
        await record_governance_event(
            settings,
            tenant_id=gate_request.tenant_id,
            entity_type="gate_approval_request",
            entity_id=gate_request.id,
            action="GATE_DECISION_REJECTED_ROLE_MISMATCH",
            actor=payload.decided_by,
            before=before_state,
            after={"error": str(exc)},
        )
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except governance.SegregationOfDutiesViolationError as exc:
        await record_governance_event(
            settings,
            tenant_id=gate_request.tenant_id,
            entity_type="gate_approval_request",
            entity_id=gate_request.id,
            action="GATE_DECISION_REJECTED_SOD_VIOLATION",
            actor=payload.decided_by,
            before=before_state,
            after={"error": str(exc)},
        )
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except (governance.GateInactiveError, governance.AlreadyDecidedError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    gate_request.status = outcome.status
    gate_request.decided_by = payload.decided_by
    gate_request.decided_by_role = payload.decided_by_role
    gate_request.decision_comments = payload.decision_comments
    gate_request.sod_violation = outcome.sod_violation
    gate_request.decided_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(gate_request)

    await record_governance_event(
        settings,
        tenant_id=gate_request.tenant_id,
        entity_type="gate_approval_request",
        entity_id=gate_request.id,
        action="GATE_DECISION_RECORDED",
        actor=payload.decided_by,
        before=before_state,
        after={
            "status": gate_request.status,
            "decided_by": gate_request.decided_by,
            "decided_by_role": gate_request.decided_by_role,
            "sod_violation": gate_request.sod_violation,
        },
    )
    return gate_request

