from src.agents.decision.decision_reason import DecisionReason


def test_should_create_decision_reason():
    reason = DecisionReason(
        justification="Selected analytical strategy",
        confidence=0.95,
    )

    assert reason.justification == "Selected analytical strategy"
    assert reason.confidence == 0.95


def test_should_create_empty_evidence_by_default():
    reason = DecisionReason(
        justification="Strategy selected",
        confidence=0.80,
    )

    assert reason.evidence == []


def test_should_store_evidence_items():
    reason = DecisionReason(
        justification="Best execution approach",
        confidence=0.90,
        evidence=[
            "high_accuracy",
            "low_cost",
        ],
    )

    assert len(reason.evidence) == 2
    assert "high_accuracy" in reason.evidence
    assert "low_cost" in reason.evidence


def test_should_preserve_confidence_value():
    reason = DecisionReason(
        justification="Validated strategy",
        confidence=0.75,
    )

    assert reason.confidence == 0.75


def test_should_allow_zero_confidence():
    reason = DecisionReason(
        justification="Unknown strategy",
        confidence=0.0,
    )

    assert reason.confidence == 0.0


def test_should_support_full_reason_definition():
    reason = DecisionReason(
        justification="Selected based on historical performance",
        confidence=0.98,
        evidence=[
            "previous_success",
            "execution_efficiency",
        ],
    )

    assert reason.justification.startswith("Selected")
    assert reason.confidence == 0.98
    assert len(reason.evidence) == 2