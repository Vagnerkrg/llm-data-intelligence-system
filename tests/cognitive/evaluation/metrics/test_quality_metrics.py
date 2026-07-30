from src.cognitive.evaluation.metrics.quality_metrics import QualityMetrics


def test_quality_metrics_creation():

    metrics = QualityMetrics(
        evaluator="reasoning",
        quality_score=0.90
    )

    assert metrics.evaluator == "reasoning"
    assert metrics.quality_score == 0.90


def test_quality_metrics_score_range():

    metrics = QualityMetrics(
        evaluator="planning",
        quality_score=0.75
    )

    assert 0 <= metrics.quality_score <= 1


def test_quality_metrics_threshold():

    metrics = QualityMetrics(
        evaluator="memory",
        quality_score=0.85,
        threshold=0.80
    )

    assert metrics.is_high_quality() is True