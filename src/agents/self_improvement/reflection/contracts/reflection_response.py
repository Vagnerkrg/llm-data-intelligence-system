"""Reflection response contract."""

from dataclasses import dataclass, field
from typing import Any

from ..domain import ReflectionSummary


@dataclass(slots=True)
class ReflectionResponse:
    """Response returned after a reflection cycle."""

    success: bool
    summary: ReflectionSummary
    execution_time: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def has_summary(self) -> bool:
        """Return True when the response contains findings."""
        return self.summary.has_findings