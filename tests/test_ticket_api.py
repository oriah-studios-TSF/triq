import unittest
from unittest.mock import patch

from app import create_app
from app.services.ai_ticket_analyzer import AIAnalysisError


class TestTicketAPI(unittest.TestCase):

    def setUp(self):
        """Create a fresh application for each test."""

        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["AI_PROVIDER"] = "ollama"
        self.client = self.app.test_client()

    def get_sample_analysis(self):
        """Return a predictable analysis for API tests."""

        return {
            "category": "Network Connectivity",
            "priority": "Medium",
            "summary": "Unable to connect to office Wi-Fi.",
            "troubleshooting_steps": [
                "Check the device's Wi-Fi settings.",
                "Verify the correct network is selected."
            ],
            "explanation": (
                "The issue may be specific to the employee's device."
            )
        }

    def test_health_endpoint(self):
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    @patch("app.routes.analyze_ticket_with_ai")
    def test_valid_ticket_returns_analysis(self, mock_ai):
        mock_ai.return_value = self.get_sample_analysis()

        response = self.client.post(
            "/api/tickets",
            json={
                "description": "I cannot connect to the office Wi-Fi."
            }
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Ticket analyzed successfully."
        )
        self.assertIn("ticket", data)
        self.assertIn("analysis", data)
        self.assertEqual(data["analysis_source"], "ai")
        self.assertEqual(
            data["analysis"]["category"],
            "Network Connectivity"
        )

        mock_ai.assert_called_once()

    @patch("app.routes.analyze_ticket_with_ai")
    def test_ai_failure_uses_rules_based_analyzer(self, mock_ai):
        mock_ai.side_effect = AIAnalysisError(
            "The AI service could not produce a valid analysis."
        )

        response = self.client.post(
            "/api/tickets",
            json={
                "description": "I cannot connect to the office Wi-Fi."
            }
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertEqual(data["analysis_source"], "rules")
        self.assertEqual(
            data["analysis"]["category"],
            "Network Connectivity"
        )
        self.assertIn("explanation", data["analysis"])
        self.assertIn(
            "troubleshooting_steps",
            data["analysis"]
        )

        mock_ai.assert_called_once()

    def test_mock_provider_uses_rules_based_analyzer(self):
        self.app.config["AI_PROVIDER"] = "mock"

        response = self.client.post(
            "/api/tickets",
            json={
                "description": "My laptop keyboard is not working."
            }
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertEqual(data["analysis_source"], "rules")
        self.assertEqual(
            data["analysis"]["category"],
            "Hardware Issue"
        )
        self.assertIn("explanation", data["analysis"])

    def test_unsupported_provider_returns_error(self):
        self.app.config["AI_PROVIDER"] = "unsupported"

        response = self.client.post(
            "/api/tickets",
            json={
                "description": "My laptop keyboard is not working."
            }
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.get_json()["error"],
            "The configured AI provider is not supported."
        )

    def test_empty_description_is_rejected(self):
        response = self.client.post(
            "/api/tickets",
            json={"description": "   "}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_missing_description_is_rejected(self):
        response = self.client.post(
            "/api/tickets",
            json={}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_description_over_2000_characters_is_rejected(self):
        response = self.client.post(
            "/api/tickets",
            json={"description": "a" * 2001}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_invalid_json_body_is_rejected(self):
        response = self.client.post(
            "/api/tickets",
            data="this is not JSON",
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())


if __name__ == "__main__":
    unittest.main()
