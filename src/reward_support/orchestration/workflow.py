from src.reward_support.orchestration.state import (
    WorkflowState,
    add_audit_event,
    safe_step,
)

from src.reward_support.agents.intent_agent import intent_agent
from src.reward_support.agents.data_agent import data_agent
from src.reward_support.agents.risk_agent import risk_agent
from src.reward_support.agents.decision_agent import decision_agent
from src.reward_support.agents.response_agent import response_agent


def should_stop_workflow(state: WorkflowState) -> bool:
    return len(state.get("errors", [])) > 0


def run_workflow(state: WorkflowState) -> WorkflowState:
    add_audit_event(state, "workflow", "Starting workflow")

    state = safe_step(state, "intent_agent", intent_agent)
    if should_stop_workflow(state):
        return response_agent(state)

    state = safe_step(state, "data_agent", data_agent)
    if should_stop_workflow(state):
        return response_agent(state)

    state = safe_step(state, "risk_agent", risk_agent)
    if should_stop_workflow(state):
        return response_agent(state)

    state = safe_step(state, "decision_agent", decision_agent)
    if should_stop_workflow(state):
        return response_agent(state)

    state = safe_step(state, "response_agent", response_agent)

    add_audit_event(state, "workflow", "Workflow completed")

    return state