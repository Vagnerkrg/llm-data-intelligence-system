"""Reflection context domain model."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ReflectionContext:
    """Aggregates the information required for a reflection cycle."""

    evaluation_result: Any | None = None
    knowledge_entries: list[Any] = field(default_factory=list)
    adaptation_results: list[Any] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def has_knowledge(self) -> bool:
        """Return True when knowledge entries are available."""
        return bool(self.knowledge_entries)

    @property
    def has_adaptations(self) -> bool:
        """Return True when adaptation results are available."""
        return bool(self.adaptation_results)