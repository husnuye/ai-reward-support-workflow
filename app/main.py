import streamlit as st
import json
from datetime import datetime
import os
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()
# Use environment variable or a test key for development
api_key = os.getenv("OPENAI_API_KEY", "sk-test-key-for-testing")
client = OpenAI(api_key=api_key)
# ============================================================
# AI REWARD REDEMPTION SUPPORT WORKFLOW
# ============================================================

SCENARIOS = {
    "high_risk": {
        "label": "High Risk — Balance deducted, voucher missing (Balance transaction exists, but voucher record is missing.)",
        "message": "My balance was deducted but my flight voucher was not created."
    },
    "medium_risk": {
        "label": "Medium Risk — Expired campaign still visible (Campaign is visible but inactive in backend.)",
        "message": "I can still see the flight voucher campaign, but I can’t redeem it."
    },
    "low_risk": {
        "label": "Low Risk — Voucher already issued (Voucher exists and is available to the user.)",
        "message": "I redeemed a $500 flight voucher, but I can’t find it."
    }
}



def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# ============================================================
# AGENTS
# ============================================================

def intent_agent(message: str):
    msg = message.lower()

    if "voucher" in msg and ("where" in msg or "status" in msg or "find" in msg):
        return {
            "intent": "voucher_status",
            "confidence": 0.91
        }

    if (
        "balance" in msg
        or "deducted" in msg
        or "points" in msg
        or "not created" in msg
        or "doesn't appear" in msg
        or "doesn’t appear" in msg
    ):
        return {
            "intent": "reward_balance_issue",
            "confidence": 0.94
        }

    if (
        "campaign" in msg
        or "eligible" in msg
        or "can't redeem" in msg
        or "can’t redeem" in msg
        or "redeem" in msg
    ):
        return {
            "intent": "campaign_issue",
            "confidence": 0.86
        }

    return {
        "intent": "unknown",
        "confidence": 0.45
    }


def router_agent(intent):
    """
    Router Agent:
    Decides which backend tools/APIs should be called
    based on the detected intent.
    """

    if intent == "reward_balance_issue":
        return {
            "tools": ["Balance API", "Voucher API"],
            "reason": "Verify balance deduction and check if voucher was created."
        }

    if intent == "voucher_status":
        return {
            "tools": ["Voucher API"],
            "reason": "Retrieve voucher status from backend."
        }

    if intent == "campaign_issue":
        return {
            "tools": ["Campaign API"],
            "reason": "Check campaign status and validate if it is active or incorrectly displayed."
        }

    return {
        "tools": [],
        "reason": "No matching intent, no tools selected."
    }


def risk_agent(intent_res, balance_res, voucher_res, campaign_res):
    intent = intent_res["intent"]

    if intent_res["confidence"] < 0.7:
        return {
            "risk_level": "unknown",
            "action": "escalate",
            "reason": "Low intent confidence."
        }

    if intent == "reward_balance_issue":
        if balance_res["balance_deducted"] and not voucher_res["voucher_found"]:
            return {
                "risk_level": "high",
                "action": "escalate",
                "reason": "Balance was deducted but voucher was not created."
            }

    if intent == "campaign_issue":
        if campaign_res.get("campaign_visible") and not campaign_res.get("campaign_active"):
            return {
                "risk_level": "medium",
                "action": "flag_campaign_display_issue",
                "reason": "Campaign is visible in the app but inactive in the backend."
            }

    if intent == "voucher_status":
        if voucher_res["voucher_found"]:
            return {
                "risk_level": "low",
                "action": "auto_respond",
                "reason": "Voucher exists and status can be safely shared."
            }

    return {
        "risk_level": "unknown",
        "action": "escalate",
        "reason": "No safe automation path matched."
    }

