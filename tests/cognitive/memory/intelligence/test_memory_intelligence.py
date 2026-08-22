from src.agents.memory.services.memory_intelligence import MemoryIntelligence

from src.agents.memory.services.relevance_analyzer import RelevanceAnalyzer

from src.agents.memory.domain.memory_entry import MemoryEntry

from src.agents.memory.domain.memory_type import MemoryType

from src.agents.memory.domain.relevance_result import RelevanceResult


def test_memory_intelligence_create():

    analyzer = RelevanceAnalyzer()

    intelligence = MemoryIntelligence(analyzer)

    assert intelligence is not None


def test_memory_intelligence_analyze():

    analyzer = RelevanceAnalyzer()

    intelligence = MemoryIntelligence(analyzer)

    memory = MemoryEntry(
        memory_id="memory_001",
        content="Customer payment behavior pattern",
        memory_type=MemoryType.SEMANTIC,
    )

    result = intelligence.analyze(memory)

    assert result is not None

    assert isinstance(result, RelevanceResult)


def test_memory_intelligence_result():

    analyzer = RelevanceAnalyzer()

    intelligence = MemoryIntelligence(analyzer)

    memory = MemoryEntry(
        memory_id="memory_002",
        content="Successful agent decision pattern",
        memory_type=MemoryType.SEMANTIC,
    )

    result = intelligence.analyze(memory)

    assert result.memory_id == ("memory_002")

    assert result.score >= 0
