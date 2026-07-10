from src.agents.runtime.agent_runtime import AgentRuntime
from src.agents.planning.dynamic_execution_planner import DynamicExecutionPlanner



def test_agent_runtime_context_tracking():

    planner = DynamicExecutionPlanner()


    runtime = AgentRuntime(
        planner=planner
    )


    context = runtime.prepare(
        "Analise os dados"
    )


    assert context.question == (
        "Analise os dados"
    )



def test_agent_runtime_context_tracking_has_execution_plan():

    planner = DynamicExecutionPlanner()


    runtime = AgentRuntime(
        planner=planner
    )


    context = runtime.prepare(
        "Explique o documento"
    )


    assert context.plan is not None



def test_agent_runtime_context_tracking_updates_step():

    planner = DynamicExecutionPlanner()


    runtime = AgentRuntime(
        planner=planner
    )


    context = runtime.prepare(
        "Faça análise estatística"
    )


    assert context.current_step is not None