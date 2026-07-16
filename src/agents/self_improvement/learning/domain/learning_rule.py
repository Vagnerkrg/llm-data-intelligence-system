"""Learning rule domain model."""

from dataclasses import dataclass


@dataclass(slots=True)
class LearningRule:
    """Reusable cognitive rule learned by the agent."""

    condition: str
    action: str
    confidence: float = 0.0

    @property
    def is_applicable(self) -> bool:
        """Return whether rule can be applied."""
        return bool(self.condition and self.action)

    @property
    def is_confident(self) -> bool:
        """Return whether rule has enough confidence."""
        return self.confidence >= 0.7