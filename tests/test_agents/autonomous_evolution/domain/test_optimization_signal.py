
import pytest

from src.agents.autonomous_evolution.domain import (
    OptimizationSignal,
)


def test_signal_creation() -> None:
    signal = OptimizationSignal(
        signal_type="strategy_preference",
        target="direct_execution",
        direction="reinforce",
        strength=0.85,
        confidence=0.90,
        reason="Repeated positive outcomes.",
        supporting_patterns=[
            "effective_execution_pattern",
        ],
    )

    assert signal.signal_type == "strategy_preference"
    assert signal.target == "direct_execution"
    assert signal.direction == "reinforce"
    assert signal.strength == 0.85


def test_signal_rejects_invalid_strength() -> None:
    with pytest.raises(ValueError):
        OptimizationSignal(
            signal_type="strategy",
            target="agent",
            direction="reinforce",
            strength=1.1,
        )


def test_signal_serialization() -> None:
    signal = OptimizationSignal(
        signal_type="strategy_preference",
        target="agent",
        direction="avoid",
    )

    data = signal.to_dict()

    assert data["signal_type"] == "strategy_preference"
    assert data["target"] == "agent"
    assert data["direction"] == "avoid"