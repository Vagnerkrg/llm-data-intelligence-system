from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ImprovementContext:
    experience: Any
    objective: str
    metadata: dict[str, Any] = field(default_factory=dict)