from src.reward_support.orchestration.state import WorkflowState, add_audit_event
from src.reward_support.integrations.balance_api import balance_api
from src.reward_support.integrations.voucher_api import voucher_api
from src.reward_support.integrations.campaign_api import campaign_api


def data_agent(state: WorkflowState) -> WorkflowState:
    intent = state.get("intent", "general_support")
    user_id = state.get("user_id", "C001")
    scenario = state.get("scenario") or "low_risk"

    backend_data = {}
    required_apis = []

    if intent == "reward_issue":
        required_apis = ["balance_api", "voucher_api"]
        balance = balance_api(user_id, scenario)
        voucher = voucher_api(user_id, scenario)

        backend_data = {
            "balance": balance,
            "voucher": voucher,
        }

    elif intent == "campaign_issue":
        required_apis = ["campaign_api"]
        campaign = campaign_api(user_id, scenario)

        backend_data = {
            "campaign": campaign,
        }

    elif intent == "balance_issue":
        required_apis = ["balance_api"]
        balance = balance_api(user_id, scenario)

        backend_data = {
            "balance": balance,
        }

    state["required_apis"] = required_apis
    state["backend_data"] = backend_data

    add_audit_event(
        state,
        step="data_agent",
        message=(
            f"Fetched backend data using scenario: {scenario}; "
            f"required APIs: {', '.join(required_apis) if required_apis else 'none'}"
        ),
    )

    return state
