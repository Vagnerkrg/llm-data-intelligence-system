from src.agents.memory.domain.cognitive_knowledge import CognitiveKnowledge


def test_cognitive_knowledge_creation():

    knowledge = CognitiveKnowledge(
        knowledge_id="know_001",
        description="Repeated customer payment delay",
        source_patterns=["pattern_001"],
        confidence=0.85,
    )

    assert knowledge.knowledge_id == "know_001"

    assert knowledge.description == "Repeated customer payment delay"

    assert "pattern_001" in knowledge.source_patterns

    assert knowledge.confidence == 0.85
