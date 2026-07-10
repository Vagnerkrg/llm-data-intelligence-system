from src.agents.planning.dynamic_execution_planner import DynamicExecutionPlanner


def test_dynamic_planner_uses_strategy_for_analytics_request():

    planner = DynamicExecutionPlanner()

    plan = planner.create_plan(
        "Analise os dados de vendas e encontre padrões"
    )

    actions = [
        step.action
        for step in plan.steps
    ]

    assert "route_request" in actions
    assert "execute_tool" in actions
    assert "generate_response" in actions



def test_dynamic_planner_uses_strategy_for_document_request():

    planner = DynamicExecutionPlanner()

    plan = planner.create_plan(
        "Explique o conteúdo deste documento"
    )

    actions = [
        step.action
        for step in plan.steps
    ]

    assert "route_request" in actions
    assert "execute_tool" in actions
    assert "generate_response" in actions



def test_dynamic_planner_returns_valid_execution_plan():

    planner = DynamicExecutionPlanner()

    plan = planner.create_plan(
        "Faça uma análise estatística dos dados"
    )

    assert plan is not None
    assert len(plan.steps) > 0

    for step in plan.steps:
        assert step.status == "pending"