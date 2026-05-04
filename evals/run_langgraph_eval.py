import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from src.reward_support.orchestration.state import create_initial_state
from src.reward_support.orchestration.langgraph_workflow import run_langgraph_workflow


def load_dataset():
    with open("evals/eval_dataset.json") as f:
        return json.load(f)


def run_eval():
    dataset = load_dataset()

    for case in dataset:
        state = create_initial_state("test", case["message"])
        state["scenario"] = case.get("scenario")
        state = run_langgraph_workflow(state)

        print("\n--- CASE ---")
        print("Message:", case["message"])
        print("Scenario:", case.get("scenario"))
        print("Intent:", state.get("intent"))
        print("Risk:", state.get("risk_level"))
        print("Decision:", state.get("decision"))


if __name__ == "__main__":
    run_eval()
