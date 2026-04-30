from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, Mapping, MutableMapping, Optional, Sequence

import requests

from ..data.Errors import ConfigurationError, KrossAPIError, LoginError


DEFAULT_API_KEY = "apf6phf4eeb70da55fa972e3b7g403d4"
DEFAULT_BASE_URL = "https://apiapp.krossbooking.com/v5"
DEFAULT_TIMEOUT = 30
DEFAULT_LANG = "en"
DEFAULT_APP = "krossapp"
DEFAULT_NOTIFICATION_TYPE = "FCM"
VALID_DASHBOARD_TYPES = {"arrivals", "departures", "stays", "booked"}


def _normalize_date(value: Any) -> str:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        return value
    raise TypeError("Date values must be str, date, or datetime")


@dataclass
class KrossConfig:
    """Configuration for the Kross v5 JSON API client."""

    base_url: str = DEFAULT_BASE_URL
    timeout: int = DEFAULT_TIMEOUT
    lang: str = DEFAULT_LANG
    api_key: str = DEFAULT_API_KEY
    app: str = DEFAULT_APP
    with_priv: bool = True
    session_headers: MutableMapping[str, str] = field(
        default_factory=lambda: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "krossApy/0.2.0",
        }
    )


class KrossAPI:
    """Client for the reverse-engineered Kross mobile API."""

    def __init__(
        self,
        hotel_id: Optional[str] = None,
        token: Optional[str] = None,
        config: Optional[KrossConfig] = None,
    ) -> None:
        self.config = config or KrossConfig()
        self.session = requests.Session()
        self.session.headers.update(dict(self.config.session_headers))
        self.hotel_id = hotel_id
        self.token = token

    def set_hotel(self, hotel_id: str) -> None:
        if not hotel_id or not isinstance(hotel_id, str):
            raise ConfigurationError("Hotel ID must be a non-empty string")
        self.hotel_id = hotel_id

    def set_token(self, token: str) -> None:
        if not token or not isinstance(token, str):
            raise ConfigurationError("Token must be a non-empty string")
        self.token = token

    def clear_token(self) -> None:
        self.token = None

    @property
    def is_authenticated(self) -> bool:
        return bool(self.token)

    def _make_url(self, path: str) -> str:
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self.config.base_url}{path}"

    def _request(
        self,
        path: str,
        body: Optional[Mapping[str, Any]] = None,
        *,
        token: Optional[str] = None,
    ) -> Dict[str, Any]:
        bearer_token = token or self.token
        headers: Dict[str, str] = {}
        if bearer_token:
            headers["Authorization"] = f"Bearer {bearer_token}"

        try:
            response = self.session.post(
                self._make_url(path),
                json=dict(body or {}),
                headers=headers,
                timeout=self.config.timeout,
            )
        except requests.RequestException as exc:
            raise KrossAPIError(f"Request to {path} failed: {exc}") from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise KrossAPIError(
                f"Invalid JSON response from {path}: status={response.status_code}"
            ) from exc

        if not response.ok:
            error_message = payload.get("message") or payload.get("error") or payload
            raise KrossAPIError(
                f"Kross API request failed for {path}: status={response.status_code}, error={error_message}"
            )

        return payload

    def request(
        self,
        path: str,
        body: Optional[Mapping[str, Any]] = None,
        *,
        token: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self._request(path, body, token=token)

    def login(
        self,
        username: str,
        password: Optional[str] = None,
        **extra_fields: Any,
    ) -> Dict[str, Any]:
        hotel_id = extra_fields.pop("hotel_id", self.hotel_id)
        if not hotel_id:
            raise ConfigurationError("Hotel ID must be set before logging in")
        if not username:
            raise ConfigurationError("Username must be a non-empty string")
        if not password and not {"otp", "otp_gen_code", "id_otp"}.intersection(extra_fields):
            raise ConfigurationError("Password is required unless completing an OTP flow")

        body: Dict[str, Any] = {
            "hotel_id": hotel_id,
            "username": username,
            "password": password,
            "api_key": self.config.api_key,
            "with_priv": self.config.with_priv,
            "app": self.config.app,
        }
        body.update({key: value for key, value in extra_fields.items() if value is not None})
        body.setdefault("type", DEFAULT_NOTIFICATION_TYPE)

        payload = self._request("/auth/get-token", body)
        auth_token = payload.get("auth_token")
        if not auth_token:
            raise LoginError("Login did not return auth_token")

        self.hotel_id = hotel_id
        self.token = auth_token
        return payload

    def login_with_token(self, token: str) -> None:
        self.set_token(token)

    def get_properties(self, with_app_flags: bool = True) -> Dict[str, Any]:
        payload = self._request("/properties/get-list", {"with_app_flags": with_app_flags})
        return payload.get("data", {})

    def get_dashboard_totals(self, id_property: int, value_date: Any) -> Dict[str, Any]:
        payload = self._request(
            "/app/dashboard-totals",
            {"id_property": id_property, "date": _normalize_date(value_date)},
        )
        return payload.get("data", {})

    def get_dashboard_bucket(
        self,
        bucket_type: str,
        id_property: int,
        value_date: Any,
        page: int = 0,
    ) -> Dict[str, Any]:
        if bucket_type not in VALID_DASHBOARD_TYPES:
            raise ConfigurationError(
                f"bucket_type must be one of {sorted(VALID_DASHBOARD_TYPES)}"
            )
        body = {
            "type": bucket_type,
            "page": page,
            "id_property": id_property,
            "date": _normalize_date(value_date),
        }
        return self._request(f"/app/dashboard-{bucket_type}?page={page}", body)

    def search_reservations(self, **search_payload: Any) -> Dict[str, Any]:
        return self._request("/app/search-reservation", search_payload)

    def get_reservation(self, id_reservation: int, lang: Optional[str] = None) -> Dict[str, Any]:
        payload = self._request(
            "/app/get-reservation",
            {"id_reservation": id_reservation, "lang": lang or self.config.lang},
        )
        return payload.get("data", {}).get("reservation", {})

    def save_reservation(self, reservation_payload: Mapping[str, Any]) -> Dict[str, Any]:
        body = dict(reservation_payload)
        for key in ("arrival", "departure", "date_expiration"):
            if body.get(key) is not None:
                body[key] = _normalize_date(body[key])
        return self._request("/app/save-reservation", body)

    def cancel_reservation(self, id_reservation: int, id_property: int) -> Dict[str, Any]:
        return self._request(
            "/app/cancel-reservation",
            {"id_reservation": id_reservation, "id_property": id_property},
        )

    def assign_operation(self, operation_payload: Mapping[str, Any]) -> Dict[str, Any]:
        return self._request("/app/assign-operation", dict(operation_payload))

    def get_reservation_params(self, id_reservation: int, lang: Optional[str] = None) -> Dict[str, Any]:
        payload = self._request(
            "/app/get-params-for-reservation",
            {"id_reservation": id_reservation, "lang": lang or self.config.lang},
        )
        return payload.get("data", {})

    def get_room_for_reservation_params(
        self,
        id_property: int,
        arrival: Any,
        departure: Any,
    ) -> Dict[str, Any]:
        payload = self._request(
            "/app/get-room-for-reservation-params",
            {
                "id_property": id_property,
                "arrival": _normalize_date(arrival),
                "departure": _normalize_date(departure),
            },
        )
        return payload.get("data", {})

    def save_room_for_reservation(self, room_payload: Mapping[str, Any]) -> Dict[str, Any]:
        body = dict(room_payload)
        for key in ("arrival_guest", "departure_guest"):
            if body.get(key) is not None:
                body[key] = _normalize_date(body[key])
        return self._request("/app/save-room-for-reservation", body)

    def get_guests(self, id_reservation: int, lang: Optional[str] = None) -> Dict[str, Any]:
        payload = self._request(
            "/app/get-guests",
            {"id_reservation": id_reservation, "lang": lang or self.config.lang},
        )
        return payload.get("data", {})

    def check_in(self, check_in_payload: Mapping[str, Any]) -> Dict[str, Any]:
        return self._request("/app/check-in", dict(check_in_payload))

    def check_out(self, check_out_payload: Mapping[str, Any]) -> Dict[str, Any]:
        return self._request("/app/check-out", dict(check_out_payload))

    def undo_check_in(self, undo_payload: Mapping[str, Any]) -> Dict[str, Any]:
        return self._request("/app/undo-check-in", dict(undo_payload))

    def save_guest_data(self, guest_payload: Mapping[str, Any]) -> Dict[str, Any]:
        return self._request("/app/save-guest-data", dict(guest_payload))

    def get_contracts_for_reservation(
        self,
        id_property: int,
        id_reservation: int,
        lang: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = self._request(
            "/app/get-contracts-for-reservation",
            {
                "id_property": id_property,
                "id_reservation": id_reservation,
                "lang": lang or self.config.lang,
            },
        )
        return payload.get("data", {})

    def sign_contract(self, contract_payload: Mapping[str, Any]) -> Dict[str, Any]:
        return self._request("/app/sign-contract", dict(contract_payload))

    def preview_contract(
        self,
        id_template: int,
        id_room_4_reservation_4_guest: int,
        id_reservation: int,
    ) -> Dict[str, Any]:
        return self._request(
            "/app/preview-contract",
            {
                "id_template": id_template,
                "id_room_4_reservation_4_guest": id_room_4_reservation_4_guest,
                "id_reservation": id_reservation,
            },
        )

    def get_checklists_for_reservation(self, id_reservation: int) -> Sequence[Dict[str, Any]]:
        payload = self._request("/app/get-checklists-for-reservation", {"id_reservation": id_reservation})
        return payload.get("data", [])

    def get_checklist(self, id_checklist: int) -> Dict[str, Any]:
        payload = self._request("/app/get-checklist", {"id_checklist": id_checklist})
        return payload.get("data", {})

    def save_answers(self, answers_payload: Mapping[str, Any]) -> Dict[str, Any]:
        return self._request("/app/save-answers", dict(answers_payload))

    def save_custom_fields(self, custom_fields_payload: Mapping[str, Any]) -> Dict[str, Any]:
        return self._request("/app/save-custom-fields", dict(custom_fields_payload))

    def get_charges_payments_docs(
        self,
        id_property: int,
        id_reservation: int,
        lang: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = self._request(
            "/app/get-charges-payments-docs",
            {
                "id_property": id_property,
                "id_reservation": id_reservation,
                "lang": lang or self.config.lang,
            },
        )
        return payload.get("data", {})

    def save_charge(self, charge_payload: Mapping[str, Any]) -> Dict[str, Any]:
        return self._request("/app/save-charge", dict(charge_payload))

    def save_payment(self, payment_payload: Mapping[str, Any]) -> Dict[str, Any]:
        return self._request("/app/save-payment", dict(payment_payload))

    def delete_charge(self, delete_payload: Mapping[str, Any]) -> Dict[str, Any]:
        return self._request("/app/delete-charge", dict(delete_payload))

    def delete_payment(self, delete_payload: Mapping[str, Any]) -> Dict[str, Any]:
        return self._request("/app/delete-payment", dict(delete_payload))

    def invalid_cc(self, invalid_cc_payload: Mapping[str, Any]) -> Dict[str, Any]:
        return self._request("/reservations/invalid-cc", dict(invalid_cc_payload))

    def save_document(self, document_payload: Mapping[str, Any]) -> Dict[str, Any]:
        return self._request("/documents/save", dict(document_payload))

    def get_planner(self, id_property: int, planner_payload: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        payload = self._request(f"/app/get-planner?id_property={id_property}", planner_payload or {})
        return payload.get("data", {})

    def __enter__(self) -> "KrossAPI":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.session.close()
