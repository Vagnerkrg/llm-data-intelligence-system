"""Reflection request contract."""

from dataclasses import dataclass, field
from typing import Any

from ..domain import ReflectionContext


@dataclass(slots=True)
class ReflectionRequest:
    """Request for a reflection cycle."""

    context: ReflectionContext
    objective: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def has_objective(self) -> bool:
        """Return True when an objective was provided."""
        return bool(self.objective.strip())