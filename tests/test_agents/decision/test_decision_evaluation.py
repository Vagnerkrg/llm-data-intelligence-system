from src.agents.decision.decision_evaluation import DecisionEvaluation


def test_decision_evaluation_creation():

    evaluation = DecisionEvaluation(
        decision_id="decision-001",
        success=True,
        score=0.95,
        expected_outcome="Improve performance",
        observed_outcome="Performance improved"
    )

    assert evaluation.decision_id == "decision-001"
    assert evaluation.success is True
    assert evaluation.score == 0.95


def test_add_feedback():

    evaluation = DecisionEvaluation(
        decision_id="decision-001",
        success=True,
        score=0.95,
        expected_outcome="Improve performance",
        observed_outcome="Performance improved"
    )

    evaluation.add_feedback(
        "Decision achieved expected objective"
    )

    assert len(evaluation.feedback) == 1
    assert evaluation.feedback[0] == (
        "Decision achieved expected objective"
    )


def test_is_successful():

    evaluation = DecisionEvaluation(
        decision_id="decision-001",
        success=True,
        score=1.0,
        expected_outcome="Success",
        observed_outcome="Success"
    )

    assert evaluation.is_successful() is True


def test_has_feedback():

    evaluation = DecisionEvaluation(
        decision_id="decision-001",
        success=False,
        score=0.4,
        expected_outcome="Success",
        observed_outcome="Partial success"
    )

    assert evaluation.has_feedback() is False

    evaluation.add_feedback(
        "Need strategy adjustment"
    )

    assert evaluation.has_feedback() is True