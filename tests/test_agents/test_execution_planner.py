from src.agents.planning.execution_planner import ExecutionPlanner
from src.agents.planning.execution_plan import ExecutionPlan



def test_execution_planner_creates_plan():

    planner = ExecutionPlanner()

    question = "Analyze sales data"


    plan = planner.create_plan(
        question
    )


    assert isinstance(
        plan,
        ExecutionPlan
    )


    assert plan.objective == question



def test_execution_planner_creates_expected_steps():

    planner = ExecutionPlanner()


    plan = planner.create_plan(
        "Analyze customer data"
    )


    assert len(
        plan.steps
    ) == 3



    actions = [
        step.action
        for step in plan.steps
    ]


    assert actions == [
        "route_request",
        "execute_tool",
        "generate_response"
    ]



def test_execution_planner_creates_pending_steps():

    planner = ExecutionPlanner()


    plan = planner.create_plan(
        "Test execution flow"
    )


    for step in plan.steps:

        assert step.status == "pending"