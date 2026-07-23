from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Optional

from src.agents.memory.domain.memory_type import (
    MemoryType
)

from src.agents.memory.domain.memory_status import (
    MemoryStatus
)


@dataclass
class MemoryEntry:
    """
    Represents a single memory unit
    stored by the agent.
    """

    memory_id: str

    content: str

    memory_type: MemoryType

    source: Optional[str] = None

    status: MemoryStatus = (
        MemoryStatus.CREATED
    )

    metadata: Dict = field(
        default_factory=dict
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )