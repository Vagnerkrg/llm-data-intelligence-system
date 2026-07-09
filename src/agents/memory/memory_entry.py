from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict



@dataclass
class MemoryEntry:
    """
    Represents a single memory entry.

    Stores information generated
    during agent execution.
    """


    key: str

    value: Any

    memory_type: str = "general"

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )



    def to_dict(
        self
    ) -> Dict[str, Any]:
        """
        Convert memory entry
        into dictionary format.
        """


        return {

            "key": self.key,

            "value": self.value,

            "memory_type": self.memory_type,

            "metadata": self.metadata,

            "created_at": (
                self.created_at.isoformat()
            )

        }