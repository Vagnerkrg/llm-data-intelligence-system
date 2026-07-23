from src.cognitive.evaluation.signals.learning_signal import LearningSignal


def test_learning_signal_creation():

    signal = LearningSignal(
        source="reflection",
        knowledge="Better planning strategy"
    )

    assert signal.source == "reflection"
    assert signal.knowledge == "Better planning strategy"


def test_learning_signal_confidence():

    signal = LearningSignal(
        source="agent",
        knowledge="New pattern",
        confidence=0.9
    )

    assert signal.confidence == 0.9