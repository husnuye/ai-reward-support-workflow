from langgraph.graph import StateGraph, END

from src.reward_support.orchestration.state import WorkflowState, safe_step
from src.reward_support.agents.intent_agent import intent_agent
from src.reward_support.agents.data_agent import data_agent
from src.reward_support.agents.risk_agent import risk_agent
from src.reward_support.agents.decision_agent import decision_agent
from src.reward_support.agents.human_review_agent import human_review_agent
from src.reward_support.agents.response_agent import response_agent


def safe_node(step_name: str, func):
    def wrapped(state: WorkflowState) -> WorkflowState:
        return safe_step(state, step_name, func)

    return wrapped


def route_after_decision(state: WorkflowState) -> str:
    if state.get("errors"):
        return "human_review_agent" if state.get("requires_human_review") else "response_agent"

    if state.get("requires_human_review"):
        return "human_review_agent"

    return "response_agent"


def route_or_continue(next_node: str):
    def route(state: WorkflowState) -> str:
        if state.get("errors"):
            return "human_review_agent" if state.get("requires_human_review") else "response_agent"

        return next_node

    return route


def build_langgraph_workflow():
    graph = StateGraph(WorkflowState)

    graph.add_node("intent_agent", safe_node("intent_agent", intent_agent))
    graph.add_node("data_agent", safe_node("data_agent", data_agent))
    graph.add_node("risk_agent", safe_node("risk_agent", risk_agent))
    graph.add_node("decision_agent", safe_node("decision_agent", decision_agent))
    graph.add_node("human_review_agent", safe_node("human_review_agent", human_review_agent))
    graph.add_node("response_agent", safe_node("response_agent", response_agent))

    graph.set_entry_point("intent_agent")

    graph.add_conditional_edges(
        "intent_agent",
        route_or_continue("data_agent"),
        {
            "data_agent": "data_agent",
            "human_review_agent": "human_review_agent",
            "response_agent": "response_agent",
        },
    )
    graph.add_conditional_edges(
        "data_agent",
        route_or_continue("risk_agent"),
        {
            "risk_agent": "risk_agent",
            "human_review_agent": "human_review_agent",
            "response_agent": "response_agent",
        },
    )
    graph.add_conditional_edges(
        "risk_agent",
        route_or_continue("decision_agent"),
        {
            "decision_agent": "decision_agent",
            "human_review_agent": "human_review_agent",
            "response_agent": "response_agent",
        },
    )
    graph.add_conditional_edges(
        "decision_agent",
        route_after_decision,
        {
            "human_review_agent": "human_review_agent",
            "response_agent": "response_agent",
        },
    )
    graph.add_edge("human_review_agent", "response_agent")
    graph.add_edge("response_agent", END)

    return graph.compile()


def run_langgraph_workflow(state: WorkflowState) -> WorkflowState:
    app = build_langgraph_workflow()
    return app.invoke(state)
