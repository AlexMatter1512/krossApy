# krossApy

Unofficial Python client for the reverse-engineered Kross Booking mobile API.

The package now targets the documented `/v5` JSON backend used by the official app instead of the older website scraping flow. Requests are sent as authenticated JSON `POST` calls to `https://apiapp.krossbooking.com/v5`.

## Installation

```bash
pip install krossApy
```

## Quick Start

```python
from krossApy import KrossAPI

with KrossAPI("hotel-id") as api:
    auth = api.login(
        "username",
        "password",
        device_id="device-uuid",
        deviceName="MacBook Pro",
        deviceSystem="macOS",
        deviceSystemVersion="15.0",
        token="push-token",
    )

    properties = api.get_properties()
    id_property = properties["properties"][0]["id_property"]

    totals = api.get_dashboard_totals(id_property=id_property, value_date="2026-04-30")
    reservation = api.get_reservation(id_reservation=3496)

print(auth["auth_token"])
print(totals)
print(reservation)
```

## Available Methods

The client exposes the main endpoints identified in the reverse-engineered documentation:

- `login(...)`
- `get_properties()`
- `get_dashboard_totals(...)`
- `get_dashboard_bucket(...)`
- `search_reservations(...)`
- `get_reservation(...)`
- `save_reservation(...)`
- `cancel_reservation(...)`
- `get_reservation_params(...)`
- `get_room_for_reservation_params(...)`
- `save_room_for_reservation(...)`
- `get_guests(...)`
- `check_in(...)`
- `check_out(...)`
- `undo_check_in(...)`
- `save_guest_data(...)`
- `get_contracts_for_reservation(...)`
- `sign_contract(...)`
- `preview_contract(...)`
- `get_checklists_for_reservation(...)`
- `get_checklist(...)`
- `save_answers(...)`
- `save_custom_fields(...)`
- `get_charges_payments_docs(...)`
- `save_charge(...)`
- `save_payment(...)`
- `delete_charge(...)`
- `delete_payment(...)`
- `invalid_cc(...)`
- `save_document(...)`
- `get_planner(...)`
- `request(path, body)` for raw access to additional endpoints

## Notes

- Authentication uses `POST /auth/get-token` and stores the returned bearer token automatically.
- Read endpoints that require a language parameter default to `en`, configurable through `KrossConfig`.
- Date fields accepted by helper methods can be `str`, `datetime.date`, or `datetime.datetime`; they are normalized to `YYYY-MM-DD`.
- Search and mutation payloads are intentionally passed through with minimal reshaping because the app mostly sends server-shaped DTOs.

## Source Documentation

The endpoint mapping used for this refactor is captured in [KROSS_RESERVATION_API.md](KROSS_RESERVATION_API.md).