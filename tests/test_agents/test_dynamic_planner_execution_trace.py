from src.agents.planning.dynamic_execution_planner import DynamicExecutionPlanner



def test_dynamic_planner_execution_trace():

    planner = DynamicExecutionPlanner()


    plan = planner.create_plan(
        "Analise os dados de vendas"
    )


    assert plan is not None



def test_dynamic_planner_execution_trace_contains_steps():

    planner = DynamicExecutionPlanner()


    plan = planner.create_plan(
        "Explique este documento"
    )


    assert len(
        plan.steps
    ) > 0



def test_dynamic_planner_execution_trace_steps_have_actions():

    planner = DynamicExecutionPlanner()


    plan = planner.create_plan(
        "Faça uma análise estatística"
    )


    for step in plan.steps:

        assert step.action is not None