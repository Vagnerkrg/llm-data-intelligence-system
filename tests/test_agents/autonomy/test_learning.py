from src.agents.autonomy import LearningSignal


def test_learning_signal_creation():

    signal = LearningSignal(
        signal_id="signal-001",
        reflection_id="ref-001",
        source="execution",
        pattern="Successful query optimization",
        impact="Improved response time"
    )

    assert signal.signal_id == "signal-001"
    assert signal.reflection_id == "ref-001"
    assert signal.pattern == "Successful query optimization"


def test_learning_signal_defaults():

    signal = LearningSignal(
        signal_id="signal-002",
        reflection_id="ref-002",
        source="evaluation",
        pattern="Failure pattern",
        impact="Requires adjustment"
    )

    assert signal.confidence == 0.0
    assert signal.metadata == {}