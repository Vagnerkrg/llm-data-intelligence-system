from ..patterns.learning_pattern import LearningPattern
from ..consolidation.consolidation_engine import ConsolidationEngine
from ..knowledge.consolidated_knowledge import ConsolidatedKnowledge


class LearningConsolidationService:
    """
    Serviço responsável pelo ciclo completo
    de consolidação de aprendizado.
    """

    def __init__(self, consolidation_engine: ConsolidationEngine):
        self.consolidation_engine = consolidation_engine

    def process(self, pattern: LearningPattern) -> ConsolidatedKnowledge | None:
        """
        Processa um padrão aprendido
        e tenta transformá-lo em conhecimento.
        """

        return self.consolidation_engine.consolidate(pattern)

    def can_consolidate(self, pattern: LearningPattern) -> bool:
        """
        Verifica se um padrão possui
        condições para consolidação.
        """

        return pattern.is_reliable()
