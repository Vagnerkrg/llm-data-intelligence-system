"""Public API exception hierarchy."""

from __future__ import annotations

from typing import Any


class APIException(Exception):
    """Base exception for standardized API errors."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        category: str = "internal",
        severity: str = "error",
        execution_id: str | None = None,
        correlation_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.category = category
        self.severity = severity
        self.execution_id = execution_id
        self.correlation_id = correlation_id
        self.details = details or {}

        super().__init__(message)


class ValidationAPIException(APIException):
    """Invalid request or semantic validation failure."""

    def __init__(
        self,
        message: str = "Invalid request.",
        *,
        status_code: int = 400,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=status_code,
            error_code="VALIDATION_ERROR",
            category="validation",
            details=details,
        )


class NotFoundAPIException(APIException):
    """Requested resource does not exist."""

    def __init__(
        self,
        message: str = "Resource not found.",
        *,
        execution_id: str | None = None,
        correlation_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=404,
            error_code="RESOURCE_NOT_FOUND",
            category="not_found",
            execution_id=execution_id,
            correlation_id=correlation_id,
            details=details,
        )


class ConflictAPIException(APIException):
    """Resource state conflicts with the requested operation."""

    def __init__(
        self,
        message: str = "Resource conflict.",
        *,
        execution_id: str | None = None,
        correlation_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=409,
            error_code="RESOURCE_CONFLICT",
            category="conflict",
            execution_id=execution_id,
            correlation_id=correlation_id,
            details=details,
        )


class ExecutionAPIException(APIException):
    """Execution-level failure."""

    def __init__(
        self,
        message: str = "Execution failed.",
        *,
        status_code: int = 500,
        execution_id: str | None = None,
        correlation_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=status_code,
            error_code="EXECUTION_FAILED",
            category="execution",
            execution_id=execution_id,
            correlation_id=correlation_id,
            details=details,
        )


class CognitiveAPIException(APIException):
    """Cognitive subsystem failure."""

    def __init__(
        self,
        message: str = "Cognitive operation failed.",
        *,
        status_code: int = 500,
        execution_id: str | None = None,
        correlation_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=status_code,
            error_code="COGNITIVE_ERROR",
            category="cognitive",
            execution_id=execution_id,
            correlation_id=correlation_id,
            details=details,
        )


class InfrastructureAPIException(APIException):
    """Infrastructure or persistence failure."""

    def __init__(
        self,
        message: str = "Service temporarily unavailable.",
        *,
        status_code: int = 503,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=status_code,
            error_code="INFRASTRUCTURE_ERROR",
            category="infrastructure",
            details=details,
        )


class TimeoutAPIException(APIException):
    """Operation exceeded its allowed execution time."""

    def __init__(
        self,
        message: str = "Operation timed out.",
        *,
        execution_id: str | None = None,
        correlation_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=504,
            error_code="TIMEOUT",
            category="timeout",
            execution_id=execution_id,
            correlation_id=correlation_id,
            details=details,
        )


class UpstreamAPIException(APIException):
    """Upstream dependency failure."""

    def __init__(
        self,
        message: str = "Upstream service unavailable.",
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=502,
            error_code="UPSTREAM_ERROR",
            category="infrastructure",
            details=details,
        )


class InternalAPIException(APIException):
    """Unexpected internal API failure."""

    def __init__(
        self,
        message: str = "Internal server error.",
    ) -> None:
        super().__init__(
            message,
            status_code=500,
            error_code="INTERNAL_ERROR",
            category="internal",
        )


# Backward compatibility with existing imports.
BadRequestException = ValidationAPIException
NotFoundException = NotFoundAPIException
InternalServerException = InternalAPIException
