from src.cognitive.evaluation.protocols.evaluation_strategy import EvaluationStrategy


class MockEvaluationStrategy(EvaluationStrategy):

    def execute(self, evaluations):

        return {
            "score": 0.85
        }


def test_evaluation_strategy_protocol_creation():

    strategy = MockEvaluationStrategy()

    assert strategy is not None


def test_evaluation_strategy_has_execute_method():

    strategy = MockEvaluationStrategy()

    assert hasattr(strategy, "execute")


def test_evaluation_strategy_execution():

    strategy = MockEvaluationStrategy()

    result = strategy.execute(
        [
            {
                "capability": "reasoning",
                "score": 0.85
            }
        ]
    )

    assert result["score"] == 0.85
    