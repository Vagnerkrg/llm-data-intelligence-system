from src.agents.autonomy import AutonomyEngine


def test_autonomy_engine_success_execution():

    engine = AutonomyEngine()

    decision = engine.evaluate_execution(
        execution_id="exec-001",
        result="Analysis completed successfully",
        success=True,
        metrics={
            "accuracy": 0.95
        },
    )

    assert decision.decision_id == "auto-exec-001"
    assert decision.context_id == "exec-001"
    assert decision.status == "PENDING"
    assert decision.confidence == 0.8


def test_autonomy_engine_failure_execution():

    engine = AutonomyEngine()

    decision = engine.evaluate_execution(
        execution_id="exec-002",
        result="Execution failed due to timeout",
        success=False,
        metrics={
            "latency": 2.5
        },
    )

    assert decision.decision_id == "auto-exec-002"
    assert decision.context_id == "exec-002"
    assert decision.reason != ""
    assert decision.confidence == 0.7


def test_autonomy_engine_creates_adaptation_strategy():

    engine = AutonomyEngine()

    decision = engine.evaluate_execution(
        execution_id="exec-003",
        result="Performance degraded",
        success=False,
    )

    assert decision.strategy_id.startswith(
        "strategy-learning-"
    )


def test_autonomy_engine_without_metrics():

    engine = AutonomyEngine()

    decision = engine.evaluate_execution(
        execution_id="exec-004",
        result="Completed",
        success=True,
    )

    assert decision.decision_id == "auto-exec-004"
    assert decision.confidence == 0.8