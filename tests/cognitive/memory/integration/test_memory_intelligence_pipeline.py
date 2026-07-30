from src.agents.memory.services.memory_intelligence_pipeline import (
    MemoryIntelligencePipeline
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)



def test_memory_intelligence_pipeline_create():

    pipeline = MemoryIntelligencePipeline()

    assert pipeline is not None



def test_memory_intelligence_pipeline_process():

    pipeline = MemoryIntelligencePipeline()


    memory = MemoryEntry(
        memory_id="memory_pipeline_001",
        content="Customer payment behavior pattern",
        memory_type=MemoryType.SEMANTIC
    )


    result = pipeline.process(
        memory
    )


    assert result is not None

    assert result["status"] == (
        "analyzed"
    )

    assert result["memory_id"] == (
        "memory_pipeline_001"
    )



def test_memory_intelligence_pipeline_relevance():

    pipeline = MemoryIntelligencePipeline()


    memory = MemoryEntry(
        memory_id="memory_pipeline_002",
        content="Agent improved decision strategy",
        memory_type=MemoryType.PROCEDURAL
    )


    result = pipeline.process(
        memory
    )


    assert result["relevance"] is not None

    assert result["relevance_score"] >= 0