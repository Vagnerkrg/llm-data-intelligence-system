from src.agents.self_improvement.evaluation.domain.learning_signal import (
    LearningSignal,
)

from src.agents.self_improvement.evaluation.domain.evaluation_result import (
    EvaluationFinding,
)

from src.agents.self_improvement.evaluation.services.signal_generator import (
    SignalGenerator,
)


def test_signal_generator_creates_learning_signal():

    generator = SignalGenerator()

    findings = [
        EvaluationFinding(
            category="performance",
            description="high_tool_usage",
            severity="medium",
        )
    ]

    signals = generator.generate(findings)

    assert len(signals) == 1

    signal = signals[0]

    assert isinstance(signal, LearningSignal)
    assert signal.signal_type == "performance"
    assert signal.pattern == "high_tool_usage"
    assert signal.impact == "medium"
    assert signal.confidence == 0.7


def test_signal_generator_returns_empty_without_findings():

    generator = SignalGenerator()

    signals = generator.generate([])

    assert signals == []