from dataclasses import dataclass, field
from typing import Any, Dict

from .improvement_status import ImprovementStatus


@dataclass(slots=True)
class ImprovementResult:
    """
    Result produced after a cognitive improvement cycle.
    """

    status: ImprovementStatus

    insights: list[str] = field(
        default_factory=list
    )

    knowledge: list[Any] = field(
        default_factory=list
    )

    adaptations: list[Any] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )