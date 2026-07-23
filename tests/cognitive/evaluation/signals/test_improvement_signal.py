from src.cognitive.evaluation.signals.improvement_signal import ImprovementSignal


def test_improvement_signal_creation():

    signal = ImprovementSignal(
        capability="reasoning",
        score=0.4,
        reason="Low reasoning score"
    )

    assert signal.capability == "reasoning"
    assert signal.score == 0.4


def test_improvement_signal_metadata():

    signal = ImprovementSignal(
        capability="memory",
        score=0.5,
        reason="Need improvement"
    )

    signal.add_metadata("source", "evaluation")

    assert signal.metadata["source"] == "evaluation"