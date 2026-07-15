from src.agents.self_improvement.knowledge.services.knowledge_builder import (
    KnowledgeBuilder,
)


def test_knowledge_builder_creates_entry():

    builder = KnowledgeBuilder()

    entry = builder.build(
        {
            "type": "pattern",
            "title": "High tool usage",
            "description": "Agent repeatedly selects same tool",
            "confidence": 0.8,
        }
    )

    assert entry.title == "High tool usage"
    assert entry.description == "Agent repeatedly selects same tool"
    assert entry.confidence == 0.8