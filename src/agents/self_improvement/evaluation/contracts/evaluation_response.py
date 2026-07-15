from dataclasses import dataclass

from ..domain.evaluation_result import EvaluationResult


@dataclass(frozen=True)
class EvaluationResponse:
    """
    Public response contract for self evaluation.
    """

    result: EvaluationResult