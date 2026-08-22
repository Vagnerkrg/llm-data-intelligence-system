from datetime import datetime

from src.cognitive.evaluation.feedback_loop.integration.learning_memory_adapter import (
    LearningMemoryAdapter,
)

from src.cognitive.evaluation.feedback_loop.models.learning_feedback import (
    LearningFeedback,
)


def test_store_feedback_in_memory():

    adapter = LearningMemoryAdapter()

    feedback = LearningFeedback(
        feedback_id="fb-memory-001",
        source="evaluation",
        signal="quality_issue",
        impact="high",
        created_at=datetime.now(),
    )

    result = adapter.store_feedback(feedback)

    assert result is True

    stored = adapter.retrieve_feedback("fb-memory-001")

    assert stored.feedback_id == "fb-memory-001"
