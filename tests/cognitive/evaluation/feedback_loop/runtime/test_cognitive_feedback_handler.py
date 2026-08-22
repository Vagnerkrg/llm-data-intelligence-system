from datetime import datetime

from src.cognitive.evaluation.feedback_loop.runtime.cognitive_feedback_handler import (
    CognitiveFeedbackHandler,
)

from src.cognitive.evaluation.feedback_loop.runtime.runtime_feedback_context import (
    RuntimeFeedbackContext,
)


def test_handler_creates_feedback():

    handler = CognitiveFeedbackHandler()

    context = RuntimeFeedbackContext(
        execution_id="exec-001",
        agent_id="agent-001",
        capability="planning",
        signal="planning_failure",
        impact="high",
        created_at=datetime.now(),
    )

    feedback = handler.handle(context)

    assert feedback.feedback_id == "exec-001"
    assert feedback.signal == "planning_failure"
