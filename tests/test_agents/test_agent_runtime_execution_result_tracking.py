from src.agents.runtime.agent_runtime import AgentRuntime
from src.agents.planning.dynamic_execution_planner import DynamicExecutionPlanner


def test_agent_runtime_execution_result_tracking():

    planner = DynamicExecutionPlanner()

    runtime = AgentRuntime(
        planner=planner
    )

    context = runtime.execute(
        "Analise os dados de vendas"
    )

    assert context is not None



def test_agent_runtime_execution_result_tracking_has_plan():

    planner = DynamicExecutionPlanner()

    runtime = AgentRuntime(
        planner=planner
    )

    context = runtime.execute(
        "Analise os dados financeiros"
    )

    assert context.plan is not None



def test_agent_runtime_execution_result_tracking_has_execution_state():

    planner = DynamicExecutionPlanner()

    runtime = AgentRuntime(
        planner=planner
    )

    context = runtime.execute(
        "Explique este documento"
    )

    assert hasattr(
        context,
        "plan"
    )

    assert context.current_step is not None