from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class EvaluationMetric:
    """
    Represents a measurable cognitive capability.

    A metric defines what is being evaluated and stores
    the resulting score and supporting metadata.
    """

    name: str
    category: str
    score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
    description: str = ""

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Metric name cannot be empty.")

        if not self.category.strip():
            raise ValueError("Metric category cannot be empty.")

        if not 0.0 <= self.score <= 1.0:
            raise ValueError("Metric score must be between 0.0 and 1.0.")

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the evaluation metric into a dictionary.
        """
        return asdict(self)