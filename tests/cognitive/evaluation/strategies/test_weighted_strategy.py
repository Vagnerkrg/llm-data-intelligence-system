from src.cognitive.evaluation.strategies.weighted_strategy import (
    WeightedStrategy
)

from src.cognitive.evaluation.models.capability_evaluation import (
    CapabilityEvaluation
)


def test_weighted_strategy_creation():

    strategy = WeightedStrategy()

    assert strategy is not None


def test_weighted_strategy_single_evaluation():

    strategy = WeightedStrategy()

    evaluation = CapabilityEvaluation(
        capability="reasoning",
        score=0.8,
        weight=1.0
    )

    result = strategy.evaluate(
        [evaluation]
    )

    assert result == 0.8


def test_weighted_strategy_multiple_evaluations():

    strategy = WeightedStrategy()

    evaluations = [
        CapabilityEvaluation(
            capability="reasoning",
            score=0.8,
            weight=2.0
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

    expected = (
        (0.8 * 2.0) +
        (0.6 * 1.0)
    ) / 3.0

    assert result == expected


def test_weighted_strategy_empty_list():

    strategy = WeightedStrategy()

    result = strategy.evaluate([])

    assert result == 0.0