from ..data import Fields, Reservations, Field
import datetime
import typing
import logging

logger = logging.getLogger(__name__)

FIELD_TYPES = {
    Fields.ARRIVAL: datetime.date,
    Fields.DEPARTURE: datetime.date,
    Fields.NIGHTS: int,
    Fields.N_ROOMS: int,
    Fields.ROOMS: typing.List[str],
    Fields.N_BEDS: int,
    Fields.TOTAL_CHARGE: float,
    Fields.LONG_STAY: bool,
    Fields.DATE_RESERVATION: datetime.date,
    Fields.LAST_UPDATE: datetime.date,
    Fields.DATE_EXPIRATION: datetime.date,
    Fields.DATE_CANCELATION: datetime.date,
    Fields.TOTAL_CHARGE_NO_TAX: float,
    Fields.TOTAL_CHARGE_TAX: float,
    Fields.TOTAL_CHARGE_BED: float,
    Fields.TOTAL_CHARGE_SERV: float,
    Fields.TOTAL_CHARGE_CLEANING: float,
    Fields.COMMISSION_AMOUNT: float,
    Fields.COMMISSION_AMOUNT_CHANNEL: float,
    Fields.TOTAL_CHARGE_SERV_NO_VAT: float,
    Fields.TOTAL_CHARGE_CLEANING_NO_VAT: float,
    Fields.TOTAL_CHARGE_NO_VAT: float,
    Fields.TOTAL_CHARGE_BED_NO_VAT: float,
    Fields.CITY_TAX_TO_PAY: float,
    Fields.TOTAL_BED_TO_PAY: float,
    Fields.TOTAL_CHARGE_BED_CLEANING: float,
    Fields.TOTAL_CHARGE_EXTRA: float,
    Fields.TOTAL_PAID: float,
    Fields.AMOUNT_TO_PAY: float,
    Fields.ADVANCE_PAYMENT: float,
    Fields.IMPORTO_FATTURATO: float,
    Fields.IMPORTO_DA_FATTURARE: float,
    Fields.DATA_SCADENZA_VERIFICA_CC: datetime.date,
    Fields.DATA_SCADENZA_ATTESA_CC: datetime.date,
    Fields.TOTAL_DEPOSIT: float,
    Fields.TOTAL_PAID_WITH_DEPOSIT: float,
    Fields.EXPECTED_PAYOUT: float,
    Fields.TO_PAY_GUEST: float,
    Fields.TO_PAY_OTA: float,

    #Custom
    Fields.TELEPHONE: "telephone",
    Fields.EMAIL: "email",
}

def retype_fields(reservations: Reservations) -> Reservations:
    """Retype fields in reservations"""
    for reservation in reservations.data:
        for field, field_type in FIELD_TYPES.items():
            if (field_key := field.RESPONSE) in reservation.data:
                handler = CUSTOM_TYPES_HANDLERS.get(field_type)
                if handler:
                    reservation[field_key] = handler(reservation[field_key])
    return reservations


def handle_telephone(value: str, min_length: int = 7, max_length: int = 15) -> str:
    """Sanitize and normalize telephone numbers, ensuring length constraints."""

    # Keep only digits and '+' (only at the start)
    value = "".join(c for c in value if c.isdigit() or c == "+")

    # Ensure '+' is only at the beginning
    if "+" in value and not value.startswith("+"):
        value = value.replace("+", "")  # Remove misplaced '+'

    # Length check
    if not (min_length <= len(value) <= max_length):
        return ""  # Invalid length → return empty string

    return value


def handle_date(value: str) -> datetime.date:
    """Handle date fields with multiple formats."""
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
        try:
            return datetime.datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    logger.warning(f"Failed to parse date: {value}")
    return value


def handle_float(value: str) -> float:
    """Convert value to float."""
    try:
        return float(value)
    except (ValueError, TypeError):
        logger.warning(f"Failed to convert to float: {value}")
        return value


def handle_int(value: str) -> int:
    """Convert value to int."""
    try:
        return int(value)
    except (ValueError, TypeError):
        logger.warning(f"Failed to convert to int: {value}")
        return value


def handle_bool(value: str) -> bool:
    """Convert 'true'/'false' strings to boolean."""
    return value.lower() in ("true", "1", "yes")


def handle_list_str(value: str) -> typing.List[str]:
    """Convert a comma-separated string into a list of strings."""
    ret = value.split(",")
    return [x.strip() for x in ret]


CUSTOM_TYPES_HANDLERS = {
    datetime.date: handle_date,
    float: handle_float,
    int: handle_int,
    bool: handle_bool,
    typing.List[str]: handle_list_str,
    "telephone": handle_telephone,
}
