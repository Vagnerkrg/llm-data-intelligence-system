from src.agents.self_improvement.reflection.domain import (
    ReflectionFinding,
    ReflectionType,
)


def test_should_create_reflection_finding():
    finding = ReflectionFinding(
        reflection_type=ReflectionType.PERFORMANCE,
        title="Performance Pattern",
        description="Execution performance improved.",
        confidence=0.95,
    )

    assert finding.reflection_type == ReflectionType.PERFORMANCE
    assert finding.title == "Performance Pattern"
    assert finding.confidence == 0.95


def test_should_identify_high_confidence():
    finding = ReflectionFinding(
        reflection_type=ReflectionType.PERFORMANCE,
        title="Pattern",
        description="Description",
        confidence=0.90,
    )

    assert finding.is_high_confidence()


def test_should_identify_low_confidence():
    finding = ReflectionFinding(
        reflection_type=ReflectionType.PERFORMANCE,
        title="Pattern",
        description="Description",
        confidence=0.50,
    )

    assert not finding.is_high_confidence()
