from src.cognitive.evaluation.strategies.normalized_strategy import (
    NormalizedStrategy
)


def test_normalized_strategy_creation():

    strategy = NormalizedStrategy()

    assert strategy is not None


def test_normalized_strategy_default_range():

    strategy = NormalizedStrategy()

    result = strategy.evaluate(
        0.5
    )

    assert result == 0.5


def test_normalized_strategy_percentage_range():

    strategy = NormalizedStrategy()

    result = strategy.evaluate(
        score=50,
        minimum=0,
        maximum=100
    )

    assert result == 0.5


def test_normalized_strategy_lower_bound():

    strategy = NormalizedStrategy()

    result = strategy.evaluate(
        -10,
        minimum=0,
        maximum=100
    )

    assert result == 0.0


def test_normalized_strategy_upper_bound():

    strategy = NormalizedStrategy()

    result = strategy.evaluate(
        150,
        minimum=0,
        maximum=100
    )

    assert result == 1.0


def test_normalized_strategy_invalid_range():

    strategy = NormalizedStrategy()

    result = strategy.evaluate(
        10,
        minimum=100,
        maximum=50
    )

    assert result == 0.0