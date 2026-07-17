from dataclasses import dataclass

from ..domain.improvement_result import ImprovementResult


@dataclass(slots=True)
class ImprovementResponse:
    result: ImprovementResult