def response_agent(risk_res, balance_res, voucher_res, campaign_res):

    context = {
        "risk": risk_res,
        "balance": balance_res,
        "voucher": voucher_res,
        "campaign": campaign_res
    }

    instructions = """
You are a customer support AI agent for a reward redemption system.

Your task is to generate a clear, helpful, and professional response to the customer,
based only on the provided backend data.

Rules:
- Do not guess or assume anything.
- Only use the given backend context.
- Do not mention internal systems, JSON, APIs, or technical details.
- Do not make unsupported promises.

Opening guidelines:
- If the customer is reporting a problem or issue, acknowledge the concern (e.g. "I understand your concern")
- If it is a general inquiry, you may start with "Thanks for your message"
- Choose the most appropriate opening based on the situation

Response structure:
- Start with an appropriate acknowledgment (not always "Thanks")
- Clearly explain the situation in simple, user-friendly terms
- If there is an issue, explain what went wrong based on the data
- Reassure the customer when appropriate
- Explain the next step (e.g. escalation, fix, or where to check)
- End with a professional and neutral closing sentence

Tone:
- Friendly, calm, and professional
- Clear and human-like (not robotic)
- Reassuring and structured

Closing guidelines:
- Always use a professional closing
- Prefer:
  "Please let us know if you need any further assistance."
- Avoid casual phrases like:
  "happy to help", "let me know", "I’d be happy to help further"

Guidance based on scenarios:

- Balance inconsistency:
  Explain that the balance was deducted but the voucher was not created,
  and inform the user that the issue is being escalated.

- Campaign display issue:
  Explain that the campaign is no longer active,
  clearly state that it can no longer be redeemed,
  mention that it is still visible due to a display issue,
  and reassure the user that their balance has not been affected.

- Voucher issued:
  Confirm that the voucher has already been issued,
  guide the user to check the "My Rewards" section,
  and suggest checking their registered email (including spam folder).

Goal:
Generate a response that feels like it was written by a professional customer support agent,
while staying fully grounded in backend data.

Keep the response concise but complete.
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=instructions,
            input=f"Backend context: {context}"
        )

        return response.output_text

    except Exception:
        action = risk_res["action"]

        if action == "escalate":
            return (
                "I understand your concern. I can see that your balance was deducted, "
                "but the flight voucher was not created.\n\n"
                "This appears to be an issue, and I’m escalating it to our support team "
                "so it can be resolved as quickly as possible.\n\n"
                "Please don’t worry — we’ll make sure this is taken care of. "
                "Please let us know if you need any further assistance."
            )

        if action == "flag_campaign_display_issue":
            return (
                "I understand your concern. I’ve checked the campaign, and it is no longer active, "
                "even though it is still visible in the app.\n\n"
                "Because the campaign has expired, it can no longer be redeemed. "
                "This appears to be a display issue, and I’ve flagged it to the relevant team "
                "so it can be corrected. Your balance has not been affected.\n\n"
                "Please let us know if you need any further assistance."
            )

        if action == "auto_respond":
            return (
                "Thanks for your message. I’ve checked your flight voucher and it has already been issued.\n\n"
                "You can find it in your account under the My Rewards section. "
                "It has also been sent to your registered email, so I recommend checking your inbox "
                "or spam folder.\n\n"
                "Please let us know if you need any further assistance."
            )

        return "Please let us know if you need any further assistance."
# ============================================================
# API / TOOL SIMULATION
# ============================================================

def balance_api(customer_id: str, scenario: str):
    if scenario in ["high_risk", "low_risk"]:
        return {
            "customer_id": customer_id,
            "balance_deducted": True,
            "amount": 500,
            "currency": "USD",
            "transaction_status": "completed",
            "transaction_id": "TXN-9001"
        }

    return {
        "customer_id": customer_id,
        "balance_deducted": False,
        "amount": 0,
        "currency": "USD",
        "transaction_status": "not_found",
        "transaction_id": None
    }


def voucher_api(customer_id: str, scenario: str):
    if scenario == "low_risk":
        return {
            "customer_id": customer_id,
            "voucher_found": True,
            "voucher_id": "VCH-1001",
            "amount": 500,
            "currency": "USD",
            "status": "issued",
            "delivery_method": "email",
            "location": "My Rewards"
        }

    return {
        "customer_id": customer_id,
        "voucher_found": False,
        "voucher_id": None,
        "amount": 0,
        "currency": "USD",
        "status": "missing",
        "delivery_method": None,
        "location": None
    }


def campaign_api(customer_id: str, scenario: str):
    if scenario == "medium_risk":
        return {
            "customer_id": customer_id,
            "checked": True,
            "campaign_visible": True,
            "campaign_active": False,
            "issue": "expired_campaign_still_visible",
            "message": "Campaign is visible in the app, but it is no longer active in the backend."
        }

    return {
        "customer_id": customer_id,
        "checked": False,
        "campaign_visible": False,
        "campaign_active": None,
        "issue": None,
        "message": None
    }


def create_ticket(customer_id: str, risk_res):
    tickets = load_json("data/support_tickets.json")

    ticket = {
        "ticket_id": f"TCK-{len(tickets) + 1:04d}",
        "customer_id": customer_id,
        "priority": "high" if risk_res["risk_level"] == "high" else "normal",
        "reason": risk_res["reason"],
        "created_at": datetime.utcnow().isoformat()
    }

    tickets.append(ticket)
    save_json("data/support_tickets.json", tickets)

    return ticket


# ============================================================
# ORCHESTRATION
# ============================================================

def run_workflow(message: str, scenario: str, customer_id: str = "C001"):
    trace = []

    intent_res = intent_agent(message)
    trace.append(("Intent Agent", intent_res))

    router_res = router_agent(intent_res["intent"])
    trace.append(("Router Agent", router_res))

    balance_res = balance_api(customer_id, scenario)
    voucher_res = voucher_api(customer_id, scenario)
    campaign_res = campaign_api(customer_id, scenario)

    trace.append(("Balance API", balance_res))
    trace.append(("Voucher API", voucher_res))
    trace.append(("Campaign API", campaign_res))

    risk_res = risk_agent(intent_res, balance_res, voucher_res, campaign_res)
    trace.append(("Risk Agent", risk_res))

    if risk_res["action"] == "escalate":
        ticket = create_ticket(customer_id, risk_res)
        trace.append(("Ticket Action", ticket))

    response = response_agent(risk_res, balance_res, voucher_res, campaign_res)
    trace.append(("Response Agent", {"response": response}))

    return response, trace, risk_res


# ============================================================
# UI
# ============================================================

st.set_page_config(
    page_title="AI Reward Support Workflow",
    layout="wide"
)

st.markdown("""
<style>
    .block-container {
        max-width: 1180px;
        padding-top: 34px;
        padding-bottom: 36px;
        padding-left: 3.5rem;
        padding-right: 3.5rem;
    }

    .app-title {
        font-size: 38px;
        font-weight: 850;
        color: #F9FAFB;
        margin-bottom: 6px;
        letter-spacing: -0.03em;
    }

    .app-subtitle {
        font-size: 15px;
        color: #94A3B8;
        margin-bottom: 28px;
    }

    .section-title {
        font-size: 21px;
        font-weight: 800;
        color: #F9FAFB;
        margin-top: 8px;
        margin-bottom: 12px;
    }

    .workflow-step {
        background: #0F172A;
        border: 1px solid #243244;
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 10px;
        color: #E5E7EB;
        font-size: 14px;
    }

    .workflow-step strong {
        color: #FFFFFF;
    }

    .scenario-note {
        color: #CBD5E1;
        font-size: 14px;
        line-height: 1.5;
        margin-top: 8px;
        margin-bottom: 18px;
    }

    .response-card {
        background: #F8FAFC;
        color: #111827;
        padding: 24px 28px;
        border-radius: 14px;
        border: 1px solid #E5E7EB;
        font-size: 16px;
        line-height: 1.75;
        box-shadow: 0 10px 26px rgba(0,0,0,0.20);
        width: 100%;
    }

    .decision-bar {
        display: grid;
        grid-template-columns: 160px 210px 1fr;
        align-items: center;
        background: #111827;
        border: 1px solid #243244;
        border-radius: 12px;
        margin-top: 14px;
        overflow: hidden;
    }

    .decision-item {
        padding: 12px 16px;
        border-right: 1px solid #243244;
        min-height: 52px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .decision-item:last-child {
        border-right: none;
    }

    .decision-label {
        color: #94A3B8;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .risk-high {
        color: #F87171;
        font-size: 17px;
        font-weight: 850;
    }

    .risk-medium {
        color: #FBBF24;
        font-size: 17px;
        font-weight: 850;
    }

    .risk-low {
        color: #34D399;
        font-size: 17px;
        font-weight: 850;
    }

    .action-value {
        color: #F9FAFB;
        font-size: 16px;
        font-weight: 800;
    }

    .reason-value {
        color: #CBD5E1;
        font-size: 13.5px;
        line-height: 1.4;
    }

    div.stButton > button {
        height: 48px;
        font-size: 16px;
        font-weight: 750;
        border-radius: 12px;
        background: linear-gradient(135deg, #2563EB, #7C3AED);
        border: none;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8, #6D28D9);
        border: none;
    }

    textarea {
        font-size: 15px !important;
    }

    hr {
        margin-top: 22px;
        margin-bottom: 22px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="app-title">AI Reward Support Workflow</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Agent orchestration for reward redemption support issues</div>',
    unsafe_allow_html=True
)

left_col, main_col = st.columns([0.85, 3.15], gap="large")

with left_col:
    st.markdown('<div class="section-title">Workflow Steps</div>', unsafe_allow_html=True)

    steps = [
        ("1. Intent Agent", "Understand customer request"),
        ("2. Router Agent", "Select required APIs"),
        ("3. Backend APIs", "Fetch backend data"),
        ("4. Risk Agent", "Evaluate risk and action"),
        ("5. Response Agent", "Generate customer response")
    ]

    for title, desc in steps:
        st.markdown(
            f"""
            <div class="workflow-step">
                <strong>{title}</strong><br>
                <span style="color:#94A3B8;">{desc}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("**System Status**")
    st.markdown('<span style="color:#34D399;">● Operational</span>', unsafe_allow_html=True)
    st.caption("Simulated APIs + LLM response agent")

with main_col:
    st.markdown('<div class="section-title">Scenario</div>', unsafe_allow_html=True)

    scenario_label = st.selectbox(
        "Demo backend state",
        [SCENARIOS[key]["label"] for key in SCENARIOS]
    )

    selected_scenario = next(
        key for key, value in SCENARIOS.items()
        if value["label"] == scenario_label
    )

    customer_message = st.text_area(
        "Customer message",
        value=SCENARIOS[selected_scenario]["message"],
        height=105
    )

    if st.button("Run AI Workflow", type="primary", use_container_width=True):
        with st.spinner("Running agent orchestration..."):
            response, trace, risk_res = run_workflow(customer_message, selected_scenario)

        st.session_state["response"] = response
        st.session_state["trace"] = trace
        st.session_state["risk_res"] = risk_res

    if "response" in st.session_state:
        response = st.session_state["response"]
        trace = st.session_state["trace"]
        risk_res = st.session_state["risk_res"]


        st.markdown('<div class="section-title">Customer Response</div>', unsafe_allow_html=True)

        st.markdown(
            f'<div class="response-card">{response}</div>',
            unsafe_allow_html=True
        )

    

        st.caption("Generated by LLM using verified backend context")

        st.markdown('<div class="section-title">Agent / API Trace</div>', unsafe_allow_html=True)

        for step, data in trace:
            with st.expander(step, expanded=False):
                st.json(data)