from src.cognitive.memory.consolidation.pattern_extractor import PatternExtractor


def create_extractor():

    return PatternExtractor()


def test_pattern_extractor_extract():

    extractor = create_extractor()

    experiences = [
        {
            "type": "feedback",
            "topic": "query optimization",
            "result": "improved execution time",
        },
        {
            "type": "feedback",
            "topic": "query optimization",
            "result": "reduced latency",
        },
    ]

    result = extractor.extract(experiences)

    assert result is not None
    assert len(result) > 0


def test_pattern_extractor_contains_pattern():

    extractor = create_extractor()

    experiences = [
        {"topic": "memory retrieval", "action": "optimize indexing"},
        {"topic": "memory retrieval", "action": "optimize indexing"},
    ]

    patterns = extractor.extract(experiences)

    assert patterns[0]["topic"] == "memory retrieval"


def test_pattern_extractor_empty_input():

    extractor = create_extractor()

    result = extractor.extract([])

    assert result == []


def test_pattern_extractor_count():

    extractor = create_extractor()

    experiences = [
        {"topic": "agent reasoning"},
        {"topic": "agent reasoning"},
        {"topic": "memory learning"},
    ]

    patterns = extractor.extract(experiences)

    assert len(patterns) >= 1
