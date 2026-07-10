from src.agents.runtime.agent_runtime import AgentRuntime
from src.agents.planning.dynamic_execution_planner import DynamicExecutionPlanner


def test_runtime_agent_memory_integration():

    planner = DynamicExecutionPlanner()

    runtime = AgentRuntime(
        planner=planner
    )

    context = runtime.execute(
        "Analise histórico de vendas"
    )


    assert context is not None



def test_runtime_agent_memory_integration_preserves_context():

    planner = DynamicExecutionPlanner()

    runtime = AgentRuntime(
        planner=planner
    )


    context = runtime.execute(
        "Explique este relatório"
    )


    assert context.plan is not None



def test_runtime_agent_memory_integration_tracks_execution():

    planner = DynamicExecutionPlanner()

    runtime = AgentRuntime(
        planner=planner
    )


    context = runtime.execute(
        "Faça uma previsão"
    )


    assert context.current_step is not None