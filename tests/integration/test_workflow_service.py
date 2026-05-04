import os
import tempfile
import unittest

from src.reward_support.application.workflow_service import RewardSupportWorkflowService


class WorkflowServiceIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        os.environ["OPENAI_API_KEY"] = ""
        os.environ["SUPPORT_TICKET_PATH"] = os.path.join(self.temp_dir.name, "tickets.json")
        self.service = RewardSupportWorkflowService()

    def tearDown(self):
        os.environ.pop("SUPPORT_TICKET_PATH", None)
        self.temp_dir.cleanup()

    def test_high_risk_routes_through_human_review(self):
        result = self.service.run(
            "My balance was deducted but my flight voucher was not created.",
            scenario="high_risk",
        )

        self.assertEqual(result["intent"], "reward_issue")
        self.assertEqual(result["risk_level"], "high")
        self.assertEqual(result["decision"], "escalate_to_human")
        self.assertTrue(result["requires_human_review"])
        self.assertEqual(result["review_ticket"]["status"], "pending_review")
        self.assertIn("human_review_agent", [event["step"] for event in result["audit_log"]])

    def test_medium_risk_skips_human_review_node(self):
        result = self.service.run(
            "I can still see the flight voucher campaign, but I can’t redeem it.",
            scenario="medium_risk",
        )

        self.assertEqual(result["intent"], "campaign_issue")
        self.assertEqual(result["risk_level"], "medium")
        self.assertEqual(result["decision"], "flag_for_review")
        self.assertFalse(result["requires_human_review"])
        self.assertIsNone(result["review_ticket"])
        self.assertNotIn("human_review_agent", [event["step"] for event in result["audit_log"]])

    def test_api_timeout_fails_safe_to_human_review(self):
        result = self.service.run(
            "My voucher is missing after redemption.",
            scenario="api_timeout",
        )

        self.assertEqual(result["risk_level"], "high")
        self.assertEqual(result["decision"], "escalate_to_human")
        self.assertTrue(result["requires_human_review"])
        self.assertTrue(result["errors"])

    def test_pii_is_redacted_before_llm_state(self):
        result = self.service.run(
            "My voucher is missing. Email me at user@example.com or 415-555-1212.",
            scenario="low_risk",
        )

        self.assertIn("[REDACTED_EMAIL]", result["redacted_customer_message"])
        self.assertIn("[REDACTED_PHONE]", result["redacted_customer_message"])


if __name__ == "__main__":
    unittest.main()
