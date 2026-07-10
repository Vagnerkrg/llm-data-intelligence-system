from src.agents.controller.agent_controller import AgentController
from src.agents.runtime.agent_runtime import AgentRuntime
from src.agents.planning.dynamic_execution_planner import DynamicExecutionPlanner



def test_agent_controller_runtime_execution_flow():

    planner = DynamicExecutionPlanner()


    runtime = AgentRuntime(
        planner=planner
    )


    controller = AgentController(
        runtime=runtime
    )


    context = controller.handle_request(
        "Analise os dados de vendas"
    )


    assert context is not None



def test_agent_controller_runtime_execution_flow_contains_context():

    planner = DynamicExecutionPlanner()


    runtime = AgentRuntime(
        planner=planner
    )


    controller = AgentController(
        runtime=runtime
    )


    context = controller.handle_request(
        "Explique este documento"
    )


    assert hasattr(
        context,
        "question"
    )



def test_agent_controller_runtime_execution_flow_contains_plan():

    planner = DynamicExecutionPlanner()


    runtime = AgentRuntime(
        planner=planner
    )


    controller = AgentController(
        runtime=runtime
    )


    context = controller.handle_request(
        "Faça uma análise estatística"
    )


    assert context.plan is not None