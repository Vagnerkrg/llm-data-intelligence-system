"""Tests for the Cognitive State API."""

from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.dependencies import (
    get_cognitive_state_service,
)
from src.api.routes import router
from src.application.cognitive_state_service import (
    CognitiveStateApplicationService,
)
from src.observability.domain.enums import EventType
from src.observability.services.execution_trace import (
    ExecutionTraceService,
)


class FakeRuntime:
    """Fake runtime with isolated observability."""

    def __init__(self) -> None:
        self.observability = type(
            "Observability",
            (),
            {
                "trace_service": ExecutionTraceService(),
            },
        )()

        self.observability.trace = self.observability.trace_service.get_trace


def build_client(
    service: CognitiveStateApplicationService,
) -> TestClient:
    """Build isolated API client."""
    app = FastAPI()
    app.include_router(router)

    app.dependency_overrides[get_cognitive_state_service] = lambda: service

    return TestClient(app)


def test_cognitive_state_endpoint_returns_all_stages() -> None:
    """Cognitive response must expose every public stage."""
    runtime = FakeRuntime()

    execution_id = "exec-cognitive"

    runtime.observability.trace_service.create_trace(
        execution_id=execution_id,
    )

    runtime.observability.trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.REASONING_STARTED,
        component="reasoning",
        stage="reasoning",
    )

    runtime.observability.trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
        stage="reasoning",
        timestamp=datetime.now(timezone.utc),
    )

    service = CognitiveStateApplicationService(
        runtime=runtime,
    )

    client = build_client(service)

    response = client.get(
        f"/api/v1/executions/{execution_id}/cognitive-state",
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["execution_id"] == execution_id

    assert payload["reasoning"]["status"] == "completed"

    for stage in (
        "planning",
        "execution",
        "memory",
        "knowledge",
        "evaluation",
        "learning",
        "evolution",
        "adaptation",
    ):
        assert stage in payload


def test_cognitive_state_supports_partial_execution() -> None:
    """Unobserved stages must remain explicitly incomplete."""
    runtime = FakeRuntime()

    execution_id = "exec-partial"

    runtime.observability.trace_service.create_trace(
        execution_id=execution_id,
    )

    runtime.observability.trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.REASONING_STARTED,
        component="reasoning",
        stage="reasoning",
    )

    service = CognitiveStateApplicationService(
        runtime=runtime,
    )

    client = build_client(service)

    response = client.get(
        f"/api/v1/executions/{execution_id}/cognitive-state",
    )

    payload = response.json()

    assert response.status_code == 200

    assert payload["reasoning"]["status"] == "running"

    assert payload["planning"]["status"] == "not_started"


def test_cognitive_state_maps_evaluation_score() -> None:
    """Evaluation score must be preserved in the public result."""
    runtime = FakeRuntime()

    execution_id = "exec-evaluation"

    runtime.observability.trace_service.create_trace(
        execution_id=execution_id,
    )

    runtime.observability.trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.COGNITIVE_EVALUATION_COMPLETED,
        component="evaluation",
        stage="evaluation",
        metadata={
            "score": 0.93,
        },
    )

    service = CognitiveStateApplicationService(
        runtime=runtime,
    )

    client = build_client(service)

    response = client.get(
        f"/api/v1/executions/{execution_id}/cognitive-state",
    )

    payload = response.json()

    assert payload["evaluation"]["status"] == "completed"

    assert payload["evaluation"]["result"]["score"] == 0.93


def test_cognitive_state_unknown_execution_returns_404() -> None:
    """Unknown execution must return HTTP 404."""
    runtime = FakeRuntime()

    service = CognitiveStateApplicationService(
        runtime=runtime,
    )

    client = build_client(service)

    response = client.get(
        "/api/v1/executions/does-not-exist/cognitive-state",
    )

    assert response.status_code == 404
