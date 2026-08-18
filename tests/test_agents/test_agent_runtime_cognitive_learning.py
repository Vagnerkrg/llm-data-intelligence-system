from src.agents.runtime.agent_runtime import AgentRuntime


class FakeLearningResult:
    learning_experiences = ["experience"]
    learning_outcomes = ["outcome"]


class FakeLearningLoop:
    def run(
        self,
        evaluation_context,
        *,
        learning_signals=(),
        execution_history=(),
    ):
        return FakeLearningResult()


def test_agent_runtime_accepts_cognitive_learning_dependency():
    loop = FakeLearningLoop()

    runtime = AgentRuntime(
        cognitive_learning_loop=loop
    )

    assert runtime.cognitive_learning_loop is loop


def test_run_cognitive_learning_persists_result():
    loop = FakeLearningLoop()

    runtime = AgentRuntime(
        cognitive_learning_loop=loop
    )

    context = runtime.create_context(
        "test question"
    )

    result = runtime.run_cognitive_learning(
        context
    )

    assert context.learning_loop_result is result
    assert context.learning_experiences == [
        "experience"
    ]
    assert context.learning_outcomes == [
        "outcome"
    ]


def test_execution_context_summary_exposes_learning_state():
    runtime = AgentRuntime(
        cognitive_learning_loop=FakeLearningLoop()
    )

    context = runtime.create_context(
        "test question"
    )

    runtime.run_cognitive_learning(
        context
    )

    summary = context.summary()

    assert summary["has_learning_experiences"]
    assert summary["learning_experiences_count"] == 1
    assert summary["has_learning_outcomes"]
    assert summary["learning_outcomes_count"] == 1
    assert summary["has_learning_loop_result"]