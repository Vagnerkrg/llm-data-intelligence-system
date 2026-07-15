from dataclasses import dataclass

from ..domain.evaluation_context import EvaluationContext


@dataclass(frozen=True)
class EvaluationRequest:
    """
    Public request contract for self evaluation.
    """

    context: EvaluationContext