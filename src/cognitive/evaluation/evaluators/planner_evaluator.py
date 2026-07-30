from src.cognitive.evaluation.models.evaluation_context import (
    EvaluationContext
)

from src.cognitive.evaluation.models.evaluation_result import (
    EvaluationResult
)


class PlannerEvaluator:
    """
    Avaliador responsável por analisar
    capacidade de planejamento do agente.
    """

    def evaluate(
        self,
        context: EvaluationContext
    ) -> EvaluationResult:

        plan = context.metadata.get(
            "plan"
        )

        if plan:

            return EvaluationResult(
                score=1.0,
                passed=True,
                evaluator="planner",
                details={
                    "plan_available": True
                },
                confidence=1.0
            )

        return EvaluationResult(
            score=0.0,
            passed=False,
            evaluator="planner",
            details={
                "plan_available": False
            },
            confidence=0.5
        )