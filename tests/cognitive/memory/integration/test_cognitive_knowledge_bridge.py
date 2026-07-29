from src.cognitive.memory.integration.cognitive_knowledge_bridge import (
    CognitiveKnowledgeBridge
)

from src.cognitive.memory.consolidation.consolidated_knowledge import (
    ConsolidatedKnowledge
)


def create_knowledge(
    knowledge_id="knowledge_001",
    content="Agent learned successful decision pattern"
):
    return ConsolidatedKnowledge(
        knowledge_id=knowledge_id,
        content=content,
        source_pattern="cognitive_pattern_extraction",
        confidence=0.95,
        metadata={
            "source": "feedback_loop",
            "type": "cognitive_pattern"
        }
    )


def test_cognitive_knowledge_bridge_create():

    bridge = CognitiveKnowledgeBridge()

    assert bridge is not None



def test_cognitive_knowledge_bridge_add():

    bridge = CognitiveKnowledgeBridge()

    knowledge = create_knowledge()

    bridge.add_knowledge(
        knowledge
    )

    assert bridge.count() == 1



def test_cognitive_knowledge_bridge_retrieve():

    bridge = CognitiveKnowledgeBridge()

    knowledge = create_knowledge()

    bridge.add_knowledge(
        knowledge
    )

    result = bridge.retrieve(
        "knowledge_001"
    )

    assert result is not None

    assert result.knowledge_id == "knowledge_001"



def test_cognitive_knowledge_bridge_exists():

    bridge = CognitiveKnowledgeBridge()

    knowledge = create_knowledge()

    bridge.add_knowledge(
        knowledge
    )

    assert bridge.exists(
        "knowledge_001"
    ) is True



def test_cognitive_knowledge_bridge_search():

    bridge = CognitiveKnowledgeBridge()

    bridge.add_knowledge(
        create_knowledge(
            content="Successful planning pattern extracted"
        )
    )

    result = bridge.search(
        "planning"
    )

    assert len(result) > 0



def test_cognitive_knowledge_bridge_consolidate():

    bridge = CognitiveKnowledgeBridge()

    knowledge_list = [
        create_knowledge(
            "knowledge_001"
        ),
        create_knowledge(
            "knowledge_002"
        )
    ]

    result = bridge.consolidate(
        knowledge_list
    )

    assert result is not None

    assert len(result) > 0



def test_cognitive_knowledge_bridge_metadata():

    bridge = CognitiveKnowledgeBridge()

    bridge.add_knowledge(
        create_knowledge()
    )

    result = bridge.retrieve(
        "knowledge_001"
    )

    assert result.metadata["source"] == "feedback_loop"

    assert result.metadata["type"] == "cognitive_pattern"