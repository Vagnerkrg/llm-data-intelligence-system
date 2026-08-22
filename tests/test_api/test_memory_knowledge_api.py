"""Tests for the Memory and Knowledge API."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.dependencies import (
    get_memory_knowledge_service,
)
from src.api.routes import router
from src.application.memory_knowledge_service import (
    MemoryKnowledgeApplicationService,
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
    service: MemoryKnowledgeApplicationService,
) -> TestClient:
    """Build an isolated API client."""
    app = FastAPI()

    app.include_router(
        router,
    )

    app.dependency_overrides[get_memory_knowledge_service] = lambda: service

    return TestClient(
        app,
    )


def test_memory_endpoint_returns_public_items() -> None:
    """Memory observations must be mapped to the public contract."""
    runtime = FakeRuntime()

    execution_id = "exec-memory"

    runtime.observability.trace_service.create_trace(
        execution_id=execution_id,
    )

    runtime.observability.trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.MEMORY_RETRIEVAL_COMPLETED,
        component="memory",
        stage="memory",
        metadata={
            "memory_id": "memory-001",
            "content": "public memory content",
            "relevance_score": 0.91,
            "source": {
                "type": "semantic",
            },
            "model": "internal-model",
        },
    )

    service = MemoryKnowledgeApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    response = client.get(
        f"/api/v1/executions/{execution_id}/memory",
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["execution_id"] == execution_id

    assert payload["total"] == 1

    assert payload["items"][0]["id"] == "memory-001"

    assert payload["items"][0]["relevance"] == 0.91

    assert payload["items"][0]["content"] == "public memory content"

    assert "model" in payload["items"][0]["metadata"]


def test_knowledge_endpoint_returns_public_items() -> None:
    """Knowledge observations must be mapped to the public contract."""
    runtime = FakeRuntime()

    execution_id = "exec-knowledge"

    runtime.observability.trace_service.create_trace(
        execution_id=execution_id,
    )

    runtime.observability.trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.KNOWLEDGE_ACCESSED,
        component="knowledge",
        stage="knowledge",
        metadata={
            "knowledge_id": "knowledge-001",
            "source": "documentation",
            "relevance": 0.87,
            "chapter": "api",
        },
    )

    service = MemoryKnowledgeApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    response = client.get(
        f"/api/v1/executions/{execution_id}/knowledge",
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["execution_id"] == execution_id

    assert payload["total"] == 1

    assert payload["items"][0]["id"] == "knowledge-001"

    assert payload["items"][0]["source"] == "documentation"

    assert payload["items"][0]["relevance"] == 0.87


def test_memory_supports_partial_data() -> None:
    """Missing optional memory fields must remain nullable."""
    runtime = FakeRuntime()

    execution_id = "exec-memory-partial"

    runtime.observability.trace_service.create_trace(
        execution_id=execution_id,
    )

    runtime.observability.trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.MEMORY_RETRIEVAL_COMPLETED,
        component="memory",
        stage="memory",
        metadata={
            "memory_id": "memory-partial",
        },
    )

    service = MemoryKnowledgeApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    response = client.get(
        f"/api/v1/executions/{execution_id}/memory",
    )

    payload = response.json()

    assert response.status_code == 200

    assert payload["items"][0]["content"] is None

    assert payload["items"][0]["relevance"] is None


def test_knowledge_supports_empty_observability() -> None:
    """Knowledge endpoint must return an explicit empty state."""
    runtime = FakeRuntime()

    execution_id = "exec-knowledge-empty"

    runtime.observability.trace_service.create_trace(
        execution_id=execution_id,
    )

    service = MemoryKnowledgeApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    response = client.get(
        f"/api/v1/executions/{execution_id}/knowledge",
    )

    payload = response.json()

    assert response.status_code == 200

    assert payload["items"] == []

    assert payload["total"] == 0

    assert payload["metadata"]["partial"] is True


def test_missing_execution_returns_404() -> None:
    """Unknown execution IDs must return HTTP 404."""
    runtime = FakeRuntime()

    service = MemoryKnowledgeApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    response = client.get(
        "/api/v1/executions/does-not-exist/memory",
    )

    assert response.status_code == 404

    assert response.json()["detail"]["error"] == "EXECUTION_NOT_FOUND"


def test_memory_contract_does_not_expose_storage_details() -> None:
    """Storage implementation details must not leak through the API."""
    runtime = FakeRuntime()

    execution_id = "exec-memory-safe"

    runtime.observability.trace_service.create_trace(
        execution_id=execution_id,
    )

    runtime.observability.trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.MEMORY_RETRIEVAL_COMPLETED,
        component="memory",
        metadata={
            "memory_id": "memory-safe",
            "content": "safe",
            "database_url": "secret-value",
            "api_key": "secret-key",
        },
    )

    service = MemoryKnowledgeApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    response = client.get(
        f"/api/v1/executions/{execution_id}/memory",
    )

    payload = response.json()

    metadata = payload["items"][0]["metadata"]

    assert "database_url" not in metadata

    assert "api_key" not in metadata
