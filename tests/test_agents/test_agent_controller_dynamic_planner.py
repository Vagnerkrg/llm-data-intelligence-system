from src.agents.controller.agent_controller import AgentController
from src.agents.planning.dynamic_execution_planner import DynamicExecutionPlanner


def test_agent_controller_uses_dynamic_planner():

    planner = DynamicExecutionPlanner()

    controller = AgentController(
        planner=planner
    )

    result = controller.run(
        "Analise os dados de vendas e encontre padrões"
    )

    assert result is not None



def test_agent_controller_dynamic_planner_creates_plan():

    planner = DynamicExecutionPlanner()

    controller = AgentController(
        planner=planner
    )

    plan = controller.create_plan(
        "Faça uma análise estatística dos dados"
    )

    assert plan is not None
    assert len(plan.steps) == 3



def test_agent_controller_dynamic_plan_contains_expected_steps():

    planner = DynamicExecutionPlanner()

    controller = AgentController(
        planner=planner
    )

    plan = controller.create_plan(
        "Explique o conteúdo deste documento"
    )

    actions = [
        step.action
        for step in plan.steps
    ]

    assert "route_request" in actions
    assert "execute_tool" in actions
    assert "generate_response" in actions