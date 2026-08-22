"""FastAPI application entrypoint."""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.api.error_handlers import (
    api_exception_handler,
    application_exception_handler,
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from src.api.exceptions import APIException
from src.api.routes import (
    router,
)
from src.core.exceptions import ApplicationException


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="LLM Data Intelligence System API",
        version="1.29.0",
        description=("Public API contract for the LLM Data Intelligence System."),
    )

    application.add_exception_handler(
        APIException,
        api_exception_handler,
    )

    application.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )

    application.add_exception_handler(
        StarletteHTTPException,
        http_exception_handler,
    )

    application.add_exception_handler(
        ApplicationException,
        application_exception_handler,
    )

    application.add_exception_handler(
        Exception,
        generic_exception_handler,
    )

    application.include_router(
        router,
    )

    return application


app = create_app()
