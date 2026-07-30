from datetime import datetime

from src.cognitive.evaluation.feedback_loop.runtime.runtime_feedback_context import (
    RuntimeFeedbackContext,
)


def test_runtime_feedback_context_creation():

    context = RuntimeFeedbackContext(
        execution_id="exec-001",
        agent_id="agent-001",
        capability="reasoning",
        signal="low_quality",
        impact="high",
        created_at=datetime.now(),
    )

    assert context.execution_id == "exec-001"
    assert context.capability == "reasoning"