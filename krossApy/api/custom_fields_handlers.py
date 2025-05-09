from ..data import Fields, Reservations, CustomFields
import logging

logger = logging.getLogger(__name__)

def check_in_info_handler(reservations: Reservations) -> Reservations:
    """Handler for the check in info field."""
    logger.debug("Handling check-in info field")
    for reservation in reservations.data:
        if Fields.GUEST_PORTAL_LINK.RESPONSE in reservation.keys():
            reservation[Fields.CHECK_IN_INFO.RESPONSE] = reservation[
                Fields.GUEST_PORTAL_LINK.RESPONSE
            ].replace("my-reservation", "check-in-instructions")
    return reservations

# Map custom fields to their handlers
CUSTOM_FIELDS_HANDLERS = {
    CustomFields.CHECK_IN_INFO.value: check_in_info_handler
}
