from dataclasses import dataclass, field
from typing import List

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)


@dataclass
class MemoryContext:
    """
    Represents the memory context
    available during agent execution.
    """

    agent_id: str

    memories: List[MemoryEntry] = field(
        default_factory=list
    )

    query: str = ""