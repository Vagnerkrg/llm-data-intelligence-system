from src.agents.runtime.agent_runtime import AgentRuntime
from src.agents.reasoning.reasoning_result import ReasoningResult



def test_agent_runtime_reasoning_influences_planning():

    runtime = AgentRuntime()


    context = runtime.prepare(
        "Analyze product sales performance"
    )


    assert context.reasoning is not None


    assert isinstance(
        context.reasoning,
        ReasoningResult
    )


    assert context.plan is not None


    assert len(
        context.plan.steps
    ) == 3


    assert (
        context.plan.objective
        ==
        "Analyze product sales performance"
    )