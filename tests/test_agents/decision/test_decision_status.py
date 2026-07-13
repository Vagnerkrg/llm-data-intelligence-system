from src.agents.decision.decision_status import DecisionStatus


def test_should_define_all_expected_statuses():
    expected = {
    "pending",
    "analyzing",
    "selected",
    "committed",
    "evaluated",
    "completed",
}

    actual = {status.value for status in DecisionStatus}

    assert actual == expected


def test_should_inherit_from_str():
    assert isinstance(DecisionStatus.PENDING.value, str)


def test_should_keep_pending_as_initial_status():
    assert DecisionStatus.PENDING.value == "pending"


def test_should_keep_evaluated_as_final_status():
    assert DecisionStatus.EVALUATED.value == "evaluated"