from dataclasses import dataclass

from ..domain.improvement_context import ImprovementContext


@dataclass(slots=True)
class ImprovementRequest:
    context: ImprovementContext