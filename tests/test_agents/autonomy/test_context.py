from src.agents.autonomy import AutonomyContext


def test_autonomy_context_creation():

    context = AutonomyContext(
        context_id="ctx-001",
        execution_id="exec-001",
        goal="Analyze customer data"
    )

    assert context.context_id == "ctx-001"
    assert context.execution_id == "exec-001"
    assert context.goal == "Analyze customer data"


def test_autonomy_context_defaults():

    context = AutonomyContext(
        context_id="ctx-002",
        execution_id="exec-002"
    )

    assert context.execution_history == []
    assert context.metrics == {}
    assert context.feedback == []
    assert context.metadata == {}