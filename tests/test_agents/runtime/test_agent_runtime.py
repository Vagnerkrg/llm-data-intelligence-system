from src.agents.runtime.agent_runtime import AgentRuntime



def test_agent_runtime_creates_context():

    runtime = AgentRuntime()


    context = runtime.prepare(
        "How many products exist?"
    )


    assert context.question == (
        "How many products exist?"
    )


    assert context.plan is not None


    assert len(
        context.plan.steps
    ) == 3



def test_agent_runtime_initial_step():

    runtime = AgentRuntime()


    context = runtime.prepare(
        "Analyze products"
    )


    assert context.current_step is not None


    assert context.current_step.action == (
        "route_request"
    )