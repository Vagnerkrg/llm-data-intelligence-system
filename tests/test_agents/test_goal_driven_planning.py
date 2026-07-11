from src.agents.planning.dynamic_execution_planner import (
    DynamicExecutionPlanner
)


def test_dynamic_planner_creates_goal():

    planner = DynamicExecutionPlanner()


    plan = planner.create_plan(
        "Analyze customer sales data"
    )


    assert plan.goal is not None

    assert (
        plan.goal.objective
        ==
        "Analyze customer sales data"
    )


def test_goal_contains_intent():

    planner = DynamicExecutionPlanner()


    plan = planner.create_plan(
        "Explique este documento"
    )


    assert (
        plan.goal.intent
        ==
        "document"
    )


def test_goal_driven_plan_keeps_execution_flow():

    planner = DynamicExecutionPlanner()


    plan = planner.create_plan(
        "Analise os dados"
    )


    actions = [
        step.action
        for step in plan.steps
    ]


    assert "route_request" in actions

    assert "execute_tool" in actions

    assert "generate_response" in actions