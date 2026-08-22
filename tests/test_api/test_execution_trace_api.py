"""Tests for the Execution Trace API."""

from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.dependencies import (
    get_execution_trace_service,
)
from src.api.routes import (
    router,
)
from src.api.schemas import (
    ExecutionStatus,
    ExecutionTraceResponse,
)
from src.application.execution_trace_service import (
    ExecutionTraceApplicationService,
)
from src.observability.domain.enums import (
    ErrorSeverity,
    EventType,
    MetricType,
)
from src.observability.services.execution_trace import (
    ExecutionTraceService,
)


class FakeRuntime:
    """Fake runtime exposing a controllable observability service."""

    def __init__(self) -> None:
        self.observability = type(
            "Observability",
            (),
            {
                "trace_service": ExecutionTraceService(),
            },
        )()

        self.observability.trace = self.observability.trace_service.get_trace

    def create_execution(
        self,
        execution_id: str,
    ) -> None:
        self.observability.trace_service.create_trace(
            execution_id=execution_id,
        )


def build_client(
    service: ExecutionTraceApplicationService,
) -> TestClient:
    """Build an isolated API client."""
    app = FastAPI()

    app.include_router(
        router,
    )

    app.dependency_overrides[get_execution_trace_service] = lambda: service

    return TestClient(
        app,
    )


def test_trace_response_schema_is_public_contract() -> None:
    """Trace response must validate without domain entities."""
    response = ExecutionTraceResponse(
        execution_id="exec-001",
        status=ExecutionStatus.COMPLETED,
        started_at=datetime.now(
            timezone.utc,
        ),
        events=[],
        metrics=[],
        errors=[],
    )

    assert response.execution_id == "exec-001"

    assert response.status == ExecutionStatus.COMPLETED


def test_get_execution_returns_public_status() -> None:
    """GET execution endpoint must return public execution information."""
    runtime = FakeRuntime()

    runtime.create_execution(
        "exec-get",
    )

    service = ExecutionTraceApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    response = client.get(
        "/api/v1/executions/exec-get",
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["execution_id"] == "exec-get"

    assert payload["status"] == "pending"


def test_get_execution_trace_returns_events_metrics_and_errors() -> None:
    """Trace endpoint must map all observability record families."""
    runtime = FakeRuntime()

    execution_id = "exec-trace"

    runtime.create_execution(
        execution_id,
    )

    service = runtime.observability.trace_service

    service.record_event(
        execution_id=execution_id,
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
        timestamp=datetime(
            2026,
            1,
            1,
            0,
            0,
            3,
            tzinfo=timezone.utc,
        ),
    )

    service.record_metric(
        execution_id=execution_id,
        metric_name="reasoning_duration_ms",
        value=120,
        unit="ms",
        component="reasoning",
        metric_type=MetricType.DURATION,
    )

    service.record_error(
        execution_id=execution_id,
        component="reasoning",
        error_type="TestError",
        message="test error",
        severity=ErrorSeverity.WARNING,
    )

    application = ExecutionTraceApplicationService(
        runtime=runtime,
    )

    client = build_client(
        application,
    )

    response = client.get(
        f"/api/v1/executions/{execution_id}/trace",
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["execution_id"] == execution_id

    assert len(payload["events"]) == 1

    assert len(payload["metrics"]) == 1

    assert len(payload["errors"]) == 1

    assert payload["events"][0]["event_type"] == "reasoning.completed"

    assert payload["metrics"][0]["metric_name"] == "reasoning_duration_ms"

    assert payload["errors"][0]["error_type"] == "TestError"


def test_trace_events_are_sorted_chronologically() -> None:
    """Trace events must be returned in chronological order."""
    runtime = FakeRuntime()

    execution_id = "exec-order"

    runtime.create_execution(
        execution_id,
    )

    service = runtime.observability.trace_service

    base = datetime(
        2026,
        1,
        1,
        tzinfo=timezone.utc,
    )

    service.record_event(
        execution_id=execution_id,
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
        timestamp=base.replace(
            second=3,
        ),
    )

    service.record_event(
        execution_id=execution_id,
        event_type=EventType.REASONING_STARTED,
        component="reasoning",
        timestamp=base.replace(
            second=1,
        ),
    )

    application = ExecutionTraceApplicationService(
        runtime=runtime,
    )

    client = build_client(
        application,
    )

    response = client.get(
        f"/api/v1/executions/{execution_id}/trace",
    )

    timestamps = [item["timestamp"] for item in response.json()["events"]]

    assert timestamps == sorted(
        timestamps,
    )


def test_missing_execution_returns_404() -> None:
    """Unknown execution IDs must produce HTTP 404."""
    runtime = FakeRuntime()

    service = ExecutionTraceApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    response = client.get(
        "/api/v1/executions/does-not-exist",
    )

    assert response.status_code == 404

    assert response.json()["detail"]["error"] == "EXECUTION_NOT_FOUND"


def test_missing_trace_returns_404() -> None:
    """Unknown trace IDs must produce HTTP 404."""
    runtime = FakeRuntime()

    service = ExecutionTraceApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    response = client.get(
        "/api/v1/executions/does-not-exist/trace",
    )

    assert response.status_code == 404

    assert response.json()["detail"]["error"] == "TRACE_NOT_FOUND"


def test_execution_id_is_validated() -> None:
    """Whitespace-only execution IDs must be rejected."""
    runtime = FakeRuntime()

    service = ExecutionTraceApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    response = client.get(
        "/api/v1/executions/%20%20",
    )

    assert response.status_code == 422


def test_trace_does_not_expose_domain_object_directly() -> None:
    """API must return JSON schema data rather than domain objects."""
    runtime = FakeRuntime()

    execution_id = "exec-contract"

    runtime.create_execution(
        execution_id,
    )

    application = ExecutionTraceApplicationService(
        runtime=runtime,
    )

    client = build_client(
        application,
    )

    response = client.get(
        f"/api/v1/executions/{execution_id}/trace",
    )

    payload = response.json()

    assert isinstance(
        payload,
        dict,
    )

    assert "execution_id" in payload

    assert "events" in payload

    assert "metrics" in payload

    assert "errors" in payload
