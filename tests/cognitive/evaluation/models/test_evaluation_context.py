from src.cognitive.evaluation.models.evaluation_context import EvaluationContext


def test_evaluation_context_creation():

    context = EvaluationContext(
        agent_id="agent-001",
        execution_id="exec-001",
        input_data={"request": "analyze data"},
        output_data={"result": "ok"}
    )

    assert context.agent_id == "agent-001"
    assert context.execution_id == "exec-001"
    assert context.input_data["request"] == "analyze data"
    assert context.output_data["result"] == "ok"


def test_evaluation_context_metadata():

    context = EvaluationContext(
        agent_id="agent-002"
    )

    context.add_metadata(
        "source",
        "runtime"
    )

    assert context.get_metadata("source") == "runtime"


def test_evaluation_context_default_metadata():

    context = EvaluationContext(
        agent_id="agent-003"
    )

    assert context.metadata == {}