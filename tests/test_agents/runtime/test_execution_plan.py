from src.agents.planning.execution_plan import ExecutionPlan
from src.agents.planning.plan_step import PlanStep



def test_execution_plan_add_step():

    plan = ExecutionPlan(
        objective="Analyze data"
    )


    step = PlanStep(

        step_id=1,

        action="execute_tool",

        description="Run analytics"

    )


    plan.add_step(
        step
    )


    assert len(
        plan.steps
    ) == 1



def test_execution_plan_next_step():

    plan = ExecutionPlan(
        objective="Test plan"
    )


    step = PlanStep(

        step_id=1,

        action="analysis",

        description="Execute analysis"

    )


    plan.add_step(
        step
    )


    next_step = plan.next_step()


    assert next_step == step



def test_execution_plan_completion():

    plan = ExecutionPlan(
        objective="Complete task"
    )


    step = PlanStep(

        step_id=1,

        action="test",

        description="Test execution"

    )


    plan.add_step(
        step
    )


    assert plan.is_completed() is False


    step.complete(
        "done"
    )


    assert plan.is_completed() is True