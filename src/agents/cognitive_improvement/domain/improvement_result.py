from dataclasses import dataclass, field
from typing import Any

from .improvement_status import ImprovementStatus


@dataclass(slots=True)
class ImprovementResult:
    status: ImprovementStatus
    insights: list[str] = field(default_factory=list)
    knowledge: list[Any] = field(default_factory=list)
    adaptations: list[Any] = field(default_factory=list)