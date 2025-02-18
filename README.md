# KrossBooking API Client

Unofficial [KrossBooking](https://www.krossbooking.com/) API in Python. Requests are based on the official web interface (V2), data is extracted via static web scraping enabling easy programmatic access to it.

## Usage Examples
### Basic Setup
Note: This example is provided for demonstration purposes only. It retrieves every reservation without applying any filters, which may result in long fetch times. It is recommended to use appropriate filtering parameters to limit the dataset. See [Filtering Reservations](#filtering-reservations).

<details>
<summary>toggle example</summary>

```python
from krossApy import KrossAPI

with KrossAPI("hotel_id") as api:
    api.login("username", "password")
    reservations = api.get_reservations()

print(reservations)
```
### Output
Note: Default fields are used when none are specified. See [Filtering Reservations Fields](#filtering-reservations-fields).
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
    
</details>

---
### Filtering Reservations
<details>
    <summary>toggle example</summary>

```python
from krossApy import KrossAPI, Fields, build_filter, Reservations
from datetime import datetime

with KrossAPI("hotel_id") as api:

    api.login("username", "password")

    today = datetime.now().strftime("%d/%m/%Y")
    filter = build_filter(field=Fields.ARRIVAL, condition=">=", value=today)
    filters = [filter]

    reservations: Reservations = api.get_reservations(filters = filters)

print(reservations)
```
    
</details>

--- 
### Filtering Reservations Fields
<details>
    <summary>toggle example</summary>

```python
from krossApy import KrossAPI, Fields, build_filter, Reservations

with KrossAPI("hotel_id") as api:
    api.login("username", "password")

    reservations: Reservations = api.get_reservations(
        fields = [
            Fields.CODE,
            Fields.TELEPHONE,
        ]
    )

print(reservations)
```
### Output
```json
[
    {
        "code": "1234/5678",
        "telephone": "1234567890"
    },
    ...
]
```
    
</details>

---
## Installation

```bash
pip install krossApy
```