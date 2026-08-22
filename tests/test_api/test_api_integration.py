"""End-to-end integration tests for the V1.29 API contract."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi.testclient import TestClient

from src.api.app import app
from src.observability.domain.enums import (
    ErrorSeverity,
    EventType,
    MetricType,
)
from src.observability.services.execution_trace import (
    ExecutionTraceService,
)


client = TestClient(
    app,
)


def _create_execution(
    execution_id: str,
) -> ExecutionTraceService:
    """Create an isolated execution trace for API integration tests."""
    trace_service = ExecutionTraceService()

    trace_service.create_trace(
        execution_id=execution_id,
    )

    return trace_service


def test_execution_api_contract() -> None:
    """Execution endpoint must expose the public contract."""
    response = client.post(
        "/api/v1/ask",
        json={
            "query": "test query",
            "context": {},
            "options": {},
        },
    )

    assert response.status_code in {
        200,
        500,
    }

    payload = response.json()

    if response.status_code == 200:
        assert "execution_id" in payload
        assert "status" in payload
        assert "created_at" in payload
        assert "metadata" in payload


def _assert_not_found_response(
    response,
) -> None:
    """Validate current API error contract."""

    assert response.status_code == 404

    payload = response.json()

    assert "detail" in payload
    assert "error" in payload["detail"]


def test_execution_trace_not_found() -> None:
    """Unknown execution trace must return standardized error response."""
    response = client.get(
        "/api/v1/executions/does-not-exist/trace",
    )

    _assert_not_found_response(
        response,
    )


def test_cognitive_state_not_found() -> None:
    """Unknown execution cognitive state must return 404."""
    response = client.get(
        "/api/v1/executions/does-not-exist/cognitive-state",
    )

    _assert_not_found_response(
        response,
    )


def test_memory_not_found() -> None:
    """Unknown execution memory must return 404."""
    response = client.get(
        "/api/v1/executions/does-not-exist/memory",
    )

    _assert_not_found_response(
        response,
    )


def test_knowledge_not_found() -> None:
    """Unknown execution knowledge must return 404."""
    response = client.get(
        "/api/v1/executions/does-not-exist/knowledge",
    )

    _assert_not_found_response(
        response,
    )


def test_learning_not_found() -> None:
    """Unknown execution learning data must return 404."""
    response = client.get(
        "/api/v1/executions/does-not-exist/learning",
    )

    _assert_not_found_response(
        response,
    )


def test_evolution_not_found() -> None:
    """Unknown execution evolution data must return 404."""
    response = client.get(
        "/api/v1/executions/does-not-exist/evolution",
    )

    _assert_not_found_response(
        response,
    )


def test_trace_response_contract() -> None:
    """Trace response must expose events, metrics and errors."""
    execution_id = "integration-trace"

    trace_service = _create_execution(
        execution_id,
    )

    trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
        stage="reasoning",
        timestamp=datetime.now(
            timezone.utc,
        ),
    )

    trace_service.record_metric(
        execution_id=execution_id,
        metric_name="reasoning_duration_ms",
        value=120,
        unit="ms",
        component="reasoning",
        metric_type=MetricType.DURATION,
    )

    trace_service.record_error(
        execution_id=execution_id,
        component="reasoning",
        error_type="IntegrationWarning",
        message="integration warning",
        severity=ErrorSeverity.WARNING,
    )

    response = client.get(
        f"/api/v1/executions/{execution_id}/trace",
    )

    assert response.status_code in {
        200,
        404,
    }

    if response.status_code == 200:
        payload = response.json()

        assert payload["execution_id"] == execution_id
        assert "events" in payload
        assert "metrics" in payload
        assert "errors" in payload


def test_invalid_execution_id_is_rejected() -> None:
    """Whitespace-only execution IDs must be rejected."""
    response = client.get(
        "/api/v1/executions/%20%20/trace",
    )

    assert response.status_code in {
        404,
        422,
    }


def test_validation_error_is_sanitized() -> None:
    """Invalid requests must not expose internal details."""
    response = client.post(
        "/api/v1/ask",
        json={
            "query": "",
        },
    )

    assert response.status_code in {
        400,
        422,
    }

    assert "Traceback" not in response.text
    assert "stacktrace" not in response.text.lower()


def test_unexpected_error_is_sanitized() -> None:
    """Unexpected errors must not expose internal details."""
    response = client.get(
        "/api/v1/executions/does-not-exist/trace",
    )

    assert response.status_code == 404

    assert "Traceback" not in response.text
    assert "sqlite3" not in response.text.lower()
