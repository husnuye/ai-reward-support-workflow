from src.reward_support.orchestration.state import WorkflowState, add_audit_event


def evaluate_risk(intent: str, backend_data: dict) -> tuple[str, str | None, list[str]]:
    """
    Returns:
        risk_level, human_review_reason, risk_signals
    """
    signals = []

    if intent == "reward_issue":
        balance = backend_data.get("balance", {})
        voucher = backend_data.get("voucher", {})

        if balance.get("transaction_status") in {"customer_not_found", "unavailable"}:
            signals.append("backend_data_unavailable")
            return "high", "Reward data could not be validated from backend systems.", signals

        if balance.get("balance_deducted") and not voucher.get("voucher_found"):
            signals.extend(["balance_deducted", "voucher_missing"])
            return "high", "Balance was deducted but voucher was not generated.", signals

        if voucher.get("voucher_found"):
            signals.append("voucher_found")

        return "low", None, signals

    if intent == "campaign_issue":
        campaign = backend_data.get("campaign", {})

        if campaign.get("campaign_visible") and not campaign.get("campaign_active"):
            signals.extend(["campaign_visible", "campaign_inactive"])
            return "medium", "Campaign is visible but inactive or not redeemable.", signals

        signals.append("campaign_valid_or_not_visible")
        return "low", None, signals

    if intent == "balance_issue":
        balance = backend_data.get("balance", {})

        if balance.get("transaction_status") in {"customer_not_found", "unavailable"}:
            signals.append("backend_data_unavailable")
            return "high", "Balance issue could not be validated from backend data.", signals

        if balance.get("balance_deducted") and balance.get("transaction_status") == "completed":
            signals.extend(["balance_deducted", "completed_transaction"])
            return "medium", "Balance transaction requires verification.", signals

        signals.append("balance_unvalidated")
        return "high", "Balance issue could not be validated from backend data.", signals

    if intent == "refund_request":
        signals.append("refund_requires_approval")
        return "high", "Refund requests require human approval.", signals

    signals.append("unclear_intent")
    return "medium", "Intent is unclear and requires review.", signals


def risk_agent(state: WorkflowState) -> WorkflowState:
    intent = state.get("intent", "general_support")
    backend_data = state.get("backend_data", {})

    risk_level, review_reason, risk_signals = evaluate_risk(intent, backend_data)

    state["risk_level"] = risk_level
    state["risk_signals"] = risk_signals

    if risk_level == "high":
        state["requires_human_review"] = True
        state["human_review_reason"] = review_reason
    else:
        state["requires_human_review"] = False
        state["human_review_reason"] = review_reason

    add_audit_event(
        state,
        step="risk_agent",
        message=f"Risk level evaluated as: {risk_level}; signals: {', '.join(risk_signals) or 'none'}",
    )

    return state
