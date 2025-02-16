class KrossAPIError(Exception):
    """Base exception for KrossAPI errors"""
    pass

class LoginError(KrossAPIError):
    """Raised when login fails"""
    pass

class ConfigurationError(KrossAPIError):
    """Raised when configuration is invalid"""
    pass