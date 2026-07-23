from src.cognitive.evaluation.metrics.evaluation_summary import EvaluationSummary


def test_evaluation_summary_creation():

    summary = EvaluationSummary(
        total_evaluations=10,
        average_score=0.85
    )

    assert summary.total_evaluations == 10
    assert summary.average_score == 0.85


def test_evaluation_summary_pass_rate():

    summary = EvaluationSummary(
        total_evaluations=20,
        passed_evaluations=18,
        average_score=0.90
    )

    assert summary.pass_rate == 0.9