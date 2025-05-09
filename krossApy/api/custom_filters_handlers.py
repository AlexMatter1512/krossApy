from ..data import Field, Reservations, Errors, Fields
from ..data.Filters import get_operator_string
import logging

logger = logging.getLogger(__name__)

BASE_FILTER = "zt4_cond[{}]={}&{}={}"

def build_filter(field: Field, condition: str, value: str) -> str:
    """
    Build a filter string for the API request
    
    Args:
        field (str): The field to filter on
        condition (str): The comparison operator
        value (str): The value to compare against
        
    Returns:
        str: The filter string
    """
    try:
        actual_field = field.FILTER
    except IndexError:
        raise Errors.UnsupportedFilterField(field)
    
    operator = get_operator_string(condition)
    # actual value handling
    if field in CUSTOM_VALUE_HANDLERS:
        handler = CUSTOM_VALUE_HANDLERS[field]
        value = handler(value)
    else:
        value = value

    return BASE_FILTER.format(actual_field, operator, actual_field, value)

def status_value_handler(value: str) -> str:
    status_map = {
        "Attesa di conferma": "WAIT",
        "Attesa pagamento": "PAY",
        "Cancellata": "CANC",
        "Check in effettuato": "IN",
        "Check out effettuato": "OUT",
        "Confermata": "CONF",
        "No show": "NOSHOW",
    }

    if value not in status_map:
        raise ValueError(f"Invalid status value: {value}")
    filterValue = status_map[value] + ":|:" + value
    return filterValue

CUSTOM_VALUE_HANDLERS = {
    Fields.STATUS: status_value_handler,
}
