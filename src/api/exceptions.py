"""
API exception hierarchy.

Defines HTTP layer exceptions
used by FastAPI handlers.
"""


class APIException(Exception):
    """
    Base exception for API errors.
    """


    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "api_error"
    ):

        self.message = message

        self.status_code = status_code

        self.error_code = error_code

        super().__init__(
            self.message
        )



class BadRequestException(APIException):
    """
    Raised when the client sends
    an invalid request.
    """


    def __init__(
        self,
        message: str = "Invalid request."
    ):

        super().__init__(

            message=message,

            status_code=400,

            error_code="bad_request"

        )



class NotFoundException(APIException):
    """
    Raised when a requested resource
    does not exist.
    """


    def __init__(
        self,
        message: str = "Resource not found."
    ):

        super().__init__(

            message=message,

            status_code=404,

            error_code="not_found"

        )



class InternalServerException(APIException):
    """
    Raised for unexpected API failures.
    """


    def __init__(
        self,
        message: str = "Internal server error."
    ):

        super().__init__(

            message=message,

            status_code=500,

            error_code="internal_error"

        )