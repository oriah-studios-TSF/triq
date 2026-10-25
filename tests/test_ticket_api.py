
import unittest

from app import create_app


class TestTicketAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_valid_ticket_returns_analysis(self):
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
        self.assertEqual(data["analysis"]["category"], "Network Connectivity")

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
