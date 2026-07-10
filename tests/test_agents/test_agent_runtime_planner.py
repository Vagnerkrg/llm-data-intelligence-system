from src.agents.runtime.agent_runtime import AgentRuntime
from src.agents.planning.execution_plan import ExecutionPlan



def test_agent_runtime_prepare_creates_execution_plan():

    runtime = AgentRuntime()


    context = runtime.prepare(
        "Analyze sales data"
    )


    assert context.plan is not None


    assert isinstance(
        context.plan,
        ExecutionPlan
    )



def test_agent_runtime_plan_contains_expected_steps():

    runtime = AgentRuntime()


    context = runtime.prepare(
        "Analyze customer data"
    )


    actions = [
        step.action
        for step in context.plan.steps
    ]


    assert actions == [
        "route_request",
        "execute_tool",
        "generate_response"
    ]



def test_agent_runtime_starts_with_first_step():

    runtime = AgentRuntime()


    context = runtime.prepare(
        "Test workflow"
    )


    assert context.current_step is not None


    assert (
        context.current_step.action
        == "route_request"
    )