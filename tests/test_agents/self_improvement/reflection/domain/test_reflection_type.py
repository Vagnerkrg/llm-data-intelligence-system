from src.agents.self_improvement.reflection.domain import ReflectionType


def test_should_contain_expected_reflection_types():
    assert ReflectionType.PERFORMANCE.value == "performance"
    assert ReflectionType.STRATEGY.value == "strategy"
    assert ReflectionType.EXECUTION.value == "execution"
    assert ReflectionType.DECISION.value == "decision"
    assert ReflectionType.ADAPTATION.value == "adaptation"
    assert ReflectionType.KNOWLEDGE.value == "knowledge"
