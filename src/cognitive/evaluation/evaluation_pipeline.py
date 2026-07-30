from typing import List

from src.cognitive.evaluation.evaluation_engine import (
    EvaluationEngine
)

from src.cognitive.evaluation.models.evaluation_context import (
    EvaluationContext
)

from src.cognitive.evaluation.models.evaluation_result import (
    EvaluationResult
)


class EvaluationPipeline:
    """
    Pipeline responsável pelo fluxo completo
    de avaliação cognitiva.
    """


    def __init__(
        self,
        engine: EvaluationEngine
    ):

        self.engine = engine



    def run(
        self,
        context: EvaluationContext
    ) -> List[EvaluationResult]:

        """
        Executa todos os avaliadores registrados.
        """

        return self.engine.evaluate_all(
            context
        )



    def run_single(
        self,
        evaluator_name: str,
        context: EvaluationContext
    ) -> EvaluationResult:

        """
        Executa um avaliador específico.
        """

        return self.engine.evaluate(
            evaluator_name,
            context
        )