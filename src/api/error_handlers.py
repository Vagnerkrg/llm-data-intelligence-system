"""Centralized FastAPI error handling."""

from __future__ import annotations

from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.api.exceptions import APIException
from src.api.schemas import APIErrorDetail, APIErrorResponse
from src.core.exceptions import ApplicationException


_SENSITIVE_KEYS = {
    "password",
    "token",
    "access_token",
    "api_key",
    "secret",
    "authorization",
    "database_url",
    "connection_string",
    "stacktrace",
    "traceback",
}


def _sanitize(
    value: Any,
) -> Any:
    """Recursively remove sensitive diagnostic data."""
    if isinstance(
        value,
        dict,
    ):
        return {
            str(key): _sanitize(item)
            for key, item in value.items()
            if str(key).lower() not in _SENSITIVE_KEYS
        }

    if isinstance(
        value,
        list,
    ):
        return [_sanitize(item) for item in value]

    if isinstance(
        value,
        tuple,
    ):
        return [_sanitize(item) for item in value]

    return value


def _response(
    *,
    status_code: int,
    code: str,
    category: str,
    message: str,
    severity: str = "error",
    execution_id: str | None = None,
    correlation_id: str | None = None,
    details: dict[str, Any] | None = None,
) -> JSONResponse:
    """Build the canonical public error response."""
    payload = APIErrorResponse(
        error=APIErrorDetail(
            code=code,
            category=category,
            message=message,
            severity=severity,
            execution_id=execution_id,
            correlation_id=correlation_id,
            details=_sanitize(
                details or {},
            ),
        )
    )

    return JSONResponse(
        status_code=status_code,
        content=payload.model_dump(
            mode="json",
        ),
    )


async def api_exception_handler(
    request: Request,
    exc: APIException,
) -> JSONResponse:
    """Handle known public API exceptions."""
    return _response(
        status_code=exc.status_code,
        code=exc.error_code,
        category=exc.category,
        message=exc.message,
        severity=exc.severity,
        execution_id=exc.execution_id,
        correlation_id=exc.correlation_id,
        details=exc.details,
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Handle FastAPI request validation errors."""
    details = []

    for error in exc.errors():
        details.append(
            {
                "location": error.get(
                    "loc",
                    [],
                ),
                "type": error.get(
                    "type",
                ),
                "message": error.get(
                    "msg",
                ),
            }
        )

    return _response(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        code="VALIDATION_ERROR",
        category="validation",
        message="Request validation failed.",
        details={
            "errors": details,
        },
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    """Normalize FastAPI/Starlette HTTP exceptions."""
    code_by_status = {
        400: "BAD_REQUEST",
        401: "AUTHENTICATION_REQUIRED",
        403: "FORBIDDEN",
        404: "RESOURCE_NOT_FOUND",
        409: "RESOURCE_CONFLICT",
        422: "VALIDATION_ERROR",
        500: "INTERNAL_ERROR",
        502: "UPSTREAM_ERROR",
        503: "SERVICE_UNAVAILABLE",
        504: "TIMEOUT",
    }

    category_by_status = {
        400: "validation",
        401: "authentication",
        403: "authorization",
        404: "not_found",
        409: "conflict",
        422: "validation",
        500: "internal",
        502: "infrastructure",
        503: "infrastructure",
        504: "timeout",
    }

    public_message = (
        str(exc.detail)
        if isinstance(
            exc.detail,
            str,
        )
        else "Request could not be processed."
    )

    return _response(
        status_code=exc.status_code,
        code=code_by_status.get(
            exc.status_code,
            "API_ERROR",
        ),
        category=category_by_status.get(
            exc.status_code,
            "internal",
        ),
        message=public_message,
    )


async def application_exception_handler(
    request: Request,
    exc: ApplicationException,
) -> JSONResponse:
    """Convert application errors into safe public responses."""
    return _response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        code="APPLICATION_ERROR",
        category="internal",
        message="Application operation failed.",
        details={
            "component": exc.component,
        }
        if exc.component
        else {},
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Protect the API from unexpected internal exceptions."""
    return _response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        code="INTERNAL_ERROR",
        category="internal",
        message="Unable to process request.",
    )
