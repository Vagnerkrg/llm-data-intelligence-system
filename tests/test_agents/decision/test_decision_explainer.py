from src.agents.decision.decision_explainer import DecisionExplainer
from src.agents.decision.decision import Decision
from src.agents.decision.decision_status import DecisionStatus
from src.agents.decision.decision_trace import DecisionTrace


def test_decision_explainer_creates_explanation():

    decision = Decision(
        decision_id="decision_001",
        status=DecisionStatus.SELECTED,
        strategy="strategy_b",
        trace=DecisionTrace(
            decision_id="decision_001",
            selected_alternative_id="strategy_b"
        )
    )

    explainer = DecisionExplainer()

    explanation = explainer.explain(
        decision,
        confidence=0.9
    )

    assert isinstance(explanation, str)

    assert "strategy_b" in explanation
    assert "0.9" in explanation