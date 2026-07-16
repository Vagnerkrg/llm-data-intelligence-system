"""Reflection finding domain model."""

from dataclasses import dataclass

from .reflection_type import ReflectionType


@dataclass(slots=True, frozen=True)
class ReflectionFinding:
    """Represents an individual finding produced during reflection."""

    reflection_type: ReflectionType
    title: str
    description: str
    confidence: float

    def is_high_confidence(self, threshold: float = 0.80) -> bool:
        """Return True when confidence exceeds the given threshold."""
        return self.confidence >= threshold