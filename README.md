# KrossBooking API Client

Unofficial [KrossBooking](https://www.krossbooking.com/) API in Python. Requests are based on the official web interface (V2), data is extracted via static web scraping enabling easy programmatic access to it.

---

## Example Usage

```python
from krossApy import KrossAPI, Fields

with KrossAPI("hotel_id") as api:

    api.login("username", "password")

    data = api.get_reservations(
        fields = [
            Fields.CODE,
            Fields.ARRIVAL,
            Fields.DEPARTURE,
            Fields.GUEST_PORTAL_LINK,
        ],
    )

print(data)

# Output:
# [
#     {
#         'code': '1234/5678',
#         'arrival': '01/01/2025',
#         'departure': '02/01/2025',
#         'guest_portal_link': 'https://guestportallink,
#     },
#     ...
# ]
```
## Installation
currently not published on PyPi, but soon you can install it via pip:

```bash
pip install krossApy
```