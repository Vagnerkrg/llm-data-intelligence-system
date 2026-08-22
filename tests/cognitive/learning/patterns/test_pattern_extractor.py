from src.agents.memory.domain.memory_entry import MemoryEntry
from src.agents.memory.domain.memory_type import MemoryType
from src.agents.memory.intelligence.pattern_extractor import PatternExtractor


def test_extract_repeated_pattern():

    memories = [
        MemoryEntry(
            memory_id="mem_001",
            content="customer payment delayed",
            memory_type=MemoryType.EPISODIC,
        ),
        MemoryEntry(
            memory_id="mem_002",
            content="customer payment delayed",
            memory_type=MemoryType.EPISODIC,
        ),
    ]

    extractor = PatternExtractor()

    patterns = extractor.extract(memories)

    assert len(patterns) == 1

    assert patterns[0].occurrences == 2

    assert "mem_001" in patterns[0].memory_ids

    assert "mem_002" in patterns[0].memory_ids
