from . import Field
import logging

log = logging.getLogger(__name__)

class Reservation:
    def __init__(self, data: dict):
        self.data = data

    def __getitem__(self, key):
        # If the key is a Field object, try response fallbacks
        if isinstance(key, Field):
            log.debug(f"Accessing reservation with key: {key}")
            for response_key in key.RESPONSES:
                if response_key in self.data:
                    return self.data[response_key]
            return None  # or raise KeyError or custom behavior
        return self.data[key]  # fallback to raw access
