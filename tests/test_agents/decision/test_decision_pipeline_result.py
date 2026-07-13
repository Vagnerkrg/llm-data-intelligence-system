from src.agents.decision.decision_pipeline_result import DecisionPipelineResult


def test_decision_pipeline_result_creation():

    result = DecisionPipelineResult(
        decision_id="decision_001",
        confidence=0.9,
        explanation="Selected best alternative"
    )

    assert result.decision_id == "decision_001"
    assert result.confidence == 0.9
    assert result.explanation == "Selected best alternative"