from src.agents.cognitive_improvement.integration.knowledge_adapter import (
    KnowledgeAdapter,
)


def test_should_create_knowledge_adapter():
    adapter = KnowledgeAdapter()

    assert adapter is not None