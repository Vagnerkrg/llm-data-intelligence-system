from src.cognitive.evaluation.models.evaluation_result import (
    EvaluationResult
)


class ReflectionEvaluator:
    """
    Avaliador da capacidade de reflexão cognitiva.
    
    Verifica se o agente possui sinais
    de análise, feedback ou reflexão.
    """

    def evaluate(self, context):

        reflection_score = 0.0

        if context.metadata:
            if (
                "reflection" in context.metadata
                or "feedback" in context.metadata
            ):
                reflection_score = 1.0

        return EvaluationResult(
            score=reflection_score,
            passed=reflection_score > 0,
            evaluator="reflection"
        )