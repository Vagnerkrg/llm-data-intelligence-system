"""Helpers for V1.29 API integration tests."""

from fastapi import FastAPI

from src.api.dependencies import (
    get_cognitive_state_service,
    get_execution_service,
    get_execution_trace_service,
    get_learning_evolution_service,
    get_memory_knowledge_service,
)
from src.api.routes import router
from src.application.cognitive_state_service import (
    CognitiveStateApplicationService,
)
from src.application.execution_service import (
    ExecutionApplicationService,
)
from src.application.execution_trace_service import (
    ExecutionTraceApplicationService,
)
from src.application.learning_evolution_service import (
    LearningEvolutionApplicationService,
)
from src.application.memory_knowledge_service import (
    MemoryKnowledgeApplicationService,
)


def build_integration_app(
    runtime,
) -> FastAPI:
    """Build an isolated API application with injected runtime."""
    application = FastAPI(
        title="V1.29 API Integration Tests",
        version="1.29.0",
    )

    application.include_router(
        router,
    )

    application.dependency_overrides[get_execution_service] = lambda: (
        ExecutionApplicationService(
            runtime=runtime,
        )
    )

    application.dependency_overrides[get_execution_trace_service] = lambda: (
        ExecutionTraceApplicationService(
            runtime=runtime,
        )
    )

    application.dependency_overrides[get_cognitive_state_service] = lambda: (
        CognitiveStateApplicationService(
            runtime=runtime,
        )
    )

    application.dependency_overrides[get_memory_knowledge_service] = lambda: (
        MemoryKnowledgeApplicationService(
            runtime=runtime,
        )
    )

    application.dependency_overrides[get_learning_evolution_service] = lambda: (
        LearningEvolutionApplicationService(
            runtime=runtime,
        )
    )

    return application
