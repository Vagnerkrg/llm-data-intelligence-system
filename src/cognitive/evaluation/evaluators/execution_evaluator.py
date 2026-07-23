from src.cognitive.evaluation.models.evaluation_context import (
    EvaluationContext
)

from src.cognitive.evaluation.models.evaluation_result import (
    EvaluationResult
)


class ExecutionEvaluator:
    """
    Avaliador responsável por analisar
    qualidade da execução do agente.
    """

    def evaluate(
        self,
        context: EvaluationContext
    ) -> EvaluationResult:
        """
        Avalia uma execução.

        Critério inicial:
        execução com output válido = sucesso.
        """

        if context.output_data is not None:

            return EvaluationResult(
                score=1.0,
                passed=True,
                evaluator="execution",
                details={
                    "status": "completed"
                },
                confidence=1.0
            )

        return EvaluationResult(
            score=0.0,
            passed=False,
            evaluator="execution",
            details={
                "status": "failed"
            },
            confidence=0.5
        )