from dataclasses import dataclass, field
from typing import Optional, Any, List


@dataclass
class RetrievalResult:
    """
    Represents the result
    of a memory retrieval operation.
    """

    query: str = ""

    score: float = 0.0

    memories: List[Any] = field(
        default_factory=list
    )

    success: bool = False

    message: str = ""

    memory: Optional[Any] = None