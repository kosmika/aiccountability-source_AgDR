"""
Human Delta Chain types for AgDR v0.2
"""

from dataclasses import dataclass, field
from typing import Optional, Any


# Action codes — see human-delta-chain-spec.md
ACTION_HALTED = -1
ACTION_ESCALATED = 0
ACTION_APPROVED_AS_IS = 1
ACTION_APPROVED_WITH_MODIFICATION = 2

ACTION_LABELS = {
    ACTION_HALTED: "halted",
    ACTION_ESCALATED: "escalated",
    ACTION_APPROVED_AS_IS: "approved_as_is",
    ACTION_APPROVED_WITH_MODIFICATION: "approved_with_modification",
}


@dataclass
class HumanDelta:
    """
    A single human intervention in the delta chain.

    Parameters
    ----------
    actor : str
        Full legal name of the reviewing human.
    role : str
        Organizational role (e.g., "Senior Trader", "Chief Medical Officer").
    action : int
        -1 = halted, 0 = escalated, 1 = approved_as_is, 2 = approved_with_modification.
    modification : dict, optional
        If action == 2, describes what was changed.
    escalation_reason : str, optional
        If action == 0, why the decision was escalated.
    employee_id : str, optional
        Organizational employee identifier.
    jurisdiction : str, optional
        Legal jurisdiction of the actor.
    """

    actor: str
    role: str
    action: int
    modification: Optional[dict] = None
    escalation_reason: Optional[str] = None
    employee_id: Optional[str] = None
    jurisdiction: Optional[str] = None
    timestamp_ns: Optional[int] = None  # set automatically by aki_capture if None

    def __post_init__(self) -> None:
        if self.action not in ACTION_LABELS:
            raise ValueError(
                f"action must be one of {list(ACTION_LABELS.keys())}, got {self.action}"
            )
        if self.action == ACTION_APPROVED_WITH_MODIFICATION and not self.modification:
            raise ValueError("modification is required when action == approved_with_modification")
        if self.action == ACTION_ESCALATED and not self.escalation_reason:
            raise ValueError("escalation_reason is required when action == escalated")

    def to_dict(self, sequence: int, delta_id: str) -> dict:
        d = {
            "delta_id": delta_id,
            "sequence": sequence,
            "actor": {
                "name": self.actor,
                "role": self.role,
            },
            "action": self.action,
            "action_label": ACTION_LABELS[self.action],
            "escalated": self.action == ACTION_ESCALATED,
            "timestamp_ns": self.timestamp_ns,
        }
        if self.employee_id:
            d["actor"]["employee_id"] = self.employee_id
        if self.jurisdiction:
            d["actor"]["jurisdiction"] = self.jurisdiction
        if self.modification:
            d["modification"] = self.modification
        if self.escalation_reason:
            d["escalation_reason"] = self.escalation_reason
        return d


@dataclass
class FOIEscalation:
    """
    Terminal FOI node — see foi-formal-definition.md

    Parameters
    ----------
    actor : str
        Full legal name of the Fiduciary Office Intervener.
    title : str
        Formal title conferring fiduciary authority (e.g., "Chief Compliance Officer").
    decision : str
        Human-readable description of the FOI's decision.
    decision_code : int
        1 = approved, 0 = halted/modified.
    rationale : str, optional
        Explanation of the FOI's reasoning.
    jurisdiction : str, optional
        Legal jurisdiction of the FOI.
    """

    actor: str
    title: str
    decision: str
    decision_code: int
    rationale: Optional[str] = None
    jurisdiction: Optional[str] = None
    timestamp_ns: Optional[int] = None  # set automatically by aki_capture if None

    def __post_init__(self) -> None:
        if self.decision_code not in (0, 1):
            raise ValueError("decision_code must be 0 (halted) or 1 (approved)")

    def to_dict(self) -> dict:
        d = {
            "type": "foi_escalation",
            "actor": {
                "name": self.actor,
                "title": self.title,
            },
            "decision": self.decision,
            "decision_code": self.decision_code,
            "timestamp_ns": self.timestamp_ns,
        }
        if self.jurisdiction:
            d["actor"]["jurisdiction"] = self.jurisdiction
        if self.rationale:
            d["rationale"] = self.rationale
        return d
