from dataclasses import dataclass
from typing import Any

from src.agents.memory.domain.memory_status import (
    MemoryStatus
)


@dataclass
class MemoryResult:
    """
    Represents the result
    of a memory operation.
    """

    success: bool

    status: MemoryStatus

    message: str = ""

    data: Any = None