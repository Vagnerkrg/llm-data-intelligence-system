"""Learning pattern domain model."""

from dataclasses import dataclass


@dataclass(slots=True)
class LearningPattern:
    """Pattern discovered from experiences."""

    name: str
    frequency: int = 0
    description: str = ""
    confidence: float = 0.0

    @property
    def is_significant(self) -> bool:
        """Return whether pattern is relevant."""
        return self.frequency > 1 and self.confidence >= 0.7