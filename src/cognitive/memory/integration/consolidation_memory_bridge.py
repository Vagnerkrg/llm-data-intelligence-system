from typing import List

from src.cognitive.memory.consolidation.consolidation_pipeline import (
    ConsolidationPipeline,
)


class ConsolidationMemoryBridge:
    """
    Bridge entre Learning Memory e Knowledge Consolidation.

    Responsável por transformar experiências armazenadas
    em conhecimento cognitivo reutilizável.
    """

    def __init__(self, pipeline: ConsolidationPipeline | None = None):
        self.pipeline = pipeline or ConsolidationPipeline()

    def consolidate(self, memories: List[dict]):
        """
        Executa consolidação de memórias.

        Args:
            memories:
                Lista de experiências armazenadas.

        Returns:
            Conhecimento consolidado.
        """

        return self.pipeline.run(memories)

    def count(self):
        """
        Retorna quantidade de conhecimentos consolidados.
        """

        return self.pipeline.count()
