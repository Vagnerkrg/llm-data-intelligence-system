from src.cognitive.memory.intelligence.memory_index import (
    MemoryIndex
)

from src.cognitive.memory.intelligence.knowledge_retriever import (
    KnowledgeRetriever
)



def create_retriever():

    index = MemoryIndex()

    index.add(
        "memory-001",
        {
            "topic": "optimization",
            "type": "learning"
        }
    )

    index.add(
        "memory-002",
        {
            "topic": "decision",
            "type": "learning"
        }
    )

    return KnowledgeRetriever(
        index
    )



def test_knowledge_retriever_retrieve():

    retriever = create_retriever()


    result = retriever.retrieve(
        "memory-001"
    )


    assert result is not None
    assert result["topic"] == "optimization"



def test_knowledge_retriever_search():

    retriever = create_retriever()


    results = retriever.search(
        "type",
        "learning"
    )


    assert len(results) == 2



def test_knowledge_retriever_exists():

    retriever = create_retriever()


    assert retriever.exists(
        "memory-001"
    )



def test_knowledge_retriever_missing():

    retriever = create_retriever()


    assert retriever.retrieve(
        "unknown"
    ) is None