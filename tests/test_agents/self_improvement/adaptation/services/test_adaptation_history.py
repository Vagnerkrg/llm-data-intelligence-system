from src.agents.self_improvement.adaptation.services.adaptation_history import (
    AdaptationHistory,
)

from src.agents.self_improvement.adaptation.domain.adaptation_result import (
    AdaptationResult,
)


def test_adaptation_history_records_result():

    history = AdaptationHistory()

    result = AdaptationResult(
        success=True,
        action=None,
        message="Adaptation completed.",
    )

    history.record(result)

    entries = history.get_all()

    assert len(entries) == 1
    assert entries[0] == result