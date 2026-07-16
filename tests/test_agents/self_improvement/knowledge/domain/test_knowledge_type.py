from src.agents.self_improvement.knowledge.domain.knowledge_type import (
    KnowledgeType,
)


def test_knowledge_type_values():

    assert KnowledgeType.INSIGHT.value == "insight"
    assert KnowledgeType.PATTERN.value == "pattern"
    assert KnowledgeType.STRATEGY.value == "strategy"