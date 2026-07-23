from src.cognitive.evaluation.models.evaluation_context import (
    EvaluationContext
)

from src.cognitive.evaluation.models.evaluation_result import (
    EvaluationResult
)


class MemoryEvaluator:
    """
    Avaliador responsável por analisar
    capacidade de memória do agente.
    """

    def evaluate(
        self,
        context: EvaluationContext
    ) -> EvaluationResult:
        """
        Avaliação inicial:

        Memória válida quando existe
        contexto recuperado.
        """

        memory_context = context.metadata.get(
            "memory_context"
        )

        if memory_context:

            return EvaluationResult(
                score=1.0,
                passed=True,
                evaluator="memory",
                details={
                    "memory_available": True
                },
                confidence=1.0
            )

        return EvaluationResult(
            score=0.0,
            passed=False,
            evaluator="memory",
            details={
                "memory_available": False
            },
            confidence=0.5
        )