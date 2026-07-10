from src.agents.controller.agent_controller import AgentController
from src.agents.runtime.agent_runtime import AgentRuntime
from src.agents.planning.dynamic_execution_planner import DynamicExecutionPlanner



def test_agent_controller_runtime_integration():

    planner = DynamicExecutionPlanner()


    runtime = AgentRuntime(
        planner=planner
    )


    controller = AgentController(
        runtime=runtime
    )


    result = controller.handle_request(
        "Analise os dados de vendas"
    )


    assert result is not None



def test_agent_controller_runtime_generates_dynamic_plan():

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


    assert context.plan is not None

    assert len(
        context.plan.steps
    ) > 0



def test_agent_controller_runtime_supports_multiple_intents():

    planner = DynamicExecutionPlanner()


    runtime = AgentRuntime(
        planner=planner
    )


    controller = AgentController(
        runtime=runtime
    )


    analytics_context = controller.handle_request(
        "Faça uma análise estatística dos dados"
    )


    document_context = controller.handle_request(
        "Resuma este documento"
    )


    assert analytics_context.plan is not None

    assert document_context.plan is not None