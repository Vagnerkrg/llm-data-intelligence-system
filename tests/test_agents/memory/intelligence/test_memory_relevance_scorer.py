from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)

from src.agents.memory.intelligence.memory_relevance_scorer import (
    MemoryRelevanceScorer
)


def create_scorer():

    return MemoryRelevanceScorer()



def test_should_evaluate_memory_relevance():

    scorer = create_scorer()


    memory = MemoryEntry(
        memory_id="001",
        content=(
            "User prefers technical explanations "
            "with detailed architecture."
        ),
        memory_type=MemoryType.LONG_TERM,
        metadata={
            "category": "preference"
        }
    )


    result = scorer.evaluate(
        memory
    )


    assert result.memory_id == "001"

    assert result.score > 0

    assert (
        "cognitive_value"
        in result.factors
    )



def test_should_fail_with_invalid_memory():

    scorer = create_scorer()


    result = scorer.evaluate(
        None
    )


    assert result.score == 0.0

    assert (
        result.explanation
        ==
        "Invalid memory."
    )