from src.agents.self_improvement.evaluation.domain.learning_signal import (
    LearningSignal,
)


def test_learning_signal_creation():

    signal = LearningSignal(
        signal_type="performance",
        pattern="high_tool_usage",
        confidence=0.8,
        impact="medium",
        recommendation="Optimize execution strategy",
    )

    assert signal.signal_type == "performance"
    assert signal.pattern == "high_tool_usage"
    assert signal.confidence == 0.8
    assert signal.impact == "medium"
    assert (
        signal.recommendation
        == "Optimize execution strategy"
    )