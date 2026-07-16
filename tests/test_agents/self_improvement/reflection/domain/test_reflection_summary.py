from src.agents.self_improvement.reflection.domain import (
    ReflectionFinding,
    ReflectionSummary,
    ReflectionType,
)


def test_should_return_total_findings():
    finding = ReflectionFinding(
        reflection_type=ReflectionType.PERFORMANCE,
        title="Pattern",
        description="Description",
        confidence=0.9,
    )

    summary = ReflectionSummary(
        findings=[finding],
    )

    assert summary.total_findings == 1


def test_should_indicate_findings_exist():
    finding = ReflectionFinding(
        reflection_type=ReflectionType.PERFORMANCE,
        title="Pattern",
        description="Description",
        confidence=0.9,
    )

    summary = ReflectionSummary(
        findings=[finding],
    )

    assert summary.has_findings


def test_should_indicate_no_findings():
    summary = ReflectionSummary()

    assert not summary.has_findings
