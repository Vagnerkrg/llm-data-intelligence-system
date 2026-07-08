"""
FastAPI exception handlers.

Converts application exceptions
into standardized API responses.
"""


from fastapi import Request

from fastapi.responses import JSONResponse

from src.api.exceptions import APIException



async def api_exception_handler(
    request: Request,
    exc: APIException
):

    return JSONResponse(

        status_code=exc.status_code,

        content={

            "error": exc.error_code,

            "message": exc.message

        }

    )



async def generic_exception_handler(
    request: Request,
    exc: Exception
):

    return JSONResponse(

        status_code=500,

        content={

            "error": "internal_error",

            "message":
                "Unable to process request"

        }

    )