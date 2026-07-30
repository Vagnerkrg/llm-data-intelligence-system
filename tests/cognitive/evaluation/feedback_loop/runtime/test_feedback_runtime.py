from datetime import datetime

from src.cognitive.evaluation.feedback_loop.runtime.feedback_runtime import (
    FeedbackRuntime,
)

from src.cognitive.evaluation.feedback_loop.runtime.runtime_feedback_context import (
    RuntimeFeedbackContext,
)

from src.cognitive.evaluation.feedback_loop.models.feedback_cycle import (
    FeedbackCycleStatus,
)


def test_feedback_runtime_execution():

    runtime = FeedbackRuntime()

    context = RuntimeFeedbackContext(
        execution_id="exec-001",
        agent_id="agent-001",
        capability="reasoning",
        signal="quality_issue",
        impact="high",
        created_at=datetime.now(),
    )

    cycle = runtime.execute_feedback_cycle(
        context
    )

    assert cycle.evaluation_id == "exec-001"
    assert cycle.status == FeedbackCycleStatus.CREATED