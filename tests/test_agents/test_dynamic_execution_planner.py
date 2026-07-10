from src.agents.planning.execution_planner import ExecutionPlanner


def test_planner_creates_analytics_plan():

    planner = ExecutionPlanner()


    plan = planner.create_plan(
        "Quantos produtos existem no dataset?"
    )


    assert plan is not None

    assert len(plan.steps) > 0

    actions = [
        step.action
        for step in plan.steps
    ]


    assert "execute_tool" in actions



def test_planner_creates_document_plan():

    planner = ExecutionPlanner()


    plan = planner.create_plan(
        "Explique o conteúdo deste documento"
    )


    assert plan is not None

    assert len(plan.steps) > 0

    actions = [
        step.action
        for step in plan.steps
    ]


    assert "execute_tool" in actions



def test_planner_creates_response_step():

    planner = ExecutionPlanner()


    plan = planner.create_plan(
        "Faça uma análise dos dados"
    )


    actions = [
        step.action
        for step in plan.steps
    ]


    assert "generate_response" in actions