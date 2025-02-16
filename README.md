# KrossBooking API Client

Unofficial [KrossBooking](https://www.krossbooking.com/) API in Python. Requests are based on the official web interface (V2), data is extracted via static web scraping enabling easy programmatic access to it.

---

## Example Usage

```python
from krossApy import KrossAPI, Fields, build_filters, Reservations
from datetime import datetime

with KrossAPI("hotel_id") as api:

    api.login("username", "password")

    today = datetime.now().strftime("%d/%m/%Y")
    filters = build_filters(field=Fields.ARRIVAL, condition=">=", value=today)

    reservations: Reservations = api.get_reservations(
        fields = [
            Fields.CODE,
            Fields.CHANNEL,
            Fields.ARRIVAL,
            Fields.DEPARTURE,
            Fields.GUEST_PORTAL_LINK,
            Fields.EMAIL,
            Fields.TELEPHONE,
        ],
        filters = filters,
    )

print(reservations)
```
### Output
```json
[
    {
        "code": "1234/5678",
        "channel": "Booking.com",
        "arrival": "01/01/2025",
        "departure": "02/01/2025",
        "guest_portal_link": "https://guestportallink",
        "email": "jhon@doe.com",
        "telephone": "1234567890"
    },
    ...
]
```
## Installation
currently not published on PyPi, but soon you can install it via pip:

```bash
pip install krossApy
```