"""Learning outcome domain model."""

from dataclasses import dataclass


@dataclass(slots=True)
class LearningOutcome:
    """Result generated from learning."""

    improvement: str
    confidence: float
    success: bool = True
    improvement_detected: bool = True
    impact: str = ""

    @property
    def is_positive(self) -> bool:
        """Return whether learning generated improvement."""
        return self.success and self.improvement_detected