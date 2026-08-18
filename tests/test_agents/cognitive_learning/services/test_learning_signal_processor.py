from src.agents.cognitive_learning.services import (
    LearningSignalProcessor,
)
from src.agents.self_improvement.evaluation.domain.learning_signal import (
    LearningSignal,
)


def test_process_learning_signals():
    processor = LearningSignalProcessor()

    signals = [
        LearningSignal(
            signal_type="tool_usage",
            pattern="high tool usage",
            confidence=0.8,
            impact="medium",
            recommendation="Review execution strategy.",
        )
    ]

    result = processor.process(signals)

    assert len(result) == 1
    assert result[0].signal_type == "tool_usage"
    assert result[0].pattern == "high tool usage"
    assert result[0].confidence == 0.8
