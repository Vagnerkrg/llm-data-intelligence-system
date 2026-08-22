from src.cognitive.memory.consolidation.knowledge_extractor import KnowledgeExtractor


def create_extractor():

    return KnowledgeExtractor()


def test_knowledge_extractor_extract():

    extractor = create_extractor()

    patterns = [
        {
            "topic": "query optimization",
            "occurrences": 3,
            "examples": [{"result": "improved latency"}],
        }
    ]

    result = extractor.extract(patterns)

    assert result is not None
    assert len(result) > 0


def test_knowledge_extractor_content():

    extractor = create_extractor()

    patterns = [
        {
            "topic": "memory retrieval",
            "occurrences": 5,
            "examples": [{"action": "index optimization"}],
        }
    ]

    knowledge = extractor.extract(patterns)

    assert knowledge[0]["topic"] == "memory retrieval"


def test_knowledge_extractor_empty():

    extractor = create_extractor()

    result = extractor.extract([])

    assert result == []


def test_knowledge_extractor_confidence():

    extractor = create_extractor()

    patterns = [{"topic": "agent reasoning", "occurrences": 10, "examples": []}]

    knowledge = extractor.extract(patterns)

    assert "confidence" in knowledge[0]
    assert knowledge[0]["confidence"] > 0
