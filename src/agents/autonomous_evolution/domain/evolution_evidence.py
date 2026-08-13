from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class EvolutionEvidence:
    """
    Represents evidence supporting an autonomous evolution decision.

    Evidence remains intentionally generic so the domain does not depend
    on cognitive evaluation, memory, runtime, or external providers.
    """

    source: str
    signal: str
    value: Any = None
    confidence: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError("Evidence source cannot be empty.")

        if not self.signal.strip():
            raise ValueError("Evidence signal cannot be empty.")

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "Evidence confidence must be between 0.0 and 1.0."
            )

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the evolution evidence into a dictionary.
        """
        return asdict(self)