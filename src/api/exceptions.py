"""
API exceptions.

HTTP-related exceptions exposed
through the API layer.
"""



class APIException(Exception):
    """
    Base API exception.
    """


    def __init__(
        self,
        message: str,
        error_code: str = "api_error",
        status_code: int = 400
    ):

        self.message = message

        self.error_code = error_code

        self.status_code = status_code


        super().__init__(
            message
        )



class InvalidRequestException(
    APIException
):
    """
    Raised when user input is invalid.
    """


    def __init__(
        self,
        message: str
    ):

        super().__init__(

            message=message,

            error_code="invalid_request",

            status_code=422

        )