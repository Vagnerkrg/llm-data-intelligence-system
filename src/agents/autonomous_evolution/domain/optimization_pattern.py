from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class OptimizationPattern:
    """
    Represents a recurring pattern detected across past experiences.
    """

    name: str
    category: str
    occurrence_count: int = 0
    average_score: float = 0.0
    average_confidence: float = 0.0
    strategy: str | None = None
    evidence: list[Any] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Optimization pattern name cannot be empty.")

        if not self.category.strip():
            raise ValueError("Optimization pattern category cannot be empty.")

        if self.occurrence_count < 0:
            raise ValueError(
                "Optimization pattern occurrence count cannot be negative."
            )

        if not 0.0 <= self.average_score <= 1.0:
            raise ValueError(
                "Optimization pattern average score must be between 0.0 and 1.0."
            )

        if not 0.0 <= self.average_confidence <= 1.0:
            raise ValueError(
                "Optimization pattern average confidence must be between 0.0 and 1.0."
            )

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the pattern into a dictionary.
        """
        return asdict(self)
