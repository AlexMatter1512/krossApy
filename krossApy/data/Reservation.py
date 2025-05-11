from . import Field
import logging
import json

log = logging.getLogger(__name__)

class Reservation:
    def __init__(self, data: dict):
        self.data = data

    def __getitem__(self, key):
        response_key = self._process_field_key(key)
        if response_key is False:
            raise KeyError(f"Key {key} not found in reservation data. Available keys: {list(self.data.keys())}")
        return self.data[response_key]

    def __setitem__(self, key, value):
        response_key = self._process_field_key(key) or key.RESPONSE
        self.data[response_key] = value

    def _process_field_key(self, key):
        """
        Process a key that might be a Field object.
        Returns the matching response key if a Field object, or the original key otherwise.
        Raises KeyError if it's a Field but no matching key is found.
        """
        if not isinstance(key, Field):
            return key  # Return the original key for fallback handling
            
        log.debug(f"Processing reservation with field: {key}")
        for response_key in key.RESPONSES:
            if response_key in self.data:
                return response_key
                
        # If we get here, it was a Field but no matching keys were found
        return False

    def to_dict(self):
        """Convert reservation to a dictionary."""
        return self.data
    
    def __str__(self):
        """String representation of the reservation."""
        return json.dumps(self.to_dict())
    
    def to_json(self):
        """Convert reservation to JSON string."""
        return json.dumps(self.to_dict())
