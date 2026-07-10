from src.agents.controller.agent_controller import AgentController
from src.agents.runtime.agent_runtime import AgentRuntime
from src.agents.planning.dynamic_execution_planner import DynamicExecutionPlanner


def test_agent_controller_runtime_result_handling():

    planner = DynamicExecutionPlanner()

    runtime = AgentRuntime(
        planner=planner
    )

    controller = AgentController(
        runtime=runtime
    )

    result = controller.handle_request(
        "Analise os dados de clientes"
    )

    assert result is not None



def test_agent_controller_runtime_result_contains_context():

    planner = DynamicExecutionPlanner()

    runtime = AgentRuntime(
        planner=planner
    )

    controller = AgentController(
        runtime=runtime
    )

    result = controller.handle_request(
        "Faça uma análise estatística"
    )

    assert result.plan is not None



def test_agent_controller_runtime_result_preserves_execution_flow():

    planner = DynamicExecutionPlanner()

    runtime = AgentRuntime(
        planner=planner
    )

    controller = AgentController(
        runtime=runtime
    )

    result = controller.handle_request(
        "Explique um documento"
    )

    assert result.current_step is not None