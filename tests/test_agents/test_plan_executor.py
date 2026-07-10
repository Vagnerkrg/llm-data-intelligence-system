from src.agents.planning.plan_executor import PlanExecutor
from src.agents.planning.execution_plan import ExecutionPlan
from src.agents.planning.plan_step import PlanStep
from src.agents.runtime.execution_context import ExecutionContext


def create_test_context():

    plan = ExecutionPlan(
        objective="Test execution plan"
    )


    plan.add_step(
        PlanStep(
            step_id=1,
            action="route_request",
            description="Route request"
        )
    )


    plan.add_step(
        PlanStep(
            step_id=2,
            action="generate_response",
            description="Generate response"
        )
    )


    context = ExecutionContext(
        question="Test question"
    )


    context.set_plan(
        plan
    )


    return context



def test_plan_executor_executes_plan():

    context = create_test_context()


    executor = PlanExecutor()


    result = executor.execute(
        context
    )


    assert result.status == "completed"



def test_plan_executor_completes_steps():

    context = create_test_context()


    executor = PlanExecutor()


    executor.execute(
        context
    )


    for step in context.plan.steps:

        assert step.status == "completed"



def test_plan_executor_adds_results():

    context = create_test_context()


    executor = PlanExecutor()


    executor.execute(
        context
    )


    assert len(
        context.results
    ) > 0