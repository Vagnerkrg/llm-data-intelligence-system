from datetime import datetime

from src.cognitive.evaluation.feedback_loop.integration.cognitive_improvement_adapter import (
    CognitiveImprovementAdapter,
)

from src.cognitive.evaluation.feedback_loop.models.improvement_feedback import (
    ImprovementFeedback,
)


def test_send_improvement():

    adapter = CognitiveImprovementAdapter()

    improvement = ImprovementFeedback(
        improvement_id="imp-001",
        feedback_id="fb-001",
        action="improve_reasoning",
        expected_result="better decisions",
        created_at=datetime.now(),
    )

    result = adapter.send_improvement(
        improvement
    )

    assert result is True

    assert len(
        adapter.get_pending_improvements()
    ) == 1