"""Tests for the V1 Execution API."""

from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.dependencies import (
    get_execution_service,
)
from src.api.routes import (
    router,
)
from src.api.schemas import (
    CreateExecutionRequest,
    ExecutionErrorResponse,
    ExecutionResponse,
    ExecutionStatus,
)
from src.application.execution_service import (
    ExecutionApplicationService,
)


class FakeContext:
    """Fake Agent Runtime execution context."""

    def __init__(
        self,
        *,
        execution_id: str = "exec-test-001",
        status: str = "completed",
        result=None,
        metadata=None,
    ):
        self.execution_id = execution_id
        self.status = status
        self.results = (
            result
            if result is not None
            else [
                {
                    "answer": "Resposta de teste",
                    "source": "test",
                }
            ]
        )
        self.metadata = metadata if metadata is not None else {}


class FakeRuntime:
    """Fake runtime used to isolate the application layer."""

    def __init__(
        self,
        context: FakeContext | None = None,
    ):
        self.context = context or FakeContext()

    def execute(
        self,
        question: str,
    ):
        self.question = question
        return self.context


class FakeObservability:
    """Fake observability boundary."""

    def __init__(self):
        self._traces = {}

    def trace(
        self,
        execution_id: str,
    ):
        return self._traces.get(
            execution_id,
        )


def build_client(
    service: ExecutionApplicationService,
) -> TestClient:
    """Build isolated FastAPI test client."""
    app = FastAPI()
    app.include_router(
        router,
    )

    app.dependency_overrides[get_execution_service] = lambda: service

    return TestClient(
        app,
    )


def test_execution_request_contract_validates() -> None:
    """Execution request must accept valid public payloads."""
    request = CreateExecutionRequest(
        query="Test query",
        context={
            "channel": "api",
        },
        options={
            "timeout_ms": 1000,
            "metadata": {
                "correlation_id": "corr-001",
            },
        },
    )

    assert request.query == "Test query"
    assert request.options.timeout_ms == 1000
    assert request.options.metadata["correlation_id"] == "corr-001"


def test_execution_response_contract_validates() -> None:
    """Execution response must expose only public contract fields."""
    response = ExecutionResponse(
        execution_id="exec-001",
        status=ExecutionStatus.COMPLETED,
        created_at=datetime.now(
            timezone.utc,
        ),
        started_at=datetime.now(
            timezone.utc,
        ),
        result={
            "answer": "test",
        },
    )

    assert response.execution_id == "exec-001"

    assert response.status == ExecutionStatus.COMPLETED


def test_execution_error_contract_validates() -> None:
    """Execution errors must use the public error contract."""
    error = ExecutionErrorResponse(
        code="EXECUTION_FAILED",
        message="Execution failed.",
    )

    assert error.code == "EXECUTION_FAILED"


def test_execution_api_returns_completed_execution() -> None:
    """POST /api/v1/ask must return a public execution response."""
    runtime = FakeRuntime()

    service = ExecutionApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    response = client.post(
        "/api/v1/ask",
        json={
            "query": "Olá",
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["execution_id"] == "exec-test-001"

    assert payload["status"] == "completed"

    assert payload["result"]["answer"] == "Resposta de teste"


def test_execution_api_passes_query_to_runtime() -> None:
    """The API application service must propagate the user query."""
    runtime = FakeRuntime()

    service = ExecutionApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    client.post(
        "/api/v1/ask",
        json={
            "query": "Pergunta específica",
        },
    )

    assert runtime.question == "Pergunta específica"


def test_execution_api_maps_failed_execution() -> None:
    """Failed runtime contexts must become public failures."""
    runtime = FakeRuntime(
        context=FakeContext(
            execution_id="exec-failed",
            status="failed",
            result=[],
            metadata={
                "error": "Execution failed.",
            },
        ),
    )

    service = ExecutionApplicationService(
        runtime=runtime,
    )

    client = build_client(
        service,
    )

    response = client.post(
        "/api/v1/ask",
        json={
            "query": "Fail",
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "failed"

    assert payload["error"]["code"] == "EXECUTION_FAILED"


def test_execution_api_validates_empty_query() -> None:
    """Empty queries must be rejected by request validation."""
    service = ExecutionApplicationService(
        runtime=FakeRuntime(),
    )

    client = build_client(
        service,
    )

    response = client.post(
        "/api/v1/ask",
        json={
            "query": "",
        },
    )

    assert response.status_code == 422


def test_legacy_ask_endpoint_remains_available() -> None:
    """The existing /ask contract must remain backward compatible."""
    from src.api.dependencies import (
        get_intelligence_system,
    )
    from src.core.interfaces.response import (
        IntelligenceResponse,
    )

    class FakeSystem:
        def ask(
            self,
            question,
        ):
            return IntelligenceResponse(
                answer="Legacy response",
                source="test",
            )

    app = FastAPI()
    app.include_router(
        router,
    )

    app.dependency_overrides[get_intelligence_system] = lambda: FakeSystem()

    client = TestClient(
        app,
    )

    response = client.post(
        "/ask",
        json={
            "question": "Olá",
        },
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "Legacy response"
