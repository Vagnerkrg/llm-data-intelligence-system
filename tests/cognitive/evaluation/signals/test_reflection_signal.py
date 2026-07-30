from src.cognitive.evaluation.signals.reflection_signal import ReflectionSignal


def test_reflection_signal_creation():

    signal = ReflectionSignal(
        execution_id="exec-001",
        observation="Tool failed",
        outcome="Retry required"
    )

    assert signal.execution_id == "exec-001"
    assert signal.outcome == "Retry required"


def test_reflection_signal_metadata():

    signal = ReflectionSignal(
        execution_id="exec-002",
        observation="Good execution",
        outcome="Success"
    )

    signal.add_metadata("agent", "planner")

    assert signal.metadata["agent"] == "planner"