from src.agents.autonomy import AutonomyDecision


def test_autonomy_decision_creation():

    decision = AutonomyDecision(
        decision_id="decision-001",
        context_id="ctx-001",
        strategy_id="strategy-001",
        reason="Evidence supports adaptation"
    )

    assert decision.decision_id == "decision-001"
    assert decision.context_id == "ctx-001"
    assert decision.strategy_id == "strategy-001"
    assert decision.status == "PENDING"


def test_autonomy_decision_defaults():

    decision = AutonomyDecision(
        decision_id="decision-002",
        context_id="ctx-002",
        strategy_id="strategy-002",
        reason="Manual review required"
    )

    assert decision.confidence == 0.0
    assert decision.approval_required is False
    assert decision.metadata == {}