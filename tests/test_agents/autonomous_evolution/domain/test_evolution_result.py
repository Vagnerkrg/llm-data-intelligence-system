from src.agents.autonomous_evolution.domain import (
    EvolutionAction,
    EvolutionResult,
    EvolutionStatus,
)


def test_evolution_result_creation() -> None:
    result = EvolutionResult(
        status=EvolutionStatus.COMPLETED,
        success=True,
        message="Evolution completed successfully.",
    )

    assert result.status is EvolutionStatus.COMPLETED
    assert result.success is True
    assert result.message == "Evolution completed successfully."


def test_evolution_result_accepts_action() -> None:
    action = EvolutionAction(
        action_type="adapt_behavior",
        target="agent",
    )

    result = EvolutionResult(
        status=EvolutionStatus.APPLIED,
        success=True,
        action=action,
    )

    assert result.action is action


def test_evolution_result_serialization() -> None:
    result = EvolutionResult(
        status=EvolutionStatus.COMPLETED,
        success=True,
        message="Completed.",
        metadata={"execution_id": "exec-001"},
    )

    data = result.to_dict()

    assert data["status"] == "completed"
    assert data["success"] is True
    assert data["message"] == "Completed."
    assert data["metadata"]["execution_id"] == "exec-001"
