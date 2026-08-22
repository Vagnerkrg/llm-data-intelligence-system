from src.cognitive.learning.runtime.learning_execution_context import (
    LearningExecutionContext,
)


def test_learning_execution_context_creation():

    context = LearningExecutionContext(execution_id="exec-001")

    assert context.execution_id == "exec-001"
    assert context.learned is False


def test_learning_execution_context_mark_learning():

    context = LearningExecutionContext(execution_id="exec-002")

    context.mark_learned("knowledge-001")

    assert context.learned is True
    assert context.knowledge_id == "knowledge-001"


def test_learning_execution_context_feedback():

    context = LearningExecutionContext(execution_id="exec-003")

    context.add_feedback({"type": "performance"})

    assert context.feedback["type"] == "performance"
