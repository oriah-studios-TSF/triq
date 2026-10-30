import unittest

from app.services.ai_ticket_analyzer import validate_ai_analysis


class TestValidateAIAnalysis(unittest.TestCase):

    def setUp(self):
        self.valid_analysis = {
            "category": "Network Connectivity",
            "priority": "Medium",
            "summary": "An employee cannot connect to office Wi-Fi.",
            "troubleshooting_steps": [
                "Check the device's Wi-Fi settings.",
                "Verify the correct network is selected."
            ],
            "explanation": "Other employees can connect, suggesting a device-specific issue."
        }

    def test_accepts_valid_analysis(self):
        result = validate_ai_analysis(self.valid_analysis)

        self.assertEqual(result, self.valid_analysis)

    def test_rejects_non_dictionary_response(self):
        with self.assertRaises(ValueError):
            validate_ai_analysis("not a dictionary")

    def test_rejects_missing_field(self):
        analysis = self.valid_analysis.copy()
        del analysis["category"]

        with self.assertRaises(ValueError):
            validate_ai_analysis(analysis)

    def test_rejects_invalid_priority(self):
        analysis = self.valid_analysis.copy()
        analysis["priority"] = "Critical"

        with self.assertRaises(ValueError):
            validate_ai_analysis(analysis)

    def test_rejects_non_list_troubleshooting_steps(self):
        analysis = self.valid_analysis.copy()
        analysis["troubleshooting_steps"] = "Restart the device"

        with self.assertRaises(ValueError):
            validate_ai_analysis(analysis)

    def test_rejects_empty_troubleshooting_step(self):
        analysis = self.valid_analysis.copy()
        analysis["troubleshooting_steps"] = [""]

        with self.assertRaises(ValueError):
            validate_ai_analysis(analysis)


if __name__ == "__main__":
    unittest.main()
