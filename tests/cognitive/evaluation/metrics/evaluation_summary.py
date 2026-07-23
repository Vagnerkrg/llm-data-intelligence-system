from dataclasses import dataclass


@dataclass
class EvaluationSummary:
    """
    Resumo consolidado das avaliações cognitivas.
    """

    total_evaluations: int

    average_score: float

    passed_evaluations: int = 0


    @property
    def pass_rate(self) -> float:

        if self.total_evaluations == 0:
            return 0.0

        return self.passed_evaluations / self.total_evaluations