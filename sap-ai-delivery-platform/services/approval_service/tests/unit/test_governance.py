"""Unit tests for the governance rules module (RBAC + segregation of duties)."""
import pytest

from app.core.gates import GATE_1_BUSINESS_APPROVAL_OF_FS
from app.db import models
from app.services import governance


def _gate_definition(**overrides):
    defaults = dict(
        id="gate-def-1",
        tenant_id="tenant-1",
        gate_key=GATE_1_BUSINESS_APPROVAL_OF_FS,
        name="Business Approval of FS",
        sequence_order=1,
        entity_type="FunctionalSpecification",
        required_role="BUSINESS_APPROVER",
        allow_self_approval=False,
        is_active=True,
    )
    defaults.update(overrides)
    return models.ApprovalGateDefinition(**defaults)


def _gate_request(**overrides):
    defaults = dict(
        id="gate-req-1",
        tenant_id="tenant-1",
        gate_key=GATE_1_BUSINESS_APPROVAL_OF_FS,
        entity_type="FunctionalSpecification",
        entity_id="fs-1",
        requested_by="alice",
        requested_by_role="BUSINESS_ANALYST",
        status="PENDING",
        sod_violation=False,
    )
    defaults.update(overrides)
    return models.GateApprovalRequest(**defaults)


def test_approve_with_correct_role_and_different_approver_succeeds():
    outcome = governance.evaluate_decision(
        _gate_definition(),
        _gate_request(),
        decided_by="bob",
        decided_by_role="BUSINESS_APPROVER",
        decision="APPROVED",
    )
    assert outcome.status == "APPROVED"
    assert outcome.sod_violation is False


def test_role_mismatch_raises():
    with pytest.raises(governance.RoleMismatchError):
        governance.evaluate_decision(
            _gate_definition(),
            _gate_request(),
            decided_by="bob",
            decided_by_role="DEVELOPER",
            decision="APPROVED",
        )


def test_segregation_of_duties_violation_raises_when_self_approval_disallowed():
    with pytest.raises(governance.SegregationOfDutiesViolationError):
        governance.evaluate_decision(
            _gate_definition(allow_self_approval=False),
            _gate_request(requested_by="alice"),
            decided_by="alice",
            decided_by_role="BUSINESS_APPROVER",
            decision="APPROVED",
        )


def test_self_approval_allowed_when_gate_configured_to_permit_it():
    outcome = governance.evaluate_decision(
        _gate_definition(allow_self_approval=True),
        _gate_request(requested_by="alice"),
        decided_by="alice",
        decided_by_role="BUSINESS_APPROVER",
        decision="APPROVED",
    )
    assert outcome.status == "APPROVED"
    assert outcome.sod_violation is True


def test_inactive_gate_raises():
    with pytest.raises(governance.GateInactiveError):
        governance.evaluate_decision(
            _gate_definition(is_active=False),
            _gate_request(),
            decided_by="bob",
            decided_by_role="BUSINESS_APPROVER",
            decision="APPROVED",
        )


def test_already_decided_raises():
    with pytest.raises(governance.AlreadyDecidedError):
        governance.evaluate_decision(
            _gate_definition(),
            _gate_request(status="APPROVED"),
            decided_by="bob",
            decided_by_role="BUSINESS_APPROVER",
            decision="APPROVED",
        )


def test_invalid_decision_value_raises():
    with pytest.raises(ValueError):
        governance.evaluate_decision(
            _gate_definition(),
            _gate_request(),
            decided_by="bob",
            decided_by_role="BUSINESS_APPROVER",
            decision="MAYBE",
        )


def test_rejected_and_changes_requested_are_valid_decisions():
    for decision in ("REJECTED", "CHANGES_REQUESTED"):
        outcome = governance.evaluate_decision(
            _gate_definition(),
            _gate_request(),
            decided_by="bob",
            decided_by_role="BUSINESS_APPROVER",
            decision=decision,
        )
        assert outcome.status == decision
