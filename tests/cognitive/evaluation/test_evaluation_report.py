from src.cognitive.evaluation.models.evaluation_report import (
    EvaluationReport
)

from src.cognitive.evaluation.models.evaluation_result import (
    EvaluationResult
)



def create_result(score):

    return EvaluationResult(
        score=score,
        passed=True,
        evaluator="test"
    )



def test_evaluation_report_creation():

    report = EvaluationReport(
        evaluation_id="eval-001"
    )

    assert report is not None
    assert report.evaluation_id == "eval-001"



def test_report_add_result():

    report = EvaluationReport(
        evaluation_id="eval-002"
    )


    result = create_result(
        0.8
    )


    report.add_result(
        result
    )


    assert len(report.results) == 1
    assert report.results[0].score == 0.8



def test_report_calculate_score():

    report = EvaluationReport(
        evaluation_id="eval-003"
    )


    report.add_result(
        create_result(0.8)
    )

    report.add_result(
        create_result(0.6)
    )


    score = report.calculate_score()


    assert score == 0.7



def test_empty_report_score():

    report = EvaluationReport(
        evaluation_id="eval-004"
    )


    score = report.calculate_score()


    assert score == 0.0