from src.evaluation.answer_evaluator import AnswerEvaluator
from src.evaluation.evaluation_history import EvaluationHistory



class QualityMonitor:
    """
    Monitors answer quality.

    Combines answer evaluation with
    historical tracking.
    """


    def __init__(
        self,
        evaluator=None,
        history=None
    ):


        self.evaluator = (
            evaluator
            if evaluator
            else AnswerEvaluator()
        )


        self.history = (
            history
            if history
            else EvaluationHistory()
        )



    def evaluate(
        self,
        question: str,
        answer: str,
        route: str
    ):
        """
        Evaluates response quality
        and stores result.
        """


        evaluation = self.evaluator.evaluate(
            question,
            answer
        )


        result = {

            "question": question,

            "answer": answer,

            "route": route,

            "score": evaluation.get(
                "score",
                0
            ),

            "quality": evaluation.get(
                "quality",
                "unknown"
            ),

            "issues": evaluation.get(
                "issues",
                []
            )

        }


        self.history.save(
            result
        )


        return result