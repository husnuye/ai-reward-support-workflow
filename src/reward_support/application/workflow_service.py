from typing import Any, Dict

from src.reward_support.orchestration.state import create_initial_state
from src.reward_support.orchestration.langgraph_workflow import run_langgraph_workflow
from src.reward_support.services.pii_redaction import redact_pii


class RewardSupportWorkflowService:
    """
    Application service layer.

    This class separates the UI from the workflow/orchestration logic.
    The Streamlit app calls this service instead of directly calling agents
    or orchestration internals.

    Main orchestration path:
    - LangGraph workflow
    """

    def run(
        self,
        customer_message: str,
        user_id: str = "C001",
        scenario: str | None = None,
    ) -> Dict[str, Any]:

        state = create_initial_state(
            user_id=user_id,
            customer_message=customer_message,
        )

        state["scenario"] = scenario
        state["redacted_customer_message"] = redact_pii(customer_message)

        state = run_langgraph_workflow(state)

        return {
            "response": state.get("response"),
            "trace_id": state.get("trace_id"),
            "redacted_customer_message": state.get("redacted_customer_message"),
            "intent": state.get("intent"),
            "intent_confidence": state.get("intent_confidence"),
            "intent_mode": state.get("intent_mode"),
            "required_apis": state.get("required_apis"),
            "risk_signals": state.get("risk_signals"),
            "risk_level": state.get("risk_level"),
            "decision": state.get("decision"),
            "decision_reason": state.get("decision_reason"),
            "requires_human_review": state.get("requires_human_review"),
            "human_review_reason": state.get("human_review_reason"),
            "review_ticket": state.get("review_ticket"),
            "backend_data": state.get("backend_data"),
            "response_mode": state.get("response_mode"),
            "fallback_used": state.get("fallback_used"),
            "audit_log": state.get("audit_log"),
            "errors": state.get("errors"),
        }
