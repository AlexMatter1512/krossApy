from ..data import Fields, _Field_Idx, Reservations, CustomFields
import logging

logger = logging.getLogger(__name__)

def check_in_info_handler(reservations: Reservations) -> Reservations:
    """Handler for the check in info field."""
    logger.debug("Handling check-in info field")
    for reservation in reservations.data:
        if Fields.GUEST_PORTAL_LINK.value[_Field_Idx.RESPONSE] in reservation.keys():
            reservation[Fields.CHECK_IN_INFO.value[_Field_Idx.RESPONSE]] = reservation[
                Fields.GUEST_PORTAL_LINK.value[_Field_Idx.RESPONSE]
            ].replace("my-reservation", "check-in-instructions")
    return reservations

# Map custom fields to their handlers
CUSTOM_FIELDS_HANDLERS = {
    CustomFields.CHECK_IN_INFO.value: check_in_info_handler
}