from src.agents.decision.decision_trace import DecisionTrace
from src.agents.decision.decision_reason import DecisionReason
from src.agents.decision.decision_alternative import DecisionAlternative


def test_decision_trace_creation():

    trace = DecisionTrace(
        decision_id="decision-001"
    )

    assert trace.decision_id == "decision-001"
    assert trace.reasons == []
    assert trace.alternatives == []
    assert trace.has_selected_alternative() is False


def test_add_reason_to_trace():

    trace = DecisionTrace(
        decision_id="decision-001"
    )

    reason = DecisionReason(
        justification="Higher expected performance",
        confidence=0.9
    )

    trace.add_reason(reason)

    assert len(trace.reasons) == 1
    assert trace.reasons[0].justification == "Higher expected performance"


def test_add_alternative_to_trace():

    trace = DecisionTrace(
        decision_id="decision-001"
    )

    alternative = DecisionAlternative(
        name="Strategy A",
        description="Execute strategy A",
        expected_outcome="Better performance"
    )

    trace.add_alternative(alternative)

    assert len(trace.alternatives) == 1
    assert trace.alternatives[0].name == "Strategy A"


def test_select_alternative():

    trace = DecisionTrace(
        decision_id="decision-001"
    )

    trace.select_alternative(
        "Strategy A"
    )

    assert trace.selected_alternative_id == "Strategy A"
    assert trace.has_selected_alternative() is True


def test_get_selected_alternative():

    trace = DecisionTrace(
        decision_id="decision-001"
    )

    alternative = DecisionAlternative(
        name="Strategy A",
        description="Execute strategy A",
        expected_outcome="Better performance"
    )

    trace.add_alternative(alternative)

    trace.select_alternative(
        "Strategy A"
    )

    result = trace.get_selected_alternative()

    assert result is not None
    assert result.name == "Strategy A"


def test_get_selected_alternative_returns_none():

    trace = DecisionTrace(
        decision_id="decision-001"
    )

    result = trace.get_selected_alternative()

    assert result is None