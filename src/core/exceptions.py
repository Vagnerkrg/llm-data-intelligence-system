"""
Application exception hierarchy.

Defines domain-level exceptions
used across the intelligence system.
"""


class ApplicationException(Exception):
    """
    Base exception for application errors.
    """


    def __init__(
        self,
        message: str,
        component: str | None = None
    ):

        self.message = message

        self.component = component

        super().__init__(
            self.message
        )



# Backward compatibility
#
# Keeps compatibility with
# previous modules/tests.
#
ApplicationError = ApplicationException



class ConfigurationError(ApplicationException):
    """
    Raised when application configuration
    is invalid or unavailable.
    """



class DataProcessingError(ApplicationException):
    """
    Raised when data loading or processing
    fails.
    """



class RetrievalError(ApplicationException):
    """
    Raised when retrieval operations fail.
    """



class AnalysisError(ApplicationException):
    """
    Raised when analytical processing fails.
    """



class IntelligenceError(ApplicationException):
    """
    Raised when intelligence orchestration fails.
    """