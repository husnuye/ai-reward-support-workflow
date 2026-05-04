import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import time

from src.reward_support.orchestration.state import create_initial_state
from src.reward_support.orchestration.workflow import run_workflow


def load_dataset():
    with open("evals/eval_dataset.json") as f:
        return json.load(f)


def run_eval():
    dataset = load_dataset()

    correct_intent = 0
    correct_risk = 0
    correct_decision = 0

    total = len(dataset)
    start = time.time()

    for case in dataset:
        state = create_initial_state("test", case["message"])
        state["scenario"] = case.get("scenario")
        state = run_workflow(state)

        print("\n--- CASE ---")
        print("Trace ID:", state.get("trace_id"))
        print("Message:", case["message"])
        print("Scenario:", case.get("scenario"))

        print(f"Intent   → Expected: {case['expected_intent']} | Actual: {state['intent']}")
        print(f"Risk     → Expected: {case['expected_risk']} | Actual: {state['risk_level']}")
        print(f"Decision → Expected: {case['expected_decision']} | Actual: {state['decision']}")

        print("\nAudit Log:")
        for event in state["audit_log"]:
            print(event)

        if state["intent"] == case["expected_intent"]:
            correct_intent += 1

        if state["risk_level"] == case["expected_risk"]:
            correct_risk += 1

        if state["decision"] == case["expected_decision"]:
            correct_decision += 1

    end = time.time()

    print("\n======================")
    print("=== EVAL RESULTS ===")
    print("======================")
    print(f"Intent Accuracy: {correct_intent / total:.2f}")
    print(f"Risk Accuracy: {correct_risk / total:.2f}")
    print(f"Decision Accuracy: {correct_decision / total:.2f}")
    print(f"Avg Latency: {(end - start) / total:.4f} sec")

    print("\nSummary:")
    print(f"- Total cases: {total}")
    print(f"- Correct intent: {correct_intent}")
    print(f"- Correct risk: {correct_risk}")
    print(f"- Correct decision: {correct_decision}")


if __name__ == "__main__":
    run_eval()
