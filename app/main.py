import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from dotenv import load_dotenv

from app.styles.global_styles import load_global_styles
from src.reward_support.application.workflow_service import RewardSupportWorkflowService
from src.reward_support.config.scenarios import SCENARIOS


load_dotenv()
workflow_service = RewardSupportWorkflowService()

st.set_page_config(
    page_title="AI Support Triage Console",
    layout="wide",
)

st.markdown(load_global_styles(), unsafe_allow_html=True)


WORKFLOW_STEPS = [
    ("Intent", "LLM + fallback"),
    ("Risk", "Rules + signals"),
    ("Decision", "Rules engine"),
    ("Human Review", "Conditional route"),
    ("Response", "LLM + fallback"),
    ("Timeline", "Trace + latency"),
]

UNSAFE_ERROR_PATTERNS = (
    "api key",
    "invalid_api_key",
    "401",
    "error code",
)

SAFE_LLM_FALLBACK_MESSAGE = "LLM unavailable, fallback used"


def format_duration(duration: float | None) -> str:
    if duration is None:
        return "not recorded"

    rounded = round(float(duration), 1)
    return f"{rounded:.1f} ms"


def sanitize_ui_message(message) -> str:
    text = str(message)
    lowered = text.lower()

    if any(pattern in lowered for pattern in UNSAFE_ERROR_PATTERNS):
        return SAFE_LLM_FALLBACK_MESSAGE

    if "llm" in lowered and "fallback" in lowered and "failed" in lowered:
        return "LLM unavailable, fallback classifier used"

    return text


def sanitize_audit_event(event: dict) -> dict:
    sanitized = dict(event)
    if "message" in sanitized:
        sanitized["message"] = sanitize_ui_message(sanitized["message"])

    return sanitized


def sanitized_audit_log(result: dict) -> list[dict]:
    return [
        sanitize_audit_event(event)
        for event in result.get("audit_log", [])
    ]


def format_value(value) -> str:
    if value is None:
        return "Not run yet"

    if isinstance(value, bool):
        return "Required" if value else "Not required"

    return str(value).replace("_", " ").title()


def format_list(values: list[str] | None) -> str:
    if not values:
        return "None"

    return ", ".join(value.replace("_", " ") for value in values)


def format_mode(value: str | None) -> str:
    return value if value in {"llm", "fallback"} else "not recorded"


def confidence_label(confidence: float | None) -> str:
    if confidence is None:
        return "N/A"

    if confidence >= 0.8:
        return "High"

    if confidence >= 0.6:
        return "Medium"

    return "Low"


def step_durations(result: dict) -> dict[str, float]:
    durations = {}

    for event in result.get("audit_log", []):
        duration = event.get("duration_ms")
        if duration is not None:
            durations[event["step"]] = duration

    return durations


def mode_label(value: str | None) -> str:
    return format_mode(value).upper()


def review_status(result: dict | None) -> str:
    if result and result.get("requires_human_review"):
        return "Triggered"

    if result:
        return "Not Required"

    return "Not run yet"


def risk_class(risk: str | None) -> str:
    if risk in {"low", "medium", "high"}:
        return f"risk-{risk}"

    return ""


def build_timeline(result: dict) -> list[tuple[str, str]]:
    apis = format_list(result.get("required_apis"))
    signals = format_list(result.get("risk_signals"))
    confidence = result.get("intent_confidence")
    confidence_display = f"{confidence:.2f}" if confidence is not None else "N/A"
    confidence_display = f"{confidence_display} {confidence_label(confidence)}"
    durations = step_durations(result)

    def with_duration(step_name: str, detail: str) -> str:
        duration = durations.get(step_name)
        if duration is None:
            return detail

        return f"{detail} · {format_duration(duration)}"

    items = [
        (
            "Intent",
            with_duration(
                "intent_agent",
                f"{format_value(result.get('intent'))} · {confidence_display}",
            ),
        ),
        ("Data", with_duration("data_agent", apis)),
        (
            "Risk",
            with_duration(
                "risk_agent",
                f"{format_value(result.get('risk_level'))} · {signals}",
            ),
        ),
        (
            "Decision",
            with_duration(
                "decision_agent",
                f"{format_value(result.get('decision'))} · {result.get('decision_reason')}",
            ),
        ),
    ]

    if result.get("review_ticket"):
        ticket = result["review_ticket"]
        items.append(
            (
                "Human Review",
                with_duration(
                    "human_review_agent",
                    f"{ticket['ticket_id']} · {ticket['assigned_queue']}",
                ),
            )
        )

    items.append(
        (
            "Response",
            with_duration("response_agent", "Customer-facing draft generated"),
        )
    )
    return items


def decision_explanation_items(result: dict) -> list[str]:
    items = [format_value(signal) for signal in result.get("risk_signals", [])]
    reason = result.get("decision_reason")

    if reason:
        items.append(reason)

    if not items:
        items.append("Decision policy evaluated the available support context")

    deduped = []
    for item in items:
        if item and item not in deduped:
            deduped.append(item)

    return deduped[:3]


