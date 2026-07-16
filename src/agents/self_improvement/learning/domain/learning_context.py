"""Learning context domain model."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class LearningContext:
    """Context used during learning process."""

    experiences: list[Any] = field(default_factory=list)
    patterns: list[Any] = field(default_factory=list)
    reflections: list[Any] = field(default_factory=list)
    knowledge_entries: list[Any] = field(default_factory=list)
    adaptations: list[Any] = field(default_factory=list)

    @property
    def has_experiences(self) -> bool:
        """Return whether experiences exist."""
        return bool(self.experiences)

    @property
    def has_patterns(self) -> bool:
        """Return whether patterns exist."""
        return bool(self.patterns)

    @property
    def has_reflections(self) -> bool:
        """Return whether reflections exist."""
        return bool(self.reflections)

    @property
    def has_knowledge(self) -> bool:
        """Return whether knowledge exists."""
        return bool(self.knowledge_entries)

    @property
    def has_adaptations(self) -> bool:
        """Return whether adaptations exist."""
        return bool(self.adaptations)