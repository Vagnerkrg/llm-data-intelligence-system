from src.agents.autonomous_evolution.domain import EvolutionStatus


def test_evolution_status_contains_expected_states() -> None:
    assert EvolutionStatus.PENDING.value == "pending"
    assert EvolutionStatus.PROPOSED.value == "proposed"
    assert EvolutionStatus.APPROVED.value == "approved"
    assert EvolutionStatus.REJECTED.value == "rejected"
    assert EvolutionStatus.APPLIED.value == "applied"
    assert EvolutionStatus.COMPLETED.value == "completed"
    assert EvolutionStatus.FAILED.value == "failed"