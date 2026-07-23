from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class ConsolidationResult:
    """
    Represents the result
    of a memory consolidation process.
    """

    memory_id: str = ""

    score: float = 0.0

    consolidated: bool = False

    message: str = ""

    data: Optional[Any] = None