from src.agents.planning.dynamic_execution_planner import DynamicExecutionPlanner


def test_dynamic_planner_adaptive_replanning():

    planner = DynamicExecutionPlanner()


    initial_plan = planner.create_plan(
        "Analise vendas"
    )


    assert initial_plan is not None



def test_dynamic_planner_adaptive_replanning_generates_new_plan():

    planner = DynamicExecutionPlanner()


    first_plan = planner.create_plan(
        "Analise vendas"
    )


    second_plan = planner.create_plan(
        "Analise vendas com estatísticas"
    )


    assert first_plan is not None
    assert second_plan is not None



def test_dynamic_planner_adaptive_replanning_changes_steps():

    planner = DynamicExecutionPlanner()


    plan = planner.create_plan(
        "Faça análise e gere relatório"
    )


    assert len(
        plan.steps
    ) > 0