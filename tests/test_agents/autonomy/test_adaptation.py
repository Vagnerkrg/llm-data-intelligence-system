from src.agents.autonomy import AdaptationStrategy


def test_adaptation_strategy_creation():

    strategy = AdaptationStrategy(
        strategy_id="strategy-001",
        learning_signal_id="signal-001",
        trigger="Repeated execution failure",
        action="Change execution strategy",
        expected_effect="Improve success rate"
    )

    assert strategy.strategy_id == "strategy-001"
    assert strategy.learning_signal_id == "signal-001"
    assert strategy.action == "Change execution strategy"


def test_adaptation_strategy_defaults():

    strategy = AdaptationStrategy(
        strategy_id="strategy-002",
        learning_signal_id="signal-002",
        trigger="Performance issue",
        action="Optimize process",
        expected_effect="Reduce latency"
    )

    assert strategy.confidence == 0.0
    assert strategy.metadata == {}