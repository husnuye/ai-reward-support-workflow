from src.reward_support.orchestration.state import WorkflowState, add_audit_event


def decision_agent(state: WorkflowState) -> WorkflowState:
    risk = state.get("risk_level", "medium")
    intent = state.get("intent")
    backend_data = state.get("backend_data", {})

    decision = "flag_for_review"
    decision_reason = "Default decision applied"

    # --- LOW RISK ---
    if risk == "low":
        decision = "auto_respond"

        if intent == "reward_issue":
            decision_reason = "Voucher exists and no inconsistency detected"

        elif intent == "campaign_issue":
            decision_reason = "Campaign state is valid or non-critical"

        else:
            decision_reason = "Low risk request can be handled automatically"

    # --- MEDIUM RISK ---
    elif risk == "medium":
        decision = "flag_for_review"

        if intent == "campaign_issue":
            decision_reason = (
                "Campaign appears visible but not redeemable, possible display inconsistency"
            )

        else:
            decision_reason = "Moderate uncertainty requires manual verification"

    # --- HIGH RISK ---
    elif risk == "high":
        decision = "escalate_to_human"

        balance = backend_data.get("balance", {})
        voucher = backend_data.get("voucher", {})

        if balance and voucher:
            if balance.get("balance_deducted") and not voucher.get("voucher_found"):
                decision_reason = (
                    "Balance was deducted but voucher was not generated, indicates transaction inconsistency"
                )
            else:
                decision_reason = "High-risk inconsistency detected in backend data"

        else:
            decision_reason = "High risk scenario requires human intervention"

    # --- FALLBACK ---
    else:
        decision = "flag_for_review"
        decision_reason = "Unknown risk level, fallback decision applied"

    state["decision"] = decision
    state["decision_reason"] = decision_reason

    add_audit_event(
        state,
        step="decision_agent",
        message=f"Decision made: {decision} | Reason: {decision_reason}",
    )

    return state
