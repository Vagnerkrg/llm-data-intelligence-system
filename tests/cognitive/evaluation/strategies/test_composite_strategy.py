from src.cognitive.evaluation.strategies.composite_strategy import (
    CompositeStrategy
)

from src.cognitive.evaluation.models.capability_evaluation import (
    CapabilityEvaluation
)


def test_composite_strategy_creation():

    strategy = CompositeStrategy()

    assert strategy is not None


def test_composite_strategy_evaluation():

    strategy = CompositeStrategy()

    evaluations = [
        CapabilityEvaluation(
            capability="reasoning",
            score=0.8,
            weight=1.0
        ),
        CapabilityEvaluation(
            capability="memory",
            score=0.6,
            weight=1.0
        )
    ]

    result = strategy.evaluate(
        evaluations
    )

    assert result == 0.7


def test_composite_strategy_empty():

    strategy = CompositeStrategy()

    result = strategy.evaluate([])

    assert result == 0.0