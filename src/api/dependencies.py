"""Dependency providers for the API layer."""

from functools import lru_cache

from src.application.cognitive_state_service import (
    CognitiveStateApplicationService,
)
from src.application.execution_service import (
    ExecutionApplicationService,
)
from src.application.execution_trace_service import (
    ExecutionTraceApplicationService,
)
from src.application.intelligence_system import (
    IntelligenceSystem,
)
from src.application.learning_evolution_service import (
    LearningEvolutionApplicationService,
)
from src.application.memory_knowledge_service import (
    MemoryKnowledgeApplicationService,
)


@lru_cache
def get_intelligence_system() -> IntelligenceSystem:
    """
    Return the legacy Intelligence System singleton.
    """
    return IntelligenceSystem()


@lru_cache
def get_execution_service() -> ExecutionApplicationService:
    """
    Return the Execution API application service.

    The Agent Runtime remains behind the application boundary.
    """
    return ExecutionApplicationService()


@lru_cache
def get_execution_trace_service() -> ExecutionTraceApplicationService:
    """
    Return the read-only Execution Trace application service.

    Trace access remains behind the application layer and does not expose
    the Observability repository directly to the API controller.
    """
    return ExecutionTraceApplicationService()


@lru_cache
def get_cognitive_state_service() -> CognitiveStateApplicationService:
    """Return the cognitive state application service."""
    return CognitiveStateApplicationService()


@lru_cache
def get_memory_knowledge_service() -> MemoryKnowledgeApplicationService:
    """Return the Memory and Knowledge application service."""
    return MemoryKnowledgeApplicationService()


@lru_cache
def get_learning_evolution_service() -> LearningEvolutionApplicationService:
    """Return the Learning and Evolution application service."""
    return LearningEvolutionApplicationService()
