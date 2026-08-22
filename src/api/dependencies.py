"""Dependency providers for the API layer."""

from functools import lru_cache

from src.application.execution_service import (
    ExecutionApplicationService,
)
from src.application.execution_trace_service import (
    ExecutionTraceApplicationService,
)
from src.application.intelligence_system import (
    IntelligenceSystem,
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
