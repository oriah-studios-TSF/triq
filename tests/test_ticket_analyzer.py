import unittest

from app.services.ticket_analyzer import analyze_ticket


class TestTicketAnalyzer(unittest.TestCase):

    def test_network_ticket(self):
        analysis = analyze_ticket(
            "I cannot connect to the office Wi-Fi."
        )

        self.assertEqual(analysis["category"], "Network Connectivity")

    def test_account_access_ticket(self):
        analysis = analyze_ticket(
            "I cannot log in because I forgot my password."
        )

        self.assertEqual(analysis["category"], "Account Access")

    def test_hardware_ticket(self):
        analysis = analyze_ticket(
            "My laptop keyboard is not working."
        )

        self.assertEqual(analysis["category"], "Hardware Issue")

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

    def test_security_breach_has_high_priority(self):
        analysis = analyze_ticket(
            "There has been a security breach in the company system."
        )
    
        self.assertEqual(analysis["priority"], "High")

    def test_unknown_issue_uses_general_support(self):
        analysis = analyze_ticket(
            "The business application is behaving strangely."
        )
    
        self.assertEqual(
            analysis["category"],
            "General IT support"
        )

    def test_system_outage_has_high_priority(self):
        analysis = analyze_ticket(
            "The company system is down and nobody can work."
        )
    
        self.assertEqual(analysis["priority"], "High")

    def test_network_takes_priority_over_hardware(self):
        analysis = analyze_ticket(
            "My laptop cannot connect to Wi-Fi."
        )
    
        self.assertEqual(analysis["category"], "Network Connectivity")

    def test_network_detection_ignores_capitalization(self):
        analysis = analyze_ticket(
            "I CANNOT CONNECT TO THE OFFICE WI-FI."
        )
    
        self.assertEqual(analysis["category"], "Network Connectivity")

    def test_logging_in_issue_is_account_access(self):
        analysis = analyze_ticket(
            "I am having trouble logging in to my account."
        )
    
        self.assertEqual(
            analysis["category"],
            "Account Access"
        )


if __name__ == "__main__":
    unittest.main()
