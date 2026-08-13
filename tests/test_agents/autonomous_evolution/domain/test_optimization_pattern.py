import pytest

from src.agents.autonomous_evolution.domain import (
    OptimizationPattern,
)


def test_pattern_creation() -> None:
    pattern = OptimizationPattern(
        name="effective_execution_pattern",
        category="strategy",
        occurrence_count=3,
        average_score=0.85,
        average_confidence=0.90,
        strategy="direct_execution",
    )

    assert pattern.name == "effective_execution_pattern"
    assert pattern.category == "strategy"
    assert pattern.occurrence_count == 3
    assert pattern.strategy == "direct_execution"


def test_pattern_rejects_invalid_score() -> None:
    with pytest.raises(ValueError):
        OptimizationPattern(
            name="invalid",
            category="strategy",
            average_score=1.1,
        )


def test_pattern_rejects_negative_occurrences() -> None:
    with pytest.raises(ValueError):
        OptimizationPattern(
            name="invalid",
            category="strategy",
            occurrence_count=-1,
        )