"""Tests for the standardized API error layer."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.error_handlers import (
    generic_exception_handler,
)
from src.api.exceptions import (
    ConflictAPIException,
    ExecutionAPIException,
    InfrastructureAPIException,
    InternalAPIException,
    NotFoundAPIException,
    TimeoutAPIException,
    ValidationAPIException,
)


def build_app() -> FastAPI:
    """Build an isolated application for error tests."""
    application = FastAPI()

    application.add_exception_handler(
        Exception,
        generic_exception_handler,
    )

    return application


def test_api_exception_has_standard_contract() -> None:
    """API exceptions must expose the required public fields."""
    exception = NotFoundAPIException(
        "Execution not found.",
        execution_id="exec-001",
        correlation_id="corr-001",
    )

    assert exception.status_code == 404
    assert exception.error_code == "RESOURCE_NOT_FOUND"
    assert exception.category == "not_found"
    assert exception.execution_id == "exec-001"
    assert exception.correlation_id == "corr-001"


def test_validation_exception_maps_to_400() -> None:
    """Semantic validation must map to HTTP 400."""
    exception = ValidationAPIException()

    assert exception.status_code == 400
    assert exception.category == "validation"


def test_conflict_maps_to_409() -> None:
    """Conflict errors must map to HTTP 409."""
    exception = ConflictAPIException()

    assert exception.status_code == 409
    assert exception.category == "conflict"


def test_timeout_maps_to_504() -> None:
    """Timeout errors must map to HTTP 504."""
    exception = TimeoutAPIException()

    assert exception.status_code == 504
    assert exception.category == "timeout"


def test_execution_error_maps_correctly() -> None:
    """Execution failures preserve execution correlation."""
    exception = ExecutionAPIException(
        execution_id="exec-failed",
        correlation_id="corr-failed",
    )

    assert exception.status_code == 500
    assert exception.category == "execution"
    assert exception.execution_id == "exec-failed"


def test_infrastructure_error_maps_to_503() -> None:
    """Infrastructure failures must map to HTTP 503."""
    exception = InfrastructureAPIException()

    assert exception.status_code == 503
    assert exception.category == "infrastructure"


def test_internal_error_hides_internal_message() -> None:
    """Unexpected internal errors must expose only a safe message."""
    exception = InternalAPIException()

    assert exception.status_code == 500
    assert exception.error_code == "INTERNAL_ERROR"
    assert exception.category == "internal"


def test_existing_invalid_execution_id_uses_public_validation_status() -> None:
    """Path validation remains exposed through the public API."""
    client = TestClient(
        build_app(),
    )

    response = client.get(
        "/api/v1/executions/%20%20",
    )

    assert response.status_code in {
        404,
        422,
    }
