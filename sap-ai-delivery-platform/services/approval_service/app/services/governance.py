"""Human-in-the-Loop governance rules: RBAC + segregation of duties.

Nothing may enter SAP automatically. `decide_gate_approval` is the single
choke point through which every gate decision must pass, and it is the
only place these two invariants are enforced:

- **Role-based workflows**: the deciding user's role must match the gate
  definition's `required_role` (unless the gate has been configured with a
  different role since the request was opened).
- **Segregation of duties**: the same person who requested a gate approval
  may not also decide it, unless the gate definition explicitly opts in via
  `allow_self_approval` (default: not allowed).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.db import models


class GateNotConfiguredError(Exception):
    pass


class GateInactiveError(Exception):
    pass


class RoleMismatchError(Exception):
    def __init__(self, required_role: str, actual_role: Optional[str]):
        self.required_role = required_role
        self.actual_role = actual_role
        super().__init__(
            f"Decision requires role '{required_role}' but decider has role '{actual_role}'"
        )


class SegregationOfDutiesViolationError(Exception):
    def __init__(self, actor: str):
        self.actor = actor
        super().__init__(
            f"Segregation of duties violation: '{actor}' requested this gate approval "
            "and may not also decide it"
        )


class AlreadyDecidedError(Exception):
    pass


VALID_DECISIONS = {"APPROVED", "REJECTED", "CHANGES_REQUESTED"}


@dataclass
class DecisionOutcome:
    status: str
    sod_violation: bool


def evaluate_decision(
    gate_definition: models.ApprovalGateDefinition,
    gate_request: models.GateApprovalRequest,
    *,
    decided_by: str,
    decided_by_role: Optional[str],
    decision: str,
) -> DecisionOutcome:
    """Validate a proposed gate decision against RBAC + SoD rules.

    Raises a specific exception (mapped to an HTTP status by the route
    layer) when a rule is violated; otherwise returns the resulting status.
    """
    if not gate_definition.is_active:
        raise GateInactiveError(f"Gate '{gate_definition.gate_key}' is not active")

    if gate_request.status != "PENDING":
        raise AlreadyDecidedError(f"Gate approval request '{gate_request.id}' already decided")

    if decision not in VALID_DECISIONS:
        raise ValueError(f"Invalid decision '{decision}'; expected one of {sorted(VALID_DECISIONS)}")

    if decided_by_role != gate_definition.required_role:
        raise RoleMismatchError(gate_definition.required_role, decided_by_role)

    sod_violation = decided_by == gate_request.requested_by
    if sod_violation and not gate_definition.allow_self_approval:
        raise SegregationOfDutiesViolationError(decided_by)

    return DecisionOutcome(status=decision, sod_violation=sod_violation)
