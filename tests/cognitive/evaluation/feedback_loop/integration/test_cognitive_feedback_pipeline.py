from datetime import datetime


from src.cognitive.evaluation.feedback_loop.integration.cognitive_feedback_pipeline import (
    CognitiveFeedbackPipeline,
)


from src.cognitive.evaluation.feedback_loop.runtime.runtime_feedback_context import (
    RuntimeFeedbackContext,
)


def test_cognitive_feedback_pipeline_execution():

    pipeline = CognitiveFeedbackPipeline()

    context = RuntimeFeedbackContext(
        execution_id="exec-100",
        agent_id="agent-001",
        capability="reasoning",
        signal="quality_degradation",
        impact="high",
        created_at=datetime.now(),
    )

    result = pipeline.execute(context)

    assert "feedback_cycle" in result
    assert "learning_feedback" in result


def test_pipeline_preserves_execution_identity():

    pipeline = CognitiveFeedbackPipeline()

    context = RuntimeFeedbackContext(
        execution_id="exec-200",
        agent_id="agent-002",
        capability="planning",
        signal="planning_failure",
        impact="medium",
        created_at=datetime.now(),
    )

    result = pipeline.execute(context)

    cycle = result["feedback_cycle"]

    assert cycle.evaluation_id == "exec-200"
