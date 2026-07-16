"""Learning experience domain model."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class LearningExperience:
    """Represents an experience acquired by the agent."""

    description: str
    success: bool
    source: str = ""
    outcome: str = ""
    confidence: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def is_reliable(self) -> bool:
        """Return whether experience has enough confidence."""
        return self.confidence >= 0.7