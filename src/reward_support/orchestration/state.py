from typing import TypedDict, Optional, Literal, List, Dict, Any
from datetime import datetime, timezone
import time
from uuid import uuid4


RiskLevel = Literal["low", "medium", "high"]
Decision = Literal["auto_respond", "flag_for_review", "escalate_to_human"]


class AuditEvent(TypedDict):
    timestamp: str
    step: str
    message: str
    duration_ms: Optional[float]


class WorkflowState(TypedDict, total=False):
    trace_id: str

    # Input
    user_id: str
    customer_message: str
    redacted_customer_message: str
    scenario: Optional[str]

    # Agent outputs
    intent: Optional[str]
    intent_confidence: Optional[float]
    intent_mode: Optional[str]
    required_apis: List[str]
    backend_data: Dict[str, Any]
    risk_signals: List[str]
    risk_level: Optional[RiskLevel]
    decision: Optional[Decision]
    decision_reason: Optional[str]

    # Human-in-the-loop
    requires_human_review: bool
    human_review_reason: Optional[str]

    # Final output
    response: Optional[str]
    response_mode: Optional[str]
    review_ticket: Optional[Dict[str, Any]]

    # Production / reliability
    fallback_used: bool
    errors: List[str]
    audit_log: List[AuditEvent]


def create_initial_state(user_id: str, customer_message: str) -> WorkflowState:
    return {
        "trace_id": str(uuid4()),
        "user_id": user_id,
        "customer_message": customer_message,
        "redacted_customer_message": customer_message,
        "scenario": None,
        "intent": None,
        "intent_confidence": None,
        "intent_mode": None,
        "required_apis": [],
        "backend_data": {},
        "risk_signals": [],
        "risk_level": None,
        "decision": None,
        "decision_reason": None,
        "requires_human_review": False,
        "human_review_reason": None,
        "response": None,
        "response_mode": None,
        "review_ticket": None,
        "fallback_used": False,
        "errors": [],
        "audit_log": [
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "step": "workflow_started",
                "message": "Workflow initialized",
                "duration_ms": None,
            }
        ],
    }


def add_audit_event(
    state: WorkflowState,
    step: str,
    message: str,
    duration_ms: Optional[float] = None,
) -> WorkflowState:
    state["audit_log"].append(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "step": step,
            "message": message,
            "duration_ms": duration_ms,
        }
    )
    return state


def track_step(state: WorkflowState, step_name: str, func) -> WorkflowState:
    start = time.time()

    state = func(state)

    duration_ms = (time.time() - start) * 1000

    add_audit_event(
        state,
        step=step_name,
        message="Step completed",
        duration_ms=round(duration_ms, 2),
    )

    return state


def add_error(state: WorkflowState, step: str, error: Exception) -> WorkflowState:
    error_message = f"{step} failed: {str(error)}"

    state["errors"].append(error_message)

    add_audit_event(
        state,
        step=step,
        message=error_message,
        duration_ms=None,
    )

    return state


def safe_step(state: WorkflowState, step_name: str, func) -> WorkflowState:
    try:
        return track_step(state, step_name, func)

    except Exception as error:
        add_error(state, step_name, error)

        state["risk_level"] = "high"
        state["decision"] = "escalate_to_human"
        state["decision_reason"] = f"Workflow step failed: {step_name}"
        state["requires_human_review"] = True
        state["human_review_reason"] = (
            f"Workflow step failed and requires manual review: {step_name}"
        )

        add_audit_event(
            state,
            step="fallback",
            message=f"Fallback triggered after failure in {step_name}",
        )

        return state
