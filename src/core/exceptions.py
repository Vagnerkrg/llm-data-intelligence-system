"""
Core application exceptions.

Contains domain-level exceptions
used internally by the system.
"""



class IntelligenceSystemError(Exception):
    """
    Base exception for application errors.
    """



class ConfigurationError(
    IntelligenceSystemError
):
    """
    Raised when application configuration
    is invalid or incomplete.
    """



class DataProcessingError(
    IntelligenceSystemError
):
    """
    Raised when data processing fails.
    """