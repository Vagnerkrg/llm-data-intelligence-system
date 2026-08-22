from abc import ABC, abstractmethod

from ..patterns.learning_pattern import LearningPattern
from ..knowledge.consolidated_knowledge import ConsolidatedKnowledge


class LearningConsolidationProtocol(ABC):
    """
    Contrato para processos de consolidação
    de aprendizado cognitivo.
    """

    @abstractmethod
    def consolidate(self, pattern: LearningPattern) -> ConsolidatedKnowledge | None:
        """
        Consolida um padrão aprendido.
        """
        pass
