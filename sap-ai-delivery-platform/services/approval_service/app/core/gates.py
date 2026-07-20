"""The 5 mandatory Human-in-the-Loop governance gates.

Nothing may enter SAP automatically: every one of these gates must be
explicitly approved by a human with the configured role before the
workflow may proceed. Gate *definitions* (required role, sequence, whether
self-approval is allowed, active/inactive) are fully configurable via the
`ApprovalGateDefinition` API - the keys below are stable identifiers used
to seed sensible defaults and are not a hardcoded workflow.
"""
from __future__ import annotations

GATE_1_BUSINESS_APPROVAL_OF_FS = "GATE_1_BUSINESS_APPROVAL_OF_FS"
GATE_2_ARCHITECT_APPROVAL_OF_TS = "GATE_2_ARCHITECT_APPROVAL_OF_TS"
GATE_3_DEVELOPER_APPROVAL_OF_SAP_DESIGN = "GATE_3_DEVELOPER_APPROVAL_OF_SAP_DESIGN"
GATE_4_DEVELOPER_APPROVAL_BEFORE_OBJECT_CREATION = "GATE_4_DEVELOPER_APPROVAL_BEFORE_OBJECT_CREATION"
GATE_5_LEAD_APPROVAL_BEFORE_ACTIVATION = "GATE_5_LEAD_APPROVAL_BEFORE_ACTIVATION"

DEFAULT_GATES = [
    {
        "gate_key": GATE_1_BUSINESS_APPROVAL_OF_FS,
        "name": "Business Approval of Functional Specification",
        "description": "Business stakeholder sign-off on the generated Functional Specification.",
        "sequence_order": 1,
        "entity_type": "FunctionalSpecification",
        "required_role": "BUSINESS_APPROVER",
        "allow_self_approval": False,
    },
    {
        "gate_key": GATE_2_ARCHITECT_APPROVAL_OF_TS,
        "name": "Architect Approval of Technical Specification",
        "description": "Solution/technical architect sign-off on the generated Technical Specification.",
        "sequence_order": 2,
        "entity_type": "TechnicalSpecification",
        "required_role": "ARCHITECT",
        "allow_self_approval": False,
    },
    {
        "gate_key": GATE_3_DEVELOPER_APPROVAL_OF_SAP_DESIGN,
        "name": "Developer Approval of Generated SAP Design",
        "description": "Developer review/sign-off of the generated SAP design (RAP/CDS/OData) before packaging.",
        "sequence_order": 3,
        "entity_type": "SapExecutionPackage",
        "required_role": "DEVELOPER",
        "allow_self_approval": False,
    },
    {
        "gate_key": GATE_4_DEVELOPER_APPROVAL_BEFORE_OBJECT_CREATION,
        "name": "Developer Approval Before Object Creation",
        "description": "Explicit developer approval immediately before any SAP object is created in the target system.",
        "sequence_order": 4,
        "entity_type": "SapObject",
        "required_role": "DEVELOPER",
        "allow_self_approval": False,
    },
    {
        "gate_key": GATE_5_LEAD_APPROVAL_BEFORE_ACTIVATION,
        "name": "Lead Approval Before Activation",
        "description": "Technical/team lead approval immediately before activating any created SAP object.",
        "sequence_order": 5,
        "entity_type": "SapObject",
        "required_role": "LEAD",
        "allow_self_approval": False,
    },
]