def render_app_header() -> None:
    st.markdown(
        (
            '<div class="app-header">'
            '<div class="app-title">AI Support Decisioning Console</div>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        (
            '<div class="app-subtitle">'
            "Turns customer messages and backend reward signals into explainable decisions, "
            "human-in-the-loop review, and grounded support responses."
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def render_workflow_bar() -> None:
    steps_html = "\n".join(
        (
            '<div class="system-step">'
            f'<div class="system-step-label">{step}</div>'
            f'<div class="system-step-owner">{owner}</div>'
            "</div>"
        )
        for step, owner in WORKFLOW_STEPS
    )

    st.markdown(f'<div class="system-strip">{steps_html}</div>', unsafe_allow_html=True)


def render_metric_card(label: str, value) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_case_intake() -> None:
    with st.container(border=True):
        st.markdown('<div class="section-title">Case Intake</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-caption">Select a support case and run the agent workflow.</div>',
            unsafe_allow_html=True,
        )

        scenario_label = st.selectbox(
            "Support scenario",
            [SCENARIOS[key]["label"] for key in SCENARIOS],
        )

        selected_scenario = next(
            key for key, value in SCENARIOS.items()
            if value["label"] == scenario_label
        )

        customer_message = st.text_area(
            "Customer message",
            value=SCENARIOS[selected_scenario]["message"],
            height=82,
        )

        if st.button("Run Workflow", type="primary", use_container_width=True):
            with st.spinner("Running LangGraph orchestration..."):
                result = workflow_service.run(
                    customer_message=customer_message,
                    scenario=selected_scenario,
                )

            st.session_state["workflow_result"] = result


def render_summary_item(label: str, value: str, class_name: str = "") -> None:
    st.markdown(
        f"""
        <div class="summary-item">
            <div class="summary-label">{label}</div>
            <div class="summary-value {class_name}">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_badges(result: dict | None) -> None:
    badges = [
        ("Intent Mode", mode_label(result.get("intent_mode")) if result else "Not run yet"),
        ("Response Mode", mode_label(result.get("response_mode")) if result else "Not run yet"),
        ("Decision Engine", "Rules + Signals"),
        ("Human Review", review_status(result)),
    ]
    badges_html = "\n".join(
        (
            '<div class="status-badge">'
            f'<span class="status-label">{label}</span>'
            f'<span class="status-value">{value}</span>'
            "</div>"
        )
        for label, value in badges
    )
    st.markdown(f'<div class="status-badge-grid">{badges_html}</div>', unsafe_allow_html=True)


def render_decision_explanation(result: dict) -> None:
    items_html = "\n".join(
        f"<li>{item}</li>"
        for item in decision_explanation_items(result)
    )
    st.markdown(
        (
            '<div class="reason-box">'
            "<strong>Why</strong>"
            f"<ul>{items_html}</ul>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def render_review_ticket_link(result: dict) -> None:
    ticket = result.get("review_ticket")
    if not ticket:
        return

    st.markdown(
        (
            '<div class="review-ticket-link">'
            f'<span>{ticket["ticket_id"]} -> View ticket</span>'
            f'<small>{ticket["assigned_queue"]} · {format_value(ticket["status"])}</small>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def render_agent_timeline(result: dict) -> None:
    timeline_html = "\n".join(
        (
            '<div class="timeline-item">'
            f'<div class="timeline-step">{step}</div>'
            f'<div class="timeline-detail">{detail}</div>'
            "</div>"
        )
        for step, detail in build_timeline(result)
    )
    st.markdown(f'<div class="timeline">{timeline_html}</div>', unsafe_allow_html=True)


def render_agent_output(result: dict | None) -> None:
    with st.container(border=True):
        st.markdown('<div class="section-title">Agent Decision + Human Response</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-caption">The first screen shows the operational decision and the answer a support agent can send.</div>',
            unsafe_allow_html=True,
        )

        route = "Intent -> Data -> Risk -> Decision -> Response"
        if result and result.get("requires_human_review"):
            route = "Intent -> Data -> Risk -> Decision -> Human Review -> Response"

        st.markdown(
            (
                '<div class="orchestration-strip">'
                '<div class="orchestration-chip"><strong>Orchestration</strong>: LangGraph</div>'
                f'<div class="orchestration-chip"><strong>Route</strong>: {route}</div>'
                "</div>"
            ),
            unsafe_allow_html=True,
        )

        intent = result.get("intent") if result else None
        risk = result.get("risk_level") if result else None
        decision = result.get("decision") if result else None
        human_review = result.get("requires_human_review") if result else None

        summary_items = [
            ("Intent", format_value(intent), ""),
            ("Risk", format_value(risk), risk_class(risk)),
            ("Decision", format_value(decision), ""),
            ("Human Review", format_value(human_review), ""),
        ]
        summary_html = "\n".join(
            (
                '<div class="summary-item">'
                f'<div class="summary-label">{label}</div>'
                f'<div class="summary-value {class_name}">{value}</div>'
                "</div>"
            )
            for label, value, class_name in summary_items
        )
        st.markdown(f'<div class="summary-grid">{summary_html}</div>', unsafe_allow_html=True)

        if result:
            render_decision_explanation(result)

            st.markdown(
                (
                    '<div class="response-label">Customer-facing response</div>'
                    f'<div class="response-card">{result["response"]}</div>'
                ),
                unsafe_allow_html=True,
            )
            render_review_ticket_link(result)
            render_agent_timeline(result)
        else:
            st.markdown(
                (
                    '<div class="empty-response">'
                    "Run the workflow to generate intent, risk, decision, human review status, and a grounded response."
                    "</div>"
                ),
                unsafe_allow_html=True,
            )


def render_guardrails_panel() -> None:
    guardrails = [
        ("LLM boundary", "LLM interprets and drafts, but does not make business decisions."),
        ("Grounding", "Customer responses use workflow state and backend evidence only."),
        ("Human review", "High-risk financial inconsistencies route to review before resolution."),
        ("Fallback", "Intent and response agents have deterministic fallbacks when the LLM is unavailable."),
    ]
    items_html = "\n".join(
        (
            '<div class="guardrail-item">'
            f"<strong>{title}:</strong> {body}"
            "</div>"
        )
        for title, body in guardrails
    )

    st.markdown('<div class="section-title">Policy Guardrails</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="guardrail-list">{items_html}</div>', unsafe_allow_html=True)


def render_backend_data(result: dict) -> None:
    st.markdown(
        '<div class="section-title">Evidence</div>',
        unsafe_allow_html=True,
    )

    st.caption("Backend facts and risk signals used by the decision engine.")

    required_apis = result.get("required_apis") or []
    if required_apis:
        st.markdown(f"**APIs called:** `{format_list(required_apis)}`")

    risk_signals = result.get("risk_signals") or []
    if risk_signals:
        st.markdown(f"**Risk signals:** `{format_list(risk_signals)}`")

    review_ticket = result.get("review_ticket")
    if review_ticket:
        st.markdown("**Human review ticket**")
        st.json(review_ticket)

    st.markdown("**Backend data**")
    st.json(result.get("backend_data"))


def render_observability(result: dict) -> None:
    st.markdown(
        '<div class="section-title">Observability</div>',
        unsafe_allow_html=True,
    )

    st.markdown("**Trace ID**")
    st.code(result.get("trace_id"))

    st.markdown(
        (
            f"**Intent mode:** `{format_mode(result.get('intent_mode'))}`  "
            f"**Response mode:** `{format_mode(result.get('response_mode'))}`  "
            f"**Fallback used:** `{result.get('fallback_used')}`"
        )
    )

    if result.get("human_review_reason"):
        st.warning(result.get("human_review_reason"))

    if result.get("errors"):
        st.error("Fallback was triggered")
        for error in result.get("errors", []):
            st.markdown(f"- {sanitize_ui_message(error)}")

    st.markdown("**Readable Step Latency**")
    st.caption("Latency values are rounded for readability.")

    for step_name, duration in step_durations(result).items():
        st.markdown(f"- `{step_name}`: `{format_duration(duration)}`")


def render_raw_audit_log(result: dict) -> None:
    st.markdown("**Readable audit timeline**")

    for event in sanitized_audit_log(result):
        label = event["step"].replace("_", " ").title()
        duration = event.get("duration_ms")
        status = event.get("status", "completed")
        message = sanitize_ui_message(event.get("message", ""))
        summary_parts = [f"**{label}**", f"`{status}`"]

        if duration is not None:
            summary_parts.append(f"`{format_duration(duration)}`")

        st.markdown(" · ".join(summary_parts))
        if message:
            st.caption(message)

    st.markdown("**Sanitized audit payload**")
    st.json(sanitized_audit_log(result))


def render_workflow_result(result: dict) -> None:
    st.markdown('<div class="detail-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">System Details</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">Open only the detail layer you need for debugging, audit, or demo walkthrough.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("Evidence", expanded=False):
        render_backend_data(result)

    with st.expander("Observability", expanded=False):
        render_observability(result)

    with st.expander("Guardrails", expanded=False):
        render_guardrails_panel()

    with st.expander("Raw Audit Log", expanded=False):
        render_raw_audit_log(result)

    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    render_app_header()
    render_workflow_bar()

    left_col, right_col = st.columns([0.9, 1.35], gap="large")

    with left_col:
        render_case_intake()

    with right_col:
        render_agent_output(st.session_state.get("workflow_result"))

    if "workflow_result" in st.session_state:
        render_workflow_result(st.session_state["workflow_result"])


if __name__ == "__main__":
    main()
