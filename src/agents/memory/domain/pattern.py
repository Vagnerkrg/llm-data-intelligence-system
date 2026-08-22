from dataclasses import dataclass, field
from typing import List


@dataclass
class Pattern:
    """
    Represents a recurring pattern
    extracted from memory experiences.
    """

    pattern_id: str

    description: str

    occurrences: int = 0

    memory_ids: List[str] = field(default_factory=list)

    confidence: float = 0.0
