"""Tests for Learning and Evolution API."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.dependencies import (
    get_learning_evolution_service,
)
from src.api.routes import router
from src.application.learning_evolution_service import (
    LearningEvolutionApplicationService,
)
from src.observability.domain.enums import (
    EventType,
)
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
    service: LearningEvolutionApplicationService,
) -> TestClient:
    """Build an isolated API client."""
    app = FastAPI()

    app.include_router(
        router,
    )

    app.dependency_overrides[get_learning_evolution_service] = lambda: service

    return TestClient(
        app,
    )


def test_learning_endpoint_returns_signals_and_outcomes() -> None:
    """Learning data must be mapped to the public contract."""
    runtime = FakeRuntime()

    execution_id = "exec-learning"

    runtime.observability.trace_service.create_trace(
        execution_id=execution_id,
    )

    runtime.observability.trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.LEARNING_SIGNAL_GENERATED,
        component="learning",
        stage="learning",
        metadata={
            "signal_id": "signal-001",
            "signal_type": "improvement",
            "confidence": 0.92,
            "provenance": {
                "source": "evaluation",
            },
        },
    )

    runtime.observability.trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.LEARNING_OUTCOME_CREATED,
        component="learning",
        stage="learning",
        metadata={
            "outcome_id": "outcome-001",
            "outcome_type": "optimization",
            "success": True,
            "confidence": 0.88,
        },
    )

    service = LearningEvolutionApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    response = client.get(
        f"/api/v1/executions/{execution_id}/learning",
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["execution_id"] == execution_id

    assert len(payload["signals"]) == 1

    assert len(payload["outcomes"]) == 1

    assert payload["signals"][0]["confidence"] == 0.92

    assert payload["outcomes"][0]["success"] is True


def test_evolution_endpoint_returns_decisions_and_adaptations() -> None:
    """Evolution observations must be exposed as public contracts."""
    runtime = FakeRuntime()

    execution_id = "exec-evolution"

    runtime.observability.trace_service.create_trace(
        execution_id=execution_id,
    )

    runtime.observability.trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.EVOLUTION_DECISION_CREATED,
        component="evolution",
        stage="evolution",
        metadata={
            "decision_id": "decision-001",
            "decision_type": "adapt",
            "trigger": "evaluation",
            "confidence": 0.89,
        },
    )

    runtime.observability.trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.ADAPTATION_APPLIED,
        component="evolution",
        stage="evolution",
        metadata={
            "adaptation_id": "adaptation-001",
            "adaptation_type": "prompt",
            "adaptation_applied": True,
            "result": {
                "status": "applied",
            },
        },
    )

    service = LearningEvolutionApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    response = client.get(
        f"/api/v1/executions/{execution_id}/evolution",
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["execution_id"] == execution_id

    assert len(payload["decisions"]) == 1

    assert len(payload["adaptations"]) == 1

    assert payload["decisions"][0]["decision_type"] == "adapt"

    assert payload["adaptations"][0]["applied"] is True


def test_learning_supports_partial_data() -> None:
    """Optional learning information must remain nullable."""
    runtime = FakeRuntime()

    execution_id = "exec-learning-partial"

    runtime.observability.trace_service.create_trace(
        execution_id=execution_id,
    )

    runtime.observability.trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.LEARNING_SIGNAL_GENERATED,
        component="learning",
        metadata={
            "signal_id": "signal-partial",
        },
    )

    service = LearningEvolutionApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    response = client.get(
        f"/api/v1/executions/{execution_id}/learning",
    )

    payload = response.json()

    assert response.status_code == 200

    assert payload["signals"][0]["confidence"] is None

    assert payload["signals"][0]["signal_type"] is None


def test_evolution_supports_empty_state() -> None:
    """Evolution without observed events must remain deterministic."""
    runtime = FakeRuntime()

    execution_id = "exec-evolution-empty"

    runtime.observability.trace_service.create_trace(
        execution_id=execution_id,
    )

    service = LearningEvolutionApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    response = client.get(
        f"/api/v1/executions/{execution_id}/evolution",
    )

    payload = response.json()

    assert response.status_code == 200

    assert payload["decisions"] == []

    assert payload["adaptations"] == []

    assert payload["metadata"]["partial"] is True


def test_missing_execution_returns_404() -> None:
    """Unknown execution IDs must return HTTP 404."""
    runtime = FakeRuntime()

    service = LearningEvolutionApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    response = client.get(
        "/api/v1/executions/does-not-exist/learning",
    )

    assert response.status_code == 404

    assert response.json()["detail"]["error"] == "EXECUTION_NOT_FOUND"


def test_learning_contract_filters_sensitive_metadata() -> None:
    """Sensitive implementation details must not leak."""
    runtime = FakeRuntime()

    execution_id = "exec-learning-safe"

    runtime.observability.trace_service.create_trace(
        execution_id=execution_id,
    )

    runtime.observability.trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.LEARNING_SIGNAL_GENERATED,
        component="learning",
        metadata={
            "signal_id": "signal-safe",
            "api_key": "secret",
            "database_url": "secret-db",
            "stacktrace": "internal-stack",
        },
    )

    service = LearningEvolutionApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    response = client.get(
        f"/api/v1/executions/{execution_id}/learning",
    )

    payload = response.json()

    metadata = payload["signals"][0]["metadata"]

    assert "api_key" not in metadata
    assert "database_url" not in metadata
    assert "stacktrace" not in metadata
