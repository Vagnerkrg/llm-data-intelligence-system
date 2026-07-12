from src.agents.memory.execution_feedback_memory import (
    ExecutionFeedbackMemory,
)

from src.agents.execution.execution_feedback import (
    ExecutionFeedback,
)



def create_feedback(
    success=True,
    message="Execution completed",
):
    return ExecutionFeedback(
        success=success,
        message=message,
    )



def test_memory_starts_empty():
    """
    Validate initial state.
    """

    memory = ExecutionFeedbackMemory()

    assert memory.count() == 0

    assert memory.all() == []



def test_memory_add_feedback():
    """
    Validate feedback storage.
    """

    memory = ExecutionFeedbackMemory()

    feedback = create_feedback()

    memory.add(
        feedback
    )

    assert memory.count() == 1

    assert (
        memory.last()
        == feedback
    )



def test_memory_preserves_history():
    """
    Validate multiple feedback storage.
    """

    memory = ExecutionFeedbackMemory()

    first = create_feedback(
        True,
        "Success",
    )

    second = create_feedback(
        False,
        "Failure",
    )


    memory.add(first)

    memory.add(second)


    history = memory.all()


    assert len(history) == 2

    assert history[0] == first

    assert history[1] == second



def test_memory_clear():
    """
    Validate memory reset.
    """

    memory = ExecutionFeedbackMemory()

    memory.add(
        create_feedback()
    )

    memory.clear()


    assert memory.count() == 0

    assert memory.last() is None