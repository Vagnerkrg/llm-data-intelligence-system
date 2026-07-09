from src.agents.runtime.execution_context import ExecutionContext
from src.agents.planning.execution_plan import ExecutionPlan



def test_execution_context_creation():

    context = ExecutionContext(
        question="How many products exist?"
    )


    assert context.question == (
        "How many products exist?"
    )

    assert context.status == "initialized"

    assert context.plan is None



def test_execution_context_attach_plan():

    context = ExecutionContext(
        question="Analyze dataset"
    )


    plan = ExecutionPlan(
        objective="Analyze dataset"
    )


    context.set_plan(
        plan
    )


    assert context.plan == plan

    assert context.status == "planned"