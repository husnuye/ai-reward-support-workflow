import json
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

from src.reward_support.orchestration.state import WorkflowState, add_audit_event


load_dotenv()


VALID_INTENTS = {
    "reward_issue",
    "campaign_issue",
    "balance_issue",
    "refund_request",
    "general_support",
}

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
MIN_CONFIDENCE = 0.60


def fallback_detect_intent(message: str) -> tuple[str, float]:
    message = message.lower()

    if (
        "campaign" in message
        or "can't redeem" in message
        or "can’t redeem" in message
        or "cannot redeem" in message
        or "not redeemable" in message
    ):
        return "campaign_issue", 0.85

    if (
        "balance" in message
        or "deducted" in message
        or "charged" in message
        or "not created" in message
    ):
        return "reward_issue", 0.85

    if (
        ("where" in message or "find" in message or "locate" in message or "can't find" in message or "can’t find" in message)
        and ("voucher" in message or "reward" in message)
    ):
        return "reward_issue", 0.85

    if "refund" in message:
        return "refund_request", 0.85

    if "voucher" in message or "reward" in message:
        return "reward_issue", 0.65

    return "general_support", 0.50


def classify_intent_with_llm(message: str) -> tuple[str, float]:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set")

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are an intent classification agent for a reward redemption support workflow.

Classify the customer message into exactly one intent.

Valid intents:
- reward_issue: missing voucher, voucher not created, voucher cannot be found, reward status questions
- campaign_issue: campaign visible but inactive, cannot redeem campaign, campaign eligibility or display issue
- balance_issue: balance or points issue without clear voucher context
- refund_request: user asks for refund
- general_support: unclear or unrelated

Return ONLY valid JSON in this exact format:
{{
  "intent": "one_of_the_valid_intents",
  "confidence": 0.0
}}

Customer message:
{message}
"""

    response = client.responses.create(
        model=DEFAULT_MODEL,
        input=prompt,
    )

    data = parse_intent_json(response.output_text)

    intent = data.get("intent", "general_support")
    confidence = normalize_confidence(data.get("confidence", 0.0))

    if intent not in VALID_INTENTS or confidence < MIN_CONFIDENCE:
        return "general_support", 0.0

    return intent, confidence


def parse_intent_json(output_text: str) -> dict:
    try:
        return json.loads(output_text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", output_text, re.DOTALL)
        if not match:
            raise

        return json.loads(match.group(0))


def normalize_confidence(value) -> float:
    confidence = float(value)
    return max(0.0, min(1.0, confidence))


def intent_agent(state: WorkflowState) -> WorkflowState:
    message = state.get("redacted_customer_message") or state["customer_message"]

    try:
        intent, confidence = classify_intent_with_llm(message)
        mode = "llm"

    except Exception as error:
        intent, confidence = fallback_detect_intent(message)
        mode = "fallback"
        state["fallback_used"] = True

        add_audit_event(
            state,
            step="intent_agent",
            message=f"LLM intent classification failed, fallback used: {str(error)}",
        )

    state["intent"] = intent
    state["intent_confidence"] = confidence
    state["intent_mode"] = mode

    add_audit_event(
        state,
        step="intent_agent",
        message=f"Detected intent: {intent} with confidence {confidence:.2f} using {mode}",
    )

    return state
