from src.agents.memory.services.memory_intelligence_pipeline import (
    MemoryIntelligencePipeline
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)



def create_pipeline():

    return MemoryIntelligencePipeline()



def test_should_process_memory_intelligence_pipeline():


    pipeline = create_pipeline()


    memory = MemoryEntry(
        memory_id="001",
        content=(
            "User prefers technical "
            "architecture explanations."
        ),
        memory_type=MemoryType.LONG_TERM,
        metadata={
            "importance": "high"
        }
    )


    result = pipeline.process(
        memory
    )


    assert result is not None

    assert result["memory_id"] == "001"

    assert result["relevance"].score > 0



def test_should_fail_pipeline_with_invalid_memory():


    pipeline = create_pipeline()


    result = pipeline.process(
        None
    )


    assert result.memory_id == ""

    assert result.score == 0.0