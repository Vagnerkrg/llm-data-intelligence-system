from src.agents.runtime.execution_context import (
    ExecutionContext
)


def test_execution_context_creation():

    context = ExecutionContext(
        question="test question"
    )


    assert context.question == (
        "test question"
    )

    assert context.status == (
        "initialized"
    )



def test_execution_context_attach_plan():

    context = ExecutionContext(
        question="test"
    )


    class FakePlan:

        def next_step(self):
            return None


    plan = FakePlan()


    context.set_plan(
        plan
    )


    assert context.plan == plan

    assert context.status == (
        "planned"
    )



def test_execution_context_attach_memory_context():

    context = ExecutionContext(
        question="memory test"
    )


    memory_context = {

        "memories": [
            "previous interaction"
        ]

    }


    context.set_memory_context(
        memory_context
    )


    assert context.memory_context == (
        memory_context
    )


    summary = context.summary()


    assert summary["has_memory_context"] is True