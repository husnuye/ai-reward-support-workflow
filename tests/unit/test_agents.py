import os
import tempfile
import unittest

from src.reward_support.agents.human_review_agent import human_review_agent
from src.reward_support.agents.intent_agent import fallback_detect_intent, normalize_confidence, parse_intent_json
from src.reward_support.agents.risk_agent import evaluate_risk
from src.reward_support.agents.decision_agent import decision_agent
from src.reward_support.orchestration.state import create_initial_state
from src.reward_support.services.pii_redaction import redact_pii


class IntentAgentTests(unittest.TestCase):
    def test_fallback_detects_reward_issue(self):
        intent, confidence = fallback_detect_intent("My balance was deducted but no voucher was created")

        self.assertEqual(intent, "reward_issue")
        self.assertGreaterEqual(confidence, 0.8)

    def test_parse_intent_json_extracts_wrapped_json(self):
        data = parse_intent_json('Sure: {"intent": "campaign_issue", "confidence": 0.8}')

        self.assertEqual(data["intent"], "campaign_issue")
        self.assertEqual(data["confidence"], 0.8)

    def test_normalize_confidence_clamps_values(self):
        self.assertEqual(normalize_confidence(2), 1.0)
        self.assertEqual(normalize_confidence(-1), 0.0)


class RiskAgentTests(unittest.TestCase):
    def test_high_risk_for_deducted_balance_and_missing_voucher(self):
        risk, reason, signals = evaluate_risk(
            "reward_issue",
            {
                "balance": {"balance_deducted": True, "transaction_status": "completed"},
                "voucher": {"voucher_found": False},
            },
        )

        self.assertEqual(risk, "high")
        self.assertIn("Balance was deducted", reason)
        self.assertEqual(signals, ["balance_deducted", "voucher_missing"])

    def test_backend_unavailable_is_high_risk(self):
        risk, reason, signals = evaluate_risk(
            "reward_issue",
            {
                "balance": {"transaction_status": "unavailable"},
                "voucher": {"voucher_found": None},
            },
        )

        self.assertEqual(risk, "high")
        self.assertIn("backend_data_unavailable", signals)


class DecisionAgentTests(unittest.TestCase):
    def test_high_risk_escalates_to_human(self):
        state = create_initial_state("C001", "test")
        state["intent"] = "reward_issue"
        state["risk_level"] = "high"
        state["backend_data"] = {
            "balance": {"balance_deducted": True},
            "voucher": {"voucher_found": False},
        }

        result = decision_agent(state)

        self.assertEqual(result["decision"], "escalate_to_human")
        self.assertIn("voucher was not generated", result["decision_reason"])


class HumanReviewAgentTests(unittest.TestCase):
    def test_human_review_agent_persists_ticket_to_configured_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            ticket_path = os.path.join(temp_dir, "tickets.json")
            os.environ["SUPPORT_TICKET_PATH"] = ticket_path
            state = create_initial_state("C001", "test")
            state["trace_id"] = "12345678-test"
            state["risk_level"] = "high"
            state["human_review_reason"] = "Manual verification required."

            result = human_review_agent(state)

            self.assertEqual(result["review_ticket"]["ticket_id"], "REV-12345678")
            self.assertEqual(result["review_ticket"]["status"], "pending_review")
            self.assertTrue(os.path.exists(ticket_path))

            os.environ.pop("SUPPORT_TICKET_PATH", None)


class PiiRedactionTests(unittest.TestCase):
    def test_redacts_email_phone_and_card(self):
        text = "Email me at user@example.com or 415-555-1212. Card 4111 1111 1111 1111."

        redacted = redact_pii(text)

        self.assertIn("[REDACTED_EMAIL]", redacted)
        self.assertIn("[REDACTED_PHONE]", redacted)
        self.assertIn("[REDACTED_CARD]", redacted)


if __name__ == "__main__":
    unittest.main()
