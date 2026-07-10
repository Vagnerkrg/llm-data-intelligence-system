from src.agents.runtime.agent_runtime import AgentRuntime



def test_runtime_executes_generated_plan():

    runtime = AgentRuntime()


    context = runtime.execute(
        "Test execution workflow"
    )


    assert context is not None

    assert context.plan is not None



def test_runtime_returns_completed_context():

    runtime = AgentRuntime()


    context = runtime.execute(
        "Test execution workflow"
    )


    assert context.status == "completed"



def test_runtime_plan_steps_are_completed():

    runtime = AgentRuntime()


    context = runtime.execute(
        "Test execution workflow"
    )


    for step in context.plan.steps:

        assert step.status == "completed"