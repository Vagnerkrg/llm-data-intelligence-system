"""
FastAPI exception handlers.

Converts application exceptions
into standardized HTTP responses.
"""


from fastapi import Request

from fastapi.responses import JSONResponse


from src.core.exceptions import (
    ApplicationException
)


from src.api.exceptions import (
    APIException
)



async def application_exception_handler(
    request: Request,
    exc: ApplicationException
):

    return JSONResponse(

        status_code=500,

        content={

            "error":
                "application_error",

            "message":
                exc.message,

            "component":
                exc.component

        }

    )



async def api_exception_handler(
    request: Request,
    exc: APIException
):

    return JSONResponse(

        status_code=exc.status_code,

        content={

            "error":
                exc.error_code,

            "message":
                exc.message

        }

    )



async def generic_exception_handler(
    request: Request,
    exc: Exception
):

    return JSONResponse(

        status_code=500,

        content={

            "error":
                "internal_error",

            "message":
                "Unable to process request"

        }

    )