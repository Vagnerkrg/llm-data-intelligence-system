from dataclasses import dataclass, field
from typing import Dict


@dataclass
class RelevanceResult:
    """
    Represents the cognitive relevance
    evaluation of a memory.
    """

    memory_id: str

    score: float = 0.0

    factors: Dict[str, float] = field(
        default_factory=dict
    )

    explanation: str = ""