from src.cognitive.evaluation.metrics.capability_metrics import CapabilityMetrics


def test_capability_metrics_creation():

    metrics = CapabilityMetrics(
        capability="reasoning",
        score=0.85
    )

    assert metrics.capability == "reasoning"
    assert metrics.score == 0.85


def test_capability_metrics_score_range():

    metrics = CapabilityMetrics(
        capability="memory",
        score=0.90
    )

    assert 0 <= metrics.score <= 1


def test_capability_metrics_weighted_score():

    metrics = CapabilityMetrics(
        capability="planning",
        score=0.80,
        weight=2.0
    )

    assert metrics.weighted_score == 1.6