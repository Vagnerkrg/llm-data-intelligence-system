from dataclasses import dataclass, field
from typing import List

from .evaluation_result import EvaluationResult


@dataclass
class EvaluationReport:
    """
    Relatório agregado de uma avaliação.
    """

    evaluation_id: str

    results: List[EvaluationResult] = field(default_factory=list)

    final_score: float = 0.0


    def add_result(self, result: EvaluationResult):
        self.results.append(result)


    def calculate_score(self) -> float:
        if not self.results:
            return 0.0

        self.final_score = sum(
            result.score for result in self.results
        ) / len(self.results)

        return self.final_score