from src.agents.self_improvement.learning.domain import LearningRule


def test_learning_rule_creation():

    rule = LearningRule(
        condition="low performance",
        action="change strategy"
    )

    assert rule.condition == "low performance"
    assert rule.action == "change strategy"