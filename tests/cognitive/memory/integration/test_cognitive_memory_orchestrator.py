from src.cognitive.memory.integration.cognitive_memory_orchestrator import (
    CognitiveMemoryOrchestrator
)

from src.cognitive.memory.integration.learning_memory_bridge import (
    LearningMemoryBridge
)

from src.cognitive.memory.intelligence.learning_memory_manager import (
    LearningMemoryManager
)

from src.cognitive.memory.intelligence.memory_index import (
    MemoryIndex
)

from src.cognitive.memory.intelligence.knowledge_retriever import (
    KnowledgeRetriever
)

from src.cognitive.learning.knowledge.consolidated_knowledge import (
    ConsolidatedKnowledge
)



def create_orchestrator():

    memory_index = MemoryIndex()

    manager = LearningMemoryManager(
        memory_index
    )

    bridge = LearningMemoryBridge(
        manager
    )

    retriever = KnowledgeRetriever(
        memory_index
    )

    return CognitiveMemoryOrchestrator(
        bridge,
        retriever
    )



def create_knowledge():

    return ConsolidatedKnowledge(
        knowledge_id="knowledge-001",
        content="Improve query execution",
        source_pattern="pattern-001",
        confidence=0.95
    )



def test_cognitive_memory_orchestrator_store():

    orchestrator = create_orchestrator()

    knowledge = create_knowledge()


    result = orchestrator.store_learning(
        knowledge
    )


    assert result["stored"] is True



def test_cognitive_memory_orchestrator_retrieve():

    orchestrator = create_orchestrator()

    knowledge = create_knowledge()


    orchestrator.store_learning(
        knowledge
    )


    result = orchestrator.retrieve_learning(
        "knowledge-001"
    )


    assert result is not None
    assert result.content == "Improve query execution"



def test_cognitive_memory_orchestrator_exists():

    orchestrator = create_orchestrator()

    knowledge = create_knowledge()


    orchestrator.store_learning(
        knowledge
    )


    assert orchestrator.exists(
        "knowledge-001"
    )



def test_cognitive_memory_orchestrator_count():

    orchestrator = create_orchestrator()

    knowledge = create_knowledge()


    orchestrator.store_learning(
        knowledge
    )


    assert orchestrator.count() == 1



def test_cognitive_memory_orchestrator_search():

    orchestrator = create_orchestrator()


    result = orchestrator.search_memory(
        "query"
    )


    assert result is not None