from src.agents.runtime.agent_runtime import AgentRuntime



def test_agent_runtime_executes_plan():

    runtime = AgentRuntime()


    context = runtime.execute(
        "Quantos clientes existem?"
    )


    assert context.status == "completed"


    assert context.plan is not None


    assert len(
        context.plan.steps
    ) == 3



def test_agent_runtime_stores_execution_results():

    runtime = AgentRuntime()


    context = runtime.execute(
        "Analise os dados dos clientes."
    )


    assert len(
        context.results
    ) >= 1


    assert context.status == "completed"