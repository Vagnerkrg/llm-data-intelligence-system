from typing import List, Dict, Any


from src.cognitive.memory.consolidation.pattern_extractor import (
    PatternExtractor
)

from src.cognitive.memory.consolidation.knowledge_extractor import (
    KnowledgeExtractor
)

from src.cognitive.memory.consolidation.knowledge_consolidator import (
    KnowledgeConsolidator
)



class ConsolidationPipeline:
    """
    Pipeline completo de consolidação cognitiva.

    Responsável por transformar experiências
    armazenadas em conhecimento reutilizável.
    """



    def __init__(
        self,
        pattern_extractor=None,
        knowledge_extractor=None,
        knowledge_consolidator=None
    ):

        self.pattern_extractor = (
            pattern_extractor
            or PatternExtractor()
        )


        self.knowledge_extractor = (
            knowledge_extractor
            or KnowledgeExtractor()
        )


        self.knowledge_consolidator = (
            knowledge_consolidator
            or KnowledgeConsolidator()
        )



    def run(
        self,
        experiences: List[Dict[str, Any]]
    ):
        """
        Executa ciclo completo.

        Entrada:

        Experiências da memória


        Saída:

        Conhecimentos consolidados
        """

        patterns = (
            self.pattern_extractor.extract(
                experiences
            )
        )


        knowledge_candidates = (
            self.knowledge_extractor.extract(
                patterns
            )
        )


        consolidated = (
            self.knowledge_consolidator.consolidate(
                knowledge_candidates
            )
        )


        return consolidated



    def count(self) -> int:
        """
        Quantidade de conhecimento consolidado.
        """

        return (
            self.knowledge_consolidator.count()
        )