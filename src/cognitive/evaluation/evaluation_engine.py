from typing import List

from src.cognitive.evaluation.evaluator_registry import (
    EvaluatorRegistry
)

from src.cognitive.evaluation.models.evaluation_context import (
    EvaluationContext
)

from src.cognitive.evaluation.models.evaluation_result import (
    EvaluationResult
)


class EvaluationEngine:
    """
    Engine responsável por executar avaliações cognitivas.
    """


    def __init__(
        self,
        registry: EvaluatorRegistry
    ):

        self.registry = registry



    def evaluate(
        self,
        evaluator_name: str,
        context: EvaluationContext
    ) -> EvaluationResult:

        evaluator = self.registry.get(
            evaluator_name
        )


        if evaluator is None:

            raise ValueError(
                f"Evaluator '{evaluator_name}' not found"
            )


        return evaluator.evaluate(
            context
        )



    def evaluate_all(
        self,
        context: EvaluationContext
    ) -> List[EvaluationResult]:

        results = []


        for name in self.registry.list_evaluators():

            result = self.evaluate(
                name,
                context
            )

            results.append(
                result
            )


        return results