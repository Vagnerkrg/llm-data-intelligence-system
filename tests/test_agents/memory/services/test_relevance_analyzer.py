from src.agents.memory.services.relevance_analyzer import (
    RelevanceAnalyzer
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)


def test_should_analyze_memory_relevance():

    analyzer = RelevanceAnalyzer()

    memory = MemoryEntry(
        memory_id="001",
        content="User prefers technical explanations.",
        memory_type=MemoryType.LONG_TERM
    )


    result = analyzer.analyze(
        memory
    )


    assert result.memory_id == "001"

    assert result.score > 0

    assert result.factors

    assert (
        result.explanation
        ==
        "Memory relevance calculated."
    )



def test_should_return_zero_score_for_invalid_memory():

    analyzer = RelevanceAnalyzer()


    result = analyzer.analyze(
        None
    )


    assert result.score == 0.0

    assert result.memory_id == ""

    assert (
        result.explanation
        ==
        "Invalid memory."
    )