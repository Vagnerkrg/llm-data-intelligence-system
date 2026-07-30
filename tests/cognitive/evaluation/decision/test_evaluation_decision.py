from src.cognitive.evaluation.intelligence.evaluation_interpretation import (
    EvaluationInterpretation,
)

from src.cognitive.evaluation.decision.evaluation_decision_engine import (
    EvaluationDecisionEngine,
)

from src.cognitive.evaluation.decision.evaluation_decision import (
    EvaluationDecision,
)


def test_evaluation_decision_creates_adaptation_decision():

    interpretation = EvaluationInterpretation(
        severity="high",
        requires_improvement=True,
        areas=[
            "reasoning"
        ],
    )


    engine = EvaluationDecisionEngine()


    decision = engine.decide(
        interpretation
    )


    assert isinstance(
        decision,
        EvaluationDecision
    )


    assert decision.action == "adapt"

    assert decision.priority == "high"

    assert decision.target == "reasoning"