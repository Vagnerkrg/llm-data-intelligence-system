import pytest

from src.agents.autonomous_evolution.domain import (
    ExperienceOptimizationContext,
    OptimizationPattern,
)
from src.agents.autonomous_evolution.services import (
    ExperienceDrivenOptimizer,
)


def test_optimizer_returns_no_signal_with_insufficient_experiences() -> None:
    optimizer = ExperienceDrivenOptimizer()

    context = ExperienceOptimizationContext(
        execution_history=[
            {"score": 0.9},
        ]
    )

    assert optimizer.optimize(context) == []


def test_optimizer_detects_effective_strategy() -> None:
    optimizer = ExperienceDrivenOptimizer()

    context = ExperienceOptimizationContext(
        execution_history=[
            {
                "score": 0.90,
                "confidence": 0.90,
                "strategy": "direct_execution",
            },
            {
                "score": 0.85,
                "confidence": 0.85,
                "strategy": "direct_execution",
            },
            {
                "score": 0.88,
                "confidence": 0.90,
                "strategy": "direct_execution",
            },
        ]
    )

    patterns = optimizer.detect_patterns(
        context
    )

    assert len(patterns) == 1
    assert isinstance(
        patterns[0],
        OptimizationPattern,
    )
    assert patterns[0].name == (
        "effective_execution_pattern"
    )
    assert patterns[0].strategy == (
        "direct_execution"
    )


def test_optimizer_generates_reinforcement_signal() -> None:
    optimizer = ExperienceDrivenOptimizer()

    context = ExperienceOptimizationContext(
        execution_history=[
            {
                "score": 0.90,
                "confidence": 0.90,
                "strategy": "direct_execution",
            },
            {
                "score": 0.85,
                "confidence": 0.85,
                "strategy": "direct_execution",
            },
        ]
    )

    signals = optimizer.optimize(
        context
    )

    assert len(signals) == 1
    assert signals[0].direction == "reinforce"
    assert signals[0].target == "direct_execution"
    assert signals[0].confidence > 0.60


def test_optimizer_detects_ineffective_strategy() -> None:
    optimizer = ExperienceDrivenOptimizer()

    context = ExperienceOptimizationContext(
        execution_history=[
            {
                "score": 0.30,
                "confidence": 0.90,
                "strategy": "complex_execution",
            },
            {
                "score": 0.40,
                "confidence": 0.85,
                "strategy": "complex_execution",
            },
            {
                "score": 0.35,
                "confidence": 0.90,
                "strategy": "complex_execution",
            },
        ]
    )

    signals = optimizer.optimize(
        context
    )

    assert len(signals) == 1
    assert signals[0].direction == "avoid"
    assert signals[0].target == "complex_execution"


def test_optimizer_ignores_low_confidence_experience_pattern() -> None:
    optimizer = ExperienceDrivenOptimizer()

    context = ExperienceOptimizationContext(
        execution_history=[
            {
                "score": 0.95,
                "confidence": 0.30,
            },
            {
                "score": 0.90,
                "confidence": 0.40,
            },
        ]
    )

    assert optimizer.optimize(context) == []


def test_optimizer_handles_invalid_scores() -> None:
    optimizer = ExperienceDrivenOptimizer()

    context = ExperienceOptimizationContext(
        execution_history=[
            {
                "score": 1.5,
            },
            {
                "score": "invalid",
            },
        ]
    )

    assert optimizer.optimize(context) == []


def test_optimizer_accepts_object_experiences() -> None:
    class Experience:
        score = 0.85
        confidence = 0.90
        strategy = "validated_strategy"

    optimizer = ExperienceDrivenOptimizer()

    context = ExperienceOptimizationContext(
        execution_history=[
            Experience(),
            Experience(),
        ]
    )

    signals = optimizer.optimize(
        context
    )

    assert len(signals) == 1
    assert signals[0].target == "validated_strategy"


@pytest.mark.parametrize(
    "kwargs",
    [
        {"min_experiences": 0},
        {"min_confidence": -0.1},
        {"min_confidence": 1.1},
        {"effective_threshold": -0.1},
        {"effective_threshold": 1.1},
        {"ineffective_threshold": -0.1},
        {"ineffective_threshold": 1.1},
        {
            "effective_threshold": 0.5,
            "ineffective_threshold": 0.6,
        },
    ],
)
def test_optimizer_rejects_invalid_configuration(
    kwargs: dict[str, float | int],
) -> None:
    with pytest.raises(ValueError):
        ExperienceDrivenOptimizer(**kwargs)