from src.agents.controller.agent_controller import AgentController
from src.agents.planning.dynamic_execution_planner import (
    DynamicExecutionPlanner
)


def test_agent_controller_dynamic_planner_creates_plan():

    planner = DynamicExecutionPlanner()

    controller = AgentController(
        planner=planner
    )


    plan = controller.create_plan(
        "Faça uma análise estatística dos dados"
    )


    assert plan is not None

    assert len(plan.steps) == 4


    actions = [
        step.action
        for step in plan.steps
    ]


    assert "route_request" in actions

    assert "execute_tool" in actions

    assert "generate_insights" in actions

    assert "generate_response" in actions



def test_agent_controller_dynamic_planner_keeps_goal_information():

    planner = DynamicExecutionPlanner()

    controller = AgentController(
        planner=planner
    )


    plan = controller.create_plan(
        "Analise os dados de vendas"
    )


    assert plan.goal is not None

    assert plan.goal.objective == (
        "Analise os dados de vendas"
    )


    assert plan.goal.intent is not None



def test_agent_controller_dynamic_planner_document_flow():

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

    assert "summarize_content" in actions

    assert "generate_response" in actions