from src.agents.runtime.agent_runtime import AgentRuntime
from src.agents.planning.goal import Goal


def test_runtime_creates_goal_from_reasoning():

    runtime = AgentRuntime()

    context = runtime.prepare(
        "Analyze customer sales performance"
    )

    assert context.reasoning is not None

    assert context.goal is not None

    assert isinstance(
        context.goal,
        Goal
    )



def test_runtime_creates_goal_driven_plan():

    runtime = AgentRuntime()

    context = runtime.prepare(
        "Analyze product performance"
    )

    assert context.plan is not None

    assert context.plan.objective == (
        "Analyze product performance"
    )

    assert len(
        context.plan.steps
    ) >= 3



def test_goal_information_reaches_plan_metadata():

    runtime = AgentRuntime()

    context = runtime.prepare(
        "Generate sales insights"
    )

    assert "goal" in (
        context.plan.metadata
    )

    assert "intent" in (
        context.plan.metadata
    )