from src.agents.runtime.agent_runtime import AgentRuntime
from src.agents.planning.dynamic_execution_planner import DynamicExecutionPlanner



def test_runtime_multi_tool_planning():

    planner = DynamicExecutionPlanner()


    runtime = AgentRuntime(
        planner=planner
    )


    context = runtime.prepare(
        "Analise os dados e gere um relatório"
    )


    assert context.plan is not None



def test_runtime_multi_tool_planning_contains_multiple_steps():

    planner = DynamicExecutionPlanner()


    runtime = AgentRuntime(
        planner=planner
    )


    context = runtime.prepare(
        "Leia o documento e faça uma análise"
    )


    assert len(
        context.plan.steps
    ) >= 3



def test_runtime_multi_tool_planning_supports_different_requests():

    planner = DynamicExecutionPlanner()


    runtime = AgentRuntime(
        planner=planner
    )


    analytics_context = runtime.prepare(
        "Analise vendas"
    )


    document_context = runtime.prepare(
        "Explique documento"
    )


    assert analytics_context.plan is not None

    assert document_context.plan is not None