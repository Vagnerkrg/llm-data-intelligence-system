from src.agents.memory.intelligence.relevance_scoring import (
    RelevanceScoring
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)



def test_should_calculate_memory_relevance():


    scorer = RelevanceScoring()


    memory = MemoryEntry(
        memory_id="001",
        content=(
            "User prefers technical explanations "
            "with detailed engineering context."
        ),
        memory_type=MemoryType.LONG_TERM,
        metadata={
            "source": "interaction"
        }
    )


    result = scorer.calculate(
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



def test_should_return_zero_for_invalid_memory():


    scorer = RelevanceScoring()


    result = scorer.calculate(
        None
    )


    assert result.memory_id == ""

    assert result.score == 0.0

    assert (
        result.explanation
        ==
        "Invalid memory."
    )