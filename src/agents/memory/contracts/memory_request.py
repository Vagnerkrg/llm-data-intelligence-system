from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class MemoryRequest:
    """
    Represents a request sent to the memory subsystem.

    A memory request can be used for:
    - storing information;
    - retrieving information;
    - querying previous context.
    """

    query: str

    agent_id: Optional[str] = None

    memory_type: Optional[str] = None

    metadata: Dict = field(
        default_factory=dict
    )

    limit: int = 10