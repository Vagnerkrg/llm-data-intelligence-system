from src.agents.self_improvement.knowledge.domain.knowledge_context import (
    KnowledgeContext,
)


def test_knowledge_context_creation():

    context = KnowledgeContext(
        source="evaluation",
        domain="agent_execution",
    )

    assert context.source == "evaluation"
    assert context.domain == "agent_execution"