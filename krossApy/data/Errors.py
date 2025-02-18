class KrossAPIError(Exception):
    """Base exception for KrossAPI errors"""
    pass

class LoginError(KrossAPIError):
    """Raised when login fails"""
    pass

class ConfigurationError(KrossAPIError):
    """Raised when configuration is invalid"""
    pass

class UnsupportedFilterField(KrossAPIError):
    """Raised when the filter field is not supported"""
    def __init__(self, field_name):
        self.message = f"'{field_name}' is not supported as a filter field yet (you can still filter on the result data)"
        super().__init__(self.message)
    pass