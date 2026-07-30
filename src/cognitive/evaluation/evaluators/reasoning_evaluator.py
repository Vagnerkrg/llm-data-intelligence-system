from src.cognitive.evaluation.models.evaluation_result import (
    EvaluationResult
)


class ReasoningEvaluator:
    """
    Avaliador de capacidade de raciocínio cognitivo.
    """

    def evaluate(self, context):

        reasoning_score = 0.0

        if context.output_data:
            reasoning_score = 1.0

        return EvaluationResult(
            score=reasoning_score,
            passed=reasoning_score > 0,
            evaluator="reasoning"
        )