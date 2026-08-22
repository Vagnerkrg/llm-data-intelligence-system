from src.agents.memory.domain.memory_entry import MemoryEntry

from src.agents.memory.services.memory_intelligence_pipeline import (
    MemoryIntelligencePipeline,
)


class MemoryIntelligenceAdapter:
    """
    Adapter connecting Agent Runtime
    with Memory Intelligence Pipeline.

    V1.24:
    Enables cognitive memory analysis
    inside runtime execution.
    """

    def __init__(self, pipeline: MemoryIntelligencePipeline = None):

        self.pipeline = pipeline if pipeline else MemoryIntelligencePipeline()

    def analyze(self, memory: MemoryEntry):

        return self.pipeline.process(memory)
