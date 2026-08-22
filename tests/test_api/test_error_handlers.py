"""Tests for centralized API error handling."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.error_handlers import (
    generic_exception_handler,
)


def test_generic_exception_handler() -> None:
    """Unexpected exceptions must return the public safe error contract."""
    app = FastAPI()

    app.add_exception_handler(
        Exception,
        generic_exception_handler,
    )

    @app.get("/test-error")
    def test_error() -> None:
        raise Exception(
            "Unexpected internal detail.",
        )

    client = TestClient(
        app,
        raise_server_exceptions=False,
    )

    response = client.get(
        "/test-error",
    )

    assert response.status_code == 500

    assert response.json() == {
        "error": {
            "code": "INTERNAL_ERROR",
            "category": "internal",
            "message": "Unable to process request.",
            "severity": "error",
            "execution_id": None,
            "correlation_id": None,
            "details": {},
        }
    }


def test_generic_exception_does_not_expose_internal_message() -> None:
    """Internal exception details must never reach the client."""
    app = FastAPI()

    app.add_exception_handler(
        Exception,
        generic_exception_handler,
    )

    @app.get("/test-error")
    def test_error() -> None:
        raise Exception(
            "SECRET DATABASE PASSWORD",
        )

    client = TestClient(
        app,
        raise_server_exceptions=False,
    )

    response = client.get(
        "/test-error",
    )

    assert response.status_code == 500

    payload = response.json()

    assert payload["error"]["message"] == "Unable to process request."

    assert "SECRET DATABASE PASSWORD" not in response.text


def test_generic_exception_contains_standard_error_category() -> None:
    """Unexpected errors must expose a stable category."""
    app = FastAPI()

    app.add_exception_handler(
        Exception,
        generic_exception_handler,
    )

    @app.get("/test-error")
    def test_error() -> None:
        raise RuntimeError(
            "internal failure",
        )

    client = TestClient(
        app,
        raise_server_exceptions=False,
    )

    response = client.get(
        "/test-error",
    )

    payload = response.json()

    assert payload["error"]["code"] == "INTERNAL_ERROR"

    assert payload["error"]["category"] == "internal"

    assert payload["error"]["severity"] == "error"


def test_generic_exception_contains_empty_diagnostic_context() -> None:
    """Unexpected errors must not invent execution context."""
    app = FastAPI()

    app.add_exception_handler(
        Exception,
        generic_exception_handler,
    )

    @app.get("/test-error")
    def test_error() -> None:
        raise RuntimeError(
            "internal failure",
        )

    client = TestClient(
        app,
        raise_server_exceptions=False,
    )

    response = client.get(
        "/test-error",
    )

    payload = response.json()

    assert payload["error"]["execution_id"] is None

    assert payload["error"]["correlation_id"] is None

    assert payload["error"]["details"] == {}
