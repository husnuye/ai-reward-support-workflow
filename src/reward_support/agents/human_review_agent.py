from src.reward_support.orchestration.state import WorkflowState, add_audit_event
from src.reward_support.services.ticket_service import create_review_ticket


def human_review_agent(state: WorkflowState) -> WorkflowState:
    state["review_ticket"] = create_review_ticket(
        customer_id=state.get("user_id", "unknown"),
        reason=state.get("human_review_reason") or state.get("decision_reason") or "Manual review required",
        trace_id=state.get("trace_id", ""),
        priority="high" if state.get("risk_level") == "high" else "normal",
    )

    add_audit_event(
        state,
        step="human_review_agent",
        message=(
            "Human review ticket created: "
            f"{state['review_ticket']['ticket_id']}"
        ),
    )

    return state
