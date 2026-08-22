from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class OptimizationSignal:
    """
    Represents a deterministic signal suggesting how future
    agent behavior or strategy could be optimized.
    """

    signal_type: str
    target: str
    direction: str
    strength: float = 0.0
    confidence: float = 0.0
    reason: str = ""
    supporting_patterns: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.signal_type.strip():
            raise ValueError("Optimization signal type cannot be empty.")

        if not self.target.strip():
            raise ValueError("Optimization signal target cannot be empty.")

        if not self.direction.strip():
            raise ValueError("Optimization signal direction cannot be empty.")

        if not 0.0 <= self.strength <= 1.0:
            raise ValueError(
                "Optimization signal strength must be between 0.0 and 1.0."
            )

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "Optimization signal confidence must be between 0.0 and 1.0."
            )

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the optimization signal into a dictionary.
        """
        return asdict(self)
