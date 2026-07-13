from src.agents.decision.alternative_evaluation import AlternativeEvaluation


def test_alternative_evaluation_creation():

    evaluation = AlternativeEvaluation(
        alternative_id="analysis_optimization",
        score=0.85,
        confidence=0.8,
        risk_level="low",
        evaluation_reason="Good alignment with objective"
    )

    assert evaluation.alternative_id == "analysis_optimization"
    assert evaluation.score == 0.85
    assert evaluation.confidence == 0.8
    assert evaluation.risk_level == "low"