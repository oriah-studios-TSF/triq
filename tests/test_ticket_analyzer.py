import unittest

from app.services.ticket_analyzer import analyze_ticket


class TestTicketAnalyzer(unittest.TestCase):

    def test_network_ticket(self):
        analysis = analyze_ticket(
            "I cannot connect to the office Wi-Fi."
        )

        self.assertEqual(analysis["category"], "Network")

    def test_account_access_ticket(self):
        analysis = analyze_ticket(
            "I cannot log in because I forgot my password."
        )

        self.assertEqual(analysis["category"], "Account Access")

    def test_hardware_ticket(self):
        analysis = analyze_ticket(
            "My laptop keyboard is not working."
        )

        self.assertEqual(analysis["category"], "Hardware")

    def test_urgent_ticket_has_high_priority(self):
        analysis = analyze_ticket(
            "Urgent: the entire office has lost its network connection."
        )

        self.assertEqual(analysis["priority"], "High")

    def test_normal_ticket_has_medium_priority(self):
        analysis = analyze_ticket(
            "I cannot connect to the office Wi-Fi."
        )

        self.assertEqual(analysis["priority"], "Medium")

    def test_analysis_has_required_fields(self):
        analysis = analyze_ticket(
            "I cannot connect to the office Wi-Fi."
        )

        self.assertIn("category", analysis)
        self.assertIn("priority", analysis)
        self.assertIn("summary", analysis)
        self.assertIn("troubleshooting_steps", analysis)

        self.assertIsInstance(
            analysis["troubleshooting_steps"], list
        )


if __name__ == "__main__":
    unittest.main()
