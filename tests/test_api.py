from datetime import date, datetime
from unittest import TestCase
from unittest.mock import Mock, patch

from krossApy import ConfigurationError, KrossAPI, LoginError


class KrossAPITestCase(TestCase):
    def setUp(self) -> None:
        self.api = KrossAPI("hotel-id")

    def _mock_response(self, payload, status_code=200):
        response = Mock()
        response.ok = status_code < 400
        response.status_code = status_code
        response.json.return_value = payload
        return response

    @patch("krossApy.api.api.requests.Session.post")
    def test_login_stores_auth_token(self, mock_post):
        mock_post.return_value = self._mock_response({"auth_token": "secret-token"})

        payload = self.api.login("user", "password", deviceName="MacBook Pro")

        self.assertEqual(payload["auth_token"], "secret-token")
        self.assertEqual(self.api.token, "secret-token")
        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["hotel_id"], "hotel-id")
        self.assertEqual(kwargs["json"]["deviceName"], "MacBook Pro")

    @patch("krossApy.api.api.requests.Session.post")
    def test_login_requires_auth_token_in_response(self, mock_post):
        mock_post.return_value = self._mock_response({"devices": []})

        with self.assertRaises(LoginError):
            self.api.login("user", "password")

    @patch("krossApy.api.api.requests.Session.post")
    def test_authenticated_request_adds_bearer_token(self, mock_post):
        self.api.set_token("bearer-token")
        mock_post.return_value = self._mock_response({"data": {"ok": True}})

        payload = self.api.get_properties()

        self.assertEqual(payload, {"ok": True})
        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer bearer-token")

    @patch("krossApy.api.api.requests.Session.post")
    def test_save_reservation_normalizes_dates(self, mock_post):
        mock_post.return_value = self._mock_response({"data": {"saved": True}})

        self.api.save_reservation(
            {
                "id_reservation": 10,
                "arrival": date(2026, 4, 30),
                "departure": datetime(2026, 5, 1, 11, 0, 0),
            }
        )

        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["arrival"], "2026-04-30")
        self.assertEqual(kwargs["json"]["departure"], "2026-05-01")

    def test_invalid_dashboard_bucket_type_is_rejected(self):
        with self.assertRaises(ConfigurationError):
            self.api.get_dashboard_bucket("invalid", id_property=1, value_date="2026-04-30")