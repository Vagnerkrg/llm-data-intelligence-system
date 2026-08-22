import pytest

from src.agents.autonomous_evolution.domain import EvolutionAction


def test_evolution_action_creation() -> None:
    action = EvolutionAction(
        action_type="update_behavior",
        target="agent",
        parameters={"temperature": 0.2},
        reason="Improve deterministic behavior.",
    )

    assert action.action_type == "update_behavior"
    assert action.target == "agent"
    assert action.parameters["temperature"] == 0.2
    assert action.reason == "Improve deterministic behavior."


def test_evolution_action_serialization() -> None:
    action = EvolutionAction(
        action_type="update_prompt",
        target="reasoning",
    )

    result = action.to_dict()

    assert result["action_type"] == "update_prompt"
    assert result["target"] == "reasoning"
    assert result["parameters"] == {}
    assert result["metadata"] == {}


@pytest.mark.parametrize(
    "field",
    ["action_type", "target"],
)
def test_evolution_action_rejects_empty_required_fields(field: str) -> None:
    kwargs = {
        "action_type": "valid_action",
        "target": "valid_target",
    }
    kwargs[field] = ""

    with pytest.raises(ValueError):
        EvolutionAction(**kwargs)
