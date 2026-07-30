from src.cognitive.evaluation.models.capability_evaluation import CapabilityEvaluation


def test_capability_evaluation_creation():

    evaluation = CapabilityEvaluation(
        capability="reasoning",
        score=0.85
    )

    assert evaluation.capability == "reasoning"
    assert evaluation.score == 0.85


def test_capability_weighted_score():

    evaluation = CapabilityEvaluation(
        capability="memory",
        score=0.80,
        weight=2.0
    )

    assert evaluation.weighted_score == 1.6