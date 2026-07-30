from src.cognitive.evaluation.strategies.threshold_strategy import (
    ThresholdStrategy
)


def test_threshold_strategy_creation():

    strategy = ThresholdStrategy()

    assert strategy is not None


def test_threshold_strategy_default_threshold():

    strategy = ThresholdStrategy()

    assert strategy.threshold == 0.7


def test_threshold_strategy_pass():

    strategy = ThresholdStrategy()

    result = strategy.evaluate(0.9)

    assert result is True


def test_threshold_strategy_fail():

    strategy = ThresholdStrategy()

    result = strategy.evaluate(0.5)

    assert result is False


def test_threshold_strategy_custom_threshold():

    strategy = ThresholdStrategy(
        threshold=0.8
    )

    assert strategy.evaluate(0.8) is True