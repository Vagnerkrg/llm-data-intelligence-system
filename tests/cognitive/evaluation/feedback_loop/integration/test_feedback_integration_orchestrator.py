from datetime import datetime

from src.cognitive.evaluation.feedback_loop.integration.feedback_integration_orchestrator import (
    FeedbackIntegrationOrchestrator,
)

from src.cognitive.evaluation.feedback_loop.models.learning_feedback import (
    LearningFeedback,
)

from src.cognitive.evaluation.feedback_loop.models.improvement_feedback import (
    ImprovementFeedback,
)


def test_feedback_integration_flow():

    orchestrator = FeedbackIntegrationOrchestrator()

    feedback = LearningFeedback(
        feedback_id="fb-flow-001",
        source="evaluation",
        signal="planner_failure",
        impact="high",
        created_at=datetime.now(),
    )

    result = orchestrator.integrate_feedback(feedback)

    assert result is True


def test_improvement_integration_flow():

    orchestrator = FeedbackIntegrationOrchestrator()

    improvement = ImprovementFeedback(
        improvement_id="imp-flow-001",
        feedback_id="fb-flow-001",
        action="optimize_planning",
        expected_result="better planning",
        created_at=datetime.now(),
    )

    result = orchestrator.integrate_improvement(improvement)

    assert result is True
