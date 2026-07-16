"""Reflection manager."""

from time import perf_counter

from ..contracts import ReflectionRequest, ReflectionResponse
from .reflection_engine import ReflectionEngine
from .reflection_history import ReflectionHistory


class ReflectionManager:
    """Coordinates reflection execution."""

    def __init__(
        self,
        engine: ReflectionEngine | None = None,
        history: ReflectionHistory | None = None,
    ) -> None:
        self._engine = engine or ReflectionEngine()
        self._history = history or ReflectionHistory()

    def reflect(
        self,
        request: ReflectionRequest,
    ) -> ReflectionResponse:
        """Execute the complete reflection pipeline."""

        start = perf_counter()

        summary = self._engine.reflect(request)

        self._history.add(summary)

        elapsed = perf_counter() - start

        return ReflectionResponse(
            success=True,
            summary=summary,
            execution_time=elapsed,
        )

    @property
    def history(self) -> ReflectionHistory:
        """Return the reflection history."""
        return self._history