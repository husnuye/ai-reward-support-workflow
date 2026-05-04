import os
from dotenv import load_dotenv
from openai import OpenAI

from src.reward_support.orchestration.state import WorkflowState, add_audit_event


load_dotenv()
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def build_fallback_response(state: WorkflowState) -> str:
    decision = state.get("decision")
    intent = state.get("intent")
    backend_data = state.get("backend_data", {})
    reason = state.get("human_review_reason")

    voucher = backend_data.get("voucher", {})
    campaign = backend_data.get("campaign", {})
    balance = backend_data.get("balance", {})

    if decision == "auto_respond" and intent == "reward_issue":
        if voucher.get("voucher_found"):
            return (
                "Thanks for reaching out. I checked your reward information and confirmed that "
                "your flight voucher has already been issued.\n\n"
                "You can find it in the My Rewards section of your account. It may also have been sent "
                "to your registered email address, so please check your inbox and spam folder as well.\n\n"
                "Please let us know if you need any further assistance."
            )

    if decision == "flag_for_review" and intent == "campaign_issue":
        return (
            "I understand your concern. The flight voucher campaign appears to be visible in the app, "
            "but it is no longer active and cannot be redeemed.\n\n"
            "This looks like a campaign display issue rather than a problem with your account balance. "
            "We have flagged it for review so the campaign visibility can be corrected.\n\n"
            "Please let us know if you need any further assistance."
        )

    if decision == "escalate_to_human":
        if balance.get("balance_deducted") and not voucher.get("voucher_found"):
            return (
                "I understand your concern. I checked the available reward information and can see that "
                "your balance was deducted, but the flight voucher was not created.\n\n"
                "This requires review by a support specialist. Our support team will verify the case "
                "and follow up as soon as possible.\n\n"
                "Please let us know if you need any further assistance."
            )

        return (
            "I understand your concern. This request requires review by a support specialist.\n\n"
            f"Reason: {reason}\n\n"
            "Our support team will review the case and follow up as soon as possible."
        )

    return (
        "Thanks for reaching out. Your request has been received and will be reviewed.\n\n"
        "Please let us know if you need any further assistance."
    )


def build_llm_response(state: WorkflowState) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set")

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are a professional customer support AI agent for a reward redemption system.

Your job is to write the final customer-facing response.
You do NOT make decisions. The workflow has already classified the issue, checked backend data, and selected the action.

Use ONLY the provided workflow state and backend data.
Do not invent information.
Do not mention JSON, APIs, internal systems, agents, orchestration, workflow state, or technical details.
Do not make unsupported promises.

Customer message:
{state.get("redacted_customer_message") or state.get("customer_message")}

Intent:
{state.get("intent")}

Risk level:
{state.get("risk_level")}

Decision:
{state.get("decision")}

Human review required:
{state.get("requires_human_review")}

Human review reason:
{state.get("human_review_reason")}

Backend data:
{state.get("backend_data")}

Write the response based on these rules:

1. If the decision is auto_respond and the voucher exists:
   - Confirm that the flight voucher has already been issued.
   - Tell the user to check the My Rewards section.
   - Mention that it may also be in their registered email inbox or spam folder.

2. If the decision is flag_for_review and the issue is campaign-related:
   - Explain that the campaign may still be visible in the app.
   - Explain that it is no longer active and cannot be redeemed.
   - Reassure the user that this appears to be a display issue.
   - Say it has been flagged for review.

3. If the decision is escalate_to_human:
   - Explain that the case requires review by a support specialist.
   - If balance was deducted and voucher was not created, clearly say that.
   - Do not promise an exact resolution time.

Tone:
- Calm
- Clear
- Professional
- Helpful
- Human-like

End exactly with:
Please let us know if you need any further assistance.
"""

    response = client.responses.create(
        model=DEFAULT_MODEL,
        input=prompt,
    )

    return response.output_text


def response_agent(state: WorkflowState) -> WorkflowState:
    try:
        response = build_llm_response(state)
        generation_mode = "llm"

    except Exception as error:
        response = build_fallback_response(state)
        generation_mode = "fallback"
        state["fallback_used"] = True

        add_audit_event(
            state,
            step="response_agent",
            message=f"LLM response generation failed, fallback used: {str(error)}",
        )

    state["response"] = response
    state["response_mode"] = generation_mode

    add_audit_event(
        state,
        step="response_agent",
        message=f"Generated final response using {generation_mode}",
    )

    return state
